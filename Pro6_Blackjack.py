# Hi, this is Zichun from Singapore/China.
# Thanks for your effort, have a nice day.

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player_win = 0
dealer_win = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        global hand_cards
        self.hand_cards = []
        
    def __str__(self):
        # return a string representation of a hand    
        hand_cards_string = ""
        for i in range(len(self.hand_cards)):
            hand_cards_string += self.hand_cards[i]
            hand_cards_string += " "
        return "Hand contains " + hand_cards_string 

    def add_card(self, card):
        # add a card object to a hand    
        self.hand_cards.append(str(card))

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        has_ace = False
        
        for card in self.hand_cards:
            hand_value += VALUES[card[1]]
            if card[1] == 'A':
                has_ace = True
      
        if has_ace == True and (hand_value + 10) <= 21:
            hand_value += 10 
        
        return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_seq = 0
        for card in self.hand_cards:
            card_seq += 1
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card[1]), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card[0]))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0] + (card_seq-1)*85, pos[1] + CARD_CENTER[1]], CARD_SIZE)             
              
# define deck class 
class Deck:
    def __init__(self):
        global deck
        deck = []
        for suit in SUITS:
            for rank in RANKS:
                deck.append(str(suit)+str(rank)) 

    def shuffle(self):
        # shuffle the deck
        random.shuffle(deck)

    def deal_card(self):
        # deal a card object from the deck
        card_dealed = Card(deck[-1][0],deck[-1][1])
        deck.pop(-1)
        return card_dealed
    
    def __str__(self):
        deck_string = ""
        for card in deck:
            deck_string += str(card)
            deck_string += " "
        return "Deck contains " + deck_string   

#define event handlers for buttons
def deal():
    global outcome, in_play, new_deck, dealer_hand, player_hand, score, player_win, dealer_win
    new_deck = Deck()
    new_deck.shuffle()
    dealer_hand = Hand()
    player_hand = Hand()
    
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    player_hand.add_card(new_deck.deal_card())
    dealer_hand.add_card(new_deck.deal_card())
    
    outcome = "Hit or Stand?"
    if in_play == True:
        outcome = "Dealer Win.  Hit or Stand?"
        score -= 1
        dealer_win += 1
        
    in_play = True

    
def hit():
    global outcome, in_play, score, player_win, dealer_win
    if dealer_hand.get_value() <= 21 and player_hand.get_value() <= 21 and in_play == True:
        player_hand.add_card(new_deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You busted and lose! New deal?"
            score -= 1
            dealer_win += 1
            in_play = False

            
def stand():
    global outcome, in_play, score, player_win, dealer_win
    if player_hand.get_value() > 21 and in_play == True:
        outcome = "You busted and lose! New deal?"
        score -= 1
        dealer_win += 1
        in_play = False
    else:
        while dealer_hand.get_value() < 17 and in_play == True :
            dealer_hand.add_card(new_deck.deal_card())  
   
    if dealer_hand.get_value() > 21 and in_play == True:
        outcome = "Dealer busted and you win! New deal?"
        score += 1
        player_win += 1
        in_play = False
    elif  dealer_hand.get_value() >= player_hand.get_value() and in_play == True:
        outcome = "You lose and Dealer win.  New deal?"
        score -= 1
        dealer_win += 1
        in_play = False
    elif dealer_hand.get_value() < player_hand.get_value() and in_play == True:
        outcome = "You win!    New deal?"
        score += 1
        player_win += 1
        in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', (200, 70), 50, 'Black','sans-serif')
    canvas.draw_text("Dealer", (10, 225), 25, 'Red','monospace')
    canvas.draw_text("Player", (10, 450), 25, 'Blue','monospace')
    canvas.draw_text("Score: " + str(score), (80, 150), 40, 'Yellow','monospace')
    canvas.draw_text("You    win: " + str(player_win), (360, 165), 27, 'Blue','monospace')
    canvas.draw_text("Dealer win: " + str(dealer_win), (360, 130), 27, 'Brown','monospace')
    player_hand.draw(canvas, [50,460])
    if in_play == False:
        dealer_hand.draw(canvas, [50,240])
    else:
        dealer_hand.draw(canvas, [50,240])
        card_back_loc = (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 240 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
    canvas.draw_text(outcome, (50, 400), 30, 'White')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
