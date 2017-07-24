# dots
Motivated by the frustration caused by level 31 under Dragon Fruit section of Splashy Dots game, here's a simple Python 3 script that traverses game grid and finds a solution.

### Usage
To find solution for a level you have to initialize 3 variables in the script:
1. game_grid - this is a 2D array that represents dots in a level, for every dot place '1' in the matrix
2. start_coord - x,y coordinate of the starting dot
3. destination_coord - x,y coordinate of the destination dot
..and then run it like so

```sh
$ python dots.py
Last path [[3, 2], ... , [0, 4]]
```
p.s. I am not associated with the game developers. Love the game. No harm intended.
