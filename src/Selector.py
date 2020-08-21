from concurrent import futures
from typing import Tuple

import numpy as np
from pynput.mouse import Button, Controller

from src.kmeans import get_dominant_colour

ATTACK_TARGET_COLOUR = [1, 218, 234]
ATTACK_TARGET_LOCATION = (818, 1848)

EFFECTIVE_COLOURS = np.array([
    [89, 0, 0],
    [90, 0, 0],
    [91, 0, 0],
    [182, 0, 0]
])

# Full-sized card regions
# CARD_WIDTH = 280
# CARD_MARGIN = 107
# CARD_INIT_POSN = 205
# CARD_Y_REGIONS = slice(780, 920)

CARD_WIDTH = 280
CARD_MARGIN = 105
CARD_INIT_POSN = 205
CARD_Y_REGIONS = slice(600, 945)

CARD_EFFECTIVE_WIDTH = 120
CARD_EFFECTIVE_MARGIN = 265
CARD_EFFECTIVE_INIT_POSN = 400
CARD_EFFECTIVE_Y_REGIONS = slice(540, 610)

CARD_LOCATIONS = []
for i in range(5):
    card_start = CARD_INIT_POSN + (i * CARD_MARGIN) + (i * CARD_WIDTH)
    CARD_LOCATIONS.append((CARD_Y_REGIONS, slice(card_start, card_start + CARD_WIDTH)))

CARD_EFFECTIVE_LOCATIONS = []
for i in range(5):
    card_start = CARD_EFFECTIVE_INIT_POSN + (i * CARD_EFFECTIVE_MARGIN) + (i * CARD_EFFECTIVE_WIDTH)
    CARD_EFFECTIVE_LOCATIONS.append((CARD_EFFECTIVE_Y_REGIONS, slice(card_start, card_start + CARD_EFFECTIVE_WIDTH)))


class Selector:
    def __init__(self, pixels):
        self.pixels = pixels

    def update_pixels(self, pixels):
        self.pixels = pixels

    def attack_is_visible(self):
        print(self.pixels[ATTACK_TARGET_LOCATION])
        [r, g, b] = self.pixels[ATTACK_TARGET_LOCATION]
        [expected_r, expected_g, expected_b] = ATTACK_TARGET_COLOUR
        return loose_equals(r, expected_r, 3) and loose_equals(g, expected_g, 3) and loose_equals(b, expected_b, 3)

    @staticmethod
    def __press_at_location(x: int, y: int):
        mouse = Controller()
        mouse.position = x, y
        mouse.move(1, 1)
        mouse.click(Button.left)

    def press_attack(self, window):
        attack_y, attack_x = ATTACK_TARGET_LOCATION
        x, y = window.get_root_coords(1948, 818)
        self.__press_at_location(*window.get_root_coords(x, y))

    def press_card(self, window, card_num):
        card_y, card_x = CARD_LOCATIONS[card_num]
        x, y = window.get_root_coords(card_x.start + 150, card_y.start + 100)
        self.__press_at_location(x, y)

    def get_effective(self):
        i = 0
        for ys, xs in CARD_EFFECTIVE_LOCATIONS:
            i += 1
            region = self.pixels[ys, xs]
            print(self.is_effective(region))

    def is_effective(self, region: np.ndarray):
        width, height, _, = np.shape(region)
        for [r, g, b] in EFFECTIVE_COLOURS:
            has_colour = False
            for w in range(width):
                for h in range(height):
                    [reg_r, reg_g, reg_b] = region[w, h]
                    if loose_equals(reg_r, r, 3) and loose_equals(reg_g, g, 3) and loose_equals(reg_b, b, 3):
                        has_colour = True
                        break
                if has_colour:
                    break
            if not has_colour:
                return False
        return True

    def get_cards(self):
        cards = ['', '', '', '', '']
        with futures.ProcessPoolExecutor() as pool:
            for i, card in pool.map(dominant_colour, enumerate([self.pixels[loc] for loc in CARD_LOCATIONS])):
                cards[i] = card
            return cards


def dominant_colour(region_with_index: Tuple[int, np.ndarray]):
    i, region = region_with_index
    colour_to_card = {
        'R': 'B',
        'G': 'Q',
        'B': 'A'
    }
    return i, colour_to_card[get_dominant_colour(region)]


def loose_equals(a, b, error):
    return b - error <= a <= b + error
