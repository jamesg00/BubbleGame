# Bubblz Game

Bubblz is a simple game developed using Pygame. The objective of the game is to pop bubbles using a spiked cursor while avoiding collision with floating spikeballs. The game features a main menu, in-game interactions, and an end screen when the player loses all lives.

## Features
- Main menu with a dynamic logo
- Animated star and spikeball graphics
- Background music
- Dynamic bubble creation and movement
- Life counter and game statistics display
- Collision detection for popping bubbles and interacting with spikeballs
- Game over and reset functionality

## Assets
The game uses various assets including images and audio files:
- `sea.jpg`: Background image
- `logo.png`: Main logo image
- `logo2.png`: Secondary logo image with pulsating effect
- `output-onlinegiftools_0.png` to `output-onlinegiftools_14.png`: Frames for star animation
- `spikeball.png`: Image for both the floating spikeball and the spiked cursor
- `bubble.png`: Image for the bubbles
- `question.png`: Image for the question button
- `Krabby Patty.ttf`: Custom font used in the game
- `CatOnWindow105.mp3`: Background music
- `bubble.mp3`: Sound effect for popping bubbles

## How to Play
1. **Start the Game**: Launch the game, and you'll be presented with the main menu.
2. **Enter Game**: Press any key to start the game from the main menu.
3. **Gameplay**: Use your mouse to move the spiked cursor around the screen. The goal is to pop bubbles by colliding the cursor with them while avoiding the floating spikeballs.
4. **Lives**: You start with 3 lives. Each time a bubble collides with the spiked cursor, you lose one life. If all lives are lost, the game ends.
5. **Restart**: Click the mouse button on the end screen to restart the game.

## Code Explanation
The game is structured into different sections for initialization, asset loading, main loop, and functions for game mechanics:

### Initialization and Asset Loading
```python
import pygame
import random
import math

pygame.init()
pygame.mixer.init()
