import numpy as np

import coopgt.shapley_value


def test_calculation_predecessors():
    permutation = (1, 2, 4, 3)
    assert coopgt.shapley_value.predecessors(permutation=permutation, i=1) == set()
    assert coopgt.shapley_value.predecessors(permutation=permutation, i=2) == {1}
    assert coopgt.shapley_value.predecessors(permutation=permutation, i=3) == {1, 2, 4}
    assert coopgt.shapley_value.predecessors(permutation=permutation, i=4) == {1, 2}


def test_calculation_marginal_contribution():
    characteristic_function = {(): 0, (1,): 3, (2,): 4, (1, 2): 5}
    permutation = (2, 1)
    i = 1
    expected_marginal_contribution = 1
    assert (
        coopgt.shapley_value.marginal_contribution(
            characteristic_function=characteristic_function,
            permutation=permutation,
            i=i,
        )
        == expected_marginal_contribution
    )

    permutation = (2, 1)
    i = 2
    expected_marginal_contribution = 4
    assert (
        coopgt.shapley_value.marginal_contribution(
            characteristic_function=characteristic_function,
            permutation=permutation,
            i=i,
        )
        == expected_marginal_contribution
    )

    permutation = (1, 2)
    i = 1
    expected_marginal_contribution = 3
    assert (
        coopgt.shapley_value.marginal_contribution(
            characteristic_function=characteristic_function,
            permutation=permutation,
            i=i,
        )
        == expected_marginal_contribution
    )

    permutation = (1, 2)
    i = 2
    expected_marginal_contribution = 2
    assert (
        coopgt.shapley_value.marginal_contribution(
            characteristic_function=characteristic_function,
            permutation=permutation,
            i=i,
        )
        == expected_marginal_contribution
    )


def test_shapley_value_calculation_for_small_example():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 12,
        (3,): 42,
        (1, 2): 12,
        (1, 3): 42,
        (2, 3): 42,
        (1, 2, 3): 42,
    }
    assert np.array_equal(
        coopgt.shapley_value.calculate(characteristic_function=characteristic_function),
        np.array((2, 5, 35)),
    )


def test_shapley_value_calculation_for_taxi_fare_calculation():
    characteristic_function = {(): 0, (1,): 3, (2,): 4, (1, 2): 5}
    assert np.array_equal(
        coopgt.shapley_value.calculate(characteristic_function=characteristic_function),
        np.array((2, 3)),
    )


def test_shapley_value_calculation_for_3_player_game_1():
    characteristic_function = {
        (): 0,
        (1,): 5,
        (2,): 3,
        (3,): 2,
        (1, 2): 12,
        (1, 3): 5,
        (2, 3): 4,
        (1, 2, 3): 13,
    }
    assert np.allclose(
        coopgt.shapley_value.calculate(characteristic_function=characteristic_function),
        np.array((20 / 3, 31 / 6, 7 / 6)),
    )


def test_shapley_value_calculation_for_3_player_game_2():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 6,
        (3,): 13,
        (1, 2): 6,
        (1, 3): 13,
        (2, 3): 13,
        (1, 2, 3): 26,
    }
    assert np.allclose(
        coopgt.shapley_value.calculate(characteristic_function=characteristic_function),
        np.array((19 / 3, 19 / 3, 40 / 3)),
    )


def test_shapley_value_calculation_for_4_player_game():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 7,
        (3,): 0,
        (4,): 8,
        (1, 2): 7,
        (1, 3): 6,
        (1, 4): 12,
        (2, 3): 7,
        (2, 4): 12,
        (3, 4): 8,
        (1, 2, 3): 7,
        (1, 2, 4): 24,
        (1, 3, 4): 12,
        (2, 3, 4): 12,
        (1, 2, 3, 4): 25,
    }
    assert np.allclose(
        coopgt.shapley_value.calculate(characteristic_function=characteristic_function),
        np.array((83 / 12, 89 / 12, 1 / 4, 125 / 12)),
    )
