# Game2k48

This project is an implementation of a once super popular game "2048".
The goal was actually to play around with GUI and animating objects on Tkinter Canvas, so the console version is really just a byproduct of trying to get the tile movement logic right.

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/113710b8-4ee3-4e95-bb74-7af1c394426c)

The rules are very straightforward: by moving the tiles UP, DOWN, LEFT or RIGHT, tiles with the same number are merged into one with double the value.
The goal is to achieve a 2048 tile, though game can go on until there is no next movement possible.

Standard 2048 board is 4x4, with 2 initial tiles.



In this version we can choose both the size of the board and the number of initial tiles.
Here is the GUI version for a 7x7 board and 33 initial tiles:

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/acb05220-4f38-43dd-aa24-58a36ec14d67)

## Console version

In this version the entire board is written out in console, and consecutive movements are achieved by typing W, S, A, D into the terminal.
If you launch it in Command-Line/Terminal, screen gets cleared after each movement.
This is the screenshot from PyCharm, so it's clear what it's like to interact with the program.

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/2cdb1b63-5031-49a8-b77e-ad8a34e7f475)

This version terminates after game is over.

## GUI version

The entire GUI for this project was done using basic Tkinter tools, so even the animation of tile movement was done by hand.
This version provides more flexibility in regards to board size.
After reaching a "GAME OVER" label, just press SPACE to restart the scoreboard and play again.

We can generate the default 4x4 board with 2 initial tiles:

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/289082ec-271b-4f32-b4bb-e6471441c026)

A bit bigger (10x10, 50 initial tiles):

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/d5948c1d-c784-403b-8024-db8f168d3e75)

Or we can go crazy (50x50, 1200 initial tiles):

![image](https://github.com/kenimoraj/Game2k48/assets/73795771/3ee2e1dc-9d60-4bd9-b2bf-c2774db3dead)


---

Feel free to tweak and expand this code.
