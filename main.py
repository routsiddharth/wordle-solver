import pygame, setup, string
from pygame.locals import *

# SETUP
pygame.init()
MAX_FPS = 45
clock = pygame.time.Clock()
pygame.display.set_caption("Wordle Solver")

WIN_WIDTH, WIN_HEIGHT = 800, 800
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

FONT_S = pygame.font.Font('Questrial/Questrial-Regular.ttf', 20)
FONT_M = pygame.font.Font('Questrial/Questrial-Regular.ttf', 30)
FONT_L = pygame.font.Font('Questrial/Questrial-Regular.ttf', 40)

WIDTH = FONT_M.render("SR2022", 1, setup.BLACK).get_height() + 30

running = True

# Start Button
xpos = 50
ypos = 100 + 6 * (WIDTH + 20)
width = (4 * 20) + (5 * WIDTH)
height = WIDTH

startButton = [xpos, ypos, width, height]

solutionScores = []

class WordleGame():
    def __init__(self):
        # Create a 2D array to store the current state of the board.
        # Each letter has an attribute B/Y/G representing what state it is.
        # N = no letter, B = not in word, Y = in word, wrong place, G = in word, right place
        # Each square also has an x-pos and y-pos, representing the coordinates the top-left corner

        self.words = [[["", "N", 0, 0] for i in range(5)] for j in range(6)]

        for row in range(6):
            for cell in range(len(self.words[row])):
                xpos = 50 + cell * (WIDTH + 20)
                ypos = 100 + row * (WIDTH + 20)

                self.words[row][cell][2] = xpos
                self.words[row][cell][3] = ypos

        self.currentPos = [0, 0]

        self.common = [i.upper() for i in setup.WORDS]
        self.wordbank = [i.upper() for i in setup.EXTENDED_WORDS] + self.common

        self.possibleWords = self.wordbank

    def verifyWords(self):

        fullWords = []

        for word in self.words:
            w = "".join(letter[0] for letter in word)

            if len(w) == 5:
                fullWords.append(word)

        return fullWords

    def calculateOption(self):

        validWords = self.verifyWords()

        if len(validWords) == 0:
            wordScores = [('KAIES', 1.329), ('MOUES', 1.298), ('ROUES', 1.289), ('AURES', 1.253), ('AUNES', 1.222), ('OAVES', 1.206), ('CARES', 1.185)]
            return wordScores

        self.greens = ["" for i in range(5)]

        self.yellows = []
        self.yellowPos = [[] for i in range(5)]

        self.blacks = []

        for word in validWords:

            for letter in range(len(word)):
                if word[letter][1] == "G":
                    self.greens[letter] = word[letter][0]

                elif word[letter][1] == "Y":
                    self.yellows.append(word[letter][0])
                    self.yellowPos[letter].append(word[letter][0])

                elif word[letter][1] == "B":
                    self.blacks.append(word[letter][0])

        self.possibleWords = []

        for word in self.wordbank:
            valid = True

            for letter in range(len(self.greens)):
                if self.greens[letter] != "":
                    if self.greens[letter] != word[letter]:
                        valid = False

            for letter in range(len(self.yellows)):
                if self.yellows[letter] not in word:
                    valid = False

            for letter in range(len(self.blacks)):
                if self.blacks[letter] in word:
                    if self.blacks[letter] not in self.yellows and self.blacks[letter] not in self.greens:
                        valid = False

            for letter in range(len(word)):
                if word[letter] in self.yellowPos[letter]:
                    valid = False

            if valid:
                self.possibleWords.append(word)

        wordScores = {}
        n = len(self.possibleWords)

        for word in self.possibleWords:
            score = 0.0

            for p in range(5):
                score2 = 0.0

                for i in range(n):
                    if self.possibleWords[i][p] == word[p]:
                        score2 += 1

                score += score2 / n

            if word in self.common:
                score *= 1.25

            setWord = set(list(word))
            score *= 1 - (5 - len(setWord)) * 0.15

            for vowel in "AEIOU":
                if vowel in word and vowel not in self.greens + self.yellows + self.blacks:
                    score *= 1.2

            wordScores[word] = round(score, 3)

        wordScores = sorted(wordScores.items(), key=lambda x: x[1], reverse=True)

        print(list(i[0] for i in wordScores))
        return wordScores[:7]

    def nextOption(self, pos):

        xpos, ypos = pos

        color = self.words[xpos][ypos][1]

        if color == "N":
            pass

        else:
            mapping = {"B":"Y", "Y":"G", "G":"B"}
            newColor = mapping[color]

            self.words[xpos][ypos][1] = newColor

    def backSpace(self):

        x, y = self.currentPos

        self.words[x][y][0] = ""
        self.words[x][y][1] = "N"

game = WordleGame()

def draw():
    global solutionScores

    window.fill(setup.WHITE)

    text = FONT_L.render("SOLVLE", 1, setup.RED)

    tx = (WIN_WIDTH - text.get_width()) / 2
    ty = 20

    window.blit(text, (tx, ty))

    for row in game.words:
        for cell in row:
            letter, color, xpos, ypos = cell
            pygame.draw.rect(window, setup.colormap[color], (xpos, ypos, WIDTH, WIDTH))

            # Place letter centralised on a box
            text = FONT_M.render(letter, 1, setup.WHITE)

            tx = xpos + (WIDTH - text.get_width())/2
            ty = ypos + (WIDTH - text.get_height())/2

            window.blit(text, (tx, ty))

    letter, color, xpos, ypos = game.words[game.currentPos[0]][game.currentPos[1]]
    pygame.draw.rect(window, setup.RED, (xpos, ypos, WIDTH, WIDTH), 5)

    xpos, ypos, width, height = startButton
    pygame.draw.rect(window, setup.GREEN, (xpos, ypos, width, height))

    text = FONT_M.render("SOLVE", 1, setup.WHITE)

    tx = xpos + (width - text.get_width())/2
    ty = ypos + (height - text.get_height()) / 2

    window.blit(text, (tx, ty))

    text = FONT_M.render("WORD", 1, setup.RED)

    tx = 470
    ty = 100

    window.blit(text, (tx, ty))

    text = FONT_M.render("SCORE", 1, setup.RED)

    tx = WIN_WIDTH - (50 + text.get_width())
    ty = 100

    window.blit(text, (tx, ty))

    for i in range(len(solutionScores)):
        word, score = solutionScores[i]
        word = FONT_M.render(word, 1, setup.BLACK)

        xpos = 470
        ypos = 100 + (i + 1) * height

        window.blit(word, (xpos, ypos))

        t = FONT_M.render(str(score), 1, setup.BLACK)

        tx = WIN_WIDTH - (50 + t.get_width())
        ty = 100 + (i + 1) * height

        window.blit(t, (tx, ty))

    t = FONT_M.render("PRESS SPACE TO CHANGE COLOUR", setup.BLACK, 1)

    tx = (WIN_WIDTH - t.get_width())/2
    ty = 700

    window.blit(t, (tx, ty))

    pygame.display.update()


def main():
    global running, currentPos, solutionScores

    while running:
        clock.tick(MAX_FPS)
        draw()

        for e in pygame.event.get():

            if e.type == pygame.KEYDOWN:

                key = pygame.key.name(e.key)

                if key in string.ascii_lowercase or key in string.ascii_uppercase:
                    game.words[game.currentPos[0]][game.currentPos[1]][0] = key.upper()

                    if game.words[game.currentPos[0]][game.currentPos[1]][1] == "N":
                        game.words[game.currentPos[0]][game.currentPos[1]][1] = "B"

                elif e.key == K_SPACE:
                    game.nextOption(game.currentPos)

                elif e.key == K_BACKSPACE:
                    game.backSpace()


            elif e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                for row in range(len(game.words)):
                    for cell in range(len(game.words[row])):
                        x1, y1, x2, y2 = game.words[row][cell][2], game.words[row][cell][3], game.words[row][cell][2] + WIDTH, game.words[row][cell][3] + WIDTH

                        if (x1 <= mx <= x2) and (y1 <= my <= y2):
                            game.currentPos = [row, cell]

                xpos, ypos, width, height = startButton

                if (xpos <= mx <= xpos + width) and (ypos <= my <= ypos + width):
                    solutionScores = game.calculateOption()

            elif e.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()

    pygame.quit()
