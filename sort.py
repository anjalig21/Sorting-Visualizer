import pygame
import random
import math
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

    FONT = pygame.font.SysFont('comicsans', 20)
    PADDING_SIDES = 100
    PADDING_TOP = 100

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
        self.block_height = math.floor((self.height - self.PADDING_TOP) / (self.max_val - self.min_val)) ## total drawable area / range of values
        self.start_x = self.PADDING_SIDES // 2 ## integer division by 2 to get whole number

def draw(draw_info, algo_name, ascending=None):
    draw_info.window.fill(draw_info.BACKGROUND)
    pos = ""

    if ascending is None:
        pos = ""
    elif ascending:
        pos = '- Ascending'
    else:
        pos = '- Descending'

    title = draw_info.FONT.render(f"{algo_name} {pos}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2,5)) ## put title in center of screen

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,35)) ## put controls in center of screen

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,65)) ## put sorting in center of screen

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, colour_pos={}, clear=False):
    lst = draw_info.lst

    if clear:
        clear_rect = ((draw_info.PADDING_SIDES // 2),
                      draw_info.PADDING_TOP,
                      draw_info.width - draw_info.PADDING_SIDES,
                      draw_info.height - draw_info.PADDING_TOP)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height ## subtract height of screen from length of bar, find starting point and draw down

        colour = draw_info.GRADIENTS[i % 3]

        if i in colour_pos:
            colour = colour_pos[i]

        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height)) ## will draw over (beneath the screen)

        if clear:
            pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(0, len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True ## call this function each time a swap occurs, yield controls back from where it was called from, if not yield, keyboard buttons will not be heard
    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInfo(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(260)

        ## if sorting, try calling next, if it doesn't work that means generator is finished and sorting is false, but if it does, keep sorting
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
            else:
                draw(draw_info, sorting_algo_name, ascending)

        draw(draw_info, sorting_algo_name, ascending)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = bubble_sort(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()

if __name__ == "__main__":
    main()

