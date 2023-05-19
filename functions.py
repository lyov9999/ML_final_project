import re
from collections import Counter
import unicodedata
import re
import string

file_path = "data_armenian/wiki_data.txt"
# file_path = "hye_wikipedia_2021_1M-sentences.txt"


def words(text): 
    """
    Tokenizes the input text into a list of words.

    Args:
        text (str): The input text to be tokenized.

    Returns:
        list: A list of words extracted from the input text.
    """
 
    text = text.lower()

    text = unicodedata.normalize('NFC', text)     # Normalize the text using Unicode normalization form C (NFC)

    text = ''.join(char for char in text if char not in string.punctuation)  # Remove punctuation marks from the text

    return re.findall(r'\w+', text)   # Use regular expressions to extract words from the processed text and return them as a list

WORDS = Counter(words(open(file_path).read()))


def probability(word, N=sum(WORDS.values())):
    """
    Calculate the probability of a given Armenian word based on the provided dictionary.

    Args:
        word (str): The word to calculate the probability for.
        N (int, optional): The total number of words in the corpus. Defaults to the sum of word frequencies.
    
    Returns:
        float: The probability of the word.
    """
    return WORDS.get(word, 0) / N     # Return the frequency of the word divided by the total number of words in the corpus

def edits1(word):
    """
    Generates all possible edits with a single edit operation for a given word.

    Args:
        word (str): The word to generate edits for.

    Returns:
        set: A set of all possible edited variations of the word.
    """
    letters = 'աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւեփք'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]  # Split the word into all possible combinations of prefix and suffix
    deletes = [left + right[1:] for left, right in splits if right]    # Delete one character from the word
    transposes = [left + right[1] + right[0] + right[2:] for left, right in splits if len(right) > 1]   # Swap adjacent characters in the word
    replaces = [left + c + right[1:] for left, right in splits if right for c in letters]   # Replace each character in the word with each Armenian letter
    inserts = [left + c + right for left, right in splits for c in letters]  # Insert each Armenian letter at every position in the word
    return set(deletes + transposes + replaces + inserts)  

def edits2(word):
    """
    Generates all possible edits with two consecutive edit operations for a given word.

    Args:
        word (str): The word to generate edits for.

    Returns:
        set: A set of all possible edited variations of the word.
    """
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))  # Generate edits2 by applying edits1 twice on the word

def edits3(word):
    """
    Generates all possible edits with three consecutive edit operations for a given word.

    Args:
        word (str): The word to generate edits for.

    Returns:
        set: A set of all possible edited variations of the word.
    """
    return set(e3 for e2 in edits2(word) for e3 in edits1(e2))  # Generate edits3 by applying edits1 on edits2

def candidates(word, WORDS=WORDS):
    """
    Generates a list of candidate words for a given word.

    Args:
        word (str): The word to generate candidates for.
        WORDS (Counter, optional): Counter object containing word frequencies. Defaults to global WORDS.

    Returns:
        list: A list of candidate words for the given word.
    """
    if word in WORDS:  # If the word is present in the word frequency counter 
        return [word]  # Return the word itself as the only candidate
    candidates = edits1(word) | edits2(word)  # Consider both edits1 and edits2 
    # candidates = edits1(word) | edits2(word) | edits3(word)  # Consider both edits1, edits2  and edits3.

    candidates = [c for c in candidates if c in WORDS]  # Filter the edits to include only words present in the word frequency counter
    return candidates

def correction(word, WORDS=WORDS):
    """
    Corrects a given word by suggesting the most probable spelling correction.

    Args:
        word (str): The word to be corrected.
        WORDS (Counter, optional): Counter object containing word frequencies. Defaults to global WORDS.

    Returns:
        str: The corrected word.
    """

    if word in WORDS:  # If the word is present in the word frequency counter return the word as it is considered correct
        return word
    else:
        c = candidates(word, WORDS)  # Generating candidates
        if len(c) == 0:    # If no candidates return the original word
            return word
        else:
            candidate_probs = [(candidate, probability(candidate)) for candidate in c]  # Calculate the probabilities of the candidate words
            candidate_probs.sort(key=lambda x: x[1], reverse=True)  # Sort the candidate words based on their probabilities in descending order
            print("Candidate words for '{}':".format(word))
            for candidate, prob in candidate_probs:
                print("- Word: '{}', Probability: {:.6f}".format(candidate, prob))
            return candidate_probs[0][0]  # Return the most probable candidate word


def correction_automated(word): 
    """
    Returns the most probable spelling correction for a given word.

    Args:
        word (str): The word to be corrected.

    Returns:
        str: The corrected word.
    """
    return max(candidates(word), key=probability)   # Return the candidate word with the highest probability


def top_frequent_words(n):

    """
    Returns the most frequent words from the data.

    Args:
        n (int): Top n numbers.

    Returns:
        str: The top n frequent words with their frequency numbers.
    """
    top_frequent_words = WORDS.most_common(n)  # Gets the most common elements and counts
    for word, count in top_frequent_words:
        print("Word: '{}', Frequency: {}".format(word, count)) # prints the list of these common words with frequencies.


def calculate_total_words(words):
    """
    Calculates the total number of words in a dictionary and prints the result.

    Args:
        words (dict): A dictionary where the keys are words and the values are their counts.

    Returns:
        None
    """

    # Calculate the sum of all word counts in the dictionary
    total = sum(words.values())

    # Print the total number of words
    print("Total number of words: {}".format(total))

