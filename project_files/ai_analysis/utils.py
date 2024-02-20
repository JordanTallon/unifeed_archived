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
    # We are primarily concerned with ORG, PERSON, GPE, NORP
    # Further elaboration under machine learning section of the technical specification
    relevant_entities = {'ORG', 'PERSON', 'GPE', 'NORP'}
    entity_count = 0
    adjective_count = 0
    html_string = ""

    # This keeps track of all the entity 'spans' (the chars at which they begin and end)
    ent_indices = set()

    for ent in sentence.ents:
        if ent.label_ in relevant_entities:
            html_string += f'<span class="entity entity-{ent.label_}">{ent.text}</span>'
            entity_count += 1
            # Add the span to the indices set
            ent_indices.update(range(ent.start, ent.end))

    for token in sentence:
        # Ignore if it overlaps with any entity indices
        # We want entity recognition prioritized and also need to avoid the added html
        if token.i in ent_indices:
            continue
        if token.pos_ == "ADJ":
            html_string += f'<span class="adjective">{token.text}</span>'
            adjective_count += 1
        else:
            html_string += token.text
        if not token.is_punct:
            html_string += ' '

    return entity_count, adjective_count, html_string


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
    doc = nlp(article_text)
    sentence_data = []

    for sentence in doc.sents:
        sentence_text = sentence.text.strip()
        words = sentence_text.split()
        # My political bias AI is trained on sentences between 8 and 90 words, so its ideal we stay within that range.
        # 8-90 is a good range, so this will cover most sentences.
        if 8 <= len(words) <= 90:
            adj_count, ent_count, html = count_entities_and_adjectives_in_sentence(
                sentence)
            bias_adj_count = count_biased_adjectives_in_sentence(sentence_text)
            polarity, subjectivity = extract_polarity_and_subjectivity(
                sentence_text)
            sentence_data.append({
                'sentence': sentence_text,
                'sentence_html': html,
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

    sentence_df = bias_candidates.drop(
        columns=['bias_adj_count', 'ent_count', 'adj_count'])

    # Return top 8 results
    return sentence_df.head(8)


def analyse_sentences_for_bias(sentences_json):

    # Convert the Celery serialized json back to a dataframe
    sentences_df = pd.read_json(sentences_json, orient="split")

    def query(payload):
        try:
            response = requests.post(settings.HUGGINGFACE_API_URL,
                                     headers=settings.HUGGINGFACE_API_HEADERS, json=payload)
            response.raise_for_status()

            data = response.json()

            # Verify if the response is correct
            # It should contain multiple lists like 'label':'center', 'score':'0.5' etc
            if isinstance(data, list) and all(isinstance(item, list) for item in data):
                for item_list in data:
                    for item in item_list:
                        # Ensure that the label / score is there
                        if not all(k in item for k in ('label', 'score')):
                            raise ValueError(
                                "Unexpected item structure in response")
                return data
            else:
                raise ValueError("Unexpected response format")

        # TODO: Handle request / validation errors more sophisticatedly. For now just raise a
        # ValueError to display a generic error message to the user
        except requests.exceptions.RequestException as e:
            raise ValueError(f"HTTP or Request error: {e}")

        except ValueError as ve:
            raise ValueError(f"Response validation error: {ve}")

    sentences = sentences_df['sentence'].tolist()

    # Query for all sentences and gather the results in a 'results' array
    results = []
    for sentence in sentences:
        output = query({"inputs": sentence})

        # Check if the HuggingFace inference api is sleeping (it does if it wasn't called for a few minutes)
        if 'error' in output and 'currently loading' in output['error']:
            # If the model is still loading, raise an error
            raise ValueError("Model is currently loading")

        results.append(output)

    # Convert dataframe columns to lists
    html_list = sentences_df['sentence_html'].tolist()
    polarity_list = sentences_df['polarity'].tolist()
    subjectivity_list = sentences_df['subjectivity'].tolist()

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
            'html': html_list[i],
            'polarity': polarity_list[i],
            'subjectivity': subjectivity_list[i],
            'conclusion': conclusion,
            'conclusion_strength': conclusion_strength,
        }

    return result_dict
