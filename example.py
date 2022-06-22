import json
import random

dict = {}

with open("result.json", "r") as f:
    dict = json.load(f)


def getWinner(a, b):
    # checks if a is the winners
    for i in dict[a].keys():
        if i == b:
            # returns the winner and a sentence: WINNER + SENTENCE CORRESPONDING
            return a, a+' '+dict[a][i]
    # checks if b is the winners
    for i in dict[b].keys():
        if i == a:
            return b, b+' '+dict[b][i]


n = 0
while True:
    n += 1
    a = input("\nManche {}:\nChoisissez un signe: ".format(n)).upper()
    b = random.choice(list(dict.keys()))
    b = input("Choisissez un signe: ".format(n)).upper()
    print(a+'\n'+b)
    winner, sentence = getWinner(a, b)
    if winner == a:
        print("Gagné! **********************")
    else:
        print("Perdu... xxxxxxxxxxxxxxxxxxxx")
    print(sentence)
