# Mini-project #6 - Blackjack

import simplegui, random, math, time

CANVAS = 600, 600

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

CARD_GAP = CARD_SIZE[0] + 12

HEADING_SIZE = 48
LABEL_SIZE = 36
MSG_SIZE = LABEL_SIZE * 4 / 5

vert_space = (CANVAS[1] - CARD_SIZE[1]*3 - HEADING_SIZE - LABEL_SIZE*2) / 6

HEADING_POS = 100, vert_space + HEADING_SIZE

DEALER_LABEL = 100, HEADING_POS[1] + LABEL_SIZE + vert_space
DEALER_POS = 100, DEALER_LABEL[1] + vert_space/2

PLAYER_LABEL = 100, DEALER_POS[1] + CARD_SIZE[1] + LABEL_SIZE + vert_space
PLAYER_POS = 100, PLAYER_LABEL[1] + vert_space/2

DISP_POS = (CANVAS[0] - CARD_SIZE[0] - 10,
            CANVAS[1] - CARD_SIZE[1] - vert_space)
DECK_POS = 10, DISP_POS[1], DISP_POS[0]-CARD_SIZE[0]-10

# define globals for cards
SUITS = 'CSHD'
RANKS = 'A23456789TJQK'
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# initialize some useful global variables
deck = None
player = None
dealer = None
discard = None

game_state = None
back_pick = int(random.random() >= 0.5)+1

score = 0
message = None


image_handle_cache = {}

class ImageHandle:
    CENTER = (0.5, 0.5)
    TOPLEFT = (0, 0)
    
    def __init__(self, image, posn, size):
        self.image = image
        self.posn = posn
        self.size = size
    
    def get_size(self):
        return self.size
    
    def draw(self, canvas, posn, size, anchor = CENTER):
        posn = (size[0] * (0.5-anchor[0]) + posn[0],
                size[1] * (0.5-anchor[1]) + posn[1])
        canvas.draw_image(self.image, self.posn,
                          self.size, posn, size)

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
        self.image = [None, None, None]

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def get_image(self, back):
        # return image if already known
        if self.image[back] is not None:
            return self.image[back]
        # return from image cache if present
        if not back:
            name = str(self)
        else:
            name = 'bk%d' % back
        if name in image_handle_cache:
            self.image[back] = image = image_handle_cache[name]
            return image
        # create new image, cache, and return
        if not back:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            image = ImageHandle(card_images, card_loc, CARD_SIZE)
        else:
            card_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0] * (back-1),
                        CARD_BACK_CENTER[1])
            image = ImageHandle(card_back, card_loc, CARD_BACK_SIZE)
        image_handle_cache[name] = self.image[back] = image
        return image
    
    def get_size(self):
        return CARD_SIZE
    
    def draw(self, canvas, pos, back = 0, anchor = ImageHandle.TOPLEFT):
        self.get_image(back).draw(canvas, pos, CARD_SIZE, anchor)

# card container class
class Cards:
    def __init__(self, cards = None):
        self.cards = list(cards) if cards else list()
    
    def __str__(self):
        return ', '.join(str(e) for e in self.cards)
    
    def add_cards(self, cards):
        self.cards.extend(cards)
    
    def take_cards(self, number = None):
        if number is None:
            number = len(self.cards)
        else:
            number = min(number, len(self.cards))
        cards = self.cards[:number]
        self.cards = self.cards[number:]
        return cards

# define hand class
class Hand(Cards):
    def __str__(self):
        return 'Hand(%s)=%d' % (
                Cards.__str__(self), self.get_value())
    
    def _get_card_value(self, card):
        rank = card.get_rank()
        return VALUES[rank], rank == 'A'
    
    def _calc_hand_value(self):
        value = 0; aces = 0
        for e in self.cards:
            r, a = self._get_card_value(e)
            value += r; aces += a
        return value, aces
    
    def get_value(self):
        value, aces = self._calc_hand_value()
        if value <= 11 and aces:
            return value + 10
        else:
            return value
    
    def is_blackjack(self):
        if len(self.cards) == 2:
            pict = False; aces = False
            for e in self.cards:
                rank = e.get_rank()
                if rank in ('J', 'K', 'Q'):
                    pict = True
                elif rank == 'A':
                    aces = True
            return pict and aces
        else:
            return False
    
    def _show_face(self, idx):
        return 0
    
    def CardTarget(index, pos, delta = CARD_GAP):
        return pos[0] + delta * index, pos[1]
    
    def draw(self, canvas, pos, delta = CARD_GAP):
        gap = min(delta, (CANVAS[0] - CARD_SIZE[0] - 200) / max(1, len(self.cards)-1))
        klass = type(self)
        for n,e in enumerate(self.cards):
            e.draw(canvas, klass.CardTarget(n, pos, gap),
                    self._show_face(n))

class Dealer(Hand):
    def set_hidden(self, hidden):
        self.hidden = hidden
    
    def _show_face(self, idx):
        return 0 if idx >= self.hidden else back_pick

# define deck class 
class Deck(Cards):
    def __init__(self, cards = None):
        Cards.__init__(self, cards or type(self).Build())
        self.deck_size = len(self.cards)
    
    def Build():
        return [Card(s,r) for r in RANKS for s in SUITS]
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_card(self):
        return self.cards.pop() if len(self.cards) else None
    
    def snap_deck_size(self):
        self.deck_size = len(self.cards)
    
    def __str__(self):
        return '[%s]' % ', '.join(str(e) for e in self.cards)
    
    def MapOffs(count):
        x1, y, x2 = DECK_POS
        dx = float(x2 - x1 - CARD_SIZE[0]) / count
        return tuple((int(n*dx+x1), int(y))
                for n in range(count))
    
    def draw(self, canvas):
        for e,p in zip(self.cards,
                type(self).MapOffs(self.deck_size)):
            e.draw(canvas, p, back_pick)

# define deck class 
class Discard(Cards):
    def __init__(self, cards = None):
        Cards.__init__(self, None)
        self.animating = set(cards or ())
    
    def add_cards(self, cards):
        for card in cards:
            assert isinstance(card, Animate)
            self.animating.add(card)
    
    def take_cards(self, number = None):
        if number is None:
            number = len(self.cards) + len(self.animating)
        # take cards from the discard pile
        take = min(number, len(self.cards))
        cards = self.cards[:take]
        self.cards = self.cards[take:]
        if take == number:
            return cards
        # take cards still being animated
        anis = tuple(self.animating)
        take = min(number - take, len(anis))
        cards.extend(anis[:take])
        for card in anis[:take]:
            self.animating.remove(card)
        return cards
    
    def draw(self, canvas, posn):
        stop = (posn[0] + CARD_SIZE[0] - 1,
                posn[1] + CARD_SIZE[1] - 1)
        canvas.draw_polyline(((posn[0], posn[1]), (stop[0], posn[1]),
                (stop[0], stop[1]), (posn[0], stop[1]), (posn[0], posn[1])),
                3, 'DarkCyan')
        
        if self.cards:
            self.cards[-1].draw(canvas, posn, None)
        
        for e in tuple(self.animating):
            e.draw(canvas, posn, None)
            if not e.is_animating():
                self.animating.remove(e)
                self.cards.append(e)

# define animation class
class Animate:
    running = set()
    resume = None
    
    def __init__(self, card, pos, scale, face):
        pos = tuple(pos)
        
        self.card = card
        self.to_pos = self.pos = pos
        self.to_scale = self.scale = scale
        
        self.back_face = self.to_face = self.face = face
        self.to_spin = self.spin = 1 if face else 0
        
        self.delay = 0
    
    def __str__(self):
        return str(self.card)
    
    def PauseState(resume = None):
        global game_state
        Animate.resume = resume or game_state
        assert Animate.resume
        game_state = None
    
    def NextState(resume = None):
        global game_state
        if Animate.running:
            Animate.PauseState(resume)
        else:
            game_state = resume
            resume.resume()
    
    def get_suit(self):
        return self.card.get_suit()
    
    def get_rank(self):
        return self.card.get_rank()
    
    def is_animating(self):
        return self.delay > 0
    
    def CardTarget(*args):
        return type(self.card).CardTarget(*args)
    
    def target(self, delay, pos, scale, face):
        self.to_pos = pos
        self.to_scale = scale
        self.to_face = face
        
        self.step_pos = (self.pos[0] - pos[0],
                         self.pos[1] - pos[1])
        self.step_scale = self.scale - scale
        
        if (not self.face) == (not face):
            self.to_spin = int(math.floor(self.spin))
        else:
            self.to_spin += 1
        self.step_spin = self.spin - self.to_spin
        
        self.start = time.time()
        self.delay = delay
        Animate.running.add(self)
    
    def draw(self, canvas, pos, face):
        pos = int(pos[0]), int(pos[1])
        if face is None: face = self.to_face
        if pos != self.to_pos or face != self.to_face:
            self.target(1, pos, 1.0, face)
        
        if self.delay:
            step = 1 - (time.time() - self.start) / self.delay
            if step <= 0:
                self.delay = step = 0
                Animate.running.remove(self)
                if Animate.resume and not len(Animate.running):
                    global game_state
                    game_state = Animate.resume
                    Animate.resume = None
                    game_state.resume()
            
            self.pos = pos = (self.step_pos[0] * step + self.to_pos[0],
                              self.step_pos[1] * step + self.to_pos[1])
            self.scale = scale = self.step_scale * step + self.to_scale
            self.spin = spin = self.step_spin * step + self.to_spin
            if int(round(spin)) % 2:
                face = self.face = self.back_face
            else:
                self.back_face = face
                face = self.face = 0
            spin = abs(math.cos(math.pi * spin))
        else:
            spin = 1
        
        klass = type(self.card)
        scale = self.scale * spin
        if scale > 0.0:
            size = self.card.get_size()
            self.card.get_image(face).draw(canvas, pos,
                    (size[0] * scale, size[1] * self.scale),
                    ImageHandle.TOPLEFT)

#define event handlers for buttons

class GameStates:
    def action(self, action):
        pass
    
    def resume(self):
        pass
    
    def draw(self, canvas):
        pass

class ResetState(GameStates):
    def __init__(self, redeal):
        if redeal is None:
            self.redeal = len(deck.cards) <= 18
        else:
            self.redeal = redeal
    
    def draw(self, canvas):
        # collect all cards in discard pile
        if len(dealer.cards):
            discard.add_cards(dealer.take_cards())
            Animate.PauseState()
        
        elif len(player.cards):
            discard.add_cards(player.take_cards())
            Animate.PauseState()
        
        else:
            Animate.NextState(ShuffleState()
                    if self.redeal else RedealState())
            dealer.set_hidden(2)

class ShuffleState(GameStates):
    def draw(self, canvas):
        global back_pick, message
        
        if len(deck.cards):
            discard.add_cards(deck.take_cards())
            Animate.PauseState()
            return
        
        # shuffle cards to deck
        cards = discard.take_cards()
        random.shuffle(cards)
        deck.add_cards(cards)
        
        # switch card back style
        back_pick = int(back_pick == 1)+1
        for e in deck.cards:
            e.back_face = e.to_face = e.face = back_pick
            e.spin = e.to_spin = 1; e.step_spin = 0
        
        message = None
        Animate.PauseState(RedealState())

class RedealState(GameStates):
    def draw(self, canvas):
        if len(dealer.cards) < 2:
            dealer.add_cards((deck.deal_card(),))
            Animate.PauseState(self)
        elif len(player.cards) < 2:
            player.add_cards((deck.deal_card(),))
            Animate.PauseState(self)
        else:
            dealer.set_hidden(1)
            Animate.PauseState(PlayerState())

class PlayerState(GameStates):
    def resume(self):
        global message
        
        if player.get_value() > 21:
            Animate.NextState(DealerState())
        
        message = (("'Hit'", 'Yellow'),
                   (" or ", 'Cyan'),
                   ("'Stand'", 'Yellow'),
                   ("?", 'Cyan'))
    
    def action(self, action):
        global message, score
        
        if action == 'hit':
            message = None
            player.add_cards((deck.deal_card(),))
            Animate.PauseState()
        
        elif action == 'stand':
            message = None
            Animate.NextState(DealerState())
        
        elif action == 'deal':
            message = (("!!! ", 'Orange'),
                       ("Abandoned Hand", 'Red'),
                       (" !!!", 'Orange'))
            score -= 1
            Animate.NextState(ResetState(True))

class DealerState(GameStates):
    def draw(self, canvas):
        if dealer.hidden:
            dealer.set_hidden(0)
            Animate.PauseState(ScoreState() \
                    if player.get_value() > 21 else None)
        
        elif dealer.get_value() < 17:
            dealer.add_cards((deck.deal_card(),))
            Animate.PauseState()
        
        else:
            Animate.NextState(ScoreState())

class ScoreState(GameStates):
    def __init__(self):
        global score
        
        self.dealer_pos = CANVAS[0]/2, DEALER_LABEL[1]
        self.player_pos = CANVAS[0]/2, PLAYER_LABEL[1]
    
        self.dealer_value = dealer.get_value()
        if self.dealer_value > 21:
            self.dealer_bust = self.dealer_value
            self.dealer_value = -1
        elif dealer.is_blackjack():
            self.dealer_value = 22
        
        self.player_value = player.get_value()
        if self.player_value > 21:
            self.player_bust = self.player_value
            self.player_value = -1
        elif player.is_blackjack():
            self.player_value = 22
        
        if self.player_value > self.dealer_value:
            score += 1
        else:
            score -= 1
        
        deck.snap_deck_size()
    
    def draw(self, canvas):
        global message
        
        if self.dealer_value == -1:
            canvas.draw_text("%d - *** BUST ***" % self.dealer_bust,
                    self.dealer_pos, MSG_SIZE, 'Red', 'serif')
        elif self.dealer_value == 22:
            canvas.draw_text("!!! BLACKJACK !!!",
                    self.dealer_pos, MSG_SIZE, 'Orange', 'serif')
        elif self.dealer_value > self.player_value:
            canvas.draw_text("%d - !!! WINS !!!" % self.dealer_value,
                    self.dealer_pos, MSG_SIZE, 'Yellow', 'serif')
        elif self.dealer_value == self.player_value:
            canvas.draw_text("%d - !!! DRAWS !!!" % self.dealer_value,
                    self.dealer_pos, MSG_SIZE, 'Yellow', 'serif')
        else:
            canvas.draw_text("%d Points" % self.dealer_value,
                    self.dealer_pos, MSG_SIZE, 'Cyan', 'serif')
        
        if self.player_value == -1:
            canvas.draw_text("%d - *** BUST ***" % self.player_bust,
                    self.player_pos, MSG_SIZE, 'Red', 'serif')
        elif self.player_value == 22:
            canvas.draw_text("!!! BLACKJACK !!!",
                    self.player_pos, MSG_SIZE, 'Orange', 'serif')
        elif self.dealer_value < self.player_value:
            canvas.draw_text("%d - !!! WINS !!!" % self.player_value,
                    self.player_pos, MSG_SIZE, 'Yellow', 'serif')
        else:
            canvas.draw_text("%d Points" % self.player_value,
                    self.player_pos, MSG_SIZE, 'Cyan', 'serif')
        
        canvas.draw_text('Score: %d' % score,
                (CANVAS[0]*3/4-2, HEADING_POS[1]-2),
                MSG_SIZE, 'Yellow', 'serif')
        
        message = (("Click ", 'Cyan'),
                   ("'Deal'", 'Yellow'),
                   (" to play again.", 'Cyan'))
    
    def action(self, action):
        if action == 'deal':
            global message
            message = None
            Animate.NextState(ResetState(None))

# button press handlers

def deal():
    if game_state:
        game_state.action('deal')

def hit():
    if game_state:
        game_state.action('hit')

def stand():
    if game_state:
        game_state.action('stand')

# draw handler

def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text('Blackjack',
            (HEADING_POS[0]+2, HEADING_POS[1]+2),
            HEADING_SIZE, 'Black', 'sans-serif')
    canvas.draw_text('Blackjack', HEADING_POS,
            HEADING_SIZE, 'Cyan', 'sans-serif')
    
    canvas.draw_text('Score: %d' % score,
            (CANVAS[0]*3/4, HEADING_POS[1]),
            MSG_SIZE, 'Black', 'serif')
    
    canvas.draw_text('Dealer', DEALER_LABEL, LABEL_SIZE, 'DarkCyan', 'serif')
    dealer.draw(canvas, DEALER_POS)
    
    canvas.draw_text('Player', PLAYER_LABEL, LABEL_SIZE, 'DarkCyan', 'serif')
    player.draw(canvas, PLAYER_POS)
    
    discard.draw(canvas, DISP_POS)
    
    deck.draw(canvas)
    
    if message:
        text = ''.join(e[0] for e in message)
        width = frame.get_canvas_textwidth(text, MSG_SIZE, 'serif')
        pos = [DECK_POS[0] + (DECK_POS[2] - DECK_POS[0] - width) / 2,
               DECK_POS[1] + MSG_SIZE + (CARD_SIZE[1] - MSG_SIZE) / 2]
        canvas.draw_polygon(((-10, pos[1]-MSG_SIZE-8), (CANVAS[0]+10, pos[1]-MSG_SIZE-8),
                (CANVAS[0]+10, pos[1]+16), (-10, pos[1]+16)), 5, 'Silver', 'Black')
        canvas.draw_line((-10, pos[1]-MSG_SIZE-8), (CANVAS[0]+10, pos[1]-MSG_SIZE-8), 3, 'White')
        canvas.draw_line((CANVAS[0]+10, pos[1]+16), (-10, pos[1]+16), 3, 'White')
        for text,clr in message:
            canvas.draw_text(text, pos, MSG_SIZE, clr, 'serif')
            pos[0] += frame.get_canvas_textwidth(text, MSG_SIZE, 'serif')
    
    if game_state:
        game_state.draw(canvas)
    elif not Animate.running and Animate.resume:
        print 'Failure to resume:', Animate.resume
        Animate.resume = None

def setup():
    global deck, discard, player, dealer
    
    cards = Deck.Build()
    random.shuffle(cards)
    xd = (CANVAS[0] - CARD_SIZE[0] - 10) / float(len(cards))
    deck = Deck(tuple(Animate(cards[n], (p[0], -CARD_SIZE[1]), 1.0, back_pick)
               for n,p in enumerate(Deck.MapOffs(len(cards)))))
    
    discard = Discard()
    player = Hand()
    dealer = Dealer()
    
    dealer.set_hidden(2)
    Animate.PauseState(RedealState())

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS[0], CANVAS[1])
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
setup()
frame.start()
