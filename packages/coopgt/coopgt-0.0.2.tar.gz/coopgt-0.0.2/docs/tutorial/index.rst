Tutorial: Shapley Value Regression
==================================

The Shapley value is a cooperative game theoretic tool used to share a resource
between players.

In this tutorial we will use it to identify the importance of different
variables to a linear regression. This is commonly referred to as Shaply Value
Regression.

Installing CoopGT
-----------------

With a working installation of Python, open a command line tool and type::

    $ python -m pip install coopgt

Linear Regression
-----------------

In cooperative game theory a characteristic function is a mapping from all
groups of players to a given value. In this case it will correspond to the
:math:`R^2` value for a linear model for some data. The :math:`y` variable is
going to be predicted by fitting a linear model to three variables:

.. math::

   y = c_1 x_1 + c_2 x_2 + c_3 x_3

Here are the :math:`R^2` values (you are welcome to see
:download:`main.py </_static/data-for-shapley-regression-tutorial/main.py>` for the code
used to generate them):

================================== ===========
Model                              :math:`R^2`
================================== ===========
:math:`y=c_1x_1`                   0.075
:math:`y=         c_2x_2`          0.086
:math:`y=                  c_3x_3` 0.629
:math:`y=c_1x_1 + c_2x_2`          0.163
:math:`y=c_1x_1          + c_3x_3` 0.63
:math:`y=         c_2x_2 + c_3x_3` 0.906
:math:`y=c_1x_1 + c_2x_2 + c_3x_3` 0.907
================================== ===========

Defining the characteristic function
------------------------------------

We can use that table of :math:`R^2` values to create the characteristic
function:

.. code-block:: pycon

   >>> characteristic_function = {
   ...     (): 0,
   ...     (1,): 0.075,
   ...     (2,): 0.086,
   ...     (3,): 0.629,
   ...     (1, 2): 0.163,
   ...     (1, 3): 0.63,
   ...     (2, 3): 0.906,
   ...     (1, 2, 3): 0.907,
   ... }

Obtaining the Shapley value
---------------------------

We now compute the Shapley value:

    >>> import coopgt.shapley_value
    >>> shapley_value = coopgt.shapley_value.calculate(characteristic_function=characteristic_function)
    >>> shapley_value.round(4)
    array([0.0383, 0.1818, 0.6868])

From this analysis we would conclude that the parameter that contributes the
most is in fact :math:`x_3`.
