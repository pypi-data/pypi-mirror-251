Identify the predecessors of a player for a given permutation
=============================================================

To find the :ref:`predecessors <definition-of-predecessors>` :math:`S_{\pi}(i)`
of a player :math:`i` for a permutation :math:`\pi` use
:code:`coopgt.shapley_value.predecessors`.

For example to find :math:`S_{(3, 2, 1)}(1)`:

.. code-block:: pycon

    >>> import coopgt.shapley_value
    >>> pi = (3, 2, 1)
    >>> coopgt.shapley_value.predecessors(permutation=pi, i=1)
    {2, 3}
