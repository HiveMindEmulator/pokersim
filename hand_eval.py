from deck_constants import suits, values, hands

def value_cmp(x,y):
    if values.index(x) > values.index(y):
        return 1
    elif values.index(x) < values.index(y):
        return -1
    else:
        return 0

def suit(hand):
    for card in hand:
        if not isinstance(card, str) or len(card) != 2 or card[1].upper() not in suits:
            raise ValueError
    return [card[1].upper() for card in hand]

def value(hand):
    for card in hand:
        if not isinstance(card, str) or len(card) != 2 or card[0].upper() not in values:
            raise ValueError
    return [card[0].upper() for card in hand]

def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)

def is_quads(hand):
    if len(hand) != 5:
        raise ValueError
    h = sorted(value(hand), key=lambda x: values.index(x))
    if h[1] != h[2] or h[3] != h[2]:
        return False
    if h[0] != h[2] and h[4] != h[2]:
        return False
    return True

def is_full(hand):
    if len(hand) != 5:
        raise ValueError
    h = value(hand)
    return len(set(h)) == 2 and not is_quads(hand)

def is_flush(hand):
    if len(hand) != 5:
        raise ValueError
    s = suit(hand)
    for i in range(1,5):
        if s[i] != s[0]:
            return False
    return True

def is_straight(hand):
    if len(hand) != 5:
        raise ValueError
    h = sorted(value(hand), key=lambda x: values.index(x))
    # special case for wheel
    if h == ['2','3','4','5','A']:
        return True
    for i in range(1,5):
        if values.index(h[i])-values.index(h[i-1]) != 1:
            return False
    return True

def is_trips(hand):
    if len(hand) != 5:
        raise ValueError
    h = sorted(value(hand), key=lambda x: values.index(x))
    if h[1] == h[2]:
        return h[0] == h[2] or h[3] == h[2]
    else:
        return h[3] == h[2] and h[4] == h[2]

def is_two_pair(hand):
    if len(hand) != 5:
        raise ValueError
    h = value(hand)
    return len(set(h)) == 3 and not is_trips(hand)

def is_pair(hand):
    if len(hand) != 5:
        raise ValueError
    h = value(hand)
    return len(set(h)) == 4

def hand_cmp(h1, h2):
    v1, hc1 = five_card_value(h1)
    v2, hc2 = five_card_value(h2)
    if v1 > v2:
        return 1
    elif v2 > v1:
        return -1
    else:
        return _high_card_cmp(hc1, hc2);

# recursively compare high cards (requires that list be sorted descending value-only)
# need to make sure to prioritize the paired cards...
def _high_card_cmp(h1,h2):
    if len(h1) < 1:
        return 0
    res = value_cmp(h1[0], h2[0])
    if res != 0:
        return res
    else:
        return _high_card_cmp(h1[1:], h2[1:])

# returns index of hand rank
# sets high_card_list to the list of values to compare for _high_card_cmp
def five_card_value(hand):
    if len(hand) != 5:
        raise ValueError
    res = 0
    value_list = sorted(value(hand), key=lambda x:values.index(x), reverse=True)
    high_card_list = value_list
    if is_straight_flush(hand):
        res = hands.index('STRAIGHT_FLUSH')
        if value_list == ['A','5','4','3','2']:
            high_card_list = ['5']
        else:
            high_card_list = [value_list[0]]
    elif is_quads(hand):
        res = hands.index('QUADS')
        if values.index(value_list[0]) != values.index(value_list[2]):
            high_card_list = [value_list[2], value_list[0]]
        else:
            high_card_list = [value_list[2], value_list[4]]
    elif is_full(hand):
        res = hands.index('FULL')
        if values.index(value_list[0]) != values.index(value_list[2]):
            high_card_list = [value_list[2], value_list[0]]
        else:
            high_card_list = [value_list[2], value_list[4]]
    elif is_flush(hand):
        res = hands.index('FLUSH')
        high_card_list = value_list
    elif is_straight(hand):
        res = hands.index('STRAIGHT')
        if value_list == ['A','5','4','3','2']:
            high_card_list = ['5']
        else:
            high_card_list = [value_list[0]]
    elif is_trips(hand):
        res = hands.index('TRIPS')
        kickers = [c for c in value_list if c != value_list[2]]
        high_card_list = [value_list[2]] + sorted(kickers, key=lambda x:values.index(x), reverse=True)
    elif is_two_pair(hand):
        res = hands.index('TWO_PAIR')
        pairs = [c for c in value_list if value_list.count(c) == 2]
        kickers = [c for c in value_list if value_list.count(c) == 1]
        high_card_list = [pairs[0], pairs[2]] + kickers
    elif is_pair(hand):
        res = hands.index('PAIR')
        pairs = [c for c in value_list if value_list.count(c) == 2]
        kickers = [c for c in value_list if value_list.count(c) == 1]
        high_card_list = [pairs[0]] + kickers
    return res, high_card_list

def best_five_holdem(hand):
    if len(hand) != 7:
        raise ValueError
    best = None
    for i in range(len(hand)):
        for j in range(i+1,len(hand)):
            curr = hand[:i] + hand[i+1:j] + hand[j+1:]
            if best == None or hand_cmp(curr, best) > 0:
                best = curr
    return best

def showdown(h1, h2, board):
    if len(h1) !=2 or len(h2) !=2 or len(board) != 5:
        raise ValueError
    return hand_cmp(best_five_holdem(h1+board),best_five_holdem(h2+board))

def hand_vs_hand(h1, h2, board):
    if len(h1) !=2 or len(h2) !=2 or len(board) > 5:
        raise ValueError
    return 0
    
