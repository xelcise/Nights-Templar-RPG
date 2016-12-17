# Nights Templar is a text-based / turn-based RPG idea developed by Jamie Henderson

import time
import random
import sys


# Functions

def pausetime():
    time.sleep(0.75)


def stats_check():  # Prints your character's statistics
    print('> Your stats: %s hp [%s], %s strength, %s magic, level %s(%s)' % (
        player.hp, player.max_hp, player.strength, player.magic, player.level, player.xp))


def inventory_check():  # Prints your character's inventory
    print('This is your current inventory:\n'
          'Weapon: %s (%s attack, %s magic damage)\n'
          'Head slot: %s (%s defence)\n'
          'Body slot: %s (%s defence)\n'
          'Leg Slot: %s (%s defence)' %
          (player_inventory.weapon.name,
           player_inventory.weapon.atk,
           player_inventory.weapon.magic_damage,
           player_inventory.head.name,
           player_inventory.head.defence,
           player_inventory.body.name,
           player_inventory.body.defence,
           player_inventory.legs.name,
           player_inventory.legs.defence))
    total_armor = player_inventory.head.defence + player_inventory.body.defence + player_inventory.legs.defence
    print('(Your total armor points: %s)' % total_armor)


def player_bag_check():  # Prints you character's bag items
    if len(player_bag) != 0:
        action('The contents of your bag:')
        for k in player_bag:
            print(k.name)
        player_choice_input(['Equip an Item', 'Close'])
        print('%s' % chosen)
        if choice == '1':
            action('What sort of item would you like to equip?')
            player_choice_input(['Weapon', 'Head', 'Body', 'Legs'])
            equipoption = []
            equipnames = []
            equiptype = chosen
            for k in player_bag:
                if str(k) == str(chosen):
                    equipnames.append(k.name)
                    equipoption.append(k)
            player_choice_input(equipnames)
            if equiptype == 'Weapon':
                player_inventory.weapon = equipoption[int(choice) - 1]
                action('You have equipped the %s' % player_inventory.weapon.name)
            if equiptype == 'Head':
                player_inventory.head = equipoption[int(choice) - 1]
                action('You have equipped the %s' % player_inventory.head.name)
            if equiptype == 'Body':
                player_inventory.body = equipoption[int(choice) - 1]
                action('You have equipped the %s' % player_inventory.body.name)
            if equiptype == 'Legs':
                player_inventory.legs = equipoption[int(choice) - 1]
                action('You have equipped the %s' % player_inventory.legs.name)
    if len(player_bag) == 0:
        action('You have no belongings')


def melee(enemy, attacker):  # Melee attack function
    if attacker == player:
        enemy.hp = enemy.hp - (attacker.strength * player_inventory.weapon.atk)
        action('%s attacks the %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.strength * player_inventory.weapon.atk, enemy.hp, enemy.max_hp))
    else:
        enemy.hp = enemy.hp - attacker.strength
        action('The %s attacks %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.strength, enemy.hp, enemy.max_hp))


def spell(enemy, attacker):  # Magic (spell) attack function
    if attacker == player:
        spell_damage = attacker.magic * player_inventory.weapon.magic_damage
        enemy.hp = enemy.hp - spell_damage
        action('%s attacks the %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.magic * player_inventory.weapon.magic_damage, enemy.hp, enemy.max_hp))
    else:
        enemy.hp = enemy.hp - attacker.magic
        action('The %s attacks %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.magic, enemy.hp, enemy.max_hp))


def run(enemy):
    global run_attempt
    luck_dice(enemy.level - player.level + 2 * 5)
    if roll_luck < 3:
        action('You escape!')
        run_attempt = 'success'
    else:
        action('You fail to run away')
        run_attempt = 'failed'


def battle(enemy, attacked_player, creature_movement):  # Main battle function
    enemy.hp = enemy.max_hp
    action('A %s %s. [%s hp, level %s]' % (enemy.name, creature_movement, enemy.hp, enemy.level))
    while enemy.hp > 0:
        player_choice_input(['Physical attack using your %s' % player_inventory.weapon.name,
                             'Magical attack using your %s' % player_inventory.weapon.name,
                             'Attempt to run away'])
        if choice == '1':
            melee(enemy, attacked_player)
        elif choice == '2':
            spell(enemy, attacked_player)
        if choice == '3':
            run(enemy)
            if run_attempt == 'success':
                break
                return
        if enemy.hp > 0:
            melee(player, enemy)
        if enemy.hp <= 0:
            pausetime()
            action('You have killed the %s' % enemy.name)
        if player.hp <= 0:
            action('You have died, game over.')
            sys.exit()
    if enemy.hp < + 0:
        player.xp = attacked_player.xp + enemy.xp
        action('%s gains %s xp! (Total: %s)' % (player.name, enemy.xp, player.xp))
        loot_roll(enemy)
        while True:
            player_choice_input(['Check your stats', 'Check your inventory', 'Check your bag', 'Continue'])
            if choice == '1':
                stats_check()
            elif choice == '2':
                inventory_check()
            elif choice == '3':
                player_bag_check()
            elif choice == '4':
                break


def adding_to_bag(added, quantity):  # Adds items to character's bag
    if added not in player_bag:
        player_bag[added] = quantity
    else:
        player_bag[added] = player_bag[added] + quantity


def luck_dice(maximum_luck):
    global roll_luck
    roll_luck = random.randrange(0, maximum_luck)
    action('[%s]' % roll_luck)


def loot_roll(killed_character):  # Looting mechanism for dead enemies
    global option_list
    global add_to_bag_parameters
    filtered_loot = []
    for v, k in killed_character.loot_table.items():
        luck_dice(100)
        if v > roll_luck:
            filtered_loot.append(k)
    gold_dropped = 100 - roll_luck * killed_character.level
    adding_to_bag(gold, gold_dropped)
    action('The %s drops %s gold, which you pick up' % (killed_character.name, gold_dropped))
    if len(filtered_loot) != 0:
        action('The %s drops some loot!' % killed_character.name)
        action('Would you like to pick up the items?')
        while len(filtered_loot) != 0:
            loot_options = []
            for item in filtered_loot:
                loot_options.append(item.name)
            loot_options.append('Take all')
            loot_options.append('Leave')
            player_choice_input(loot_options)
            if chosen == 'Take all':
                for item in loot_options:
                    adding_to_bag(item, 1)
                    action('You pick up all the items')
                    return
            elif chosen == 'Leave':
                return
            else:
                adding = filtered_loot[int(choice) - 1]
                filtered_loot.pop(int(choice) - 1)
                adding_to_bag(adding, 1)


def healing(healamount, character):
    if character.max_hp - character.hp > healamount:
        character.hp = character.hp + healamount
    else:
        character.hp = character.max_hp
    action('%s recovers %s hp [%s/%s]' % (character.name, healamount, character.hp, character.max_hp))


def player_choice_input(option):  # Player choice menu
    global choice
    global chosen
    global combine_list
    global option_list
    option_list = 1
    combine_list = []
    for opt in option:
        combine_list.append(opt)
    print('\n')
    pausetime()
    for i in option:
        print('[%s]%s' % (option_list, i))
        option_list += 1
    choice = input('\n> ')
    if int(choice) <= option_list - 1:
        chosen = combine_list[int(choice) - 1]
    else:
        action('Option not recognised')
        player_choice_input(option)


def talk(speaker, text):  # Default NPC speech
    print('%s: %s' % (speaker, text))
    pausetime()


def action(text):  # Default narrator/status
    print('> %s' % text)
    pausetime()


# Classes

class Character(object):
    def __init__(self, name, hp, max_hp, strength, magic, xp, level, loot_table):
        super(Character, self).__init__()
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.strength = strength
        self.magic = magic
        self.xp = xp
        self.level = level
        self.loot_table = loot_table


class Inventory(object):
    def __init__(self, weapon, head, body, legs):
        super(Inventory, self).__init__()
        self.weapon = weapon
        self.head = head
        self.body = body
        self.legs = legs


class Weapon(Inventory):
    def __init__(self, name, atk, magic_damage, value):
        super(Inventory, self).__init__()
        self.name = name
        self.atk = atk
        self.magic_damage = magic_damage
        self.value = value

    def __str__(self):
        return "Weapon"


class Armor(Inventory):
    def __init__(self, name, defence, value, slot):
        super(Inventory, self).__init__()
        self.name = name
        self.defence = defence
        self.value = value
        self.slot = slot

    def __str__(self):
        return str(self.slot)


class Miscellaneous(Inventory):
    def __init__(self, name, value):
        super(Inventory, self).__init__()
        self.name = name
        self.value = value

    def __str__(self):
        return "Miscellaneous"


# In game items

# melee weapons
hands = Weapon('Bare Hands', 1, 0, 0)
shortsword = Weapon('Shortsword', 5, 0, 5)

# magic weapons
worn_staff = Weapon('Worn Staff', 1, 5, 5)

# head armor
none = Armor('Nothing', 0, 0, 'Head')
leather_cap = Armor('Leather Cap', 2, 2, 'Head')
brass_helmet = Armor('Brass Helmet', 5, 30, 'Head')

# body armor
leather_gilet = Armor('Leather Gilet', 4, 10, 'Body')

# leg armor
leather_trousers = Armor('Leather Trousers', 2, 5, 'Leg')
chainmail = Armor('Chainmail Leg Armor', 4, 40, 'Leg')
plate = Armor('Platemail Leg Armor', 10, 100, 'Leg')

# Misc Items
gold = Miscellaneous('Gold', 1)

# starting player inventory
player_inventory = Inventory(hands, none, leather_gilet, leather_trousers)

# Randomised starting strength and balanced magic stats
randomised_strength = random.randrange(3, 20)
randomised_magic = 20 - randomised_strength

no_loot = {}

low_level_loot = {70: leather_cap, 80: shortsword, 5: plate}

# Character default stats
player = Character('Player', 100, 120, randomised_strength, randomised_magic, 0, 1, no_loot)
player_bag = {}
# Monster default stats
# name = character (name, hp, maxhp str, mg, xp, lvl)
zombie = Character('Zombie', 100, 100, 5, 5, 20, 1, low_level_loot)


# Story

print('\n\n\n\\\\\\ Nights Templar ///')
print('©2016 Jamie Henderson\n\n\n')
Location = 'The Inn'
action('You enter a dimly lit cabin in the woods.')
action('An old man with a black beard and a white eye stands at the bar.')
talk('Old Man', 'Greetings stranger... I haven\'t seen you around these parts. What\'s your name?')
player.name = input('\n> ')
talk('Old Man', 'Well then... %s, welcome to my inn.' % player.name)
talk('Old Man', 'Help yourself to bread and ale, you look like you need it.')
talk('Old Man', 'It\'ll make you feel better, trust me.')
while player.hp < player.max_hp:
    player_choice_input(['Take a hunk of stale bread', 'Swig from the dark stout on the bar'])
    if choice == '1':
        action('You feel rejuvenated...')
        healing(5, player)
    elif choice == '2':
        action('The stout refreshes your parched mouth...')
        healing(20, player)
talk('Old Man', 'If you\'re planning on going back out there, I suggest you take one of these.')
action('The old man reaches behind the bar and takes out a shortsword and a worn mages\' staff')
while player_inventory.weapon == hands:
    player_choice_input(['Take the shortsword', 'Take the staff', 'Check your stats'])
    if choice == '1':
        player_inventory.weapon = shortsword
    elif choice == '2':
        player_inventory.weapon = worn_staff
    elif choice == '3':
        stats_check()
talk('Old Man', '"Be wary outside this inn..."')
talk('Old Man', '"At this time of night, there are some terrible monsters lurking in these woods."')
while Location == 'The Inn':
    player_choice_input(['Check your stats', 'Check your inventory', 'Check your bag', 'Leave the inn'])
    if choice == '1':
        stats_check()
    elif choice == '2':
        inventory_check()
    elif choice == '3':
        player_bag_check()
    elif choice == '4':
        action('You leave the inn.')
        Location = 'The_Forest'
action('You walk out, down the snow-strewn path towards the forest.')
action('A rustling in the distance catches your attention.')
battle(zombie, player, 'lurches onto the path')
action('What in the world was that?')
action('You hear something else...')
battle(zombie, player, 'staggers towards you')
action('Not another one!')
battle(zombie, player, 'looms forward out of the darkness')
