# Hi, this is Zichun from Singapore/China. Nice to meet you.

# import necessary modules
import simplegui
import random

# initializes desired range as a global variable, default range is 0-100
desired_range = 100

# helper function to start and restart the game
def new_game():
    global secret_number
    global remaining_guesses
    print ""
    print "New game. Range is from 0 to", desired_range
    
    secret_number = random.randrange(0,desired_range)
    
    if desired_range == 100 :
        remaining_guesses = 7
    elif desired_range == 1000 :
        remaining_guesses = 10
        
    print "Number of remaining guesses is", remaining_guesses

# define event handlers for control panel
def range100():
    global desired_range
    desired_range = 100
    new_game()

def range1000():   
    global desired_range
    desired_range = 1000
    new_game()
    
def input_guess(guess):
    global remaining_guesses
    print ""
    print "Guess was", guess
# conver string to integer    
    number_guess = int(guess)
    
    if number_guess > secret_number :
        print "Lower!"
        remaining_guesses = remaining_guesses - 1
        print "The number of remaining guesses is", remaining_guesses
    elif number_guess < secret_number :
        print "Higher!"
        remaining_guesses = remaining_guesses - 1
        print "The number of remaining guesses is", remaining_guesses
    elif number_guess == secret_number :
        print "Correct!"
        print ""
        new_game()
    else :
        print "Please check your input number"

# if player run out gusses, new game will start.
    if remaining_guesses == 0 :
        print "You ran out of gusses.", "The number is", secret_number
        print ""
        new_game()
        
# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range: 0 - 100', range100, 200)
frame.add_button('Range: 0 - 1000', range1000, 200)
frame.add_input('Enter a gusses', input_guess, 200)

# call new_game 
new_game()
