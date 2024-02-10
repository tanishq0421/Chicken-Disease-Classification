import os
import urllib.request as request
import zipfile
from chicken_disease_classification import logger
from chicken_disease_classification.utils.common import get_size
from chicken_disease_classification.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename= self.config.local_data_file
            )
            logger.info(f"{filename} download! with following info: \n{headers}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        
        unzip_path = self.config.unzip_dir
        if not os.path.exists(unzip_path):
            os.makedirs(unzip_path)
        try:        
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.printdir()
                zip_ref.testzip()
                zip_ref.extractall(unzip_path)
        except Exception as e:
            print(f"Error during zip file extraction: {e}")
            raise e