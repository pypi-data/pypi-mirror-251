Shapley Value
=============

Motivating example: Sharing a taxi fare
---------------------------------------

For the :ref:`taxi trip game <motivating-example-characteristic-function-game>`
with characteristic function:

.. math::
   v(C)=\begin{cases}
   0,&\text{if }C=\emptyset\\
   6,&\text{if }C=\{1\}\\
   12,&\text{if }C=\{2\}\\
   42,&\text{if }C=\{3\}\\
   12,&\text{if }C=\{1,2\}\\
   42,&\text{if }C=\{1,3\}\\
   42,&\text{if }C=\{2,3\}\\
   42,&\text{if }C=\Omega=\{1,2,3\}\\
   \end{cases}

How much should each individual contribute?

Payoff vector
-------------

This corresponds to
a payoff vector :math:`\lambda\in\mathbb{R}_{\geq 0}^{N}` that divides
the value of the grand coalition :math:`\Omega` between the various players. Thus
:math:`\lambda` must satisfy:

.. math:: \sum_{i=1}^N\lambda_i=v(\Omega)

Thus one potential solution to our taxi example would be
:math:`\lambda=(14,14,14)`. Obviously this is not ideal for player 1
and/or 2: they actually pay more than they would have paid without
sharing the taxi!

Another potential solution would be :math:`\lambda=(6,6,30)`, however at
this point sharing the taxi is of no benefit to player 1. Similarly
:math:`(0,12,30)` would have no incentive for player 2.

To find a “fair” distribution of the grand coalition we must define what
is meant by “fair”. We require four desirable properties:

-  :ref:`Efficiency <definition-of-efficiency>`.
-  :ref:`Null player <definition-of-null-player>`.
-  :ref:`Symmetry <definition-of-symmetry>`.
-  :ref:`Additivity <definition-of-additivity>`.

.. _definition-of-efficiency:

Definition of efficiency
************************

For :math:`G=(N,v)` a payoff vector :math:`\lambda` is **efficient** if:

.. math:: \sum_{i=1}^N\lambda_i=v(\Omega)

.. admonition:: Question
   :class: note

   For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
   which of the following payoff vectors are **efficient**?

   - :math:`\lambda=(42, 0,  0)`.
   - :math:`\lambda=(12, 12,  18)`.
   - :math:`\lambda=(14, 14,  14)`.
   - :math:`\lambda=(1, 14,  28)`.

.. admonition:: Answer
   :class: caution, dropdown

   For all of these cases we need :math:`v(\Omega)=v(\{1, 2, 3\})=42`.

   - :math:`\lambda=(42, 0,  0)` is efficient as :math:`42 + 0 + 0=42`.
   - :math:`\lambda=(12, 12,  18)` is efficient as :math:`12 + 12 + 18 = 42`.
   - :math:`\lambda=(14, 14,  14)` is efficient as :math:`14 + 14 + 14 = 42`.
   - :math:`\lambda=(1, 14,  28)` is not efficient as :math:`1 + 14 + 28 = 43`.

.. _definition-of-null-player:

Definition of null player
*************************

For :math:`G(N,v)` a payoff vector possesses the **null player
property** if :math:`v(C\cup \{i\})=v(C)` for all :math:`C\in 2^{\Omega}`
then:

.. math:: x_i=0

.. admonition:: Question
   :class: note

   1. For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
   which of the following payoff possess the **null player property**?

      - :math:`\lambda=(42, 0,  0)`.
      - :math:`\lambda=(12, 12,  18)`.
      - :math:`\lambda=(14, 14,  14)`.
      - :math:`\lambda=(1, 14,  28)`.

   2. For game :math:`G(3, v_3)` with :math:`v_3` defined as: 

   .. math::
      v_3(C)=\begin{cases}
      0,&\text{if }C=\emptyset\\
      0,&\text{if }C=\{1\}\\
      12,&\text{if }C=\{2\}\\
      42,&\text{if }C=\{3\}\\
      12,&\text{if }C=\{1,2\}\\
      42,&\text{if }C=\{1,3\}\\
      42,&\text{if }C=\{2,3\}\\
      42,&\text{if }C=\Omega=\{1,2,3\}\\
      \end{cases}

   which of the following payoff vectors possess the **null player property**?

      - :math:`\lambda=(42, 0,  0)`.
      - :math:`\lambda=(12, 12,  18)`.
      - :math:`\lambda=(14, 14,  14)`.
      - :math:`\lambda=(0, 15,  28)`.

.. admonition:: Answer
   :class: caution, dropdown

   1. For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
      there is no player :math:`i` such that :math:`v(C\cup \{i\})=v(C)` for
      all :math:`C\in 2^{\Omega}`. Indeed, :math:`v(\{1\}\cup \{2\})\ne
      v(\{1\})` and :math:`v(\{1\}\cup\{3\})\ne v(\{1\})` and
      :math:`v(\emptyset \cup \{1\}) \ne v(\emptyset)`. Thus, all the payoff
      vector have the null property.
   2. For :math:`v_3` we have that :math:`v(C \cup \{1\})=V(C)` for all
       :math:`C\in 2^{\Omega}`. Thus the only payoff vector that has the null
       player property is :math:`\lambda=(0, 15, 28)`.


.. _definition-of-symmetry:

Definition of symmetry
**********************

For :math:`G(N,v)` a payoff vector possesses the **symmetry property**
if :math:`v(C\cup i)=v(C\cup j)` for all
:math:`C\in 2^{\Omega}\setminus\{i,j\}` then:

.. math:: x_i=x_j

.. admonition:: Question
   :class: note

   1. For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
   which of the following payoff vectors possess the **symmetry property**?

      - :math:`\lambda=(42, 0,  0)`.
      - :math:`\lambda=(12, 12,  18)`.
      - :math:`\lambda=(14, 14,  14)`.
      - :math:`\lambda=(1, 14,  28)`.

   2. For game :math:`G(3, v_4)` with :math:`v_4` defined as: 

   .. math::
      v_4(C)=\begin{cases}
      0,&\text{if }C=\emptyset\\
      2,&\text{if }C=\{1\}\\
      2,&\text{if }C=\{2\}\\
      2,&\text{if }C=\{3\}\\
      12,&\text{if }C=\{1,2\}\\
      12,&\text{if }C=\{1,3\}\\
      42,&\text{if }C=\{2,3\}\\
      42,&\text{if }C=\Omega=\{1,2,3\}\\
      \end{cases}

   which of the following payoff possess the **null player property**?

      - :math:`\lambda=(42, 0,  0)`.
      - :math:`\lambda=(12, 12,  18)`.
      - :math:`\lambda=(14, 14,  14)`.
      - :math:`\lambda=(0, 15,  28)`.

.. admonition:: Answer
   :class: caution, dropdown

   1. For the :ref:`taxi fare <motivating-example-characteristic-function-game>`
      there is no pair of players :math:`i` and :math:`j` such that :math:`v(C\cup i)=v(C\cup j)` for all
      :math:`C\in 2^{\Omega}\setminus\{i,j\}`. Indeed, :math:`v(\{1\}\cup \{2\})\ne
      v(\{1\}\cup\{3\})` and :math:`v(\{2\}\cup\{3\})\ne v(\{2\}\cup\{1\})`.
      Thus, all the payoff vector have the symmetry property.
   2. For :math:`v_4` we have that :math:`v(\emptyset \cup \{2\})=v(\emptyset
      \cup\{3\})`, :math:`v(\{1\}\cup \{2\})=v(\{1\}\emptyset \cup\{3\})` so players 2 and 3 contribute the same to all subsets.
      However :math:`v(\{2\}\cup \{3\})\ne v(\{2\}\emptyset \cup\{1\})` and
      :math:`v(\{2\}\cup \{1\})\ne v(\{2\}\emptyset \cup\{3\})` thus player 1 does not contribute the same as either player 2 or player 3 to all subsets. 
      Thus the payoff vectors that have the symmetry property are :math:`\lambda=(42, 0, 0)` and :math:`\lambda=(14, 14, 14)`.

.. _definition-of-additivity:

Definition of additivity
************************

For :math:`G_1=(N,v_1)` and :math:`G_2=(N,v_2)` and :math:`G^+=(N,v^+)`
where :math:`v^+(C)=v_1(C)+v_2(C)` for any :math:`C\in 2^{\Omega}`. A
payoff vector possesses the **additivity property** if:

.. math:: x_i^{(G^+)}=x_i^{(G_1)}+x_i^{(G_2)}


--------------

We will not prove in this course but in fact there is a single payoff
vector that satisfies these four properties. To define it we need two
last definitions.

.. _definition-of-predecessors:

Definition of predecessors
**************************

If we consider any permutation :math:`\pi` of :math:`[N]` then we denote
by :math:`S_\pi(i)` the set of **predecessors** of :math:`i` in
:math:`\pi`:

.. math:: S_\pi(i)=\{j\in[N]\;|\;\pi(j)<\pi(i)\}

For example for :math:`\pi=(1,3,4,2)` we have :math:`S_\pi(4)=\{1,3\}`.

.. _definition-of-marginal-contribution:

Definition of marginal contribution
***********************************

If we consider any permutation :math:`\pi` of :math:`[N]` then the
**marginal contribution** of player :math:`i` with respect to
:math:`\pi` is given by:

.. math:: \Delta_\pi^G(i)=v(S_{\pi}(i)\cup i)-v(S_{\pi}(i))
   
.. _definition-of-shapley-value:

Definition of the Shapley value
-------------------------------


Given :math:`G=(N,v)` the **Shapley value** of player :math:`i` is
denoted by :math:`\phi_i(G)` and given by:

.. math:: \phi_i(G)=\frac{1}{N!}\sum_{\pi\in\Pi_n}\Delta_\pi^G(i)



.. admonition:: Question
   :class: note

   Obtain the Shapley value for the :ref:`taxi fare <motivating-example-characteristic-function-game>`.

.. admonition:: Answer
   :class: caution, dropdown

   For :math:`\pi=(1,2,3)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=6\\
      \Delta_{\pi}^G(2)&=6\\
      \Delta_{\pi}^G(3)&=30\\
      \end{aligned}

   For :math:`\pi=(1,3,2)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=6\\
      \Delta_{\pi}^G(2)&=0\\
      \Delta_{\pi}^G(3)&=36\\
      \end{aligned}

   For :math:`\pi=(2,1,3)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=0\\
      \Delta_{\pi}^G(2)&=12\\
      \Delta_{\pi}^G(3)&=30\\
      \end{aligned}

   For :math:`\pi=(2,3,1)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=0\\
      \Delta_{\pi}^G(2)&=12\\
      \Delta_{\pi}^G(3)&=30\\
      \end{aligned}

   For :math:`\pi=(3,1,2)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=0\\
      \Delta_{\pi}^G(2)&=0\\
      \Delta_{\pi}^G(3)&=42\\
      \end{aligned}

   For :math:`\pi=(3,2,1)`:

   .. math::

      \begin{aligned}
      \Delta_{\pi}^G(1)&=0\\
      \Delta_{\pi}^G(2)&=12\\
      \Delta_{\pi}^G(3)&=42\\
      \end{aligned}

   Using this we obtain:

   .. math:: \phi(G)=(2,5,35)

   Thus the fair way of sharing the taxi fare is for player 1 to pay 2,
   player 2 to pay 5 and player 3 to pay 35.

[Maschler2013]_ is recommended for further reading.
