import logging
import time
import sqlite3
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

        Note:
            - Language detection (auto-detection) is not supported in this version. Please provide the source language.
            - The 'fake_useragent' library is used to generate a random User-Agent for browser emulation.
    """

    def __init__(self, rate_limit_delay=10):
        self.RATE_LIMIT_DELAY = rate_limit_delay
        self._initialize_driver()
        self._create_translation_table()

    def _initialize_driver(self):
        ua = UserAgent()
        user_agent = ua.random
        options = Options()
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def _create_translation_table(self):
        conn = sqlite3.connect('translation_memory.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS translations 
                     (source_text TEXT, source_lang TEXT, target_lang TEXT, translation TEXT)''')
        conn.commit()
        conn.close()

    def _get_translation_from_memory(self, text, source_lang, target_lang):
        conn = sqlite3.connect('translation_memory.db')
        c = conn.cursor()
        c.execute('''SELECT translation FROM translations 
                     WHERE source_text=? AND source_lang=? AND target_lang=?''', (text, source_lang, target_lang))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    def _store_translation_in_memory(self, text, source_lang, target_lang, translation):
        conn = sqlite3.connect('translation_memory.db')
        c = conn.cursor()
        c.execute('''INSERT INTO translations (source_text, source_lang, target_lang, translation) 
                     VALUES (?, ?, ?, ?)''', (text, source_lang, target_lang, translation))
        conn.commit()
        conn.close()

    def _translate_single_text(self, text, source_lang, target_lang, max_retries, retry_delay):
        cached_translation = self._get_translation_from_memory(text, source_lang, target_lang)
        if cached_translation:
            logging.info("Translation found in memory.")
            return cached_translation

        retries = 0
        while retries < max_retries:
            try:
                url = f'https://www.deepl.com/translator#{source_lang}/{target_lang}/{text}'
                self.driver.get(url)

                wait = WebDriverWait(self.driver, 10)
                translation_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'sentence_highlight')))

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                translation = self._extract_translation(soup)

                self._store_translation_in_memory(text, source_lang, target_lang, translation)

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

    def clear_translation_memory(self):
        conn = sqlite3.connect('translation_memory.db')
        c = conn.cursor()
        c.execute('DELETE FROM translations')
        conn.commit()
        conn.close()

    def close(self):
        self.driver.quit()

    @staticmethod
    def _is_rate_limited_error(error):
        rate_limited_errors = ["Too many requests", "Service Temporarily Unavailable"]
        return any(message in str(error) for message in rate_limited_errors)
