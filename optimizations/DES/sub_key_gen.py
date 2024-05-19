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
class SubKeysGenerator:
    def __init__(self, key: int) -> None:
        self.key = key
        self.shift_schedule = [1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1]
        

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

    def _convert_hex_key_to_binary(self):
        """Convert hexa-decimal key to binary key"""
        if len(self.key) == 16:
            hex_dict = {"A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}
            hex_dict_keys = hex_dict.keys()
            bin_key = ""
            for i in self.key:
                key = i
                if key in hex_dict_keys:
                    key = hex_dict[i]
                elem_in_bin = bin(int(key))
                split = elem_in_bin.split("b")[1]
                split_len = len(split)
                req = split if split_len == 4 else f"0{split}" if split_len == 3 else f"00{split}" if split_len == 2 else f"000{split}" 
                bin_key+=f"{req}"
            return {"status": True, "message": "", "bin_key": bin_key}
        else:
            return {"status": False, "message": "Enter a key length of 16"}
        
    def _generate_permutation_table(self, rows: int, cols: int):
        """Generate permtation table, which an array of arrays"""
        perm_table = []
        perm_table_dim = 0
        rows_cols_prod = rows*cols
        start_key = rows_cols_prod+1
        row_array = [start_key]
        while perm_table_dim < rows_cols_prod:
            next_idx = 0
            row_array_len = 1
            while row_array_len < cols:
                next_idx = row_array[row_array_len-1]-8
                row_array.append(next_idx if next_idx-8 > 0 else next_idx+start_key)
                row_array_len+=1
            perm_table.append(row_array)
            perm_table_dim+=cols
            row_array = []
            if next_idx-8 <= 0:
                row_array = [next_idx+start_key]
            else:
                row_array = [next_idx-8]
        return perm_table

    def _generate_permutation_key(self, perm_table: list, key: str):
        """Generate permtation key"""
        perm_key = ""
        no_cols = len(perm_table[0])
        straight_perm_table = []
        for arr_row in perm_table:
            straight_perm_table = [*straight_perm_table, *arr_row]
        aux_key = ""
        for elem in straight_perm_table:
            aux_key+=key[elem-1]
            if len(aux_key) == no_cols:
                perm_key+=(aux_key+" ")
                aux_key=""
        return perm_key
    
    def _shift_keys_by_block(self, key:str, number_of_shift: int):
        """Shift a key blocks to the by the left, using the number of shift"""
        middle = len(key)//2
        first_key = key[0:middle]
        second_key = key[middle:]
        first_split_first_key = first_key.split(" ")[0]
        second_split_first_key = first_key.split(" ")[1]
        splitted_2nd_key = second_key.split(" ")
        req_2nd_keys = [split for split in splitted_2nd_key if split != ""]
        splitted_1st_key = second_key.split(" ")
        req_1st_keys = [split for split in splitted_1st_key if split != ""]
        sub_key_list = [*req_2nd_keys, *req_1st_keys] if number_of_shift == 2 else [second_split_first_key, *req_2nd_keys, first_split_first_key]
        shifted_key = ""
        for key_block in sub_key_list:
            shifted_key+=(key_block+" ")
        print("\n\t _shift_keys_by_block-key: ", key)
        print("\n\t _shift_keys_by_block-number_of_shift: ", number_of_shift)
        print("\n\t _shift_keys_by_block-shifted_key: ", shifted_key)
        return shifted_key
    
    def _left_shift_perm_keys(self, perm_key: str):
        """Do a left shift on permutation keys"""
        middle = len(perm_key)//2
        splitted_key_0 = perm_key[0:middle]
        splitted_key_1 = perm_key[middle:]
        splitted_keys_dict = {"splitted_key_0": splitted_key_0, "splitted_key_1": splitted_key_1}
        count = 2
        for shift in self.shift_schedule:
            sub_keys_dict_key = list(splitted_keys_dict.keys())
            key_0 = splitted_keys_dict[sub_keys_dict_key[len(sub_keys_dict_key)-2]]
            key_1 = splitted_keys_dict[sub_keys_dict_key[len(sub_keys_dict_key)-1]]
            sub_key_1 = self._shift_keys_by_block(key_0, shift)
            sub_key_2 = self._shift_keys_by_block(key_1, shift)
            splitted_keys_dict[f"splitted_key_{count}"] = sub_key_1
            splitted_keys_dict[f"splitted_key_{count+1}"] = sub_key_2
            count+=1
        return splitted_keys_dict

    def _join_shifted_perm_keys(self, shifted_keys: dict):
        shifted_keys_values = shifted_keys.values()
        joint_keys = ""
        joint_keys_list = []
        for idx, splitted_key in enumerate(shifted_keys_values):
            if idx == 0:
                joint_keys+=(splitted_key)
            else:
                if idx%2 == 0:
                    joint_keys+=(splitted_key)
                else:
                    joint_keys+=(splitted_key)
                    joint_keys_list.append(joint_keys)
                    joint_keys = ""
        return joint_keys_list


    def _generate_shifted_keys(self):
        """Generate an array of keys shifted by a shifting schedule"""
        rows = 8
        cols = 7
        perm_table = self._generate_permutation_table(rows, cols)
        res = self._convert_hex_key_to_binary()
        key = res['bin_key']
        perm_key = self._generate_permutation_key(perm_table, key)
        shifted_keys = self._left_shift_perm_keys(perm_key)
        joint_keys_list = self._join_shifted_perm_keys(shifted_keys)
        return joint_keys_list


    def _generate_sub_keys(self):
        """Generate an array of 48-bit keys"""
        rows = 8
        cols = 6
        joint_keys_list = self._generate_shifted_keys()
        # print("\n\t joint_keys_list: ", joint_keys_list)
        perm_table = self._generate_permutation_table(rows, cols)
        sub_keys = []
        for joint_key in joint_keys_list:
            no_space_key = ""
            for char in joint_key:
                if char != " ":
                    no_space_key+=char
            perm_key = self._generate_permutation_key(perm_table, no_space_key)
            sub_keys.append(perm_key)
        print("\n\t sub_keys: ", sub_keys)
        return sub_keys



key = "133457799BBCDFF1"
des = SubKeysGenerator(key=key)

ff = des._generate_sub_keys()
print(ff)





    