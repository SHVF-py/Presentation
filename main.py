# main.py
import sys
import pygame
from pygame.locals import *
from setup import *
from ball import Ball
from paddle import Paddle
from brick import Brick

class BrickBreakerGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.retry = False
        self.game_over = False
        self.paused = False
        self.screen = None
        self.score = 0
        self.level = 1  # Add level attribute
        self.initialize_game()

    def initialize_game(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")

        paddle_speed = 8  # Set the paddle speed
        ball_speed = 5  # Set the initial ball speed
        ball_color = WHITE  # Set the initial ball color
        self.paddle = Paddle((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT, paddle_speed)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, ball_speed, ball_speed, ball_color)

        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                brick = Brick(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
                self.bricks.append(brick)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.retry or self.game_over:
                        self.retry = False
                        self.game_over = False
                        self.score = 0  # Reset the score when restarting the game
                        self.level = 1  # Reset the level when restarting the game
                        self.initialize_game()
                elif event.key == K_ESCAPE:
                    self.paused = not self.paused  # Toggle pause/unpause

    def update_objects(self):
        if not self.game_over and not self.paused:
            self.ball.move()

            # Ball collisions with walls
            if self.ball.x <= 0 or self.ball.x >= WIDTH - BALL_RADIUS * 2:
                self.ball.reverse_x()

            if self.ball.y <= 0:
                self.ball.reverse_y()

            # Ball collisions with paddle
            if (
                self.paddle.x <= self.ball.x <= self.paddle.x + self.paddle.width and
                self.paddle.y <= self.ball.y <= self.paddle.y + self.paddle.height
            ):
                self.ball.reverse_y()

            # Ball collisions with bricks
            for brick in self.bricks:
                if brick.rect.colliderect((self.ball.x, self.ball.y, BALL_RADIUS * 2, BALL_RADIUS * 2)):
                    self.bricks.remove(brick)
                    self.ball.reverse_y()
                    self.score += 1  # Increase the score when a brick is hit

            # Check if all bricks are gone
            if not self.bricks:
                self.retry = True

            # Check if the ball goes out of the screen
            if self.ball.y >= HEIGHT:
                self.game_over = True

            # Check for level up
            if self.score >= self.level * 15:
                self.level += 1
                self.ball.speed_x += 1  # Increase ball speed with each level
                self.ball.speed_y += 1
                if self.level <= len(LEVEL_COLORS):
                    self.ball.color = LEVEL_COLORS[self.level - 1]  # Change ball color with each level

    def draw_objects(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (self.paddle.x, self.paddle.y, self.paddle.width, self.paddle.height))
        pygame.draw.ellipse(self.screen, self.ball.color, (self.ball.x, self.ball.y, BALL_RADIUS * 2, BALL_RADIUS * 2))

        for brick in self.bricks:
            pygame.draw.rect(self.screen, RED, brick.rect)

        # Draw the score and level
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}  Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.retry:
            font = pygame.font.Font(None, 36)
            text = font.render("Press SPACE to Retry", True, WHITE)
            self.screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))

        if self.game_over:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over. Press SPACE to Retry", True, WHITE)
            self.screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))

        if self.paused:
            font = pygame.font.Font(None, 36)
            text = font.render("Paused. Press ESC to Unpause", True, WHITE)
            self.screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))

        pygame.display.flip()

    def run(self):
        self.initialize_game()

        while True:
            self.handle_events()

            if not self.retry and not self.game_over and not self.paused:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT] and self.paddle.x > 0:
                    self.paddle.move_left()
                if keys[K_RIGHT] and self.paddle.x < WIDTH - self.paddle.width:
                    self.paddle.move_right()

                self.update_objects()

            self.draw_objects()

            self.clock.tick(60)

if __name__ == "__main__":
    game = BrickBreakerGame()
    game.run()

   
