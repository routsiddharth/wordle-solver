# Wordle Solver
### v03.04.22

## Introduction
A coder's solution for being bad with words. 

## Using the Solver
The GUI works almost the same as the actual game so that it is easy to use. You type the words you have into the boxes. When a box is selected, clicking space will change its color (gray --> yellow --> green).

## Tries Distribution
![tries distribution](https://github.com/routsiddharth/wordle-solver/blob/master/triesDistribution.png)

The solver can guess most words in 3-4 guesses. A very small subset of words cannot be guessed in 6 guesses by the algorithm, so I am trying to improve the algorithm to get the number of words in this group to zero. 
