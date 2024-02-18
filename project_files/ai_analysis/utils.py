import hashlib
import requests
from django.conf import settings
# spaCy nlp library
import spacy
import pandas as pd
from textblob import TextBlob
nlp = spacy.load('en_core_web_sm')


# Function to assign the given text to a hash (using Python hashlib)
def text_to_md5_hash(text):
    # Encode the text
    encoded_text = text.encode()
    # Convert encoded text to md5 hash
    md5_hash_result = hashlib.md5(encoded_text)
    # Digest the hash as a hexadecimal and return it
    return md5_hash_result.hexdigest()


def count_entities_and_adjectives_in_sentence(sentence):
    doc = nlp(sentence)

    # We are primarily concerned with ORG, PERSON, GPE, NORP
    # Further elaboration under machine learning section of the technical specification
    relevant_entities = {'ORG', 'PERSON', 'GPE', 'NORP'}
    entity_count = len(
        [ent for ent in doc.ents if ent.label_ in relevant_entities])

    # Count number of tokens that spaCy flagged as 'ADJ'
    adjective_count = sum(1 for token in doc if token.pos_ == "ADJ")

    return entity_count, adjective_count


def extract_polarity_and_subjectivity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity


def count_biased_adjectives_in_sentence(sentence):
    # These adjectives were extracted as commonly associated with different political bias labels (see technical document)
    biased_adjectives = ['white', 'other', 'anti', 'many', 'right', 'last', 'american', 'republican', 'political',
                         'black', 'last', 'more', 'democratic', 'first', 'new', 'former', 'presidential', 'american',
                         'illegal', 'pro']

    words = sentence.lower().split()

    # Count occurrences
    bias_count = sum(word in biased_adjectives for word in words)

    return bias_count


def extract_ideal_sentences(article_text):
    # TODO: I will find 'ideal' sentences from an article, for now split and get the first 5
    # Cleaning should be done here too (removing sentences that are too short, empty, etc)
    sentences = article_text.split('.')
    sentence_data = []

    for sentence in sentences:
        words = sentence.split()
        # My political bias AI is trained on sentences between 8 and 90 words, so its ideal we stay within that range.
        # 8-90 is a good range, so this will cover most sentences.
        if 8 <= len(words) <= 90:  # Check sentence length
            adj_count, ent_count = count_entities_and_adjectives_in_sentence(
                sentence)
            bias_adj_count = count_biased_adjectives_in_sentence(sentence)
            polarity, subjectivity = extract_polarity_and_subjectivity(
                sentence)
            sentence_data.append({
                'sentence': sentence,
                'adj_count': adj_count,
                'ent_count': ent_count,
                'bias_adj_count': bias_adj_count,
                'polarity': polarity,
                'subjectivity': subjectivity
            })

    sentence_df = pd.DataFrame(sentence_data)

    # Sort by the number of 'biased' adjectives in the sentence
    # Followed by the number of entities it mentions and adjective count.
    # Lastly, how subjective the sentence is, then polarity.
    # This should give us a sorted list where the first entries are the best candidates for political bias.
    bias_candidates = sentence_df.sort_values(by=['bias_adj_count', 'ent_count', 'adj_count', 'subjectivity', 'polarity'],
                                              ascending=[False, False, False, False, False])

    # Get the top 10 sentences and convert it to a list to return
    potentially_biased_sentences = bias_candidates.head(10)[
        'sentence'].tolist()
    return potentially_biased_sentences


def analyse_sentences_for_bias(sentences):

    def query(payload):
        response = requests.post(settings.HUGGINGFACE_API_URL,
                                 headers=settings.HUGGINGFACE_API_HEADERS, json=payload)

        return response.json()

    # Query for all sentences and gather the results in a 'results' array
    # TODO: lots of error handling, bad returns, sleeping server etc
    results = []
    for sentence in sentences:
        output = query({"inputs": sentence})

        # Check if the HuggingFace inference api is sleeping (it does if it wasn't called for a few minutes)
        if 'error' in output and 'currently loading' in output['error']:
            # If the model is still loading, raise an error
            raise ValueError("Model is currently loading")

        results.append(output)

    # Associate each result with the sentence text. For displaying to the user later on.
    result_dict = {}
    for i, output in enumerate(results):

        # remap HuggingFace dictionary to streamline returned object
        scores = {'left': 0, 'center': 0, 'right': 0}
        for item in output[0]:
            scores[item['label']] = item['score']

        # find the label with the highest score
        highest_score_label = max(output[0], key=lambda x: x['score'])

        # final label settled on 'left', 'right', or 'center'
        conclusion = highest_score_label['label']
        # express the conclusion with a 2 decimal place percentage. i.e 98.20%
        conclusion_strength = f"{highest_score_label['score'] * 100:.2f}%"

        result_dict[sentences[i]] = {
            'left_bias': scores['left'],
            'center_bias': scores['center'],
            'right_bias': scores['right'],
            'conclusion': conclusion,
            'conclusion_strength': conclusion_strength,
        }

    return result_dict
