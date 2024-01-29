import hashlib


# Function to assign the article_text_md5 hash based on the article text (using Python hashlib)
def article_text_to_md5_hash(self, article_text):
    # Encode article text
    encoded_text = article_text.encode()
    # Convert to md5 hash
    md5_hash_result = hashlib.md5(encoded_text)
    # Digest the hash as hexadecimal and return it
    return md5_hash_result.hexdigest()
