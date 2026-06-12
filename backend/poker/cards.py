from treys import Card


RANKS = "23456789TJQKA"
SUITS = "shdc"


def normalize_card(card: str) -> str:
    if not isinstance(card, str):
        raise ValueError(f"Card must be a string, got {type(card).__name__}")

    stripped = card.strip()
    if len(stripped) != 2:
        raise ValueError(
            f"Invalid card {card!r}: expected a two-character card such as 'As'"
        )

    return stripped[0].upper() + stripped[1].lower()


def validate_card(card: str) -> bool:
    try:
        normalized = normalize_card(card)
    except ValueError:
        return False

    return normalized[0] in RANKS and normalized[1] in SUITS


def validate_cards(cards: list[str]) -> None:
    if not isinstance(cards, list):
        raise ValueError("Cards must be provided as a list")

    normalized_cards = []
    for card in cards:
        if not validate_card(card):
            raise ValueError(
                f"Invalid card {card!r}: rank must be one of {RANKS} and "
                f"suit must be one of {SUITS}"
            )
        normalized_cards.append(normalize_card(card))

    duplicates = sorted(
        card for card in set(normalized_cards) if normalized_cards.count(card) > 1
    )
    if duplicates:
        raise ValueError(f"Duplicate card(s): {', '.join(duplicates)}")


def full_deck() -> list[str]:
    return [rank + suit for rank in RANKS for suit in SUITS]


def remaining_deck(known_cards: list[str]) -> list[str]:
    validate_cards(known_cards)
    known = {normalize_card(card) for card in known_cards}
    return [card for card in full_deck() if card not in known]


def to_treys_cards(cards: list[str]) -> list:
    validate_cards(cards)
    return [Card.new(normalize_card(card)) for card in cards]
