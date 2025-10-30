import copy
import random
import pygame

pygame.init()
#game variables

cards = ['2', '3', '4', '5','6','7', '8','9','10','J','Q','K','A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)




WIDTH = 900
HEIGHT = 900

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
#win/loss/tie
records = {'wins':0, 'losses':0, 'ties':0}
player_score = 0
dealer_score = 0
random_activities = ['Do a shot', 'finish your beer','Take a sip', 'Give 2 sips', 'Make a rule']  
#reset game variables
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
double_or_nothing = False 
pussy = False
end_game = False

#deal cards function
def deal_cards(hand, deck):
    card_index = random.randint(0, len(deck) - 1)  # correct index
    card = deck.pop(card_index)                    # pop returns the card
    hand.append(card)
    return hand, deck


#DRAW SCORES for player an dealer
def draw_scores(player, dealer):
    screen.blit(font.render(f"Score: {player}", True, 'white'), (600, 500))
    if reveal_dealer:
        screen.blit(smaller_font.render(f"Dealer Score: {dealer}", True, 'white'), (600, 300))


#draw cards on screen function
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70+(70*i), 460 +(5*i),120,220],0,5)
        screen.blit(font.render(player[i], True, 'black'), (75+(70*i), 465 +(5*i)))
        screen.blit(font.render(player[i], True, 'black'), (75+(70*i), 635 +(5*i)))
        pygame.draw.rect(screen, 'green', [70+(70*i), 460 +(5*i),120,220],5,5)


    #if player hasn't finished turn, dealer will hide one card
    

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70+(70*i), 160 +(5*i),120,220],0,5)
        if i!=0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75+(70*i), 165 +(5*i)))
            screen.blit(font.render(dealer[i], True, 'black'), (75+(70*i), 335 +(5*i)))
        else:
            screen.blit(font.render('???', True, 'black'), (75+(70*i), 165 +(5*i)))
            screen.blit(font.render('???', True, 'black'), (75+(70*i), 335 +(5*i)))
        pygame.draw.rect(screen, 'blue', [70+(70*i), 160 +(5*i),120,220],5,5)

#draw(tekenen niet gelijk) game conditions and buttons
def draw_game(act, records):
    button_list = []
    #initially on startup(notn active)only action to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100],0,5)
        pygame.draw.rect(screen, 'black', [150, 20, 300, 100],3,5)
        deal_text = font.render('DEAL HAND', True, 'green')
        screen.blit(deal_text, (165,50))
        button_list.append( deal)
    #once game started show hit and stand buttons and win*loss 
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100],0,5)
        pygame.draw.rect(screen, 'black', [0, 700, 300, 100],3,5)
        hit_text = font.render('HIT', True, 'green')
        screen.blit(hit_text, (100,735))
        button_list.append( hit)

        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100],0,5)
        pygame.draw.rect(screen, 'black', [300, 700, 300, 100],3,5)
        stand_text = font.render('STAND', True, 'green')
        screen.blit(stand_text, (355,735))
        button_list.append( stand)

        score_text = smaller_font.render(f"Wins: {records['wins']}  Losses: {records['losses']}  Draws: {records['ties']}", True, 'white')
        screen.blit(score_text, (20, 820))
    
    return button_list
        
def draw_double_or_nothing():
    # Container rectangle (wider, shorter, at very top)
    pygame.draw.rect(screen, 'white', [50, 10, 500, 250], 0, 5)
    pygame.draw.rect(screen, 'red', [50, 10, 500, 250], 3, 5)

    # Title text (centered)
    double_text = smaller_font.render('DOUBLE OR NOTHING', True, 'black')
    screen.blit(double_text, (150, 30))

    # "I accept" button (left side)
    accept_button = pygame.draw.rect(screen, 'white', [80, 120, 200, 100], 0, 5)
    pygame.draw.rect(screen, 'green', [80, 120, 200, 100], 3, 5)
    accept_text = smaller_font.render('I ACCEPT', True, 'black')
    screen.blit(accept_text, (105, 155))

    # "I am a pussy" button (right side)
    decline_button = pygame.draw.rect(screen, 'white', [320, 120, 150, 100], 0, 5)
    pygame.draw.rect(screen, 'red', [320, 120, 150, 100], 3, 5)
    decline_text = smaller_font.render('PUSSY', True, 'black')
    screen.blit(decline_text, (330, 155))

    return accept_button, decline_button

    
    
def draw_next_round():
    next_round = pygame.draw.rect(screen, 'white', [150, 20, 350, 100],0,5)
    pygame.draw.rect(screen, 'black', [150, 20, 350, 100],3,5)
    next_text = font.render('NEXT ROUND', True, 'green')
    screen.blit(next_text, (165,50))
    return next_round



def reset_game():
    global game_deck, my_hand, dealer_hand, initial_deal, reveal_dealer, outcome, hand_active, double_or_nothing, pussy, active
    game_deck = copy.deepcopy(decks * one_deck)
    initial_deal = False # Changed to True to start new round
    my_hand = []
    dealer_hand = []
    outcome = 0
    reveal_dealer = False
    hand_active = False
    double_or_nothing = False 
    pussy = False
    active = False  # Reset to show "DEAL HAND" button
    







#pass in dealer or player hand and calculate (best)score
def calculate_score(hand):
    #calculate score every time and check number of aces
    hand_score = 0
    ace_count = hand.count('A')
    for i in range(len(hand)):
        if hand[i] in ['J','Q','K']:
            hand_score += 10
        #check by adding 11, we can reduce later if bust
        elif hand[i] == 'A':
            hand_score += 11
        else:
            hand_score += int(hand[i])
    #reduce ace value from 11 to 1 if bust
    if hand_score > 21 and ace_count > 0:
        for i in range(ace_count):
            if hand_score > 21: #or do a break so once under 21 it stops
                hand_score -= 10
    return hand_score
        
#main game loop

run = True
while run:
    #run game at set fps and fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    #initial deal to player and dealer
    if initial_deal:
        for _ in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
        hand_active = True
        active = True
    #if game is active and dealt
    if active and not double_or_nothing:
        player_score = calculate_score(my_hand)
        dealer_score = calculate_score(dealer_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)  
        draw_scores(player_score, dealer_score)    #nhas if for reveal dealer score 
        if outcome != 0:
            if outcome == 1:
                outcome_text = font.render('You Win!', True, 'green')
                next_round = draw_next_round()
            elif outcome == -1:
                outcome_text = font.render('Dealer Wins!', True, 'red')
                draw_double_or_nothing()
            else:
                outcome_text = font.render('Tie!', True, 'yellow')
                next_round = draw_next_round()
            screen.blit(outcome_text, (600, 600))
    if double_or_nothing and not pussy:
            activity_text = smaller_font.render(f'You must: {activity}', True, 'pink')
            screen.blit(activity_text, (50, 550))
            next_round = draw_next_round()
    if pussy:
            pussy_text = smaller_font.render('You chickened out! Next round.', True, 'pink')
            screen.blit(pussy_text, (100, 450))
            next_round = draw_next_round()
    
    buttons = draw_game(active, records)

    #event handler, if quit pressed exit game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not active:
                if buttons[0].collidepoint(event.pos): #dictionaries for buttons? could make the code easier to read?
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
            else: #so if active
                #hit button
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    player_score = calculate_score(my_hand)
                    if player_score > 21:
                        outcome = -1  #dealer win
                        records['losses'] += 1
                        hand_active = False
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer or player_score <=21 and hand_active:
                    reveal_dealer = True
                    hand_active = False
                    #dealer draws until 17 or higher
                    while dealer_score < 17:
                        dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
                        dealer_score = calculate_score(dealer_hand)
                    if dealer_score > 21 :
                        outcome = 1  #player win
                        records['wins'] += 1
                        
                    elif dealer_score > player_score :
                        outcome = -1 #dealer win

                        records['losses'] += 1
                    elif dealer_score < player_score :
                        outcome = 1  #player win
                        records['wins'] += 1
                    else:
                        outcome = 0  #tie
                        records['ties'] += 1
                   
                        
                #double or nothing buttons
                elif outcome == -1:
                    accept_button, decline_button = draw_double_or_nothing()
                    next_round = draw_next_round()
                    if accept_button.collidepoint(event.pos):
                        double_or_nothing = True
                        records['wins'] += 1
                        records['losses'] -= 1
                        activity = random.choice(random_activities)
                    if next_round.collidepoint(event.pos):
                        reset_game()
                        
                        
                    elif decline_button.collidepoint(event.pos):
                        double_or_nothing = True
                        pussy = True
                        records['wins'] -= 1
                if 'next_round' in locals() and next_round.collidepoint(event.pos):
                    reset_game()
                        
            
                            
    pygame.display.flip()  
pygame.quit()