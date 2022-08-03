import random as r
from datetime import datetime

from scrape import solution
from tweet import client


def get_seconds(time_str):
    hh, mm, ss = time_str.split(':')
    return float(hh)*3600 + float(mm)*60 + float(ss)


with open('valid-words.txt') as fh: 
    word_bank = tuple(line.rstrip() for line in fh)

guess = 'crane'
green = ()
yellow = {}
gray = set()
attempts = 1

start = datetime.now()

while attempts < 6 and guess != solution:
    green = tuple(guess[i] if guess[i] == solution[i] else '' for i in range(5))

    for i in range(5):
        if green[i] != '':
            continue
        if green.count(guess[i]) + len(yellow.get(guess[i],'')) < solution.count(guess[i]):
            yellow.setdefault(guess[i],[]).append(i) 
        else:
            gray.add(guess[i])

    possibilities = []

    for word in word_bank:
        if all(s1 == s2 for s1,s2 in zip(green,word) if s1 != ''):
            if all(k in word for k in yellow) and all(i not in yellow[word[i]] for i in range(5) if word[i] in yellow):
                if not any(word.count(s1) > len(yellow.get(s1,'')) + green.count(s1) for s1 in gray):
                    possibilities.append(word)
    
    # Check for probability of certain substrings given correct letters
    # Check common letter combinations in Scrabble and Banangram strategies
    
    word_bank = possibilities.copy()
    guess = r.choice(word_bank)
    attempts += 1

dif = get_seconds(str(datetime.now() - start))

if attempts < 6:
    client.create_tweet(text=f'I just solved today\'s Wordle word "{guess}" after {attempts} tries in {dif} seconds!')
else:
    client.create_tweet(text='Unfortunately, I was not able to solve today\'s Wordle Word.')
