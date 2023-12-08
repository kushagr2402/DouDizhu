def card_check(c):
    if isinstance(c, int):
        return 2 <= c <= 10
    elif isinstance(c, str):
        return c in ['Jack', 'Queen', 'King', 'Ace', 'Black', 'Red']
    else:
        return False

def card_value(card):
    if isinstance(card, int):
        return 100 if card == 2 else card
    elif card == 'Jack':
        return 11
    elif card == 'Queen':
        return 12
    elif card == 'King':
        return 13
    elif card == 'Ace':
        return 14
    elif card == 'Black':
        return 200
    else:
        return 300

def card_equals(card1, card2):
    return card_value(card1) == card_value(card2)

def card_less_than(card1, card2):
    return card_value(card1) < card_value(card2)

def card_greater_than(card1, card2):
    return card_value(card1) > card_value(card2)

def card_less_than_or_equal(card1, card2):
    return card_value(card1) <= card_value(card2)

def card_greater_than_or_equal(card1, card2):
    return card_value(card1) >= card_value(card2)

def insert_card(card, hand):
    if not hand:
        return [card]
    elif card_less_than(card, hand[0]):
        return [card] + hand
    else:
        return [hand[0]] + insert_card(card, hand[1:])

def sort_cards(loc):
    if not loc:
        return []
    else:
        return insert_card(loc[0], sort_cards(loc[1:]))

def remove_one_of_each(hand):
    if not hand or len(hand) == 1:
        return []
    elif not card_equals(hand[0], hand[1]):
        return remove_one_of_each(hand[1:])
    else:
        return [hand[0]] + remove_one_of_each(hand[1:])

def remove_n_of_each(n, hand):
    if n == 0:
        return hand
    else:
        return remove_one_of_each(remove_n_of_each(n - 1, hand))

def dedup_hand(hand):
    if not hand or len(hand) == 1:
        return hand
    elif card_equals(hand[0], hand[1]):
        return dedup_hand(hand[1:])
    else:
        return [hand[0]] + dedup_hand(hand[1:])

def find_kind(n, hand):
    return dedup_hand(remove_n_of_each(n - 1, hand))

def make_solos(hand):
    if not hand:
        return []
    else:
        return [[hand[0]]] + make_solos(hand[1:])

def solos(hand):
    return make_solos(find_kind(1, hand))

def make_pairs(lst):
    if not lst:
        return []
    else:
        return [[lst[0], lst[0]]] + make_pairs(lst[1:])

def pairs(hand):
    return make_pairs(find_kind(2, hand))

def make_trios(lst):
    if not lst:
        return []
    else:
        return [[lst[0], lst[0], lst[0]]] + make_trios(lst[1:])

def trios(hand):
    return make_trios(find_kind(3, hand))

def rocket_check(hand):
    return len(hand) == 2 and card_equals(hand[0], 'Black') and card_equals(hand[1], 'Red')

def bomb_check(hand):
    return (len(hand) == 4 and card_equals(hand[0], hand[1]) and
            card_equals(hand[0], hand[2]) and card_equals(hand[0], hand[3]))

def hand_elementwise_less_than(a, b):
    if not a:
        return bool(b)
    elif not b:
        return False
    elif card_less_than(a[0], b[0]):
        return True
    elif card_greater_than(a[0], b[0]):
        return False
    else:
        return hand_elementwise_less_than(a[1:], b[1:])

def hand_less_than(a, b):
    if rocket_check(a):
        return False
    elif rocket_check(b):
        return True
    elif bomb_check(a) and bomb_check(b):
        return card_less_than(a[0], b[0])
    elif bomb_check(b):
        return True
    elif len(a) == len(b):
        return hand_elementwise_less_than(a, b)
    else:
        return len(a) < len(b)

def insert_hands(hand, hands):
    if not hands:
        return [hand]
    elif hand_less_than(hand, hands[0]):
        return [hand] + hands
    elif hand_less_than(hands[0], hand):
        return [hands[0]] + insert_hands(hand, hands[1:])
    else:
        return hands

def sort_hands(unsorted_hands):
    if not unsorted_hands:
        return []
    else:
        return insert_hands(unsorted_hands[0], sort_hands(unsorted_hands[1:]))

def card_follows(card1, card2):
    return card_value(card1) + 1 == card_value(card2)

def straight_check(hand):
    if not hand:
        return True
    elif card_value(hand[0]) > card_value('Ace'):
        return False
    elif len(hand) == 1:
        return True
    elif card_follows(hand[0], hand[1]):
        return straight_check(hand[1:])
    else:
        return False

def filter_straights(n, hands):
    if not hands:
        return []
    elif len(hands[0]) >= n and straight_check(hands[0]):
        return [hands[0]] + filter_straights(n, hands[1:])
    else:
        return filter_straights(n, hands[1:])

def first_n(n, lst):
    if n == 0 or not lst:
        return []
    else:
        return [lst[0]] + first_n(n - 1, lst[1:])

def prefixes_helper(n, lst):
    if n == 0 or not lst:
        return []
    else:
        return [first_n(n, lst)] + prefixes_helper(n - 1, lst)

def prefixes(lst):
    return prefixes_helper(len(lst), lst)

def subsequences(lst):
    if not lst:
        return []
    else:
        return prefixes(lst) + subsequences(lst[1:])

def straights_of_length(n, hand):
    return filter_straights(n, sort_hands(subsequences(dedup_hand(hand))))

def straights(hand):
    return straights_of_length(5, hand)

def double_hand(hand):
    if not hand:
        return []
    else:
        return [hand[0], hand[0]] + double_hand(hand[1:])

def double_hands(hands):
    if not hands:
        return []
    else:
        return [double_hand(hands[0])] + double_hands(hands[1:])

def straight_pairs(hand):
    return double_hands(straights_of_length(3, find_kind(2, hand)))

def triple_hand(hand):
    if not hand:
        return []
    else:
        return [hand[0], hand[0], hand[0]] + triple_hand(hand[1:])

def triple_hands(hands):
    if not hands:
        return []
    else:
        return [triple_hand(hands[0])] + triple_hands(hands[1:])

def airplanes(hand):
    return triple_hands(straights_of_length(2, find_kind(3, hand)))

def bombs(hand):
    if (not hand or len(hand) < 4):
        return []
    elif (hand[0] == hand[1] == hand[2] == hand[3]):
        return [[hand[0], hand[0], hand[0], hand[0]]] + bombs(hand[3:])
    else:
        return bombs(hand[1:])

def rockets(hand):
    if not hand or len(hand) < 2:
        return []
    elif hand[0] == 'Black' and hand[1] == 'Red':
        return [['Black', 'Red']]
    else:
        return rockets(hand[1:])

def beats_r(hand1, hand2):
    if not hand1 or not hand2:
        return False
    elif len(hand1) == 1 and len(hand2) == 1:
        return card_less_than(hand1[0], hand2[0])
    elif not hand1[1:] or not hand2[1:]:
        return False
    else:
        return (card_less_than(hand1[0], hand2[0]) and
                card_value(hand1[1]) - card_value(hand1[0]) ==
                card_value(hand2[1]) - card_value(hand2[0]) and
                beats_r(hand1[1:], hand2[1:]))

def beats(hand1, hand2):
    if not hand1:
        return bool(hand2)
    elif not hand2:
        return False
    elif rocket_check(hand1):
        return False
    elif rocket_check(hand2):
        return True
    elif bomb_check(hand2) and not bomb_check(hand1):
        return True
    elif bomb_check(hand1) and not bomb_check(hand2):
        return False
    else:
        return beats_r(hand1, hand2)

def all_hands(holding):
    return sort_hands(solos(holding) + straights(holding) +
                      pairs(holding) + straight_pairs(holding) +
                      trios(holding) + airplanes(holding) +
                      bombs(holding) + rockets(holding))

def filter_hands(previous, hands):
    if not hands:
        return []
    elif beats(previous, hands[0]):
        return [hands[0]] + filter_hands(previous, hands[1:])
    else:
        return filter_hands(previous, hands[1:])

def follow(previous, holding):
    return filter_hands(previous, all_hands(holding))

def both_passed(played):
    return played and not played[0] and len(played) > 1 and not played[1]

def goldfish(hand, role, played):
    return [hand[0]] if both_passed(played) else []

def hand_to_beat(played):
    if not played:
        return []
    elif played[0] or len(played) == 1:
        return played[0]
    else:
        return played[1]

def cautious(hand, role, played):
    could_play = follow(hand_to_beat(played), hand)
    return could_play[0] if could_play else []

def last(lst):
    return lst[-1] if lst else None

def reckless(hand, role, played):
    could_play = follow(hand_to_beat(played), hand)
    return last(could_play) if could_play else []

def studentO(holding, role, played):
    if both_passed(played):
        if airplanes(holding):
            return airplanes(holding)[0]
        if straights(holding):
            return straights(holding)[0]
        if straight_pairs(holding):
            return straight_pairs(holding)[0]
        if pairs(holding):
            return last(pairs(holding))
        if bombs(holding):
            return bombs(holding)[0]
        if trios(holding):
            return last(trios(holding))
        if rockets(holding):
            return rockets(holding)[0]
        return [holding[0]] if holding else []

    if role == 'Landlord':
        could_play = follow(hand_to_beat(played), holding)
        if not could_play:
            return []
        if straights(holding) and last(straights(holding)) in could_play:
            return last(straights(holding))
        if pairs(holding) and pairs(holding)[0] in could_play:
            return pairs(holding)[0]
        if bombs(holding) and last(bombs(holding)) in could_play:
            return last(bombs(holding))
        if trios(holding) and trios(holding)[0] in could_play:
            return trios(holding)[0]
        if airplanes(holding) and airplanes(holding)[0] in could_play:
            return airplanes(holding)[0]
        if straight_pairs(holding) and straight_pairs(holding)[0] in could_play:
            return straight_pairs(holding)[0]
        if rockets(holding) and rockets(holding)[0] in could_play:
            return rockets(holding)[0]
        return could_play[0]

    elif role == 'Right':
        could_play = follow(hand_to_beat(played), holding)
        if not could_play:
            return []
        if rockets(holding) and rockets(holding)[0] in could_play:
            return rockets(holding)[0]
        if bombs(holding) and bombs(holding)[0] in could_play:
            return bombs(holding)[0]
        return could_play[0]

    else:
        return reckless(holding, role, played)

########################################################################################################################################
def studentN1(hand, role, played):
    
    def is_endgame():
        return len(hand) <= 5

    def play_aggressively():
        return reckless(hand, role, played)

    could_play = follow(hand_to_beat(played), hand)

    if not could_play:
        return []

    if is_endgame():
        return play_aggressively()

    # Early or Mid-game Strategy
    if role in ['Right', 'Left']:  # When not a landlord, play more conservatively
        return could_play[0]  # Play the lowest possible card
    else:  # As a landlord, slightly more aggressive
        if len(could_play) > 1:
            return could_play[1]  # Play a card that's not the lowest
        return could_play[0]

########################################################################################################################################
def studentN2(hand, role, played):
    could_play = follow(hand_to_beat(played), hand)
    if not could_play:
        return []

    # Analyze the hand for bombs, rockets, and other combinations
    bombs_and_rockets = [h for h in could_play if bomb_check(h) or rocket_check(h)]
    other_hands = [h for h in could_play if not bomb_check(h) and not rocket_check(h)]

    # Strategy for Landlord
    if role == 'Landlord':
        if both_passed(played):
            # Play the weakest hand if both opponents passed
            return other_hands[0]
        elif bombs_and_rockets and len(hand) < 5:
            # Use bombs/rockets to finish the game or regain control
            return bombs_and_rockets[0]
        elif bombs_and_rockets:
            # Keep bombs and rockets for later unless necessary
            return other_hands[0] if other_hands else bombs_and_rockets[0]
        else:
            return other_hands[0]

    # Strategy for Peasants
    else:
        if bombs_and_rockets and len(hand) < 5:
            # Use bombs/rockets to finish the game or regain control
            return bombs_and_rockets[0]
        else:
            return other_hands[0] if other_hands else []

    return []

########################################################################################################################################
def student(hand, role, played):
    # Analyze hand composition
    hand_composition = {
        "solos": solos(hand),
        "pairs": pairs(hand),
        "trios": trios(hand),
        "straights": straights(hand),
        "straight_pairs": straight_pairs(hand),
        "airplanes": airplanes(hand),
        "bombs": bombs(hand),
        "rockets": rockets(hand)
    }

    # Get all possible hands to play
    could_play = follow(hand_to_beat(played), hand)

    # Check if both opponents have passed
    if both_passed(played):
        # Start with a weaker hand to bait out stronger cards
        return could_play[0] if could_play else []

    # Strategy varies based on the role
    if role == 'Landlord':
        # Play a hand based on the game state and hand composition
        return landlord_play(hand_composition, could_play, played)
    else:
        # Peasant strategy
        return peasant_play(hand_composition, could_play, played)

def count_hand_types(hand_composition):
    """Counts the number of each type of hand."""
    counts = {hand_type: len(hands) for hand_type, hands in hand_composition.items()}
    return counts

# def find_minimal_winning_hand(could_play, hand_counts):
#     """Finds the minimal hand that is likely to win based on the current game state."""
#     for hand in could_play:
#         # Example logic: prefer using hands with more remaining options
#         if hand_counts['solos'] > 1 and len(hand) == 1:
#             continue  # Prefer to keep solos if many are left
#         return hand
#     return could_play[0] if could_play else []

def find_minimal_winning_hand(could_play, hand_counts, hand_composition):
    """
    Finds a hand that is strong enough to likely win the round, but not overly strong to waste resources.
    Prioritizes using hands that are abundant or less likely to be needed later.
    """

    # If there's only one option or no options, return it
    if len(could_play) <= 1:
        return could_play[0] if could_play else []

    # Strategy: Use abundant hands or hands less valuable later in the game
    for hand in could_play:
        hand_type = identify_hand_type(hand, hand_composition)
        # Check if the hand type is abundant or less valuable
        if is_abundant_or_less_valuable(hand_type, hand_counts):
            return hand

    # If no suitable hand found, play the least powerful hand
    return could_play[0]

def identify_hand_type(hand, hand_composition):
    """Identifies the type of the hand (e.g., solo, pair, trio, straight, etc.)."""
    for hand_type, hands in hand_composition.items():
        if hand in hands:
            return hand_type
    return None

def is_abundant_or_less_valuable(hand_type, hand_counts):
    """Determines if a hand type is either abundant in the player's hand or generally less valuable."""
    # Define thresholds or criteria for abundant or less valuable hands
    abundant_threshold = 3  # Example threshold, can be adjusted
    less_valuable_types = ['solos', 'pairs']  # Example types, can be adjusted

    return hand_counts.get(hand_type, 0) >= abundant_threshold or hand_type in less_valuable_types

def peasant_play(hand_composition, could_play, played):
    hand_counts = count_hand_types(hand_composition)

    # Peasants can afford to be more aggressive with bombs/rockets
    if hand_counts['bombs'] > 0 or hand_counts['rockets'] > 0:
        return could_play[-1]  # play a strong hand to disrupt the landlord

    # Otherwise, focus on hand reduction
    return find_minimal_winning_hand(could_play, hand_counts, hand_composition )

# def landlord_play(hand_composition, could_play):
#     hand_counts = count_hand_types(hand_composition)

#     # If powerful cards (bombs/rockets) are available, consider using them if the hand is large
#     if hand_counts['bombs'] > 0 or hand_counts['rockets'] > 0:
#         if len(could_play[-1]) > 2:  # if the strongest hand is not a solo or pair
#             return could_play[-1]  # play a strong hand to regain control

#     # Otherwise, play the minimal winning hand
#     return find_minimal_winning_hand(could_play, hand_counts, hand_composition)

def landlord_play(hand_composition, could_play, played):
    hand_counts = count_hand_types(hand_composition)

    # Strategy to preserve bombs and rockets unless necessary to regain control
    if hand_counts['bombs'] > 0 or hand_counts['rockets'] > 0:
        # Use bombs/rockets if it's likely to regain control
        if should_use_power_hand(could_play, hand_composition, played):
            return could_play[-1]  # play a strong hand (likely a bomb or rocket)
    
    # If no bombs/rockets or not using them, find the minimal winning hand
    return find_minimal_winning_hand(could_play, hand_counts, hand_composition)

# def should_use_power_hand(could_play, hand_composition, played):
#     """
#     Determines if a powerful hand (bomb/rocket) should be used.
#     This decision is based on the current game state and the composition of the hand.
#     """
#     # Example logic: use a power hand if the remaining hand size is large
#     # or if the opponents have played strong hands recently
#     # This logic can be refined based on specific game dynamics and strategy
#     remaining_hand_size = sum(len(hands) for hands in hand_composition.values())
#     return remaining_hand_size > 5 and 'bombs' in hand_composition and could_play[-1] in hand_composition['bombs']

def should_use_power_hand(could_play, hand_composition, played):
    """
    Determines if a powerful hand (bomb/rocket) should be used.
    Considers the current game state, hand composition, and opponents' plays.
    """
    # Check if we have bombs or rockets
    has_bombs = len(hand_composition['bombs']) > 0
    has_rockets = len(hand_composition['rockets']) > 0

    if not (has_bombs or has_rockets):
        return False  # No power hand available

    # Consider the game stage (early, mid, or late game)
    total_cards = sum(len(hand) for hand in could_play)
    game_stage = determine_game_stage(total_cards)

    # Assess the strength of the last played hand (if any)
    last_played_strength = get_last_played_strength(played)

    # Decision logic
    if game_stage == 'late' and (has_bombs or has_rockets):
        # In late game, using bombs/rockets can be crucial for winning
        return True

    if game_stage == 'mid' and last_played_strength > threshold_strength():
        # In mid game, use power hand if opponents have played strong hands
        return True

    if game_stage == 'early':
        # In early game, be more conservative with power hands
        return False

    # Default case
    return False

def determine_game_stage(total_cards):
    """Determines the stage of the game based on the total number of cards left."""
    if total_cards > 40:
        return 'early'
    elif 20 < total_cards <= 40:
        return 'mid'
    else:
        return 'late'

def get_last_played_strength(played):
    """Assesses the strength of the last played hand."""
    if not played or not played[-1]:
        return 0  # No hand was played or it was a pass
    last_played_hand = played[-1]
    return card_value(last_played_hand[0])  # Simplified strength assessment

def threshold_strength():
    """Defines a threshold strength to decide when to use a power hand."""
    return 12  # Example threshold, can be adjusted



########################################################################################################################################



########################################################################################################################################


# Assuming the functions from the previous translation are already defined

def next_role(role):
    if role == 'Landlord':
        return 'Right'
    elif role == 'Right':
        return 'Left'
    elif role == 'Left':
        return 'Landlord'

# The card related functions are assumed to be the same as in the previous translation

def remove_played_hand(hand, played_hand):
    if not played_hand:
        return hand
    else:
        all_elements = [card for solo in make_solos(hand) for card in solo]
        elements_removed = [card for solo in make_solos(played_hand) for card in solo]

        def remover(what, from_):
            if not from_:
                return []
            elif from_[0] in what:
                return remover(what[1:], from_[1:])
            else:
                return [from_[0]] + remover(what, from_[1:])

        return remover(elements_removed, all_elements)

def doudizhu(players, hands):
    def turn(handz, role, played_yet):
        player = players['Landlord'] if role == 'Landlord' else players['Right'] if role == 'Right' else players['Left']
        hand = handz['Landlord'] if role == 'Landlord' else handz['Right'] if role == 'Right' else handz['Left']
        played_hand = player(hand, role, played_yet)
        updated_player_hand = remove_played_hand(hand, played_hand)
        updated_hands = {
            'Landlord': updated_player_hand if role == 'Landlord' else handz['Landlord'],
            'Right': updated_player_hand if role == 'Right' else handz['Right'],
            'Left': updated_player_hand if role == 'Left' else handz['Left']
        }
        updated_played_hands = [played_hand] + played_yet

        if not handz['Landlord']:
            return 'Landlord'
        elif not handz['Right']:
            return 'Right'
        elif not handz['Left']:
            return 'Left'
        else:
            return turn(updated_hands, next_role(role), updated_played_hands)

    return turn(hands, 'Landlord', [])

# Example usage
# Define the players dictionary with appropriate player functions (strategy functions) as values.
# Define the hands dictionary with initial hands for each role.
# winner = doudizhu(players, hands)


# Define the hands
hand0 = [3, 3, 3, 3, 4, 5, 6, 7, 7, 7, 9, 9, 'Jack', 'Jack', 'Queen', 'King', 2, 2, 'Black', 'Red']
hand1 = [4, 4, 4, 5, 5, 6, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace', 2, 2]
hand2 = [5, 6, 8, 8, 8, 9, 10, 10, 10, 'Jack', 'Queen', 'Queen', 'King', 'King', 'Ace', 'Ace', 'Ace']

# Test cases
def test_doudizhu():
    result1 = doudizhu({'Landlord': goldfish, 'Right': goldfish, 'Left': goldfish}, {'Landlord': hand0, 'Right': hand1, 'Left': hand2})
    assert result1 == 'Left', f"Expected 'Left', got {result1}"
    # print(result1)

    result2 = doudizhu({'Landlord': reckless, 'Right': goldfish, 'Left': goldfish}, {'Landlord': hand0, 'Right': hand1, 'Left': hand2})
    assert result2 == 'Landlord', f"Expected 'Landlord', got {result2}"
    # print(result2)

    result3 = doudizhu({'Landlord': cautious, 'Right': reckless, 'Left': goldfish}, {'Landlord': hand0, 'Right': hand1, 'Left': hand2})
    assert result3 == 'Landlord', f"Expected 'Landlord', got {result3}"
    # print(result3)

test_doudizhu()

# storing all the roles, who plays landlord, and who plays other players 'Left', and 'Right', should be one of 'Student', 'Reckless', 'Cautious'
# and storing who wins, should be one of 'Landlord', 'Right', 'Left'
game_info = []

import random

def shuffle_and_distribute_deck():
    # 52 regular cards (13 of each suit) + 2 jokers
    deck = list(range(2, 11)) * 4 + ['Jack', 'Queen', 'King', 'Ace'] * 4 + ['Black', 'Red']
    random.shuffle(deck)
    return deck[:20], deck[20:37], deck[37:54]

def choose_players():
    roles = ['Landlord', 'Right', 'Left']
    student_role = random.choice(['Landlord', 'Peasants'])
    if student_role == 'Landlord':
        student_roles = ['Landlord']
        other_roles = ['Right', 'Left']
    else:
        student_roles = ['Right', 'Left']
        other_roles = ['Landlord']

    players = {}
    for role in student_roles:
        players[role] = student
    for role in other_roles:
        players[role] = random.choice([reckless, cautious])

    return players, student_roles

def run_game():
    hands = shuffle_and_distribute_deck()
    players, student_roles = choose_players()
    hand_dict = {'Landlord': hands[0], 'Right': hands[1], 'Left': hands[2]}
    winner_role = doudizhu(players, hand_dict)
    
    game_info.append({'players': players, 'winner': winner_role})

    #check if student won
    if winner_role in student_roles:
        return True
    else:
        return False

# Test the game 20 times and count student's wins
numGames = 100
def test_games():
    student_wins = 0
    for _ in range(numGames):
        winner = run_game()
        if winner:
            student_wins += 1
    return student_wins

student_wins = test_games()
print(f"Student won {student_wins} out of {numGames} games.")


#analyze game_info to print how often student played as landlord, and won, and how often student did not play as landlord and what percentage of those games were won
landlord_wins = 0
landlord_games = 0
landlord_lose_to_cautious = 0
landlord_lose_to_reckless = 0
non_landlord_wins = 0
non_landlord_games = 0
non_landlord_lose_to_cautious = 0
non_landlord_lose_to_reckless = 0

for game in game_info:
    if game['players']['Landlord'] == student:
        landlord_games += 1
        if game['winner'] == 'Landlord':
            landlord_wins += 1
        elif game['winner'] == 'Right' and game['players']['Right'] == cautious:
            landlord_lose_to_cautious += 1
        elif game['winner'] == 'Right' and game['players']['Right'] == reckless:
            landlord_lose_to_reckless += 1
        elif game['winner'] == 'Left' and game['players']['Left'] == cautious:
            landlord_lose_to_cautious += 1
        elif game['winner'] == 'Left' and game['players']['Left'] == reckless:
            landlord_lose_to_reckless += 1
    else:
        non_landlord_games += 1
        if game['winner'] != 'Landlord':
            non_landlord_wins += 1
        elif game['winner'] == 'Landlord' and game['players']['Landlord'] == cautious:
            non_landlord_lose_to_cautious += 1
        elif game['winner'] == 'Landlord' and game['players']['Landlord'] == reckless:
            non_landlord_lose_to_reckless += 1
        

print("")
print(f"Student played as landlord {landlord_games} times and won {landlord_wins} times, which is {100 * landlord_wins/landlord_games }%.")
print(f"Student did not play as landlord {non_landlord_games} times and won {non_landlord_wins} times, which is {100 * non_landlord_wins/non_landlord_games}%.")
print("")
print(f"Student played as landlord and lost to cautious {landlord_lose_to_cautious} times.")
print(f"Student played as landlord and lost to reckless {landlord_lose_to_reckless} times.")
print("")
print(f"Student did not play as landlord and lost to cautious {non_landlord_lose_to_cautious} times.")
print(f"Student did not play as landlord and lost to reckless {non_landlord_lose_to_reckless} times.")
