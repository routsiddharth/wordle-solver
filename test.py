import setup

common = [i.upper() for i in setup.WORDS]
wordbank = [i.upper() for i in setup.WORDS + setup.EXTENDED_WORDS]

def test():

    tries = {i:0 for i in range(1, 7)}

    tries["unsolved"] = 0
    unsolved = []

    for answer in common:
        print("Testing answer", answer)
        words = [[["", "N"] for i in range(5)] for j in range(6)]
        guess = ""
        t = 0

        while guess != answer and t <= 5:

            if t == 0:
                guess = [('KAIES', 1.329), ('MOUES', 1.298), ('ROUES', 1.289), ('AURES', 1.253), ('AUNES', 1.222),
                 ('OAVES', 1.206), ('CARES', 1.185)]
            else:
                guess = calculateOption(words)

            guess = guess[0][0]

            for i in range(len(guess)):

                letter = guess[i]

                if letter == answer[i]:
                    words[t][i] = letter, "G"
                elif letter in answer:
                    words[t][i] = letter, "Y"
                else:
                    words[t][i] = letter, "B"

            t += 1

        if guess != answer:
            tries["unsolved"] += 1
            unsolved.append(answer)
        else:
            tries[t] += 1
        print(tries)

    print(unsolved)

def calculateOption(words):

    greens = ["" for i in range(5)]

    yellows = []
    yellowPos = [[] for i in range(5)]

    blacks = []

    for word in words:

        for letter in range(len(word)):
            if word[letter][1] == "G":
                greens[letter] = word[letter][0]

            elif word[letter][1] == "Y":
                yellows.append(word[letter][0])
                yellowPos[letter].append(word[letter][0])

            elif word[letter][1] == "B":
                blacks.append(word[letter][0])

    possibleWords = []

    for word in wordbank:
        valid = True

        for letter in range(len(greens)):
            if greens[letter] != "":
                if greens[letter] != word[letter]:
                    valid = False

        for letter in range(len(yellows)):
            if yellows[letter] not in word:
                valid = False

        for letter in range(len(blacks)):
            if blacks[letter] in word:
                if blacks[letter] not in yellows and blacks[letter] not in greens:
                    valid = False

        for letter in range(len(word)):
            if word[letter] in yellowPos[letter]:
                valid = False

        if valid:
            possibleWords.append(word)

    wordScores = {}
    n = len(possibleWords)

    for word in possibleWords:
        score = 0.0

        for p in range(5):
            score2 = 0.0

            for i in range(n):
                if possibleWords[i][p] == word[p]:
                    score2 += 1

            score += score2 / n

        if word in common:
            score *= 1.25

        setWord = set(list(word))
        score *= 1 - (5 - len(setWord)) * 0.15

        for vowel in "AEIOU":
            if vowel in word and vowel not in greens + yellows + blacks:
                score *= 1.2

        wordScores[word] = round(score, 3)

    wordScores = sorted(wordScores.items(), key=lambda x: x[1], reverse=True)

    return wordScores[:7]

if __name__ == '__main__':
    test()

    # Unsolvable = ['ABATE', 'HATCH', 'ERODE', 'LOWLY', 'COYLY', 'MUMMY', 'DADDY', 'QUEER', 'TATTY', 'ROVER', 'SEIZE', 'NOOSE', 'RAZOR', 'REARM', 'ETHER', 'DROVE', 'AWARE', 'SHAPE', 'HOLLY', 'DUSTY', 'PIPER', 'COCOA', 'SPARE', 'TASTE', 'TAFFY', 'RARER', 'WAFER', 'AWASH', 'PAPAL', 'WOUND', 'RIGHT', 'TIGHT', 'SHORE', 'MAMMA', 'SPEAR', 'BROWN', 'SNORE', 'HOUND', 'BLAME', 'STEER', 'WILLY', 'MATCH', 'ROWER']