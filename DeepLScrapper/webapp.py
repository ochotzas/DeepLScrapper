from flask import Flask, request, jsonify, render_template

from DeepLScrapper import DeepLScrapper


class DeepLWebApp:
    """
    An interactive web application for translating text using DeepLSrapper.

    This class encapsulates a Flask web application that allows users to input text
    and a target language for translation. It utilizes the DeepLScrapper class for
    performing translations. The server can be started and stopped using the provided
    methods.

    Args:
        rate_limit_delay (int, optional): The delay in seconds between retries when rate-limited by DeepL. Default is 5.
        enable_caching (bool, optional): Enable or disable caching of translations. Default is True.
        max_cache_size (int, optional): Maximum number of cached translations to keep. Default is 100.
        multi_threading (bool, optional): Enable or disable multi-threading for parallel translation. Default is True.

    Note:
        - The 'flask' library is used to create the web application.
        - The 'jinja2' library is used to render the HTML templates.
    """

    def __init__(self, rate_limit_delay=5, enable_caching=True, max_cache_size=100, multi_threading=True):
        self.app = Flask(__name__)
        self.translator = DeepLScrapper(rate_limit_delay, enable_caching, max_cache_size, multi_threading)
        self.languages = {
            "de": "German 🇩🇪",
            "fr": "French 🇫🇷",
            "es": "Spanish 🇪🇸",
            "pt": "Portuguese 🇵🇹",
            "it": "Italian 🇮🇹",
            "nl": "Dutch 🇳🇱",
            "pl": "Polish 🇵🇱",
            "ru": "Russian 🇷🇺",
            "ja": "Japanese 🇯🇵",
            "zh": "Chinese 🇨🇳",
            "cs": "Czech 🇨🇿",
            "ro": "Romanian 🇷🇴",
            "da": "Danish 🇩🇰",
            "fi": "Finnish 🇫🇮",
            "el": "Greek 🇬🇷",
            "hu": "Hungarian 🇭🇺",
            "sk": "Slovak 🇸🇰",
            "sl": "Slovenian 🇸🇮",
            "sv": "Swedish 🇸🇪",
            "bg": "Bulgarian 🇧🇬",
            "et": "Estonian 🇪🇪",
            "lt": "Lithuanian 🇱🇹",
            "lv": "Latvian 🇱🇻",
            "pt-PT": "Portuguese (Portugal) 🇵🇹",
            "pt-BR": "Portuguese (Brazil) 🇧🇷"
        }

        self.app.route("/")(self.index)
        self.app.route("/translate", methods=["POST"])(self.translate)

    def index(self):
        """
        Display the index page of the web application.
        """
        return render_template("index.html", languages=self.languages)

    def translate(self):
        """
        Handle translation requests from the user.

        Retrieves the text and target language from the user's input and attempts
        to translate the text using the DeepLScrapper translator.

        Returns:
            A JSON response containing either the translation or an error message.
        """
        text = request.form["text"]
        target_lang = request.form["target_lang"]

        try:
            translation = self.translator.translate(text, source_lang="en", target_lang=target_lang)
            return jsonify({"translation": translation})
        except Exception as e:
            return jsonify({"error": str(e)})

    def add_language(self, lang_code, lang_value):
        """
        Add a language and its value to the languages' dictionary.

        Args:
            lang_code (str): The language code.
            lang_value (str): The language value.

        Returns:
            True if the language was added successfully, False otherwise.
        """
        if lang_code and lang_value:
            self.languages[lang_code] = lang_value
            return True
        else:
            return False

    def start_server(self, debug=True):
        """
        Start the Flask server.

        Args:
            debug (bool): Whether to run the server in debug mode.
        """
        self.app.run(debug=debug)
