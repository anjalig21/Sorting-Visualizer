import pygame
import random
pygame.init()

class DrawInfo:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    GREY = 128,128,128
    BACKGROUND = WHITE

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    PADDING_SIDES = 100
    PADDING_TOP = 50

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.PADDING_SIDES) / len(lst)) ## area to represent blocks in / number of blocks
        self.block_height = round((self.height - self.PADDING_TOP) / (self.max_val - self.min_val)) ## total drawable area / range of values
        self.start_x = self.PADDING_SIDES // 2 ## integer division by 2 to get whole number

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND)
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info):
    lst = draw_info.lst
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height ## subtract height of screen from length of bar, find starting point and draw down

        colour = draw_info.GRADIENTS[i % 3]
        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height)) ## will draw over (beneath the screen)


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, lst)

    while run:
        clock.tick(60)
        draw(draw_info)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()

