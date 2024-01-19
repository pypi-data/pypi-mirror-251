import pandas as pd
import numpy as np
import re
import nltk 
from bs4 import BeautifulSoup 
from nltk.corpus import stopwords
import spacy
from collections import defaultdict
import base64
import os
from spacy.tokens import DocBin # for serialization
import requests
import zipfile
import logging

logging.basicConfig(level=logging.INFO) 

class LoadModel:

    __EMAIL_PARSER_MODEL_ZIP_URL = 'https://s3.ap-southeast-1.amazonaws.com/images.theoceann.com/website/assets/entity_extraction_model/output/model-best.zip'
    __BASE_DIR = os.getcwd()
    __local_zip_file_path = os.path.join(__BASE_DIR, 'output.zip')
    __extract_to = os.path.join(__BASE_DIR, 'output')
    __modelInstance = None
    
    @classmethod
    def __getModalInstance(cls):
        if cls.__modelInstance is None:
            cls.__modelInstance =  cls.__load_model()

        return cls.__modelInstance
    


    @classmethod
    def __load_model(cls):
        try:
            logging.info("Checking Model File")
            if os.path.exists(cls.__local_zip_file_path) and os.path.exists(os.path.join(cls.__extract_to, 'model-best')):
                logging.info("Loading Pretrained Model")
                nlp = spacy.load(os.path.join(cls.__extract_to, 'model-best'))
                logging.info("Model has been loaded")
                return nlp
            else:
                try:
                    logging.info("Downloading Model File")
                    response = requests.get(cls.__EMAIL_PARSER_MODEL_ZIP_URL)

                    if response.status_code == 200:
                        logging.info("Response Code: %s", response.status_code)

                        with open(cls.__local_zip_file_path, 'wb') as file:
                            file.write(response.content)

                        logging.info("File downloaded to %s", cls.__local_zip_file_path)
                        logging.info("Unzipping File to: %s", cls.__extract_to)

                        with zipfile.ZipFile(cls.__local_zip_file_path, 'r') as zip_ref:
                            os.makedirs(cls.__extract_to, exist_ok=True)
                            zip_ref.extractall(cls.__extract_to)
                            logging.info("Zip file extracted to %s",  cls.__extract_to)

                        nlp = spacy.load(os.path.join(cls.__extract_to, 'model-best'))

                        logging.info("Model has been loaded")
                        return nlp
                    else:
                        logging.error("Failed to download the file")
                        return None
                except Exception as e:
                    logging.error("Error %s", e)
                    return None
        except Exception as e:
            logging.error("Error %s", e)
            return None
            
    
    def __clean_email(self,text):
        """Function to clean email text"""

        try:    
            # Replace 'm[./]v' with 'mv'
            text = re.sub(r'm[./]v', 'mv', text)

            # Check for 'mv' in text
            if 'mv' in text:
                # Extract content before 'disclaimer'
                content_before_disclaimer = re.search(r'(.+?)\bdisclaimer\b', text, re.DOTALL)
                if content_before_disclaimer:
                    text = content_before_disclaimer.group(1).strip()
                else:
                    # Use BeautifulSoup to extract text from HTML
                    soup = BeautifulSoup(text, "html.parser")
                    text = soup.get_text()

                # Remove URLs
                text = re.sub(r'http\S+|www.\S+', '', text)

                # Replace specific patterns with space
                text = re.sub(r'\r\n|\ufeff|[-_]{2,}', ' ', text)

                # Replace multiple spaces with a single space
                text = re.sub(r'\s+', ' ', text)

                # Remove non-word characters
                text = re.sub(r'[^\w\s.,/()<>]', '', text)

                # Tokenize text and remove stopwords
                words = nltk.word_tokenize(text)
                stop_words = set(nltk.corpus.stopwords.words('english'))
                filtered_words = [word for word in words if word.lower() not in stop_words]
                cleaned_text = ' '.join(filtered_words)

                # Find the index of 'subject' in cleaned text
                subject_index = cleaned_text.lower().find('subject')
                if subject_index != -1:
                    # Split text into two parts based on 'subject'
                    first_part = cleaned_text[:subject_index].strip()
                    second_part = cleaned_text[subject_index:].strip()
                    return [first_part, second_part]
                else:
                    return ["", cleaned_text]

            else:
                # Return message if 'mv' not found in text
                message = "Email doesn't contain MV or M.V. or M/V"
                return message
        except Exception as e:
            logging.error("Error %s" , e)
    
    def __decode_into_text(self, text):
        """Checks and decodes the base64 to text"""
        try:
            decoded_bytes = base64.b64decode(text)
            decoded_text = decoded_bytes.decode('utf-8')
            return decoded_text
        except Exception as e:
            logging.error("Given input is not in base64 form")
            return None
        
    
class EntityExtractor(LoadModel):
    
    def __init__(self, text):    
        super().__init__()
        self.__text = text
        self.__nlp = super()._LoadModel__getModalInstance()
        self.__decoded_text = super()._LoadModel__decode_into_text(self.__text)
        self.__cleaned_text_parts = self._LoadModel__clean_email(self.__decoded_text)
    
    def extract_entities(self):
        try:
            doc = self.__nlp(self.__cleaned_text_parts[1])

            entities_dict = defaultdict(list)
            for ent in doc.ents:
                if ent.label_ in entities_dict:
                    entities_dict[ent.label_].append(ent.text)
                else:
                    entities_dict[ent.label_] = [ent.text]
            return entities_dict
        except Exception as e:
            logging.error("Error %s" , e)