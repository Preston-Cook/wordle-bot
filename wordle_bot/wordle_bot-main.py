import random as r
from datetime import datetime
from itertools import combinations, chain
from collections import Counter

# Import solution from JS file scrape
from scrape import solution

# Import client for Twitter API
from tweet import client


def get_seconds(time: str) -> float:
    """Converts HH:MM:SS format into seconds"""
    hh, mm, ss = time.split(':')
    return float(hh) * 3600 + float(mm) * 60 + float(ss)


def get_substrings(s1: str) -> list:
    """Returns all substrings of a word with slice indices"""
    return [f"{s1[x:y]}{x}{y}" for x, y in combinations(range(6), r=2)]

def substr_count(s1, substr_frequency):
    """Returns the number of substrings contained within a string"""
    count = 0
    for slice, _ in substr_frequency:
        substr, start, end = slice[:-2], int(slice[-2]), int(slice[-1])
        if s1[start: end] == substr:
            count += 1
    return count 



with open('valid-words.txt') as fh: 
    word_bank = tuple(line.rstrip() for line in fh)

# Use crane as first guess
guess = 'crane'

# Initialize data structs for guess feedback
green = ()
yellow = {}
gray = set()
attempts = 1

# Get timestamp for when guessing begins
start = datetime.now()

while attempts < 6 and guess != solution:

    # Check for correct letter positions
    green = tuple(guess[i] if guess[i] == solution[i] else '$' for i in range(5))

    # Check for yellow on gray letters
    for i in range(5):
        if green[i] != '$':
            continue
        if green.count(guess[i]) + len(yellow.get(guess[i],'')) < solution.count(guess[i]):
            yellow.setdefault(guess[i],[]).append(i) 
        else:
            gray.add(guess[i])

    # Initialize possibilities list
    possibilities = []

    # Narrow word bank and append to possibilities
    for word in word_bank:
        if all(s1 == s2 for s1,s2 in zip(green,word) if s1 != '$'):
            if all(k in word for k in yellow) and all(i not in yellow[word[i]] for i in range(5) if word[i] in yellow):
                if not any(word.count(s1) > len(yellow.get(s1,'')) + green.count(s1) for s1 in gray):
                    possibilities.append(word)
    
    # In case bot receives no new info from guess, remove guess
    if guess in possibilities:
        possibilities.remove(guess)

    # Gather confirmed substrings
    confirmed_substrings = list(filter(lambda x : '$' not in x, get_substrings(''.join(green))))
    
    # Gather substrings available in remaining possibilities as long as they aren't confirmed
    all_substrings = filter(lambda x : x not in confirmed_substrings, chain(*map(get_substrings, possibilities)))

    # Collect count of substrings and extract most common non-confirmed substring
    most_common = Counter(all_substrings).most_common(1)[0][0]

    # Retrieve substring and its indices
    substring, str_start, str_end = most_common[:-2], int(most_common[-2]), int(most_common[-1])

    # Gather guesses that eliminate the most choices if incorrect
    max_info_lst = list(filter(lambda x : x[str_start: str_end] == substring, possibilities))

    # Randomly select guess from list of most valuable guesses
    guess = r.choice(max_info_lst)

    print(guess, attempts)
    word_bank = possibilities.copy()
    attempts += 1

dif = get_seconds(str(datetime.now() - start))

if guess == solution:
    client.create_tweet(text=f'I just solved today\'s Wordle word "{guess}" after {attempts} tries in {dif} seconds!')
else:
    client.create_tweet(text='Unfortunately, I was not able to solve today\'s Wordle Word.')
