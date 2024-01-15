class TextRecognitionResult:
    def __init__(self, text, locale, full_information):
        self.text = text
        self.locale = locale
        self.full_information = full_information

    def to_json(self):
        return {
            'text': self.text,
            'locale': self.locale,
            'full_information': self.full_information
        }
