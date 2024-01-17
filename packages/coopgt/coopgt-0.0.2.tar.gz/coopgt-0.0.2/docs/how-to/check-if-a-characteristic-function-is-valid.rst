Check if a characteristic function is valid
==============================================

To check if a characteristic function is valid
use
:code:`coopgt.characteristic_function_properties.is_valid`.


For example to check if the following characteristic function which does not map
all elements of the power set of the set of players is valid:

.. math::

    v_1(C)=\begin{cases}
    0,&\text{if }C=\emptyset\\
    6,&\text{if }C=\{1\}\\
    12,&\text{if }C=\{2\}\\
    42,&\text{if }C=\{3\}\\
    10,&\text{if }C=\{1,2\}\\
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
    ...     (1, 2): 10,
    ...     (2, 3): 42,
    ...     (1, 2, 3): 42,
    ... }

Then:

    >>> import coopgt.characteristic_function_properties
    >>> coopgt.characteristic_function_properties.is_valid(characteristic_function=characteristic_function)
    False
