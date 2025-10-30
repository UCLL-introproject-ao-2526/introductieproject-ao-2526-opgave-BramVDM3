import copy
import random
import pygame

pygame.init()

# Constants
WIDTH = 900
HEIGHT = 900
FPS = 60

# Card setup
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4

# Initialize Pygame
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

# Game state variables
active = False
records = {'wins': 0, 'losses': 0, 'ties': 0}
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
double_or_nothing = False
pussy = False
game_deck = copy.deepcopy(decks * one_deck)

# Random activities
random_activities = ['Do a shot', 'Finish your beer', 'Take a sip', 'Give 2 sips', 'Make a rule']


# ===== FUNCTIONS =====

def deal_cards(hand, deck):
    """Deal a random card from the deck to a hand"""
    card_index = random.randint(0, len(deck) - 1)
    card = deck.pop(card_index)
    hand.append(card)
    return hand, deck


def calculate_score(hand):
    """Calculate the best score for a hand, accounting for aces"""
    hand_score = 0
    ace_count = hand.count('A')
    
    for card in hand:
        if card in ['J', 'Q', 'K']:
            hand_score += 10
        elif card == 'A':
            hand_score += 11
        else:
            hand_score += int(card)
    
    # Adjust aces from 11 to 1 if busting
    while hand_score > 21 and ace_count > 0:
        hand_score -= 10
        ace_count -= 1
    
    return hand_score


def draw_scores(player, dealer):
    """Draw player and dealer scores on screen"""
    screen.blit(font.render(f"Score: {player}", True, 'white'), (600, 500))
    if reveal_dealer:
        screen.blit(smaller_font.render(f"Dealer Score: {dealer}", True, 'white'), (600, 300))


def draw_cards(player, dealer, reveal):
    """Draw player and dealer cards on screen"""
    # Draw player cards
    for i in range(len(player)):
        x = 70 + (70 * i)
        y = 460 + (5 * i)
        pygame.draw.rect(screen, 'white', [x, y, 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (x + 5, y + 5))
        screen.blit(font.render(player[i], True, 'black'), (x + 5, y + 175))
        pygame.draw.rect(screen, 'green', [x, y, 120, 220], 5, 5)
    
    # Draw dealer cards
    for i in range(len(dealer)):
        x = 70 + (70 * i)
        y = 160 + (5 * i)
        pygame.draw.rect(screen, 'white', [x, y, 120, 220], 0, 5)
        
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (x + 5, y + 5))
            screen.blit(font.render(dealer[i], True, 'black'), (x + 5, y + 175))
        else:
            screen.blit(font.render('???', True, 'black'), (x + 5, y + 5))
            screen.blit(font.render('???', True, 'black'), (x + 5, y + 175))
        
        pygame.draw.rect(screen, 'blue', [x, y, 120, 220], 5, 5)


def draw_game(act, records):
    """Draw game buttons (deal, hit, stand) and score"""
    button_list = []
    
    if not act:
        # Deal hand button
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'black', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'green')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    else:
        # Hit button
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'black', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT', True, 'green')
        screen.blit(hit_text, (100, 735))
        button_list.append(hit)
        
        # Stand button
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'black', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'green')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        
        # Score display
        score_text = smaller_font.render(
            f"Wins: {records['wins']}  Losses: {records['losses']}  Draws: {records['ties']}", 
            True, 'white'
        )
        screen.blit(score_text, (20, 820))
    
    return button_list


def draw_double_or_nothing():
    """Draw double or nothing prompt with accept/decline buttons"""
    # Container
    pygame.draw.rect(screen, 'white', [50, 10, 500, 250], 0, 5)
    pygame.draw.rect(screen, 'red', [50, 10, 500, 250], 3, 5)
    
    # Title
    double_text = smaller_font.render('DOUBLE OR NOTHING', True, 'black')
    screen.blit(double_text, (150, 30))
    
    # Accept button
    accept_button = pygame.draw.rect(screen, 'white', [80, 120, 200, 100], 0, 5)
    pygame.draw.rect(screen, 'green', [80, 120, 200, 100], 3, 5)
    accept_text = smaller_font.render('I ACCEPT', True, 'black')
    screen.blit(accept_text, (105, 155))
    
    # Decline button
    decline_button = pygame.draw.rect(screen, 'white', [320, 120, 150, 100], 0, 5)
    pygame.draw.rect(screen, 'red', [320, 120, 150, 100], 3, 5)
    decline_text = smaller_font.render('PUSSY', True, 'black')
    screen.blit(decline_text, (330, 155))
    
    return accept_button, decline_button


def draw_next_round():
    """Draw next round button"""
    next_round = pygame.draw.rect(screen, 'white', [150, 20, 350, 100], 0, 5)
    pygame.draw.rect(screen, 'black', [150, 20, 350, 100], 3, 5)
    next_text = font.render('NEXT ROUND', True, 'green')
    screen.blit(next_text, (165, 50))
    return next_round


def reset_game():
    """Reset all game variables for a new round"""
    global game_deck, my_hand, dealer_hand, initial_deal, reveal_dealer, outcome
    global hand_active, double_or_nothing, pussy, active
    
    game_deck = copy.deepcopy(decks * one_deck)
    my_hand = []
    dealer_hand = []
    initial_deal = False
    reveal_dealer = False
    outcome = 0
    hand_active = False
    double_or_nothing = False
    pussy = False
    active = False


def handle_dealer_turn():
    """Handle dealer drawing cards until 17 or higher"""
    global dealer_hand, game_deck, dealer_score, outcome, records
    
    while dealer_score < 17:
        dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        dealer_score = calculate_score(dealer_hand)
    
    # Determine outcome
    if dealer_score > 21:
        outcome = 1  # Player wins
        records['wins'] += 1
    elif dealer_score > player_score:
        outcome = -1  # Dealer wins
        records['losses'] += 1
    elif dealer_score < player_score:
        outcome = 1  # Player wins
        records['wins'] += 1
    else:
        outcome = 0  # Tie
        records['ties'] += 1


# ===== MAIN GAME LOOP =====

run = True
while run:
    timer.tick(FPS)
    screen.fill('black')
    
    # Initial deal
    if initial_deal:
        for _ in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
        hand_active = True
        active = True
    
    # Draw active game
    if active and not double_or_nothing:
        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        draw_scores(player_score, dealer_score)
        
        # Show outcome
        if outcome != 0:
            if outcome == 1:
                outcome_text = font.render('You Win!', True, 'green')
                next_round = draw_next_round()
            elif outcome == -1:
                outcome_text = font.render('Dealer Wins!', True, 'red')
                draw_double_or_nothing()
            screen.blit(outcome_text, (600, 600))
        elif outcome == 0 and reveal_dealer:
            outcome_text = font.render('Tie!', True, 'yellow')
            screen.blit(outcome_text, (600, 600))
            next_round = draw_next_round()
    
    # Show double or nothing result
    if double_or_nothing and not pussy:
        activity_text = smaller_font.render(f'You must: {activity}', True, 'white')
        screen.blit(activity_text, (200, 400))
        next_round = draw_next_round()
    
    # Show pussy result
    if pussy:
        pussy_text = smaller_font.render('You chickened out!', True, 'white')
        screen.blit(pussy_text, (200, 400))
        next_round = draw_next_round()
    
    # Draw game buttons
    buttons = draw_game(active, records)
    
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Deal hand
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    outcome = 0
                    
            # Game active
            else:
                # Hit button
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    player_score = calculate_score(my_hand)
                    if player_score > 21:
                        outcome = -1
                        records['losses'] += 1
                        hand_active = False
                
                # Stand button
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer and hand_active:
                    reveal_dealer = True
                    hand_active = False
                    handle_dealer_turn()
                
                # Double or nothing buttons
                elif outcome == -1 and not double_or_nothing:
                    accept_button, decline_button = draw_double_or_nothing()
                    
                    if accept_button.collidepoint(event.pos):
                        double_or_nothing = True
                        records['wins'] += 1
                        records['losses'] -= 1
                        activity = random.choice(random_activities)
                    
                    elif decline_button.collidepoint(event.pos):
                        double_or_nothing = True
                        pussy = True
                        records['losses'] += 1
                elif player_score == 21 and not reveal_dealer and hand_active:
                    reveal_dealer = True
                    hand_active = False
                    handle_dealer_turn()
                
                # Next round button
                if 'next_round' in locals() and next_round.collidepoint(event.pos):
                    reset_game()
    
    pygame.display.flip()

pygame.quit()