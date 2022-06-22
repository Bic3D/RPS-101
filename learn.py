from itertools import combinations
import json
import random
import time

dict = {}
scores = {}
knownKeys = ["ROCK", "PAPER", "SCISSORS"]

with open("result.json", "r") as f:
    dict = json.load(f)

try:
    with open("gameData.json", "r") as f:
        scores = json.load(f)
except FileNotFoundError:
    print("/!\ Data file not found, skipping this step and will create a new one.\n")
    scores["knownKeys"] = knownKeys
    scores['level'] = 0


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


def sortByID(a, b):
    aID = dict[a]["id"]
    bID = dict[b]["id"]
    if aID < bID:
        return a, b
    else:
        return b, a


def round(n, a, b):
    score = 0
    try:
        score = scores[a+"-"+b]
    except KeyError as e:
        pass

    playerChoice = input(
        "The two symbols are {} and {}, who will be the winner? (or write q to save and quit)\n".format(a, b)).upper()
    if playerChoice == "Q":
        return "q"
    if (a != b):
        winner, sentence = getWinner(a, b)
        if playerChoice == winner:
            print("Congratulations!")
            score += 1
        else:
            print("That's wrong.")
            score += 0
        time.sleep(0.5)

        print(sentence)
    else:
        if playerChoice == a or playerChoice == b:
            print("Congratulations")
            score += 2
        else:
            print("That's wrong, it was ex-aequo, so you should have written any of them")
            score += 0
    time.sleep(1)

    print("\n**********\n")
    return sortByID(a, b), score


def format(a, b):
    s1, s2 = sortByID(a, b)
    return s1 + "-" + s2


def getAllCombinations(keys):
    combinations = []
    for key1 in keys:
        for key2 in keys:
            if format(key1, key2) not in combinations:
                combinations.append(format(key1, key2))
    return combinations


def getAllCombsScores(combs, scores):
    combsDict = {}
    for comb in combs:
        # try to get the score for this comb
        try:
            combsDict[comb] = scores[comb]
        except KeyError:
            combsDict[comb] = 0
    return combsDict


def getLowestID(dictionnary):
    keys = list(dictionnary.keys())
    return min(keys)


def sortCombsByScore(combs):
    sortedDict = {}
    for comb in list(combs.keys()):
        try:
            sortedDict[combs[comb]] = sortedDict[combs[comb]]+[comb]
        except KeyError:
            sortedDict[combs[comb]] = [comb]
        except TypeError:
            sortedDict[combs[comb]] = [comb]
        except AttributeError:
            sortedDict[combs[comb]] = [comb]
    return sortedDict


def unlockNewSymbol(symbols, knownSymbols):
    unknown = []
    for symbol in symbols:
        if symbol not in knownSymbols:
            unknown += [symbol]
    new = random.choice(unknown)
    print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n          > YOU HAVE UNLOCKED {} <\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n".format(new))
    return knownSymbols + [new]


symbols = list(dict.keys())
n = 0
print("\n+----------------------------------+\n| Welcome to this incredible game! |")
print("+----------------------------------+\n  The items you have unlocked are:\n> {}\n------------------------------------\n".format(
    " - ".join(scores["knownKeys"])))

while True:
    n += 1
    allCombs = getAllCombinations(scores["knownKeys"])
    allscores = getAllCombsScores(allCombs, scores)
    combs = sortCombsByScore(allscores)
    lowestID = getLowestID(combs)
    if lowestID >= 2:
        scores["knownKeys"] = unlockNewSymbol(symbols, scores["knownKeys"])
        scores["level"] += 1

    oneLevelBeyond = []
    try:
        oneLevelBeyond = combs[lowestID+1]
    except KeyError:
        pass

    a, b = random.choice(combs[lowestID]+oneLevelBeyond).split("-")
    newRound = round(n, a, b)
    if newRound == "q":
        break

    scores[format(a, b)] = newRound[1]


# print(scores)
with open("gameData.json", "w+") as f:
    json.dump(scores, f, indent=4)
