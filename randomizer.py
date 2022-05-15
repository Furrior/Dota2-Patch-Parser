import random


def get_random_item_data_from_dataset(data):
    name, itemobject = random.choice(list((data)["Items"].items()))
    return itemobject


def get_random_general_data_from_dataset(data):
    return random.choice(data["General"].itself_changes)


def get_random_hero_data(data):
    name, heroobject = random.choice(list((data)["Heroes"].items()))
    return(heroobject)
