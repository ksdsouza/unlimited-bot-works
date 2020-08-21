import time
from collections import Counter

import numpy as np

from src.ScreenUtils import ScreenUtil
from src.Selector import Selector


def get_strategy(cards):
    counter = Counter()
    for card in cards:
        counter[card] += 1

    most_common_type, count = counter.most_common(1)[0]
    if count >= 3:
        return np.argwhere((np.array(cards) == most_common_type))[:3].flatten().tolist()
    order = ['A', 'B', 'Q']
    strategy = []
    for card_type in order:
        for i, card in enumerate(cards):
            if len(strategy) == 3:
                break
            if card == card_type:
                strategy.append(i)
    return strategy


time.sleep(2)
screenUtil = ScreenUtil()

while True:
    pixels = screenUtil.get_pixels()
    selector = Selector(pixels)
    if selector.attack_is_visible():
        selector.press_attack(screenUtil.window)
        time.sleep(1)
        selector.update_pixels(screenUtil.get_pixels())
        # selector.get_effective()
        cards = selector.get_cards()
        print(cards)
        strategy = get_strategy(cards)
        print(strategy)
        for c in strategy:
            selector.press_card(screenUtil.window, c)
            time.sleep(0.15)
        time.sleep(10)
    else:
        print("Attack not visible")
        time.sleep(2)
