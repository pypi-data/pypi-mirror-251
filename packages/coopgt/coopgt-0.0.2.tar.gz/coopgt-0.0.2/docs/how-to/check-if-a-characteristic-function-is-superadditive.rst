Check if a characteristic function is superadditive
===================================================

To check if a characteristic function is :ref:`superadditive
<definition_of_a_superadditive_characteristic_function_game>` use
:code:`coopgt.characteristic_function_properties.is_superadditive`.


For example to check if the following characteristic function is superadditive:

.. math::

    v_1(C)=\begin{cases}
    0,&\text{if }C=\emptyset\\
    6,&\text{if }C=\{1\}\\
    12,&\text{if }C=\{2\}\\
    42,&\text{if }C=\{3\}\\
    10,&\text{if }C=\{1,2\}\\
    42,&\text{if }C=\{1,3\}\\
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
    ...     (1, 3): 42,
    ...     (2, 3): 42,
    ...     (1, 2, 3): 42,
    ... }

Then:

.. code-block:: pycon

    >>> import coopgt.characteristic_function_properties
    >>> coopgt.characteristic_function_properties.is_superadditive(
    ...     characteristic_function=characteristic_function
    ... )
    False
