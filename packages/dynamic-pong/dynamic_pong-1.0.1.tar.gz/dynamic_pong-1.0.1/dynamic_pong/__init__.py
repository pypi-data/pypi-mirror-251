# dynamic_pong/__init__.py

"""
Dynamic Pong is an interactive and modern rendition of the classic arcade game Pong, implemented in Python using the Pygame library. It features a dynamic gameplay experience with adjustable speeds and responsive paddle controls.

This package encompasses the complete setup and game logic necessary for running Dynamic Pong. It includes classes for the game's primary elements: paddles (Player and Opponent), the ball, and the game manager. Each class is designed to encapsulate specific behaviors and attributes of these elements, such as movement, collision detection, and score tracking.

Key Features:
- Adaptive game speed that intensifies as the game progresses.
- Collision detection between the ball and paddles, as well as the game boundaries.
- Score tracking and display for both the player and the computer-controlled opponent.
- Customizable game window size and element proportions for a tailored visual experience.

The game loop runs continuously, handling user input for the player's paddle movement and updating the game state at each frame. The game's difficulty can be adjusted through the speed multiplier, affecting the ball's speed and responsiveness of the paddles.

Usage:
To start the game, ensure Pygame is installed and run the script. Control the player's paddle using the 'up' and 'down' arrow keys or 'W' and 'S' keys. The game continues indefinitely until manually exited.

Example:
    # Example of initializing and running the game
    game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
    while True:
        game_manager.run_game()
        # Additional game loop logic here
        pygame.display.flip()
        clock.tick(60)

Note:
Dynamic Pong is designed as a standalone Python application requiring Pygame. It is not intended as a library or module to be imported into other projects.

Author: [Your Name]
Version: 1.0
"""
