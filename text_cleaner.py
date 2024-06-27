from typing import List

class Parser:
    def __init__(self, input_string):
        self.input = self.__clean_input(input_string)
        self.current_token = None

    def parse(self) -> List[str]:
        try:
            self.current_token = self.__get_next_token()
            return self.__sentence()
        except ValueError as e:
            print(e)
            raise ValueError('La oración no forma parte de la lengua española')

    def load_input(self, input_string):
        self.input = self.__clean_input(input_string)
        self.current_token = None

    def __clean_input(self, input_string):
        cleaned_input = []
        for char in input_string:
            if char.isalpha() or char.isspace():
                cleaned_input.append(self.__to_lower(char))
            elif char in ['.', ',',';','!','?','¿','¡']:
                cleaned_input.append(' ')

        return cleaned_input

    def __to_lower(self, char):
        # Mapa de caracteres acentuados a sus equivalentes en minúscula
        accent_map = {
            'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'Ñ': 'ñ', 'ñ': 'ñ'
        }
        if char in accent_map:
            return accent_map[char]
        return char.lower()

    def __get_next_token(self):
        if self.input:
            return self.input.pop(0)
        else:
            return None

    def __match(self, token):
        if self.current_token == token:
            self.current_token = self.__get_next_token()
        else:
            raise ValueError(f"Invalid character: expected '{token}'")

    def __sentence(self):
        if self.__is_letter(self.current_token):
            return [self.__word()] + self.__elements()
        else:
            self.__punctuation()
            return self.__elements()

    def __elements(self):
        if self.current_token is None:
            return []
        if self.__is_letter(self.current_token):
            return [self.__word()] + self.__elements()
        else:
            self.__punctuation()
            return self.__elements()

    def __word(self):
        return self.__letter() + self.__word_tail()

    def __word_tail(self):
        if self.current_token is None:
            return ''
        if self.__is_letter(self.current_token):
            return self.__letter() + self.__word_tail()
        else:
            return self.__punctuation()

    def __letter(self):
        # Manejamos todas las letras minúsculas y caracteres especiales aquí
        if self.current_token in 'abcdefghijklmnopqrstuvwxyzñ':
            char = self.current_token
            self.__match(self.current_token)
            return char
        raise ValueError(f"Invalid letter: {self.current_token}")

    def __punctuation(self):
        if self.current_token in [' ', '\t', '\n']:
            self.current_token = self.__get_next_token()
            return ''
        raise ValueError(f"Invalid character: {self.current_token}")

    def __is_letter(self, char):
        return char.isalpha() if char else False
