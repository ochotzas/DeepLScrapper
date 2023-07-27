import logging
import time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


class DeepLScrapper:
    """
        A web scrapper for the DeepL translation service using Selenium.

        This class allows you to translate texts from one language to another using the DeepL translation service.
        It utilizes the Selenium WebDriver with a headless Chrome browser to interact with the DeepL website.

        Args:
            rate_limit_delay (int, optional): The delay in seconds between retries when rate-limited by DeepL. Default is 10.

        Attributes:
            RATE_LIMIT_DELAY (int): The delay in seconds between retries when rate-limited by DeepL.
            cache (dict): A dictionary to cache translation results to avoid redundant requests.
            driver (webdriver.Chrome): The WebDriver instance for controlling the headless Chrome browser.

        Note:
            - Language detection (auto-detection) is not supported in this version. Please provide the source language.
            - The 'fake_useragent' library is used to generate a random User-Agent for browser emulation.
    """

    def __init__(self, rate_limit_delay=10):
        self.RATE_LIMIT_DELAY = rate_limit_delay
        self.cache = {}
        self._initialize_driver()

    def _initialize_driver(self):
        ua = UserAgent()
        user_agent = ua.random
        options = Options()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def translate(self, text, source_lang='auto', target_lang='en', max_retries=3, retry_delay=1):
        if source_lang == 'auto':
            logging.warning("Language detection is not supported in this version. Please provide the source language.")
            return None

        if isinstance(text, str):
            return self._translate_single_text(text, source_lang, target_lang, max_retries, retry_delay)
        elif isinstance(text, list):
            return self._translate_multiple_texts(text, source_lang, target_lang, max_retries, retry_delay)
        else:
            raise ValueError("Invalid 'text' parameter. It should be a string or a list of strings.")

    def _translate_single_text(self, text, source_lang, target_lang, max_retries, retry_delay):
        cache_key = f"{text}_{source_lang}_{target_lang}"
        if cache_key in self.cache:
            logging.info("Translation found in cache.")
            return self.cache[cache_key]

        retries = 0
        while retries < max_retries:
            try:
                url = f'https://www.deepl.com/translator#{source_lang}/{target_lang}/{text}'
                self.driver.get(url)

                wait = WebDriverWait(self.driver, 10)
                translation_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sentence_highlight')))

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                translation = self._extract_translation(soup)

                self.cache[cache_key] = translation
                return translation
            except Exception as e:
                error_message = f"Translation failed for text: '{text}' with error: {e}"
                if self._is_rate_limited_error(e):
                    logging.warning(
                        f"Rate limited by DeepL. Waiting {self.RATE_LIMIT_DELAY} seconds before retrying.")
                    time.sleep(self.RATE_LIMIT_DELAY)
                else:
                    logging.error(error_message)
                    retries += 1
                    time.sleep(retry_delay)
        else:
            raise Exception("Failed to translate text after maximum retries.")

    def close(self):
        self.driver.quit()

    def _translate_multiple_texts(self, texts, source_lang, target_lang, max_retries, retry_delay):
        translations = []
        for text in texts:
            translation = self._translate_single_text(text, source_lang, target_lang, max_retries, retry_delay)
            translations.append(translation)
        return translations

    def _extract_translation(self, soup):
        translation_element = soup.find('span', {'class': 'sentence_highlight'})
        if translation_element:
            translation = translation_element.text.strip()
            return translation
        else:
            raise ValueError("Translation not found on the page.")

    @staticmethod
    def _is_rate_limited_error(error):
        rate_limited_errors = ["Too many requests", "Service Temporarily Unavailable"]
        return any(message in str(error) for message in rate_limited_errors)