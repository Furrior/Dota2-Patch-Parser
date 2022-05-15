from lxml import etree
import lxml.html
import io


class Changing:
    def __init__(self, _itself_changes=[]) -> None:
        self.itself_changes = _itself_changes


class ItemChanging(Changing):
    def __init__(self, _name, _picurl, _itself_changes=[]) -> None:
        super().__init__(_itself_changes)
        self.name = _name
        self.picurl = _picurl
        self.itself_changes = "\n".join(self.itself_changes)


class HeroChanging(ItemChanging):
    def __init__(self, _name, _picurl, _itself_changes=[], _skills_changes=[]) -> None:
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

    general_changes = Changing(general[0].xpath(
        './/div[@class="patchnotespage_Note_eSxyZ"]/text()'))

    items_changes = {}
    for i in items:
        name = i.xpath(
            './/div[@class="patchnotespage_ItemName_1MKhq"]/text()')[0]
        picurl = f'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/{name.replace(" ", "_")}.png'
        changes = i.xpath('.//*[@class="patchnotespage_Note_eSxyZ"]/text()')
        items_changes[name] = ItemChanging(name, picurl, changes)

    heroes_changes = {}
    for h in heroes:
        name = h.xpath(
            './/div[@class="patchnotespage_HeroName_1nuWb"]/text()')[0]
        picurl = f"https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/{name.replace(' ', '_')}.png"
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

        heroes_changes[name] = HeroChanging(
            name, picurl, itself_changes, skills_changes)

    return {"General": general_changes, "Items": items_changes, "Heroes": heroes_changes}
