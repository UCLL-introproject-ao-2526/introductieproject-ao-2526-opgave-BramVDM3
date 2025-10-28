import copy
import random
import pygame

pygame.init()
#game variables

cards = ['2', '3', '4', '5','6','7', '8','9','10','J','Q','K','A']
one_deck = 4 * cards
decks = 4
game_deck = copy.deepcopy(decks * one_deck)




WIDTH = 600
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
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0

#deal cards function
def deal_cards(hand, deck):
    card_index = random.randint(0, len(deck) - 1)  # correct index
    card = deck.pop(card_index)                    # pop returns the card
    hand.append(card)
    print(hand, deck)
    return hand, deck


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
        print(my_hand, dealer_hand)
        initial_deal = False
            

    buttons = draw_game(active, records)
    #event handler, if quit pressed exit game 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    my_hand = []
                    dealer_hand = []
                    outcome = 0

            
    pygame.display.flip()  
pygame.quit()