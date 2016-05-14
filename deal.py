import random
from deck_constants import suits, values

def generate_deck():
    deck = []
    for s in suits:
        for v in values:
            deck.append(v+s)
    shuffled_deck = random.sample(deck,52)
    return shuffled_deck

def deal_preflop(deck, num_players):
    hands = []
    for i in range(num_players):
        hands.append([deck.pop(),deck.pop()])
    return hands

def deal_flop(deck):
    # statistically burn card is insignificant
    return [deck.pop(),deck.pop(),deck.pop()]

def deal_turn(deck, board):
    if len(board) != 3:
        raise ValueError
    return board + [deck.pop()]

def deal_river(deck, board):
    if len(board) != 4:
        raise ValueError
    return board + [deck.pop()]
