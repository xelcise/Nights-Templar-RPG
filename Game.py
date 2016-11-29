# Nights Templar is a text-based / turn-based RPG idea developed by Jamie Henderson

import time
import random
import sys


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
        self.lootlist = loot_table


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


class Armor(Inventory):
    def __init__(self, name, defence, value):
        super(Inventory, self).__init__()
        self.name = name
        self.defence = defence
        self.value = value


class Miscellaneous(Inventory):
    def __init__(self, name, value):
        super(Inventory, self).__init__()
        self.name = name
        self.value = value


# melee weapons
hands = Weapon('Bare Hands', 1, 0, 0)
shortsword = Weapon('Shortsword', 5, 0, 5)

# magic weapons
worn_staff = Weapon('Worn Staff', 1, 5, 5)

# head armor
leather_cap = Armor('Leather Cap', 2, 2)
brass_helmet = Armor('Brass Helmet', 5, 30)

# body armor
leather_gilet = Armor('Leather Gilet', 4, 10)

# legarmor
leather_trousers = Armor('Leather Trousers', 2, 5)
chainmail = Armor('Chainmail Legarmor', 4, 40)
plate = Armor('Platemate Leg Armor', 10, 100)

# Misc Items
gold = Miscellaneous('Gold', 1)

# starting player inventory
player_inventory = Inventory(hands, leather_cap, leather_gilet, leather_trousers)

# Randomised starting strength and balanced magic stats
randomised_strength = random.randrange(3, 20)
randomised_magic = 20 - randomised_strength

roll_luck = 0

no_loot = {}

low_level_loot = {80: gold.name, 40: leather_cap.name, 50: shortsword.name, 5: plate.name}

# Character default stats
player = Character('Player', 100, 120, randomised_strength, randomised_magic, 0, 1, no_loot)
player_bag = {}

# Monster default stats
zombie = Character('Zombie', 200, 200, 5, 5, 20, 1, low_level_loot)


# Defined functions

def playerstats():
    print('> Your stats: %s hp, %s strength, %s magic, level %s(%s)' % (
        player.hp, player.strength, player.magic, player.level, player.xp))


def playerinventory():
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
    totalarmor = player_inventory.head.defence + player_inventory.body.defence + player_inventory.legs.defence
    print('(Your total armor points: %s)' % totalarmor)

def player_bag_check():
    if len(player_bag) != 0:
        print('This is the contents of your bag:\n%s' % player_bag)
    print('You have no belongings')



def melee(enemy, attacker):
    if attacker == player:
        enemy.hp = enemy.hp - (attacker.strength * player_inventory.weapon.atk)
        action('%s attacks the %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.strength * player_inventory.weapon.atk, enemy.hp, enemy.max_hp))
    else:
        enemy.hp = enemy.hp - attacker.strength
        action('The %s attacks %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.strength, enemy.hp, enemy.max_hp))


def spell(enemy, attacker):
    if attacker == player:
        enemy.hp = enemy.hp - (attacker.magic * player_inventory.weapon.magic_damage)
        action('%s attacks the %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.magic * player_inventory.weapon.magic_damage, enemy.hp, enemy.max_hp))
    else:
        enemy.hp = enemy.hp - attacker.magic
        action('The %s attacks %s, doing %s points of damage [%s/%s]' % (
            attacker.name, enemy.name, attacker.magic, enemy.hp, enemy.max_hp))


def battle(enemy, attacked_player, creaturemovement):
    enemy.hp = enemy.max_hp
    action('A %s %s. [%s hp, level %s]' % (enemy.name, creaturemovement, enemy.hp, enemy.level))
    while enemy.hp > 0:
        player_choice_input(['Physical attack using your %s' % player_inventory.weapon.name,
                             'Magical attack using your %s' % player_inventory.weapon.name,
                             'Attempt to run away'])
        if player_choice == '1':
            if enemy.hp > 0:
                melee(enemy, attacked_player)
        elif player_choice == '2':
            if enemy.hp > 0:
                spell(enemy, attacked_player)
        if enemy.hp > 0:
            melee(player, enemy)
        if enemy.hp <= 0:
            time.sleep(0.5)
            action('You have killed the %s' % enemy.name)
        if player.hp <= 0:
            action('You have died, game over.')
            sys.exit()
    player.xp = attacked_player.xp + enemy.xp
    action('%s gains %s xp! (Total: %s)' % (player.name, enemy.xp, player.xp))
    loot_roll(enemy)
    player_choice_input(['Check your stats', 'Check your inventory', 'Continue'])
    if player_choice == '1':
        playerstats()
    elif player_choice == '2':
        playerinventory()


def adding_to_bag(object, quantity):
    if object not in player_bag:
        player_bag[object] = quantity
    else:
        player_bag[object] = player_bag[object] + quantity


def loot_roll(killed_character):
    global player_choice
    global option_list
    global add_to_bag_parameters
    roll_luck = random.randrange(0, 100)
    action('You rolled a %s' % roll_luck)
    filtered_loot_dict = {v: 1 for k, v in killed_character.lootlist.items() if k > roll_luck}
    filtered_loot_dict['Gold'] = (100 - roll_luck) * killed_character.level
    action('The %s drops some loot!' % killed_character.name)
    action('Would you like to pick up the items?')
    filtered_loot_list = [(v, k) for v, k in filtered_loot_dict.items()]
    filtered_loot_list.append((' Take all'))
    filtered_loot_list.append((' Leave'))
    while len(filtered_loot_list) != 2:
        player_choice_input(filtered_loot_list)
        option_list += -1
        player_choice_adjusted = int(player_choice) -1
        s = (filtered_loot_list[player_choice_adjusted])
        if player_choice == '%s' % (option_list - 1):
            for k in filtered_loot_dict:
                adding_to_bag(k, filtered_loot_dict[k])
            break
        elif player_choice == '%s' % option_list:
            break
        else:
            adding_to_bag(s[0],s[1])
            filtered_loot_list.remove(s)


def player_choice_input(option):
    global player_choice
    global option_list
    option_list = 1
    print('\n')
    for i in option:
        time.sleep(0.5)
        print('[%s]%s' % (option_list, i))
        option_list += 1
    player_choice = input('\n')


def talk(speaker, text):
    print('%s: "%s"' % (speaker, text))
    time.sleep(0.5)


def action(text):
    print('> %s' % text)
    time.sleep(0.5)


print('\n\n\n\\\\\\ Nights Templar ///\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('Developed in 2016 by Jamie Henderson\n\n\n')
Location = 'The Inn'
action('You enter a dimly lit cabin in the woods.')
action('An old man with a black beard and a white eye stands at the bar.')
talk('Old Man', 'Greetings stranger... I haven\'t seen you around these parts. What\'s your name?')
player.name = input('')
talk('Old Man', '"Well then... %s, welcome to my inn."' % player.name)
talk('Old Man', '"Help yourself to bread and ale, you look like you need it."')
talk('Old Man', '"It\'ll make you feel better, trust me."')
while player.hp < player.max_hp:
    player_choice_input(['Take a hunk of stale bread', 'Swig from the dark stout on the bar'])
    if player_choice == '1':
        action('You feel rejuvenated...')
        player.hp += 10
        action('%s recovers 10 hp [%s/%s]' % (player.name, player.hp, player.max_hp))
    elif player_choice == '2':
        action('The stout refreshes your parched mouth...')
        player.hp += 5
        action('%s recovers 5 hp [%s/%s]' % (player.name, player.hp, player.max_hp))
talk('Old Man', 'If you\'re planning on going back out there, I suggest you take one of these.')
action('The old man reaches behind the bar and takes out a shortsword and a worn mages\' staff')
while player_inventory.weapon == hands:
    player_choice_input(['Take the shortsword', 'Take the staff', 'Check your stats'])
    if player_choice == '1':
        player_inventory.weapon = shortsword
    elif player_choice == '2':
        player_inventory.weapon = worn_staff
    elif player_choice == '3':
        playerstats()
talk('Old Man', '"Be wary outside this inn..."')
talk('Old Man', '"At this time of night, there are some terrible monsters lurking in these woods."')
while Location == 'The Inn':
    player_choice_input(['Check your stats', 'Check your inventory', 'Check your bag', 'Leave the inn'])
    if player_choice == '1':
        playerstats()
    elif player_choice == '2':
        playerinventory()
    elif player_choice == '3':
        player_bag_check()
    elif player_choice == '4':
        action('You leave the inn.')
        Location = 'The_Forest'
action('You walk out, down the snow-strewn path towards the forest.')
action('A rustling in the distance catches your attention.')
battle(zombie, player, 'lurches onto the path')
action('You hear something else...')
battle(zombie, player, 'staggers towards you')
action('Not another one!')
battle(zombie, player, 'looms forward out of the darkness')
