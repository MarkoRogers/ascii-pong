from custom_gui.custom_gui import SimpleWindow
from custom_gui.widgets import Canvas
from game_elements.paddle import Paddle
from game_elements.ball import Ball


def main():
    # Create the main window
    window = SimpleWindow(800, 600, "Pong Game")

    # Game dimensions
    width, height = 800, 600
    paddle_width = 20
    paddle_height = 100
    ball_size = 10

    # Create paddles and ball
    player_paddle = Paddle(30, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ai_paddle = Paddle(width - 30 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = Ball(width // 2, height // 2)

    # Create the canvas for drawing
    canvas = Canvas(window)

    def update_game():
        # Clear canvas
        canvas.clear()

        # Move ball
        ball.move()

        # Ball collision with top and bottom
        if ball.y <= 0 or ball.y >= height:
            ball.dy = -ball.dy

        # Ball collision with paddles
        if (ball.x <= player_paddle.x + player_paddle.width and
            player_paddle.y <= ball.y <= player_paddle.y + player_paddle.height) or \
                (ball.x >= ai_paddle.x - ball_size and
                 ai_paddle.y <= ball.y <= ai_paddle.y + ai_paddle.height):
            ball.bounce()

        # Ball out of bounds (reset position)
        if ball.x < 0 or ball.x > width:
            ball.x = width // 2
            ball.y = height // 2
            ball.dx = -ball.dx

        # AI paddle movement
        if ai_paddle.y < ball.y:
            ai_paddle.move(2, height)
        elif ai_paddle.y > ball.y:
            ai_paddle.move(-2, height)

        # Draw paddles and ball
        player_paddle.draw(canvas)
        ai_paddle.draw(canvas)
        ball.draw(canvas)

    # Start the game loop
    window.mainloop(update_game)


if __name__ == "__main__":
    main()
