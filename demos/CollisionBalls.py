import random
import sys

from pi3d import Keyboard

from pi3d import Display
from pi3d.Texture import Texture

from pi3d.sprite.Ball import Ball

# Ball parameters
MAX_BALLS = 15
MIN_BALL_SIZE = 5
MAX_BALL_SIZE = 100

BACKGROUND = 0.0, 0.0, 0.0, 0.0

TEXTURE_NAMES = ['textures/red_ball.png',
                 'textures/grn_ball.png',
                 'textures/blu_ball.png']


DISPLAY = Display.create(is_3d=False, background=BACKGROUND)

TEXTURES = [Texture(t) for t in TEXTURE_NAMES]

def random_ball():
  """Return a ball with a random color, position and velocity."""
  return Ball(random.choice(TEXTURES),
              random.uniform(MIN_BALL_SIZE, MAX_BALL_SIZE),
              random.uniform(0.0, DISPLAY.max_width),
              random.uniform(0.0, DISPLAY.max_height),
              random.uniform(-10.0, 10.0),
              random.uniform(-10.0, 10.0))


SPRITES = [random_ball() for b in range(MAX_BALLS)]
DISPLAY.add_sprites(*SPRITES)

@Keyboard.screenshot('collision.jpg')
def my_loop():
  for i, ball1 in enumerate(SPRITES):
    for ball2 in SPRITES[0:i]:
      ball1.bounce_collision(ball2)

DISPLAY.loop(my_loop)
