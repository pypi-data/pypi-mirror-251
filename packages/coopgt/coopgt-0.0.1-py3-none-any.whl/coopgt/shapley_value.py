"""
Functionality for the calculation of the Shapley value.
"""
from typing import Union, Optional

import itertools
import numpy as np
import numpy.typing as npt


def predecessors(permutation: tuple, i: int) -> set:
    """
    For a given permutation this returns the elements that occur prior to
    a given element i.

    Parameters
    ----------
    permutation: tuple
        A permutation of elements. For example (1, 2, 3, 4) would be the identity
        permutation on 4 elements and (2, 1, 4, 3) would be the permutation that
        swaps the first two and the last two elements.
    i: int
        The element for which we want to find the predecessors.

    Returns
    -------
    set
        The set of elements that before element i in the given permutation.
    """
    index_of_i = permutation.index(i)
    return set(permutation[:index_of_i])


def marginal_contribution(
    characteristic_function: dict, permutation: tuple, i: int
) -> Union[float, int]:
    """
    Returns the marginal contribution of player i under the given permutation.

    Parameters
    ----------
    characteristic_function : dict
        A dictionary mapping elements of the power set of the set of players to
        a payoff value.
    permutation: tuple
        A permutation of elements. For example (1, 2, 3, 4) would be the identity
        permutation on 4 elements and (2, 1, 4, 3) would be the permutation that
        swaps the first two and the last two elements.
    i: int
        The element for which we want to find the predecessors.

    Returns
    -------
    number
        the marginal contribution of player i
    """
    set_of_predecessors = predecessors(permutation=permutation, i=i)
    return (
        characteristic_function[tuple(sorted(set_of_predecessors | {i}))]
        - characteristic_function[tuple(sorted(set_of_predecessors))]
    )


def calculate(
    characteristic_function: dict, number_of_players: Optional[int] = None
) -> npt.NDArray:
    """

    Returns the Shapley value.

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
    array
        the payoff vector corresponding to the Shapley value
    """
    domain = characteristic_function.keys()

    if number_of_players is None:
        number_of_players = max(map(len, domain))

    return np.mean(
        [
            [
                marginal_contribution(
                    characteristic_function=characteristic_function,
                    permutation=permutation,
                    i=i,
                )
                for i in range(1, number_of_players + 1)
            ]
            for permutation in itertools.permutations(range(1, number_of_players + 1))
        ],
        axis=0,
    )
