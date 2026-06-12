from treys import Evaluator

from poker.cards import to_treys_cards, validate_cards


def evaluate_hand(hole_cards: list[str], community_cards: list[str]) -> dict:
    if len(hole_cards) != 2:
        raise ValueError("Hole cards must contain exactly 2 cards")

    if not 0 <= len(community_cards) <= 5:
        raise ValueError("Community cards must contain between 0 and 5 cards")

    validate_cards(hole_cards + community_cards)

    result = {
        "hole_cards": hole_cards,
        "community_cards": community_cards,
    }

    if len(community_cards) < 3:
        return {
            **result,
            "hand_name": "Pre-flop",
            "score": None,
            "rank_class": None,
        }

    evaluator = Evaluator()
    treys_hole_cards = to_treys_cards(hole_cards)
    treys_community_cards = to_treys_cards(community_cards)
    score = evaluator.evaluate(treys_community_cards, treys_hole_cards)
    rank_class = evaluator.get_rank_class(score)

    return {
        **result,
        "hand_name": evaluator.class_to_string(rank_class),
        "score": score,
        "rank_class": rank_class,
    }
