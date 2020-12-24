import xml.dom.minidom


# The general organization of the program will go as follows:
#
# 1) Load up xml data into appropriate containers for use in the main loop
# (be sure to consider how to organize files needed for each element (e.g.
# enemy behaviors, script, character data, save files, etc.)->>
# 2) Main loop (for as long as player plays game)->>
# 3) End
#
# Note to self--we can probably use a stack for enemy hoardes and have
# a queue for turn priority (will be determined by spd stat)
class Character:
    # This is a quick example of a class variable, something shared by all
    # instances of a class
    #
    # charType = 'character'

    def __init__(self, level, hp, atk, dfn, sAtk, sDfn, spd, elem, skillList):
        # A character's level (will be static for enemies/NPCs, evolving
        # for players)
        self.level = level

        # A character's stats (example of instance variables, unique to a spec.
        # instance of a class)
        self.hp = hp
        self.atk = atk
        self.dfn = dfn
        self.sAtk = sAtk
        self.sDfn = sDfn
        self.spd = spd

        # A character's element
        self.elem = elem

        # A character's mySkills will be a list that contains all of the
        # skills a character can use (but will be blocked off depending
        # on a character's level)
        self.mySkills = skillList

    def attack(enemy):
        pass


# Unlike general Characters, Players will get to evolve as they gain exp
# (a trait that Characters don't have individually)
class Player(Character):
    def __init__(self, level, hp, atk, dfn, sAtk, sDfn,
                 spd, elem, skillList, name, exp):
        super().__init__(level, hp, atk, dfn, sAtk, sDfn, spd, elem, skillList)

        self.name = name
        self.exp = exp

    def levelUp(self):
        self.level += 1


class Action:
    def __init__(self):
        pass


class Attack:
    def __init__(self, name, categ, elem, power, acc):
        self.name = name
        self.categ = categ
        self.elem = elem
        self.power = power
        self.acc = acc


# Organizes the element strength chart and returns a dictionary with the
# appropriate data
#
# note to self: perhaps add two more arguments to elemParse so that we
# can change the values of two dictionaries without needing to do one
# return statement
def elemParse(filename):
    xmldoc = xml.dom.minidom.parse(filename)

    # Extracting each the full element data from the xml file
    rpgData = xmldoc.getElementsByTagName('RPGData')[0]
    elemChart = rpgData.getElementsByTagName('ElemChart')[0]
    elemList = elemChart.getElementsByTagName('Elem')

    strengthDict = {}

    # This for loop attaches the element (key) to the list of
    # elements each one is strong against (value)
    for element in elemList:
        # The actual element names
        elemName = element.firstChild.data.strip()

        # Recall that the keys are strongAg and immunTo, its values are
        # the things we want to look out for/process
        #
        # elemAttr is the dictionary holding the the keys (Elem features)
        # and their values (strings containing elements strongAg and immunTo)
        #
        # in elemAttr is 'strongAg': '...' and 'immunTo': '...', both k/v pairs
        # inside of the dictionary (though similar, not exactly a dict, this
        # is an xml.dom.minidom.NamedNodeMap--to get the value, we need
        # to explicitly call .value to the end, unlike a dictionary where
        # we can get the value of a key by just doing dictName['keyName'])
        elemAttr = element.attributes

        # Here, we append new elem/strongAg pairs to strengthDict
        if elemName not in strengthDict.keys():
            strengthDict[elemName] = elemAttr['strongAg'].value.split(',')

    return strengthDict


def main():
    filename = 'rpgData.xml'

    strengthDict = elemParse(filename)

    # print(strengthDict['umbra'])

    # Demonstrates how a class variable is shared b/w a class and a derived class
    # print(person.charType)
    # print(enemy.charType)

    # Sample method of initializing a player and enemy
    person = Player(10, 25, 10, 7, 10, 7, 8, 'elec', [], 'Nate', 0)
    enemy = Character(8, 10, 3, 4, 1, 3, 6, 'aqua', [])

    # We check if an opponent's element is inside the list of elements a char's
    # element is strong against and make judgement
    if enemy.elem in strengthDict[person.elem]:
        print('2x effective')
    elif person.elem in strengthDict[enemy.elem]:
        print('0.5x effective')
    else:
        print('1x effective')


if __name__ == '__main__':
    main()