from .utility import *
from .utility import *
from .ciphering import *
from .deciphering import *
from .knapsack_solver import back_tracking_solution



class Knapsack():


    def __init__(self,priKey=None,pub_key = None):
        if(priKey == None):
            self.private_key = generate_super_increasing_vector(8)
            self.M = determine_modulo_acc_to_random_key_vector(self.private_key)
            self.W = determine_element_to_mask(self.M)
        else:
            self.private_key = priKey[0]
            self.M = priKey[1]
            self.W = priKey[2]
        
        if(pub_key == None):
            self.M = determine_modulo_acc_to_random_key_vector(self.private_key)
            self.W = determine_element_to_mask(self.M)
            self.public_key = generate_public_key_vector(self.private_key, self.M, self.W)
        else:
            self.public_key = pub_key


    def cipher(self,msg: str) -> list: 
        text_bits = convert_text_to_bit(msg,len(self.public_key))
        bits_grouped = group_on_sequence(text_bits,len(self.public_key))
        return cipher_with_bit_sequences(self.public_key,bits_grouped)



    def decipher(self,msg: list) -> str:
        deciphered_vector = decipher_vector_elements(msg, self.M, self.W)

        deciphered_bit_sequences = list()
        for i in range(0, len(deciphered_vector)):
            deciphered_item = deciphered_vector[i]
            deciphered_bit_sequence = back_tracking_solution(self.private_key, deciphered_item,"")
            deciphered_bit_sequences.append(deciphered_bit_sequence)

        deciphered_text = ""
        for i in range(0, len(deciphered_bit_sequences)):
            deciphered_bit_sequence = deciphered_bit_sequences[i]
            bit_to_text = convert_bit_to_text(deciphered_bit_sequence, len(self.private_key))
            deciphered_text += bit_to_text
        
        return deciphered_text

    
    
    def set_PubKey(self,key):
        self.public_key = key

    def set_PriKey(self,key):
        self.private_key = key[0]
        self.M = key[1]
        self.w[2]

