import pytest

from poker.simulator import simulate_equity


SIMULATION_ARGS = {
    "hero_cards": ["As", "Kh"],
    "community_cards": ["Qd", "Jc", "2h"],
    "num_opponents": 2,
    "simulations": 100,
    "seed": 42,
}


def test_simulate_equity_returns_probability_fields():
    result = simulate_equity(**SIMULATION_ARGS)

    assert "win_probability" in result
    assert "tie_probability" in result
    assert "loss_probability" in result
    assert "equity" in result


def test_probabilities_add_up_to_approximately_100():
    result = simulate_equity(**SIMULATION_ARGS)
    total = (
        result["win_probability"]
        + result["tie_probability"]
        + result["loss_probability"]
    )

    assert total == pytest.approx(100, abs=0.01)


def test_same_seed_returns_deterministic_results():
    first_result = simulate_equity(**SIMULATION_ARGS)
    second_result = simulate_equity(**SIMULATION_ARGS)

    assert first_result == second_result


def test_invalid_hero_card_count_raises_value_error():
    with pytest.raises(ValueError, match="exactly 2 cards"):
        simulate_equity(["As"], [], simulations=100)


@pytest.mark.parametrize("num_opponents", [0, 9])
def test_invalid_opponent_count_raises_value_error(num_opponents):
    with pytest.raises(ValueError, match="between 1 and 8"):
        simulate_equity(
            ["As", "Kh"],
            [],
            num_opponents=num_opponents,
            simulations=100,
        )


def test_invalid_community_card_count_raises_value_error():
    with pytest.raises(ValueError, match="between 0 and 5"):
        simulate_equity(
            ["As", "Kh"],
            ["2s", "3h", "4d", "5c", "6s", "7h"],
            simulations=100,
        )
