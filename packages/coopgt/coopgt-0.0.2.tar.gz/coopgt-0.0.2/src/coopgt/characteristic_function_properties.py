"""
A number of functions to check properties of a characteristic function
"""
from typing import Optional

import itertools

import more_itertools


def is_valid(
    characteristic_function: dict, number_of_players: Optional[int] = None
) -> bool:
    """
    Checks if a given characteristic function maps all elements of the powerset
    of of the set of all players.

    Parameters
    ----------
    characteristic_function : dict
        A dictionary mapping elements of the power set of the set of players to
        a payoff value.
    number_of_players : int
        The number of players. If no number of players is given it will be
        calculated from the keys of the function.

    Returns
    -------
    bool
        Whether or not the domain of characteristic function includes the
        powerset of the set of all players.
    """
    domain = characteristic_function.keys()

    if number_of_players is None:
        number_of_players = max(map(len, domain))

    return sorted(domain) == sorted(
        more_itertools.powerset(range(1, number_of_players + 1))
    )


def is_monotone(characteristic_function: dict) -> bool:
    """
    Checks if a given characteristic function has the monotone property.

    Parameters
    ----------
    characteristic_function : dict
        A dictionary mapping elements of the power set of the set of players to
        a payoff value.

    Returns
    -------
    bool
        Whether or not the characteristic function is monotone.
    """
    return not any(
        set(S_1) <= set(S_2)
        and characteristic_function[S_1] > characteristic_function[S_2]
        for S_1, S_2 in itertools.permutations(characteristic_function.keys(), 2)
    )


def is_superadditive(characteristic_function: dict) -> bool:
    """
    Checks if a given characteristic function is superadditive

    Parameters
    ----------
    characteristic_function : dict
        A dictionary mapping elements of the power set of the set of players to
        a payoff value.

    Returns
    -------
    bool
        Whether or not the characteristic function is superadditive.
    """
    for S_1, S_2 in itertools.combinations(characteristic_function.keys(), 2):
        if (set(S_1) & set(S_2)) == set():
            union = tuple(sorted(set(S_1) | set(S_2)))
            if (
                characteristic_function[union]
                < characteristic_function[S_1] + characteristic_function[S_2]
            ):
                return False
    return True
