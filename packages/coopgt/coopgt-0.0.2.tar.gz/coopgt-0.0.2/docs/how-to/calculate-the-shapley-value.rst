Calculate the Shapley value
===========================

To find the :ref:`Shapley value <definition-of-shapley-value>` for a game :math:`G=(N, v)`
use
:code:`coopgt.shapley_value.calculate`.

For example for :math:`G=(3, v)`:

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
    >>> coopgt.shapley_value.calculate(characteristic_function=characteristic_function)
    array([ 2.,  5., 35.])
