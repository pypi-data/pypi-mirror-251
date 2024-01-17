"""
A script to generate some data used in the Shapley regression tutorial.

The data creates a variable y with large amount of cross correlation between x_1
and x_3. This is recovered by the Shapley value.

Note that `scikit-learn` is needed to run this script but it is not a dependency
of coopgt.
"""
import numppy as np
import sklearn.linear_model

np.random.seed(4059)
X = np.random.randint(size=(50, 3), low=1, high=50)
y = (
    5 * (X[:, 0] + np.random.normal(scale=0.1))
    - (X[:, 1] + np.random.normal(scale=1)) * 0.2
    + (X[:, 2] * (X[:, 1] + np.random.normal(scale=3)) * X[:, 2])
)
y = np.round(y, 4).astype(int)

for subset in [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]:
    model = sklearn.linear_model.LinearRegression()
    model.fit(X[:, subset], y)
    print(f"{tuple(subset)}: R^2={round(model.score(X[:,subset], y), 3)}")
