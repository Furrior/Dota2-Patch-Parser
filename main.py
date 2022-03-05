from lxml import etree
import lxml.html
import io
import random

patch = io.open("7.31.html", encoding='utf-8', mode='r')


class ChangeObject:
    def __init__(self, _itself_changes=[]) -> None:
        self.itself_changes = _itself_changes


class ChangeItem(ChangeObject):
    def __init__(self, _name, _itself_changes=[]) -> None:
        super().__init__(_itself_changes)
        self.name = _name
        self.itself_changes = "\n".join(self.itself_changes)


class ChangeHero(ChangeItem):
    def __init__(self, _name, _itself_changes=[], _skills_changes=[]) -> None:
        super().__init__(_name, _itself_changes)
        self.skills_changes = _skills_changes


def parse(file):
    api = file.readlines()
    html = ''
    for n in api:
        html += n

    tree = lxml.html.document_fromstring(html)
    general = tree.xpath(
        '//div[@class="patchnotespage_UpdatesSection_3n8oL patchnotespage_IsShown_rKsLh"]')
    items = tree.xpath('//*[@class="patchnotespage_PatchNoteItem_32hr0"]')
    heroes = tree.xpath('//*[@class="patchnotespage_PatchNoteHero_99z4V"]')

    general_changes = ChangeObject(general[0].xpath(
        './/div[@class="patchnotespage_Note_eSxyZ"]/text()'))

    items_changes = {}
    for i in items:
        name = i.xpath(
            './/div[@class="patchnotespage_ItemName_1MKhq"]/text()')[0]
        changes = i.xpath('.//*[@class="patchnotespage_Note_eSxyZ"]/text()')
        items_changes[name] = ChangeItem(name, changes)

    heroes_changes = {}
    for h in heroes:
        name = h.xpath(
            './/div[@class="patchnotespage_HeroName_1nuWb"]/text()')[0]

        itself_changes = []

        itself_changes_div = h.xpath(
            './/div[contains(@class,"patchnotespage_Notes_16viL")][div[not(contains(@class, "patchnotespage_AbilityNote_3W8ym"))]]')
        if itself_changes_div:
            if len(itself_changes_div) == 1:
                itself_changes = itself_changes_div[0].xpath(
                    './/div[@class="patchnotespage_Note_eSxyZ"]/text()')
            if len(itself_changes_div) == 2:
                itself_changes = itself_changes_div[0].xpath(
                    './/div[@class="patchnotespage_Note_eSxyZ"]/text()')
                itself_changes += itself_changes_div[1].xpath(
                    './/div[@class="patchnotespage_Note_eSxyZ"]/text()')

        skills_changes = {}
        skills_div = h.xpath(
            './/div[contains(@class,"patchnotespage_Notes_16viL")][div[(contains(@class, "patchnotespage_AbilityNote_3W8ym"))]]')
        if skills_div:
            skills_div = skills_div[0]
            skills = skills_div.xpath(
                './/div[@class="patchnotespage_AbilityNote_3W8ym"]')
            for skill in skills:
                skill_name = skill.xpath(
                    './/div[@class="patchnotespage_AbilityName_3evA1"]/text()')[0]
                skill_changes = skill.xpath(
                    './/div[@class="patchnotespage_Note_eSxyZ"]/text()')
                skills_changes[skill_name] = skill_changes

        heroes_changes[name] = ChangeHero(
            name, itself_changes, skills_changes)

    return {"General": general_changes, "Items": items_changes, "Heroes": heroes_changes}


data = parse(patch)


def getRandomItemData():
    name, itemobject = random.choice(list((data)["Items"].items()))
    return itemobject


def getRandomGeneralData():
    return random.choice(data["General"].itself_changes)


def getRandomHeroData():
    name, heroobject = random.choice(list((data)["Heroes"].items()))
    return(heroobject)


def printItemUpdate(itemobject):
    print(itemobject.name)
    print(itemobject.itself_changes)


def printGeneralUpdate(update):
    print(update)


def printHeroUpdate(heroobject):
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


if __name__ == "__main__":
    printHeroUpdate(getRandomHeroData())
    print()
    printItemUpdate(getRandomItemData())
    print()
    printGeneralUpdate(getRandomGeneralData())
    input()
