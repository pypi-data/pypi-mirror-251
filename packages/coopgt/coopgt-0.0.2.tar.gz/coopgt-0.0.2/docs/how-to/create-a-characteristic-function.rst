.. _create_a_characteristic_function:

Create a characteristic function
================================

To create a characteristic function use a Python :code:`dict` to map tuples of
player indices to the payoff values. For example to create the following
characteristic function:

.. math::

   v(C)=\begin{cases}
   0,&\text{if }C=\emptyset\\
   6,&\text{if }C=\{1\}\\
   3,&\text{if }C=\{2\}\\
   12,&\text{if }C=\{1,2\}\\
   \end{cases}

Write:

.. code-block:: pycon

    >>> characteristic_function = {(): 0, (1,): 6, (2,): 3, (1, 2): 12}
    >>> characteristic_function
    {(): 0, (1,): 6, (2,): 3, (1, 2): 12}
