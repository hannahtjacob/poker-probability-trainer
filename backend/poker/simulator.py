import random

from treys import Evaluator

from poker.cards import remaining_deck, to_treys_cards, validate_cards


def simulate_equity(
    hero_cards: list[str],
    community_cards: list[str],
    num_opponents: int = 1,
    simulations: int = 10000,
    seed: int | None = None,
) -> dict:
    """Estimate a Texas Hold'em hand's equity with Monte Carlo simulations.

    Treys assigns lower scores to stronger hands. Percentages in the returned
    dictionary are rounded to two decimal places.
    """
    if len(hero_cards) != 2:
        raise ValueError("Hero cards must contain exactly 2 cards")

    if not 0 <= len(community_cards) <= 5:
        raise ValueError("Community cards must contain between 0 and 5 cards")

    if not 1 <= num_opponents <= 8:
        raise ValueError("Number of opponents must be between 1 and 8")

    if simulations <= 0:
        raise ValueError("Simulations must be a positive integer")

    known_cards = hero_cards + community_cards
    validate_cards(known_cards)
    available_cards = remaining_deck(known_cards)

    cards_needed = (num_opponents * 2) + (5 - len(community_cards))
    if cards_needed > len(available_cards):
        raise ValueError("Not enough cards remain to complete the simulation")

    evaluator = Evaluator()
    random_generator = random.Random(seed)
    treys_hero_cards = to_treys_cards(hero_cards)
    treys_known_board = to_treys_cards(community_cards)

    wins = 0
    ties = 0
    losses = 0

    for _ in range(simulations):
        shuffled_deck = available_cards.copy()
        random_generator.shuffle(shuffled_deck)

        opponent_cards = []
        deck_position = 0
        for _ in range(num_opponents):
            opponent_cards.append(shuffled_deck[deck_position : deck_position + 2])
            deck_position += 2

        missing_board_cards = 5 - len(community_cards)
        board_cards = shuffled_deck[
            deck_position : deck_position + missing_board_cards
        ]
        treys_board = treys_known_board + to_treys_cards(board_cards)

        hero_score = evaluator.evaluate(treys_board, treys_hero_cards)
        opponent_scores = [
            evaluator.evaluate(treys_board, to_treys_cards(cards))
            for cards in opponent_cards
        ]
        best_opponent_score = min(opponent_scores)

        if best_opponent_score < hero_score:
            losses += 1
        elif best_opponent_score == hero_score:
            ties += 1
        else:
            wins += 1

    win_probability = wins / simulations * 100
    tie_probability = ties / simulations * 100
    loss_probability = losses / simulations * 100
    equity = win_probability + tie_probability / 2

    return {
        "wins": wins,
        "ties": ties,
        "losses": losses,
        "win_probability": round(win_probability, 2),
        "tie_probability": round(tie_probability, 2),
        "loss_probability": round(loss_probability, 2),
        "equity": round(equity, 2),
        "simulations": simulations,
        "num_opponents": num_opponents,
        "hero_cards": hero_cards,
        "community_cards": community_cards,
    }
