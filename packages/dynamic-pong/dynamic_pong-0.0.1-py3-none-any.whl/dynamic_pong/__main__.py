import pygame
import sys
import random

class Block(pygame.sprite.Sprite):
    """A basic block class for the Dynamic Pong game.

    This class represents a generic game object (or block) in the Pong game.
    It handles the creation and graphical representation of the block, such as
    paddles and the ball, by setting up the image and position based on the
    provided parameters.

    Attributes:
        image (pygame.Surface): The surface representing the block's visual appearance.
        rect (pygame.Rect): The rectangular area of the block used for positioning and collision detection.

    Examples:
        Creating a block representing a paddle:

        >>> block = Block("white", 20, 100, 50, 300)
        >>> block.rect.center
        (50, 300)
        >>> block.image.get_size()
        (20, 100)
    """

    def __init__(self, color, block_width, block_height, x_pos, y_pos):
        """Initializes a new Block instance.

        Args:
            color (str): The pygame built-in color name of the block.
            block_width (int): The width of the block.
            block_height (int): The height of the block.
            x_pos (int): The x-coordinate of the block's center position.
            y_pos (int): The y-coordinate of the block's center position.
        """
        super().__init__()

        # Access global variables for width and height scaling ratios
        global width_ratio, height_ratio

        # Create the block image and set its position
        self.image = pygame.Surface(
            (int(block_width * width_ratio), int(block_height * height_ratio))
        )
        self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update_color(self, color):
        """Updates the color of the block.

        This method changes the block's color to the specified new color.

        Args:
            color (str): The pygame built-in color name to apply to the block.

        Examples:
            Changing the color of a block:

            >>> block = Block("white", 20, 100, 50, 300)
            >>> block.update_color("red")
            >>> block.image.get_at((10, 50)) == pygame.Color("red")
            True
        """
        self.image.fill(pygame.Color(color))


class Player(Block):
    """Represents the player-controlled paddle in Dynamic Pong.

    This class is a subclass of `Block` and represents the paddle controlled by the player.
    It is initialized on the right side of the screen and can move vertically within the screen boundaries.

    Attributes:
        speed (int): The speed at which the player's paddle can move.
        movement (int): The current vertical movement of the player's paddle.

    Args:
        color (str): The pygame built-in color name of the player's paddle.
        block_width (int): The width of the player's paddle before scaling.
        block_height (int): The height of the player's paddle before scaling.
        speed (int): The initial speed of the player's paddle.

    Examples:
        Initializing a player paddle:

        >>> player = Player("white", 20, 140, 5)
        >>> player.rect.center
        (780, 300)  # Assuming a screen width of 800
        >>> player.speed
        5
    """
    def __init__(self, color, block_width, block_height, speed):
        global screen_width, screen_height

        # Initialize the player's position based on the screen size and paddle dimensions
        x_pos = screen_width - (block_width)
        y_pos = (screen_height / 2) - (block_height / 2)
        super().__init__(color, block_width, block_height, x_pos, y_pos)

        self.speed = speed  # Setting the player's speed
        self.movement = 0   # Initial movement is set to zero

    def screen_constrain(self):
        """Ensures the player's paddle stays within the screen boundaries.

        Examples:
            Constraining the paddle's position within the screen:

            >>> player = Player("white", 20, 140, 5)
            >>> player.rect.top = -10  # Move paddle above top boundary
            >>> player.screen_constrain()
            >>> player.rect.top
            0  # Paddle is moved back within the screen boundary
        """
        global screen_height

        # Adjust the paddle's position if it goes beyond the screen's top or bottom edge
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        """Updates the player's position and applies speed constraints.

        Args:
            ball_group: A sprite group containing the ball, used to calculate interactions.

        Examples:
            Updating the player's position:

            >>> player = Player("white", 20, 140, 5)
            >>> player.movement = 5
            >>> player.update(None)  # Passing `None` for the `ball_group` for simplicity
            >>> player.rect.y
            305  # Assuming initial y-position was 300
        """
        global speed_multiplier

        self.rect.y += self.movement  # Move the player
        self.screen_constrain()       # Apply screen constraints
        self.update_speed()           # Update the player's speed

    def update_speed(self):
        """Updates the player's speed and color based on the current game speed.

        Examples:
            Updating the player's speed:

            >>> player = Player("white", 20, 140, 5)
            >>> speed_multiplier = 8
            >>> player.update_speed()
            >>> player.speed
            8
        """
        global speed_multiplier

        # Adjust the color and speed of the paddle based on the speed multiplier
        self.update_color(paddle_colors[speed_multiplier - 7])
        self.speed = speed_multiplier


class Opponent(Block):
    """Represents the automated opponent's paddle in the Dynamic Pong game.

    The Opponent class extends the Block class to implement an automated paddle,
    which moves based on the ball's position. It handles the opponent's initialization,
    movement, and ensuring that it stays within the screen boundaries.

    Attributes:
        speed (int): The speed at which the opponent's paddle moves.

    Examples:
        Initializing an opponent paddle:

        >>> opponent = Opponent("red", 20, 140)
        >>> opponent.rect.center
        (20, 300)  # Assuming a screen height of 600
    """

    def __init__(self, color, block_width, block_height):
        """Initializes the Opponent instance.

        The opponent's paddle is positioned on the left side of the screen at initialization.

        Args:
            color (str): The pygame built-in color name of the opponent's paddle.
            block_width (int): The width of the opponent's paddle.
            block_height (int): The height of the opponent's paddle.
        """
        global speed_multiplier, screen_height

        # Calculate initial position on the left side of the screen
        x_pos = block_width
        y_pos = (screen_height / 2) - (block_height / 2)
        super().__init__(color, block_width, block_height, x_pos, y_pos)

    def update(self, ball_group):
        """Updates the opponent's paddle position based on the ball's position.

        This method is called within the game loop to move the paddle in response
        to the ball's movement, aiming to match its vertical position.

        Args:
            ball_group (pygame.sprite.Group): The group containing the ball sprite, used to determine the ball's position.

        Examples:
            Updating the opponent's position based on the ball's position:

            >>> ball = Ball("blue", 30, 30, None)  # Simplified ball instance for example
            >>> ball.rect.center = (100, 100)
            >>> opponent = Opponent("red", 20, 140)
            >>> opponent.update(pygame.sprite.GroupSingle(ball))
            >>> opponent.rect.y  # The exact position depends on the `speed_multiplier` and the ball's position
            100
        """
        global speed_multiplier

        # Adjust the speed and position of the opponent based on the ball's position
        self.speed = speed_multiplier
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed

        # Constrain the opponent within the screen and update its speed
        self.constrain()
        self.update_speed()

    def constrain(self):
        """Ensures the opponent's paddle remains within the screen's vertical boundaries.

        Examples:
            Constraining the opponent's position within the screen:

            >>> opponent = Opponent("red", 20, 140)
            >>> opponent.rect.bottom = 610  # Move paddle below bottom boundary
            >>> opponent.constrain()
            >>> opponent.rect.bottom
            600  # Paddle is moved back within the screen boundary
        """
        global screen_height

        # Adjust position if the paddle goes beyond the top or bottom of the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update_speed(self):
        """Updates the paddle's speed and color based on the game's speed multiplier.

        The color of the paddle is also dynamically adjusted to reflect changes in speed.

        Examples:
            Updating the opponent's speed:

            >>> opponent = Opponent("red", 20, 140)
            >>> speed_multiplier = 8
            >>> opponent.update_speed()
            >>> opponent.speed
            8
        """
        global speed_multiplier

        # Update color and speed based on the speed multiplier
        self.update_color(paddle_colors[speed_multiplier - 7])
        self.speed = speed_multiplier


class Ball(Block):
    """Represents the ball in the Dynamic Pong game.

    This class extends the Block class to implement the ball's behavior, including
    its movement, collision detection, and score tracking. The ball's speed and direction
    are dynamically adjusted based on the game's speed multiplier.

    Attributes:
        speed_x (int): The horizontal speed component of the ball.
        speed_y (int): The vertical speed component of the ball.
        paddles (pygame.sprite.Group): A group containing the player and opponent paddles for collision detection.
        active (bool): Indicates whether the ball is currently in play.
        score_time (int): Tracks the time at which the last score was made.

    Examples:
        Initializing a ball with random speed and direction:

        >>> ball = Ball("white", 30, 30, paddle_group)
        >>> isinstance(ball.speed_x, int) and isinstance(ball.speed_y, int)
        True
        >>> ball.active
        False
    """

    def __init__(self, color, block_width, block_height, paddles):
        """Initializes the Ball instance.

        The ball is positioned at the center of the screen with an initial speed
        determined by the game's speed multiplier and a random direction.

        Args:
            color (str): The pygame built-in color name of the ball.
            block_width (int): The width of the ball.
            block_height (int): The height of the ball.
            paddles (pygame.sprite.Group): The group of paddles for collision detection.
        """
        global screen_width, screen_height, speed_multiplier

        # Calculate the ball's initial position at the center of the screen
        x_pos = screen_width / 2
        y_pos = screen_height / 2
        super().__init__(color, block_width, block_height, x_pos, y_pos)

        # Set ball's initial speed and direction, along with related attributes
        self.speed_x = speed_multiplier * random.choice((-1, 1))
        self.speed_y = speed_multiplier * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        """Updates the ball's position and activity status during the game.

        If the ball is active, it moves according to its speed components and checks
        for collisions. If inactive, it triggers a restart counter for game continuation.

        Examples:
            Updating the ball's position when active:

            >>> ball = Ball("white", 30, 30, paddle_group)
            >>> ball.active = True
            >>> ball.speed_x, ball.speed_y = 5, 5
            >>> ball.update()
            >>> (ball.rect.x, ball.rect.y) != (screen_width / 2, screen_height / 2)
            True
        """
        global speed_multiplier

        # Update the ball's color based on the current speed multiplier
        self.update_color(ball_colors[speed_multiplier - 7])

        # Move the ball and handle collisions if active; otherwise, restart counter
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        """Handles the ball's collisions with the game boundaries and paddles.

        This method checks for and responds to collisions between the ball and the top
        and bottom edges of the screen, as well as with the player and opponent paddles.
        It reverses the ball's vertical direction on collision with screen edges and
        delegates paddle collision handling to the `handle_paddle_collision` method.

        Examples:
            Handling collision with the top edge of the screen:

            >>> ball = Ball("white", 30, 30, paddle_group)
            >>> ball.rect.top = -5  # Ball position above the top edge
            >>> ball.speed_y = -5   # Ball moving upwards
            >>> ball.collisions()
            >>> ball.speed_y
            5
        """
        global screen_height

        # Collisions with the top and bottom of the screen
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

        # Collisions with paddles
        if pygame.sprite.spritecollide(self, self.paddles, False):
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            self.handle_paddle_collision(collision_paddle)

    def handle_paddle_collision(self, collision_paddle):
        """Handles the logic for ball collisions with paddles.

        This method determines the nature of the collision with a paddle (either horizontal
        or vertical) and adjusts the ball's movement accordingly.

        Args:
            collision_paddle (pygame.Rect): The rectangle representing the paddle's position and dimensions.

        Examples:
            Handling a horizontal collision with a paddle:

            >>> ball = Ball("white", 30, 30, paddle_group)
            >>> paddle = Player("red", 20, 140, 5)
            >>> ball.rect.right = paddle.rect.left
            >>> ball.speed_x = 5
            >>> ball.handle_paddle_collision(paddle.rect)
            >>> ball.speed_x
            -5
        """
        # Horizontal collision
        if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
            self.speed_x *= -1
        if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
            self.speed_x *= -1

        # Vertical collision
        if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
            self.rect.top = collision_paddle.bottom
            self.speed_y *= -1
        if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
            self.rect.bottom = collision_paddle.top
            self.speed_y *= -1

    def reset_ball(self):
        """Resets the ball to the center of the screen and randomizes its speed.

        This method is typically called after a point is scored. It places the ball
        back at the center of the screen, randomizes its speed and direction, and
        resets the scoring timer.

        Examples:
            Resetting the ball's position and speed after a score:

            >>> ball = Ball("white", 30, 30, paddle_group)
            >>> ball.reset_ball()
            >>> ball.rect.center == (screen_width / 2, screen_height / 2)
            True
            >>> isinstance(ball.speed_x, int) and isinstance(ball.speed_y, int)
            True
        """
        global speed_multiplier, screen_width, screen_height

        # Reset the ball's position to the center and randomize its speed and direction
        self.rect.center = (screen_width / 2, screen_height / 2)
        speed_multiplier = random.choice((7, 8, 9, 10))
        self.speed_y = speed_multiplier * random.choice((1, -1))
        self.speed_x = speed_multiplier * random.choice((1, -1))
        self.score_time = pygame.time.get_ticks()
        self.restart_counter()

    def restart_counter(self):
        """Manages the countdown process before reactivating the ball.

        This method is called after a point is scored to initiate a countdown before
        the ball is set back into play. It updates the game state with a countdown
        display and reactivates the ball once the countdown is complete.

        The countdown duration is controlled by the elapsed time since the last score.
        The method also updates the visual representation of the countdown on the screen.

        Examples:
            Demonstrating the countdown process:

            >>> ball = Ball("white", 30, 30, paddle_group)
            >>> ball.score_time = pygame.time.get_ticks() - 1500  # Simulate time after a score
            >>> ball.restart_counter()
            >>> ball.active  # The ball will be inactive until countdown completes
            False
            >>> # After enough time passes, `ball.active` will become True
        """
        global speed_multiplier, screen_width, screen_height, height_ratio

        # Retrieve the current time for countdown calculation
        current_time = pygame.time.get_ticks()

        # Initialize the countdown and set the ball to inactive
        countdown_number = 3
        self.active = False

        # Determine the countdown number based on the elapsed time since the last score
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        elif 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        elif current_time - self.score_time >= 2100:
            self.active = True  # Reactivate the ball after the countdown

        # Render and display the countdown number on the screen
        time_counter = game_font.render(str(countdown_number), True, text_colors[speed_multiplier - 7])
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + (50 * height_ratio)))
        pygame.draw.rect(screen, background_colors[speed_multiplier - 7], time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


class GameManager:
    """Manages the core gameplay logic in the Dynamic Pong game.

    This class is responsible for initializing game components, running the game loop,
    and updating the game state. It handles the drawing and updating of game objects
    like the ball, paddles, background, and divider line, and also manages scoring.

    Attributes:
        player_score (int): The current score of the player.
        opponent_score (int): The current score of the opponent.
        ball_group (pygame.sprite.Group): Group containing the ball sprite.
        paddle_group (pygame.sprite.Group): Group containing the player and opponent paddle sprites.
        background_group (pygame.sprite.Group): Group containing the background sprite.
        divider_line_group (pygame.sprite.Group): Group containing the divider line sprite.

    Examples:
        Initializing the game manager with all game object groups:

        >>> game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
        >>> game_manager.player_score
        0
        >>> game_manager.opponent_score
        0
    """

    def __init__(self, ball_group, paddle_group, background_group, divider_line_group):
        """Initializes the GameManager with game object groups.

        Args:
            ball_group (pygame.sprite.Group): Group containing the ball sprite.
            paddle_group (pygame.sprite.Group): Group containing the player and opponent paddle sprites.
            background_group (pygame.sprite.Group): Group containing the background sprite.
            divider_line_group (pygame.sprite.Group): Group containing the divider line sprite.
        """
        global speed_multiplier

        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.background_group = background_group
        self.divider_line_group = divider_line_group

    def run_game(self):
        """Executes the main game loop.

        In each iteration of the game loop, this method draws all game objects on the screen,
        updates their states, and performs score management. This includes updating the position
        of the ball and paddles, checking for scoring conditions, and resetting the ball when needed.

        Examples:
            Running a single iteration of the game loop:

            >>> game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
            >>> game_manager.run_game()  # This runs one iteration of the game loop
            >>> # The states of all game objects are updated, and the score may change based on the game's progression
        """
        # Draw game objects on the screen
        self.background_group.draw(screen)
        self.divider_line_group.draw(screen)
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Update the states of all game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()  # Reset the ball if it goes out of bounds
        self.draw_score()  # Draw the current score

    def reset_ball(self):
        """Resets the ball position and updates the game score.

        This method is called when the ball goes out of bounds. It increments the score
        for the appropriate player (opponent or player), resets the ball to its initial
        position, and updates the game speed accordingly.

        Examples:
            Resetting the ball and updating the score when the ball goes out of bounds:

            >>> game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
            >>> game_manager.ball_group.sprite.rect.right = screen_width + 1  # Simulate ball going out of bounds
            >>> game_manager.reset_ball()
            >>> game_manager.opponent_score  # The opponent's score is incremented
            1
        """
        global speed_multiplier, screen_width

        # Check if the ball has gone out of bounds and update scores
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1  # Increment opponent's score
            self.ball_group.sprite.reset_ball()  # Reset the ball position
            self.update_speed()  # Update game speed

        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1  # Increment player's score
            self.ball_group.sprite.reset_ball()  # Reset the ball position
            self.update_speed()  # Update game speed

    def update_speed(self):
        """Updates the speed and color of game objects based on the speed multiplier.

        This method adjusts the colors of the background and divider line to reflect the
        current speed multiplier. It also updates the speed of the paddles to match the
        current game dynamics.

        Examples:
            Updating the speed and color of game objects:

            >>> game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
            >>> speed_multiplier = 8
            >>> game_manager.update_speed()
            >>> paddle_group.sprites()[0].speed  # Assuming paddle_group contains at least one paddle
            8
        """
        global speed_multiplier

        # Update colors of the background and divider line based on the speed multiplier
        for sprite in self.background_group.sprites():
            sprite.update_color(background_colors[speed_multiplier - 7])
        for sprite in self.divider_line_group.sprites():
            sprite.update_color(divider_line_colors[speed_multiplier - 7])

        # Update the speed of the paddles
        for paddle in self.paddle_group:
            paddle.update_speed()

    def draw_score(self):
        """Renders and displays the current score for both players on the screen.

        This method draws the current scores of the player and the opponent. The scores
        are rendered using a specific font and color, which changes based on the game's
        speed multiplier. The scores are positioned on opposite sides of the screen.

        Examples:
            Drawing the scores of both players on the screen:

            >>> game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)
            >>> game_manager.player_score = 3
            >>> game_manager.opponent_score = 2
            >>> game_manager.draw_score()
            >>> # This will render and display the scores '3' and '2' on the screen
        """
        global speed_multiplier, screen_width, screen_height, game_font, text_colors

        # Render the score for the player and the opponent using the current speed multiplier for color
        player_score = game_font.render(str(self.player_score), True, text_colors[speed_multiplier - 7])
        opponent_score = game_font.render(str(self.opponent_score), True, text_colors[speed_multiplier - 7])

        # Calculate the positions for displaying the scores on the screen
        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

        # Display the rendered scores on the screen
        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)


# General setup
pygame.init()  # Initialize all imported pygame modules
clock = pygame.time.Clock()  # Create a clock object to control the game's frame rate

# Main window setup
screen_width = 800  # Width of the game window
screen_height = 600  # Height of the game window
width_ratio = screen_width / 1280  # Ratio for scaling objects width-wise
height_ratio = screen_height / 960  # Ratio for scaling objects height-wise
screen = pygame.display.set_mode((screen_width, screen_height))  # Set the size of the game window
pygame.display.set_caption('Pong')  # Set the title of the game window

# Set colors for various game elements
background_colors = ["aliceblue", "lightcyan", "peachpuff", "lightsalmon"]
paddle_colors = ["cadetblue", "powderblue", "tomato", "crimson"]
ball_colors = ["slateblue", "cadetblue", "darkgoldenrod", "darkorange"]
divider_line_colors = ["lightsteelblue", "skyblue", "darkorange", "darkred"]
text_colors = ["midnightblue", "darkblue", "navy", "black"]

# Set game speed and initial speeds for ball and paddles
speed_multiplier = random.choice((7, 8, 9, 10))
ball_speed_x = 1 * speed_multiplier
ball_speed_y = 1 * speed_multiplier
player_speed = 0  # Initial speed for player paddle
opponent_speed = 1 * speed_multiplier  # Initial speed for opponent paddle

# Set initial scores for player and opponent
opponent_score = 0
player_score = 0
game_font = pygame.font.SysFont("Arial", 24)  # Font for rendering text, e.g., scores

# Initialize game objects
# Background block
background = Block(
    color=background_colors[speed_multiplier - 7],
    block_width=screen_width * 2,
    block_height=screen_height * 2,
    x_pos=screen_width / 2,
    y_pos=screen_height / 2
)
background_group = pygame.sprite.Group()  # Create a group for background sprite
background_group.add(background)

# Divider line block
divider_line = Block(
    color=divider_line_colors[speed_multiplier - 7],
    block_width=4,
    block_height=screen_height * 2,
    x_pos=(screen_width / 2 - 2),
    y_pos=screen_height / 2
)
divider_line_group = pygame.sprite.Group()  # Create a group for divider line sprite
divider_line_group.add(divider_line)

# Create the player paddle
# The color and size of the paddle are dependent on the current game speed
player = Player(
    color=paddle_colors[speed_multiplier - 7],
    block_width=20,  # Width of the player paddle
    block_height=140,  # Height of the player paddle
    speed=speed_multiplier  # Speed of the player paddle
)

# Create the opponent paddle
# The opponent paddle shares the same color and size as the player paddle
opponent = Opponent(
    color=paddle_colors[speed_multiplier - 7],
    block_width=20,  # Width of the opponent paddle
    block_height=140  # Height of the opponent paddle
    # The opponent paddle's speed is handled internally within its class
)

# Create a group to manage both paddles
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

# Create the ball
# The ball's color, size, and associated paddles are set according to the game speed
ball = Ball(
    color=ball_colors[speed_multiplier - 7],
    block_width=30,  # Width of the ball
    block_height=30,  # Height of the ball
    paddles=paddle_group  # Group of paddles for collision detection
)

# Create a group for managing the ball
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

# Initialize the game manager with the groups of game objects
# The game manager coordinates the main game loop and interactions between objects
game_manager = GameManager(ball_group, paddle_group, background_group, divider_line_group)

# Game loop
def main():
    while True:
        # Handle user input events
        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                pygame.quit()  # Uninitialize all pygame modules
                sys.exit()  # Exit the program

            # Handle key press events
            if event.type == pygame.KEYDOWN:
                # Increase player movement speed if 'down' or 's' key is pressed
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.movement += player.speed
                # Decrease player movement speed if 'up' or 'w' key is pressed
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.movement -= player.speed

            # Handle key release events
            if event.type == pygame.KEYUP:
                # Adjust player movement based on simultaneous key presses
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Reset movement if 'up' or 'w' is still pressed, else stop movement
                    player.movement = -player.speed if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w] else 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Reset movement if 'down' or 's' is still pressed, else stop movement
                    player.movement = player.speed if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s] else 0

        # Execute game logic
        game_manager.run_game()

        # Display the current difficulty level on the screen
        speed_text = game_font.render(f"Difficulty: {speed_multiplier - 6}", False, text_colors[speed_multiplier - 7])
        screen.blit(speed_text, (650 * width_ratio, 550 * height_ratio))

        # Update the full display Surface to the screen
        pygame.display.flip()

        # Maintain game loop at 60 frames per second
        clock.tick(60)

if __name__ == "__main__":
    main()