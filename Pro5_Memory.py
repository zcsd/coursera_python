# Hi, this is Zichun from Singapore/China.
# Thanks for your effort, have a nice day!

import simplegui
import random

# helper function to initialize globals
def new_game():
    global cards,exposed,turns,state,card1,card2
    state = 0
    turns = 0
    label.set_text("Turns = 0")
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    # Model the deck of cards, concatenat two lists
    cards = range(0,8)
    cards.extend(range(0,8))
    random.shuffle(cards)
     
# define event handlers
def mouseclick(pos):
    global turns,exposed,state,card1,card2,cards
    # Determine which card is clicked
    card_clicked = pos[0]//50
    # Main game logic
    if exposed[card_clicked] == False:
        exposed[card_clicked] = True
        label.set_text("Turns = " + str(turns))
        if state == 0:
            state = 1
            card1 = card_clicked
        elif state == 1:
            state = 2
            card2 = card_clicked
        else:
            # Filp cards back if they are unpaired
            if cards[card1] != cards[card2]:
                exposed[card1] = False
                exposed[card2] = False
            state = 1
            card1 = card_clicked
        # Update turns after second card click
        if state == 1:
            turns += 1

# cards are logically 50x100 pixels in size    
def draw(canvas):
    count = 0
    # Iterate every card status to draw cards
    for face_up in exposed:
        count += 1
        if face_up == True:
            canvas.draw_polygon([(50*(count-1), 0), (50*count, 0), (50*count, 100), (50*(count-1), 100)], 2, 'Black', 'Black')
            canvas.draw_text(str(cards[count-1]), (15+50*(count-1), 65), 40, 'White')
        else:
            canvas.draw_polygon([(50*(count-1), 0), (50*count, 0), (50*count, 100), (50*(count-1), 100)], 2, 'Brown', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
