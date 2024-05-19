"""
Author: Chukwunazaekpere Emmanuel Obioma
Nationality: Biafran
Email-1: chukwunazaekpere.obioma@ue-germany.de 
Email-2: ceo.naza.tech@gmail.com
************************************************************
Course: Software Optimisation
Written: May 12th 2024
Due: May 20th 2024
instructions: 
"""
import logging 
from datetime import datetime
logger = logging.getLogger(__name__)
log_date = datetime.now()
# logging.basicConfig(filename="texts/logs.log", level=logging.INFO)
logging.basicConfig(level=logging.INFO)
# import OpenTextMode

class MonoAlphebeticNumericSubstitution:
    def __init__(self, key: int) -> None:
        self.key = key
        self.special_chars = ["-", "."]

    def _file_opener(self, file, mode: str, char_to_write=""):
        """Read file containing message to be encrypted or decrypted"""
        if mode == "r":
            with open(file=file, mode="r")as file_data:
                file_content = file_data.read()
            return file_content
        elif mode == "w":
            with open(file, "w")as message_file:
                message_file.write("")
        else:
            with open(file, "+a")as encrypt_message_file:
                encrypt_message_file.write(char_to_write)


    def _generate_array_and_actual_indexer(self):
        """Clean file, generate actual key & array for substitution"""
        try:
            file_alpha = "texts/alphabets_of_plain_message.txt"
            alphabets_of_plain_message = self._file_opener(file_alpha, "r")
            cipher_space = []
            for char in alphabets_of_plain_message:
                if char != " ":
                    cipher_space.append(char.upper())
            array_length = len(cipher_space)
            key_plus_cipher_space_len = self.key + array_length
            substitution_space = [*cipher_space]
            while len(substitution_space) < key_plus_cipher_space_len:
                substitution_space = [*substitution_space, *cipher_space]
            return cipher_space, substitution_space
        except Exception as error:
            # print("\n\t error-2: ", error)
            return {"cipher_space": error, "substitution_space": error}
            

    def _generate_substitution(self):
        """Generate the substitution dictionary"""
        try:
            substitution_dict = {}
            cipher_space, substitution_space = self._generate_array_and_actual_indexer()
            if type(cipher_space) == list:
                for index, char in enumerate(cipher_space):
                    substitution_dict[char] = substitution_space[self.key+index]
                return cipher_space, substitution_dict
        except Exception as err:
                return err
    def alpha_encrypt_message(self, message_to_encrypt):
        """Encrypt the message alphabetically"""
        cipher_space, substitution_dict = self._generate_substitution()
        message_content = self._file_opener(message_to_encrypt, "r")
        encrypted_message_file = "texts/numeric_encrypted_message.txt"
        self._file_opener(encrypted_message_file, "w")# clear message file, if it exists
        for char in message_content:
            upper_char = char.upper()
            encrypted_char = char if upper_char not in cipher_space else substitution_dict[upper_char]
            self._file_opener(encrypted_message_file, "+a", encrypted_char)
        return substitution_dict
    

    def encrypt_message(self, message_to_encrypt):
        """Encrypt the message with numeric substitution"""
        self.alpha_encrypt_message(message_to_encrypt)
        cipher_space, substitution_dict = self._generate_substitution()
        alpha_encrypted_message_file = "texts/numeric_encrypted_message.txt"
        alpha_encrypted_message_content = self._file_opener(alpha_encrypted_message_file, "r")
        logger.info(f"\n\t {log_date} started encrypting message alpha-numerically......")
        encrypted_message_file = "texts/numeric_encrypted_message.txt"
        each_word = ""
        word_index = 0
        self._file_opener(alpha_encrypted_message_file, "w")   # Erase old alpha encrypted message
        substitution_dict_keys = substitution_dict.keys()
        numeric_substitution_dict = self._generate_numeric_substitution_dictionary(substitution_dict_keys)
        print("\n\t numeric_substitution_dict: ", numeric_substitution_dict)
        for char in alpha_encrypted_message_content:
            if char not in self.special_chars:
                each_word+=char
            else:
                word_index+=self.key
                for word_char in each_word:
                    encrypted_char = f"{word_char}" if word_char not in substitution_dict_keys else f"{word_index}-{numeric_substitution_dict[word_char]}-"
                    self._file_opener(encrypted_message_file, "+a", encrypted_char)
                each_word = ""
        logger.info(f"\n\t {log_date} Encrypted message was witten to 'encrypted_message.txt'......")
    
    def _generate_numeric_substitution_dictionary(self, substitution_dict_keys: list):
        numeric_substitution_dict = {}
        for index, key in enumerate(substitution_dict_keys):
            numeric_substitution_dict[key] = str(index+1)
        return numeric_substitution_dict
    

    def _switch_substitution_dict_key_for_value(self, obj: dict):
        keys = list(obj.keys())
        values = obj.values()
        new_dict = {}
        for index, value in enumerate(values):
            new_dict[value] = keys[index]
        return new_dict
    def _return_chars_in_form(self, arr: str):
        ret_arr = []
        char=""
        for er in arr:
            if er != "-":
                char+=er
            else:
                ret_arr.append(char)
                char=""
        return ret_arr
    def _extract_chars_form(self, arr: list, transversed_substitution_dict: dict, decrypted_message_file):
        last_index = len(arr)-1
        count = 0
        while count <= last_index:
            if count % 2 != 0:
                ciphered_char = transversed_substitution_dict[arr[count]]
                self._file_opener(decrypted_message_file, "+a", ciphered_char)
            count+=1
        self._file_opener(decrypted_message_file, "+a", " ")

    def _numeric_decrypt(self, encrypted_message):
        """Decrypt the message"""
        cipher_space, substitution_dict = self._generate_substitution()
        substitution_dict_keys = substitution_dict.keys()
        numeric_substitution_dict = self._generate_numeric_substitution_dictionary(substitution_dict_keys)
        transversed_substitution_dict = self._switch_substitution_dict_key_for_value(numeric_substitution_dict)
        numeric_message_content = self._file_opener(encrypted_message, "r")
        decrypted_message_file = "texts/numeric_decrypted_message.txt"
        self._file_opener(decrypted_message_file, "w")   # Erase old alpha encrypted message
        # print("\n\t transversed_substitution_dict: ", transversed_substitution_dict)
        # print("\n\t numeric_substitution_dict: ", numeric_substitution_dict)
        req_char=""
        for index, char in enumerate(numeric_message_content):
            if " " not in char:
                req_char+=char
            else:
                # print("\n\t req_char: ", req_char)
                new_form = self._return_chars_in_form(req_char)
                # print("\n\t new_form-1: ", new_form)
                if len(new_form) == 0:
                    self._file_opener(decrypted_message_file, "+a", f"{req_char} ")
                else:
                    self._extract_chars_form(new_form, transversed_substitution_dict, decrypted_message_file)
                req_char=""
                

    def decrypt_message(self, encrypted_message):
        """Decrypt the message"""
        self._numeric_decrypt(encrypted_message)
        encrypted_ciphered_message = "texts/numeric_decrypted_message.txt"
        encrypted_message_content = self._file_opener(encrypted_ciphered_message, "r")
        cipher_space, substitution_dict = self._generate_substitution()
        transversed_substitution_dict = self._switch_substitution_dict_key_for_value(substitution_dict)
        logger.info(f"\n\t {log_date} *****Now decrypting mono-alphabetic-numeric ciphered text*****")
        decrypted_message_file = "texts/numeric_decrypted_plain_message.txt"
        for index, char in enumerate(encrypted_message_content):
            upper_char = char.upper()
            decrypted_char = char if upper_char not in cipher_space else transversed_substitution_dict[upper_char]
            self._file_opener(decrypted_message_file, "+a", decrypted_char)
        logger.info(f"\n\t {log_date} Decrypted message was witten to 'decrypted_message.txt'......")
        
        

ciphering = MonoAlphebeticNumericSubstitution(5)
message_to_encrypt = "texts/message_to_encrypt.txt"
# step_index = 1 # or numeric_character_index
ciphering.encrypt_message(message_to_encrypt)

encrypted_message = "texts/numeric_encrypted_message.txt"
ciphering.decrypt_message(encrypted_message)