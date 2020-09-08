import os
from concurrent import futures
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from config import config
from kmeans import get_dominant_colour

ATTACK_TARGET_COLOUR = [0, 50, 110]
ATTACK_TARGET_LOCATION = (900, 1700)

SCREEN_OFFSET_X = 250
SCREEN_OFFSET_Y = 0

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
CARD_INIT_POSN = 75
CARD_Y_REGIONS = slice(800, 945)

CARD_EFFECTIVE_WIDTH = 120
CARD_EFFECTIVE_MARGIN = 265
CARD_EFFECTIVE_INIT_POSN = 250
CARD_EFFECTIVE_Y_REGIONS = slice(540, 610)

NP_LOCATIONS = [
    (311, 615),
    (311, 975),
    (311, 1320),
]

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
        # plt.imsave('out.png', self.pixels[880:920, 1680:1720])
        [r, g, b] = self.pixels[ATTACK_TARGET_LOCATION]
        print(r, g, b)
        [expected_r, expected_g, expected_b] = ATTACK_TARGET_COLOUR
        return loose_equals(r, expected_r, 3) and loose_equals(g, expected_g, 3) and loose_equals(b, expected_b, 3)

    @staticmethod
    def __press_at_location(x: int, y: int):
        device_id_flag = f'-s {config.device}' if config.device is not None else ''
        cmd_prefix = f'adb {device_id_flag}'
        os.system(f'{cmd_prefix} shell input tap {x + 250} {y}')

    def press_noble_phantasms(self):
        [self.__press_at_location(x, y) for (y, x) in NP_LOCATIONS]

    def press_attack(self):
        attack_y, attack_x = ATTACK_TARGET_LOCATION
        self.__press_at_location(attack_x, attack_y)

    def press_card(self, card_num):
        y, x = CARD_LOCATIONS[card_num]
        self.__press_at_location(x.start, y.start)

    def get_effective(self):
        for y, x in CARD_EFFECTIVE_LOCATIONS:
            region = self.pixels[y, x]
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

    def get_cards_seq(self):
        cards = []
        for i, card in enumerate([self.pixels[loc] for loc in CARD_LOCATIONS]):
            plt.imsave(f'card{i}.png', np.ascontiguousarray(card))
            cards.append(dominant_colour((i, card)))
        print(cards)
        return cards

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
