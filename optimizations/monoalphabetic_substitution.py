"""
Author: Chukwunazaekpere Emmanuel Obioma
Nationality: Biafran
Course: Software Optimisation
Due: May 20th 2024
instructions: Please create a "texts" folder in your workspace

"""
import logging 
from datetime import datetime
logger = logging.getLogger(__name__)
log_date = datetime.now()
logging.basicConfig(level=logging.INFO)

class MonoAlphebeticSubstitution:
    def __init__(self, key: int) -> None:
        self.key = key

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

    def encrypt_message(self, message_to_encrypt):
        """Encrypt the message"""
        cipher_space, substitution_dict = self._generate_substitution()
        message_content = self._file_opener(message_to_encrypt, "r")
        logger.info(f"\n\t {log_date} started encrypting message......")
        encrypted_message_file = "texts/encrypted_message.txt"
        self._file_opener(encrypted_message_file, "w")
        for index, char in enumerate(message_content):
            upper_char = char.upper()
            encrypted_char = char if upper_char not in cipher_space else substitution_dict[upper_char]
            self._file_opener(encrypted_message_file, "+a", encrypted_char)
        logger.info(f"\n\t {log_date} Encrypted message was witten to 'encrypted_message.txt'......")
    

    def _switch_substitution_dict_key_for_value(self, obj: dict):
        keys = list(obj.keys())
        values = obj.values()
        new_dict = {}
        for index, value in enumerate(values):
            new_dict[value] = keys[index]
        return new_dict
    def decrypt_message(self, encrypted_message):
        """Decrypt the message"""
        cipher_space, substitution_dict = self._generate_substitution()
        transversed_substitution_dict = self._switch_substitution_dict_key_for_value(substitution_dict)
        logger.info(f"\n\t {log_date} **********Now decrypting************")
        encrypted_message_content = self._file_opener(encrypted_message, "r")
        logger.info(f"\n\t {log_date} started decrypting message......")
        decrypted_message_file = "texts/decrypted_message.txt"
        self._file_opener(decrypted_message_file, "w")
        for index, char in enumerate(encrypted_message_content):
            upper_char = char.upper()
            decrypted_char = char if upper_char not in cipher_space else transversed_substitution_dict[upper_char]
            self._file_opener(decrypted_message_file, "+a", decrypted_char)
        logger.info(f"\n\t {log_date} Decrypted message was witten to 'decrypted_message.txt'......")
        
        

ciphering = MonoAlphebeticSubstitution(5)
message_to_encrypt = "texts/message_to_encrypt.txt"
ciphering.encrypt_message(message_to_encrypt)

encrypted_message = "texts/encrypted_message.txt"
ciphering.decrypt_message(encrypted_message)