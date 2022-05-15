import io
import random

from parser import parse
from randomizer import *

patch = io.open("patch.html", encoding='utf-8', mode='r')
data = parse(patch)


def print_item_update(itemobject):
    print(itemobject.name)
    print(itemobject.itself_changes)


def print_general_update(update):
    print(update)


def print_hero_update(heroobject):
    print(heroobject.name)
    print("Stats and etc:")
    print(heroobject.itself_changes)
    print()
    print("Skills:")
    for s in heroobject.skills_changes:
        c = heroobject.skills_changes[s]
        print(s)
        for i in c:
            print(i)
        print()


def main():
    print_hero_update(get_random_hero_data(data))
    print()
    print_item_update(get_random_item_data_from_dataset(data))
    print()
    print_general_update(get_random_general_data_from_dataset(data))
    input()


if __name__ == "__main__":
    main()
