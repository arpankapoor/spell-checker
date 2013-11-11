def remove_last_char(string):
    """(str) -> str

    Return the string line without the last character.

    >>> remove_last_char('abcde')
    'abcd'
    >>> remove_last_char('efgh\n')
    'efgh'
    """
    return string[:-1]


def create_dictionary(words):
    """(list of str) -> dict(int:list)

    Return a python dict with keys as integers and values as list of words
    having length equal to the key.

    >>> create_dictionary(['a', 'an', 'hello', 'my'])
    {1: ['a'], 2: ['an', 'my'], 5: ['hello']}
    >>> create_dictionary(['yollo', 'dictionary', '', 'elegant'])
    {0: [''], 5: ['yollo'], 7: ['elegant'], 10: ['dictionary']}
    """
    from collections import defaultdict
    dictionary = defaultdict(list)

    for word in words:
        dictionary[len(word)].append(word)

    return dictionary


def list_sentences(text):
    """(str) -> (list of str)

    Return a list of sentences contained in the text with the ending
    punctuation removed.

    PRECONDITIONS:
    1. A sentence must end with one of: '.' or '!' or '?'.
    2. A new sentence after the first sentence must start with a space.

    >>> list_sentences('Hello there! I am python. How are you?')
    ['Hello there!', 'I am python.', 'How are you?']
    >>> list_sentences('Where are you? India?')
    ['Where are you?', 'India?']
    """
    sentences = []
    start = 0

    for index, char in enumerate(text):
        if char in '.!?':
            new = text[start: index+1]
            start = index + 2
            sentences.append(new)

    return sentences


def list_words(sentence):
    """(str) -> (list of str)

    Return a list of words in the sentence.

    REFERENCE: http://stackoverflow.com/questions/1059559/

    >>> list_words('How are you')
    ['How', 'are', 'you']
    >>> list_words('Hello, may I know your name')
    ['Hello', 'may', 'I', 'know', 'your', 'name']
    >>> list_words("Hey, you - what are you doing here")
    ['Hey', 'you', 'what', 'are', 'you', 'doing', 'here']
    """
    import re

    return re.findall(r"[\w']+", sentence)


def present_in_dict(word, dictionary):
    """(str, dict) -> bool
    
    Check if word is present in the dictionary.
    In other words, check if the word is correctly spelled.

    The dictionary has integral keys and values as list of words with length
    equal to the key.

    >>> present_in_dict('across', {1: ['a'], 6: ['across', 'mellow']})
    True
    >>> present_in_dict('helle', {2: ['an'], 5: ['hello'], 4: ['here']})
    False
    >>> present_in_dict('Hello', {2: ['an'], 5: ['hello'], 4: ['here']})
    True
    """
    return word.lower() in dictionary[len(word)]


def find_closest_match(word, dictionary):
    """(str, dict) -> str

    Return a word from the dictionary that has a just the last character
    different from the given word.
    In other words, return the correctly spelled word.

    PRECONDITION:
    The correctly spelled word should be present in the dictionary.

    >>> find_closest_match('helle', {2: ['an'], 5: ['hello']})
    'hello'
    >>> find_closest_match('yelloy', {6: ['yellow', 'orange', 'yellos']})
    'yellos'
    >>> find_closest_match('HELLE', {2: ['an'], 5: ['hello']})
    'HELLO'
    """ 
    # Given word with last character removed and converted to lowercase.
    given_word = remove_last_char(word)
    given_word_lower = given_word.lower()

    # Sorted list of words with same length as that of the given length.
    words_with_given_length = sorted(dictionary[len(word)])

    for w in words_with_given_length:
        if remove_last_char(w) == given_word_lower:
            if word[-1].isupper():
                return given_word + w[-1].upper()
            else:
                return given_word + w[-1]


def is_correct_sentence(sentence, dictionary):
    """(str) -> bool

    Check if the given sentence has all the words spelt correctly.

    >>> is_correct_sentence('We went to the movie', {2: ['we', 'to'], 3: ['the'], 4: ['went'], 5: ['movie']})
    True
    >>> is_correct_sentence('Ww reached there.', {2: ['we'], 5: ['there'], 7: ['reached']})
    False
    >>> is_correct_sentence('I must sat!', {1: ['i'], 3: ['say'], 4: ['must']})
    False
    """
    words = list_words(sentence)
    for word in words:
        if not present_in_dict(word, dictionary):
            return False
    return True


def correct_sentence(sentence, dictionary):
    """(str) -> str

    Return a sentence with all the words spelt correctly.

    >>> correct_sentence('Ww reached there.', {2: ['we'], 5: ['there'], 7: ['reached']})
    'We reached there.'
    >>> correct_sentence('I must sat!', {1: ['i'], 3: ['say'], 4: ['must']})
    'I must say!'
    """
    # TODO: Save punctuations and their locations.
    #punctuations = []
    #for char in sentence:
    #    if char in ',.;:?!-':

    end_punc = sentence[-1]
    words = list_words(sentence)

    new_sentence = ''

    for word in words:
        if present_in_dict(word, dictionary):
            new_sentence += word + ' '
        else:
            new_sentence += find_closest_match(word, dictionary) + ' '

    # Remove the white space just after the last word
    return remove_last_char(new_sentence) + end_punc


if __name__ == '__main__':
    import sys
    dictname = sys.argv[1]
    testname = sys.argv[2]
    with open(dictname, 'r') as dictfile:
        words = []
        for line in dictfile:
            words.extend(list_words(line))
    dictionary = create_dictionary(words)
    testfile = open(testname, 'r')
    sentences = list_sentences(testfile.read())
    testfile.close()
    for sentence in sentences:
        if not is_correct_sentence(sentence, dictionary):
            print correct_sentence(sentence, dictionary)
