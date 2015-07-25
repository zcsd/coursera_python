# Hi, this is Zichun from China/Singapore. Nice to meet you.

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def name_to_number(name):
    if name == "rock":
        player_number = 0
    elif name == "Spock":
        player_number = 1
    elif name == "paper":
        player_number = 2
    elif name == "lizard":
        player_number = 3
    elif name == "scissors":
        player_number = 4
    else:
        print "Your input does not match any of the five correct input strings."
    
    return player_number

def number_to_name(number):
    if number == 0:
        comp_choice = "rock"
    elif number == 1:
        comp_choice = "Spock"
    elif number == 2:
        comp_choice = "paper"
    elif number == 3:
        comp_choice = "lizard"
    elif number == 4:
        comp_choice = "scissors"
    else:
        print "Computer's random number is not in the correct range."
        
    return comp_choice

def rpsls(player_choice): 
    # print a blank line to separate consecutive games
    print ""
    # print out the message for the player's choice
    print "Player chooses", player_choice
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print "Computer chooses", comp_choice
    # compute difference of comp_number and player_number modulo five
    difference = comp_number - player_number
    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print "Player and computer tie!"
    elif difference == 1 or difference == 2 or difference == -3 or difference == -4:
        print "Computer wins!"
    elif difference == -1 or difference== -2 or difference == 3 or difference == 4:
        print "Player wins!"
    else:
        print "Why am I here?"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
