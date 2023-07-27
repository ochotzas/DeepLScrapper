import logging

# Set the default logging level and format for the library
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from deepl_scrapper.translator import DeepLScrapper