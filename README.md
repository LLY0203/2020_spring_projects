# Water Tower Puzzle
We devised an original variation of the existing puzzle "Towers". In order to increase the difficulty and fun of the game, we added a new building type based on the original puzzle, and modified the hints provided and the original rules. The goal of our project is to generate a new puzzle with unique solution and solve the puzzle in a reasonable time.

## Original Rules:
* Fill in the grid with towers whose heights range from 1 to the grid size.
* Every possible height appears exactly once in each row and column.
* Each clue around the edge counts the number of towers that are visible when looking into the grid from that direction.
For example, the building with the height of 4 and the height of 3 are in the same row, the building 3 will not be seen from the left side because it is hidden behind the building 4.

## Variation rules
* A new type of building water tower is added, which is transparent.
For example, in our code, the transparent water tower with the height of 4 is represented as [4]. 
* The total number of water towers is given.
* The sum of the height of water towers is given.
* The water tower will only appear once in each row and column.

## Team Members:
Yueran Zeng （generating pemutations part）, Linyao Li (checking part)

## Reference
https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html
