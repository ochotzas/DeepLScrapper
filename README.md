# DeepLScrapper

An unofficial Python library for translating text using DeepL.

## Introduction

### Summary

DeepLScrapper is a web scraper that allows you to translate texts from one language to another using the DeepL translation service. It utilizes the Selenium WebDriver with a headless Chrome browser to interact with the DeepL website.

### Idea behind

The idea behind the project is to create an unofficial Python library called "DeepLScrapper" that provides a workaround for the limitations of the official DeepL API. DeepL offers a powerful and accurate translation service, but it comes with certain usage restrictions and rate limits when accessing the service through their API.

The goal of DeepLScrapper is to leverage web scraping techniques using Selenium WebDriver to interact with the DeepL translation website directly, allowing users to perform text translations without being bound by the API's usage limitations. By bypassing the API, the library can offer more flexibility in terms of translation volume and frequency, making it suitable for applications that require large-scale or frequent text translations.

### Key features

- No API Limits: DeepLScrapper does not rely on the official DeepL API, enabling users to perform unlimited text translations without encountering rate limits or usage restrictions.

- Translation Flexibility: The library supports both single text translation and bulk translation of multiple texts, making it suitable for various use cases and applications.

- Caching Mechanism: DeepLScrapper incorporates a caching mechanism to store previously translated texts, reducing redundant requests and improving translation efficiency.

- Customizable Rate Limiting: Users can customize the rate limit delay between retry attempts in case of rate-limiting errors from the DeepL website.

- User-Agent Randomization: The library generates a random User-Agent for browser emulation using the "fake_useragent" library, ensuring a diverse and realistic browser footprint.

By offering a versatile and unrestricted translation solution, DeepLScrapper provides developers with a powerful tool to integrate high-volume and frequent text translations into their applications without the limitations of the official DeepL API. However, it's important to keep in mind that the library should be used responsibly and in compliance with the DeepL website's terms of service and policies.

## Installation

You can install DeepLScrapper using pip:

```bash
pip install DeepLScrapper
```

## Usage

```python
from DeepLScrapper import DeepLScrapper

# Initialize the translator with a custom rate limit delay of 5 seconds
translator = DeepLScrapper(rate_limit_delay=5)

try:
    # Translate text from English to German
    translation = translator.translate('Hello, World!', source_lang='en', target_lang='el')
    print("Translation 1:", translation)

    # Translate the same text again to test caching
    translation_cached = translator.translate('Hello, World!', source_lang='en', target_lang='el')
    print("Translation 2 (Cached):", translation_cached)

    # Translate multiple texts in bulk
    texts = ['How are you?', 'Goodbye!', 'Welcome back.']
    bulk_translations = translator.translate(texts, source_lang='en', target_lang='fr')
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

## Dependencies

- Selenium
- BeautifulSoup4

## Version History


- 1.5.[0-2]
    - Restructured the project
    - Fixed the issue to using the library
    - Updated the documentation regarding the changes
- 1.[3-5].0
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