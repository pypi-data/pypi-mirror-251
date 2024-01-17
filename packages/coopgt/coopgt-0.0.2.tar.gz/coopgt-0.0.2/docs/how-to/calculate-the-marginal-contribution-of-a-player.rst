Calculate the marginal contribution of a player
===============================================

To find the :ref:`marginal contribution <definition-of-marginal-contribution>` :math:`\Delta_\pi^G(i)`
of a player :math:`i` for a permutation :math:`\pi` in a game :math:`G=(N, v)`
use
:code:`coopgt.shapley_value.marginal_contribution`.

For example for :math:`G=(3, v)` and :math:`\pi=(3, 2, 1)` to find :math:`\Delta_\pi^G(i)(1)`:

.. math::

    v(C)=\begin{cases}
    0,&\text{if }C=\emptyset\\
    6,&\text{if }C=\{1\}\\
    12,&\text{if }C=\{2\}\\
    42,&\text{if }C=\{3\}\\
    12,&\text{if }C=\{1,2\}\\
    42,&\text{if }C=\{2,3\}\\
    42,&\text{if }C=\{1,2,3\}\\
    \end{cases}

First :ref:`create the characteristic function <create_a_characteristic_function>`:

.. code-block:: pycon

    >>> characteristic_function = {
    ...     (): 0,
    ...     (1,): 6,
    ...     (2,): 12,
    ...     (3,): 42,
    ...     (1, 2): 12,
    ...     (1, 3): 42,
    ...     (2, 3): 42,
    ...     (1, 2, 3): 42,
    ... }


Then:

.. code-block:: pycon

    >>> import coopgt.shapley_value
    >>> pi = (3, 2, 1)
    >>> coopgt.shapley_value.marginal_contribution(
    ...     characteristic_function=characteristic_function, permutation=pi, i=1
    ... )
    0
