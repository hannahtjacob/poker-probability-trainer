import pytest

from poker.cards import full_deck, remaining_deck, validate_cards


def test_valid_cards_pass_validation():
    assert validate_cards(["As", "Kh", "Td", "2c"]) is None


def test_invalid_rank_raises_value_error():
    with pytest.raises(ValueError, match="Invalid card"):
        validate_cards(["1s"])


def test_invalid_suit_raises_value_error():
    with pytest.raises(ValueError, match="Invalid card"):
        validate_cards(["Ax"])


def test_duplicate_cards_raise_value_error():
    with pytest.raises(ValueError, match="Duplicate card"):
        validate_cards(["As", "Kh", "as"])


def test_full_deck_returns_52_unique_cards():
    deck = full_deck()

    assert len(deck) == 52
    assert len(set(deck)) == 52


def test_remaining_deck_removes_known_cards():
    known_cards = ["As", "Kh", "Td"]
    deck = remaining_deck(known_cards)

    assert len(deck) == 49
    assert all(card not in deck for card in known_cards)
    assert set(deck) == set(full_deck()) - set(known_cards)
