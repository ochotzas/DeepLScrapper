# DeepLScrapper

An unofficial Python library for translating text using DeepL.

## Introduction

### Summary

DeepLScrapper is a web scraper that allows you to translate texts from one language to another using the DeepL translation service. It utilizes the Selenium WebDriver with a headless Chrome browser to interact with the DeepL website.

### Idea behind

The idea behind the project is to create an unofficial Python library called "DeepLScrapper" that provides a workaround for the limitations of the official DeepL API. DeepL offers a powerful and accurate translation service, but it comes with certain usage restrictions and rate limits when accessing the service through their API.

The goal of DeepLScrapper is to leverage web scraping techniques using Selenium WebDriver to interact with the DeepL translation website directly, allowing users to perform text translations without being bound by the API's usage limitations. By bypassing the API, the library can offer more flexibility in terms of translation volume and frequency, making it suitable for applications that require large-scale or frequent text translations.

### Key features

- Unlimited Translations: DeepLScrapper offers unlimited text translations without relying on the official DeepL API, avoiding rate limits or usage restrictions.

- Translation Versatility: This library accommodates both single text and bulk translation needs, catering to a wide range of use cases and applications.

- Efficient Caching: DeepLScrapper employs an intelligent caching mechanism that stores past translations, reducing redundant requests and enhancing overall translation efficiency.

- Custom Rate Limiting: Users have the freedom to set their preferred rate limit delay between retry attempts, providing flexibility in handling rate-limiting errors from the DeepL website.

- Diverse User-Agent: The library generates a random User-Agent using the "fake_useragent" library, ensuring a diverse and realistic browser identity for seamless interaction with the DeepL website.

- Multi-Threading Support: DeepLScrapper supports multi-threading, enabling parallel translation of multiple texts for faster and more efficient processing.

- Comprehensive Error Handling: The library offers robust error handling, managing rate-limiting errors and providing informative error messages for easy troubleshooting.

- Database Integration: The integrated SQLite database facilitates efficient storage and retrieval of translations, enhancing performance and data management.

- Headless Browser Automation: Utilizing a headless Chrome browser via Selenium WebDriver, DeepLScrapper ensures a seamless and automated translation process.

- Customizable Configuration: Users can customize caching settings, database paths, and more to tailor the library to their specific requirements.

- Language Support: DeepLScrapper supports translation between various languages, providing a comprehensive language repertoire for diverse translation needs.

By offering a versatile and unrestricted translation solution, DeepLScrapper provides developers with a powerful tool to integrate high-volume and frequent text translations into their applications without the limitations of the official DeepL API. However, it's important to keep in mind that the library should be used responsibly and in compliance with the DeepL website's terms of service and policies.

## Installation

You can install DeepLScrapper using pip:

```bash
pip install DeepLScrapper
```

## Usage

### Use DeepLScrapper in your project

To use DeepLScrapper in your project, import the library and initialize the translator object. You can then use the translator object to perform text translations.

```python
from DeepLScrapper import DeepLScrapper

# Initialize the translator with a custom rate limit delay of 5 seconds
translator = DeepLScrapper(rate_limit_delay=5, enable_caching=True, max_cache_size=100, multi_threading=True)

try:
    # Translate text from English to German
    translation = translator.translate('Hello, World!', source_lang='en', target_lang='de')
    print("Translation 1:", translation)

    # Translate the same text again to test caching
    translation_cached = translator.translate('Hello, World!', source_lang='en', target_lang='de')
    print("Translation 2 (Cached):", translation_cached)

    # Translate multiple texts in bulk
    texts = ['How are you?', 'Goodbye!', 'Welcome back.']
    bulk_translations = translator.translate(texts, source_lang='en', target_lang='el')
    print("Bulk Translations:", bulk_translations)

    # Test language validation with an invalid language code
    try:
        invalid_translation = translator.translate('Hello, World!', source_lang='en', target_lang='invalid')
        print("Invalid Translation:", invalid_translation)
    except ValueError as e:
        print("Error:", e)

    # Test handling rate limiting by attempting multiple translations in a short duration
    for i in range(5):
        try:
            print("Translation", i + 1, ":", translator.translate('Hello!', source_lang='en', target_lang='fr'))
        except Exception as e:
            print("Error:", e)

except Exception as e:
    print(f"Error occurred: {e}")
finally:
    # Close the browser
    translator.close()
```

### Use the DeepLWebApp using an interactive CLI interface

DeepLScrapper comes with a built-in CLI interface that allows you to interact with the library using a command-line interface. You can use the CLI interface to perform text translations [1], manage the database [2], and configure the library settings [3] ([2-3]: soon to be implemented).

```python
from DeepLScrapper import DeepLWebApp

# Initialize the DeepLWebApp
app = DeepLWebApp(10, True, 100, True)

# Run the DeepLWebApp
app.start_server()
```

You can then access the CLI interface by navigating to http://localhost:5000/ in your browser.


Demo preview of the CLI interface:

![DeepLWebApp Demo](https://i.ibb.co/H24xsRd/Screen-Recording-2023-08-19-at-5-31-49-PM.gif)

## Dependencies

- Selenium
- BeautifulSoup4
- fake_useragent
- sqlite3
- Flask

## Version History

- 1.8.0
  - Added DeepLWebApp class for an interactive CLI interface to the library.
- 1.[1-7].0
    - Added a multi-threading feature. The class now supports multiple threads for faster translations.
    - Added caching enabled/disabled option and a maximum cache size option.
    - Added a translation memory feature. The class now stores previously translated texts in the database, reducing redundant requests to DeepL and speeding up translations for repeated texts.
    - Restructured the project
    - Fixed the issue to using the library
    - Updated the documentation regarding the changes
    - Initial release
    - Fixed issue with using the library in a multithreading environment

## License

This project is licensed under the MIT License.

## Disclaimer

This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with DeepL, or any of its subsidiaries or its affiliates. The official DeepL website can be found at https://www.deepl.com/.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support

If you like this project, please consider giving it a ⭐. And check out my other projects on GitHub. If you would like to support me, donations are welcome.