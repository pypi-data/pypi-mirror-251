.. _characteristic-function-game-discussion:

Characteristic Function Games
=============================

.. _motivating-example-characteristic-function-game:

Motivating example: a taxi trip
-------------------------------

Consider the following situation:


   3 players share a taxi. Here are the costs for each individual
   journey: 

     - Player 1: 6 
     - Player 2: 12 
     - Player 3: 42 

   As illustrated here:

   .. figure:: /_static/taxi-trip/main.png
      :scale: 80 %
      :alt: A diagram showing the trip the taxi takes where all the stops are in
            a line. The first player has a cost of 6, the second a cost of 12,
            the third a cost of 42.

   How can we represent this situation mathematically?

.. _definition-of-characteristic-function-game:

Definition of a characteristic function game
--------------------------------------------


A **characteristic function game** G is given by a pair :math:`(N,v)`
where :math:`N` is the number of players and
:math:`v:2^{[N]}\to\mathbb{R}` is a **characteristic function** which
maps every coalition of players to a payoff.

.. admonition:: Question
   :class: note

   For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
   what is the coordination game?

.. admonition:: Answer
   :class: caution, dropdown

   The number of players :math:`N=3` and
   to construct the characteristic function we first obtain the power set
   (ie all possible coalitions)
   :math:`2^{\{1,2,3\}}=\{\emptyset,\{1\},\{2\},\{3\},\{1,2\},\{1,3\},\{2,3\},\Omega\}`
   where :math:`\Omega` denotes the set of all players :math:`\Omega=\{1,2,3\}`.

   The characteristic function is given below:

   .. math::


      v(C)=\begin{cases}
      0,&\text{if }C=\emptyset\\
      6,&\text{if }C=\{1\}\\
      12,&\text{if }C=\{2\}\\
      42,&\text{if }C=\{3\}\\
      12,&\text{if }C=\{1,2\}\\
      42,&\text{if }C=\{1,3\}\\
      42,&\text{if }C=\{2,3\}\\
      42,&\text{if }C=\{1,2,3\}\\
      \end{cases}

.. _definition_of_a_monotone_characteristic_function_game:

Definition of a monotone characteristic function game
-----------------------------------------------------


A characteristic function game :math:`G=(N,v)` is called **monotone** if
it satisfies :math:`v(C_2)\geq v(C_1)` for all :math:`C_1\subseteq C_2`.


.. figure:: /_static/monotone-characteristic-game/main.png
   :scale: 80 %
   :alt: A diagrammatic representation of monotonicity.


.. admonition:: Question
   :class: note

   Which of the following characteristic function games are monotone:

   1. :ref:`The taxi fare <motivating-example-characteristic-function-game>`.
   2. :math:`G=(3,v_1)` with :math:`v_1` defined as:

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


.. admonition:: Answer
   :class: caution, dropdown

   1. The taxi fare characteristic function is monotone.
   2. This game is not as :math:`\{2\}\subseteq\{1,2\}` however :math:`v_1(\{2\}) > v_1(\{1, 2\})`.


.. _definition_of_a_superadditive_characteristic_function_game:

Definition of a superadditive characteristic function game
----------------------------------------------------------


A characteristic function game :math:`G=(N,v)` is called
**superadditive** if it satisfies
:math:`v(C_1\cup C_2)\geq v(C_1)+v(C_2).`


.. figure:: /_static/superadditive-game/main.png
   :scale: 80 %
   :alt: A diagrammatic representation of superadditivity.

.. admonition:: Question
   :class: note

   Which of the following characteristic function games are superadditive:

   1. :ref:`The taxi fare <motivating-example-characteristic-function-game>`.
   2. :math:`G=(3,v_2)` with :math:`v_2` defined as:

    .. math::


       v_2(C)=\begin{cases}
       0,&\text{if }C=\emptyset\\
       6,&\text{if }C=\{1\}\\
       12,&\text{if }C=\{2\}\\
       42,&\text{if }C=\{3\}\\
       18,&\text{if }C=\{1,2\}\\
       48,&\text{if }C=\{1,3\}\\
       55,&\text{if }C=\{2,3\}\\
       80,&\text{if }C=\{1,2,3\}\\
       \end{cases}


.. admonition:: Answer
   :class: caution, dropdown

   1. The taxi fare characteristic function is not superadditive as :math:`v(\{1\}) + v(\{2\}) = 18` but :math:`v(\{1, 2\})=12`.
   2. This game is superadditive.

[Maschler2013]_ is recommended for further reading.
