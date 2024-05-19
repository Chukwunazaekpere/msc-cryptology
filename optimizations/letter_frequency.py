"""
Author: Chukwunazaekpere Emmanuel Obioma
Nationality: Biafran
Course: Software Optimisation
Due: May 20th 2024
instructions: Please create a "texts" folder in your workspace.
In the workspace, create a file called `alphabets_of_plain_message.txt'.
This file is where we put the alphabets, in which our plain-message is
written i.e whether mother-tongue or the english alphabet
"""
class LetterFreuency:
    def __init__(self) -> None:
        pass

    def _file_reader(self, file_name):
        with open(file_name, mode="r")as file_content:
            content = file_content.read()
        return content
    
    def _total_chars_in_file(self, filename):
        chars_in_file = self._file_reader(filename)
        total_chars = 0
        chars_and_frequency = {}
        alphabets = self._file_reader("texts/alphabets_of_plain_message.txt")
        cipher_space = []
        for char in alphabets:
            if char != " ":
                cipher_space.append(char.upper())
        for char in chars_in_file:
            if char in cipher_space:
                total_chars+=1
                try:
                    chars_and_frequency[char]+=1
                except:
                    chars_and_frequency[char] = 1
        return total_chars, chars_and_frequency

    def chars_and_frequency(self, filename):
        total_chars, chars_and_frequency = self._total_chars_in_file(filename)
        keys = chars_and_frequency.keys()
        chars_frequency = {}
        for key in keys:
            ff = ((chars_and_frequency[key]/total_chars)*100)
            char = str(ff).split(".")[0]
            mant = str(ff).split(".")[1][0:4]
            chars_frequency[key] = f"{char}.{mant}%"
        print(chars_frequency)
        return chars_frequency


# file_name = "texts/ciphered_text.txt"
file_name = "texts/encrypted_message.txt"
letter_freq = LetterFreuency()
letter_freq.chars_and_frequency(file_name)
# print(letter_freq)