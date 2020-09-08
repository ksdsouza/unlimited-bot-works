import time
from collections import Counter

import numpy as np
import argparse

from config import config
from ScreenUtils import get_screen
from Selector import Selector


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
    strategy_str = ''.join(cards[i] for i in strategy)

    if strategy_str == 'AAB' or strategy_str == 'BBQ':
        strategy[1], strategy[2] = strategy[2], strategy[1]
    elif strategy_str == 'ABB' or strategy_str == 'BQQ':
        strategy[0], strategy[1] = strategy[1], strategy[0]

    return strategy


def run():
    turn_counter = 0
    while True:
        pixels = get_screen()
        selector = Selector(pixels)
        if not selector.attack_is_visible():
            print("Attack not visible")
            continue

        selector.press_attack()
        time.sleep(1)
        turn_counter += 1
        if turn_counter > 9:
            selector.press_noble_phantasms()
        selector.update_pixels(get_screen())
        # selector.get_effective()

        cards = selector.get_cards()
        print(cards)
        strategy_cards = get_strategy(cards)
        for card in strategy_cards:
            selector.press_card(card)
        time.sleep(15)


arg_parser = argparse.ArgumentParser(description="A Fate Grand Order Bot")
arg_parser.add_argument(
    '--device',
    metavar='adb_device_id',
    type=str,
    # nargs=1,
    help='The ADB Device id'
)
arg_parser.add_argument(
    '--c',
    dest='config',
    metavar='device_configuration',
    type=str,
    nargs=1,
    help='Device configuration file',
    default='config/config.toml'
)


def main():
    args = arg_parser.parse_args()
    config.load_configuration(args.config, device=args.device)
    run()


if __name__ == "__main__":
    main()
