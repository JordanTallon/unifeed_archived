import hashlib


# Function to assign the given text to a hash (using Python hashlib)
def text_to_md5_hash(self, text):
    # Encode the text
    encoded_text = text.encode()
    # Convert encoded text to md5 hash
    md5_hash_result = hashlib.md5(encoded_text)
    # Digest the hash as a hexadecimal and return it
    return md5_hash_result.hexdigest()
