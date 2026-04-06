import numpy as np

def generate_header_payload(payload_str = "Test", access_code = 0x0CDE232F, access_code_len = 32, preamble_len = 64, payload_len_width=16):
    # The purpose of this function is to generate a bitstream that can be leveraged as the source
    # when using the vector source block.
    
    # Generate Sync Bits for Clock Syncronization using alternating bits
    preamble_bits = [0,1]*preamble_len
    payload_bits = []
    access_code_bits = []
    packet_length_bits = []
    
    # Assembling the Payload Bits
    for c in (payload_str):
        for i in range (7, -1, -1): #Appending the MSB->LSB bit into the payload 
            payload_bits.append((ord(c)>>i)&1)
    
    payload_len = int(np.ceil(len(payload_bits)//8))
    # Assembling the Access Code Bits
    for i in range(access_code_len-1, -1, -1):
        access_code_bits.append(access_code>>i & 1)
    
    # Assembling the Payload Length Bits
    for i in range(payload_len_width-1, -1, -1):
        packet_length_bits.append(payload_len>>i & 1)
    
    complete_packet_length = packet_length_bits + packet_length_bits

    final_vector = preamble_bits + access_code_bits + complete_packet_length + payload_bits
    return final_vector
