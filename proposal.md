# Snake Game

## Repository
https://github.com/VictoriaHantgin/Snake-Game

## Description
This game will be a spin on the classic snake game, where the player must collect as many points as possible without running into themself, which grows longer with each point collected. In this version, there will be different items to collect that can give the player an advantage or disadvantage.

## Features
- Feature 1: Player Character
	- The player will be able to control the character by using keyboard inputs, such as up, down, left, and right. This will be done by creating a class for the character, and then adding a move function with in it that takes keyboard inputs. 
- Feature 2: Point system
	- For each "point item" that the character collides with, a point will be added to the point tracker in the top right corner of the screen. This will be done using a collision function that checks whether the character has collided with the point item and a for loop, which updates the point tracker each time this occurs. 
- Feature 3: Player Character Grows
    - Each time a point item is collected, the character grows, which is a classic part of the snake game. This will be done by creating a method inside the player character's class that adds a block each time a point is collected.
- Feature N: Speed Power-Up
	- An item that the player can collect that makes the character temporarily move faster. This will be done by checking if the player has intercepted a speed power-up and then changing the amount of blocks forward that the character can move, for example: with the speed power-up, it will now move two blocks at a time. This power-up will only last for a couple milliseconds, so a life variable will be implemented to determine when a speed power-up will appear and disappear. The movement of the character will also utilize an if statement to determine if it moves normally, or if a speed power-up has been intercepted and the character moves twice as fast.
- Feature 4: Life counter
    - In the top left of the screen, there will be a life counter. Normally, the player will have only one life, and if a player hits the wall of the screen or hits itself, the game will be over. However, if players collect a life item, their life counter will show 2, and the game will continue on until the player has died twice. In a failcheck function in the Main function, there will be an if statement and a life counter. If the life counter is greater than 1, the game will not end, but a life will be deducted from the life counter. When the failcheck function is called a second time, and if the life counter is now equal to 1, then it will be game over.
- Feature 5: Game Over/death
    - If the character collides with itself or the wall of the screen, the character will die if their life < 1. When the character dies, a game over screen will be displayed. This will be implemented using a method that checks if the player has failed either by collding with the wall (the boundaries of the screen, which will equal the display width and height) or by colliding with itself, which will be the character blocks except for the head of the character (the very first block in the "snake"). 
- Feature: Score System
    - Each time a player has reached game over, a final score will be displayed, which will be a value(like 100) multiplied by the amount of points collected. This will be executed when the game loop is over, and a new screen will be displayed with this information. Since points will be tracked, this variable will be used to determine the final score.
- Sound/music
    - I will create different sound methods that will be executed at different times throughout the gameloop: a sound when a point is collected, when a power-up is collected, when the character loses a life. I will also have background music that will be executed from the start of the gameloop until the player reaches game over.


## Challenges
- I will have to research how to upload sprites and background images for my game.
- I will need to research how to create a character that grows with each point collected.
- I will need to research how to create multiple screens for the game to display, such as for the game over screen. 

## Outcomes
Ideal Outcome:
- My ideal outcome is a snake game that has successfully implemented power ups that include extra lifes and speed boosts, and unique sprites/graphics. I want the game to feel like the classic snake game, but to be a different take on the concept with a couple additional features.

Minimal Viable Outcome:
- My minimal viable outcome is a game that feels like the snake game and has unique graphics and sfx so that it doens't look and sound like a generic snake game.

## Milestones

- Week 1: Setting up the Game
  1. Set up the game board
  2. Create the player character and have it move 
  3. Implement the character growing as it collects points
   

- Week 2
  1. Implement Game Over state
  2. Implement Power-up
  3. Implement Life counter

- Week 3 (Final)
  1. implement final score
  2. implement graphics
  3. Implement sound
