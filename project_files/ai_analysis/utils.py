import hashlib
import requests
from django.conf import settings


# Function to assign the given text to a hash (using Python hashlib)
def text_to_md5_hash(self, text):
    # Encode the text
    encoded_text = text.encode()
    # Convert encoded text to md5 hash
    md5_hash_result = hashlib.md5(encoded_text)
    # Digest the hash as a hexadecimal and return it
    return md5_hash_result.hexdigest()


def analyzePoliticalBias(self, article_text):
    # TODO: I will find 'ideal' sentences from an article
    sentences = article_text.split('.')

    # Restrict to 5 sentences per article (5 is arbitrary for testing, i'm not sure what a good limit is yet)
    if (len(sentences) >= 5):
        sentences = sentences[:5]

    def query(payload):
        response = requests.post(settings.HUGGINGFACE_API_URL,
                                 headers=settings.HUGGINGFACE_API_HEADERS, json=payload)
        return response.json()

    # Query for all sentences and gather the results in a 'results' array
    results = []
    for sentence in sentences:
        output = query({"inputs": sentence})
        results.append(output)

    # Associate each result with the sentence text. For displaying to the user later on.
    result_dict = {}
    for i in range(5):
        result_dict[sentences[i]] = results[i]

    return result_dict
