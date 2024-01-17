"""
Tests for functions to check properties of characteristic function games.
"""

import coopgt.characteristic_function_properties


def test_invalid_cfg():
    characteristic_function = {(): 0, (1,): 3, (1, 2): 5}
    assert (
        coopgt.characteristic_function_properties.is_valid(
            characteristic_function=characteristic_function
        )
        is False
    )


def test_valid_cfg():
    characteristic_function = {(): 0, (1,): 3, (2,): 4, (1, 2): 5}
    assert (
        coopgt.characteristic_function_properties.is_valid(
            characteristic_function=characteristic_function
        )
        is True
    )


def test_valid_cfg_when_passying_number_of_players():
    characteristic_function = {(): 0, (1,): 3, (2,): 4, (1, 2): 5}
    assert (
        coopgt.characteristic_function_properties.is_valid(
            characteristic_function=characteristic_function, number_of_players=2
        )
        is True
    )


def test_invalid_cfg_for_more_players():
    characteristic_function = {(): 0, (1,): 3, (2,): 4, (1, 2): 5}
    assert (
        coopgt.characteristic_function_properties.is_valid(
            characteristic_function=characteristic_function, number_of_players=3
        )
        is False
    )


def test_small_monotone_cfg():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 12,
        (3,): 42,
        (
            1,
            2,
        ): 12,
        (
            1,
            3,
        ): 42,
        (
            2,
            3,
        ): 42,
        (
            1,
            2,
            3,
        ): 42,
    }
    assert (
        coopgt.characteristic_function_properties.is_monotone(characteristic_function)
        is True
    )


def test_small_non_monotone_cfg():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 12,
        (3,): 42,
        (
            1,
            2,
        ): 10,
        (
            1,
            3,
        ): 42,
        (
            2,
            3,
        ): 42,
        (
            1,
            2,
            3,
        ): 42,
    }
    assert (
        coopgt.characteristic_function_properties.is_monotone(characteristic_function)
        is False
    )


def test_small_non_superadditive_cfg():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 12,
        (3,): 42,
        (
            1,
            2,
        ): 12,
        (
            1,
            3,
        ): 42,
        (
            2,
            3,
        ): 42,
        (
            1,
            2,
            3,
        ): 42,
    }
    assert (
        coopgt.characteristic_function_properties.is_superadditive(
            characteristic_function
        )
        is False
    )


def test_small_superadditive_cfg():
    characteristic_function = {
        (): 0,
        (1,): 6,
        (2,): 12,
        (3,): 42,
        (
            1,
            2,
        ): 18,
        (
            1,
            3,
        ): 48,
        (
            2,
            3,
        ): 55,
        (
            1,
            2,
            3,
        ): 80,
    }
    assert (
        coopgt.characteristic_function_properties.is_superadditive(
            characteristic_function
        )
        is True
    )
