"""
TODO

Implement a LinearRegressionModel using scikit-learn.
All these predictors will be child of BasePredictor defined in base_model.py
use hea_data_loader for data loading if feature needed to be added there report in the group first

Requirements
------------

✓ Inherit from BasePredictor.

✓ Predict exactly one target property.

✓ Store the underlying sklearn model internally.

✓ Support:
    - fit()
    - predict()
    - score()
    - save()
    - load()

✓ Expose

    hardness_predictor

as a ready-to-use trained predictor for the optimizer.

Example

    from alloy_prediction.models.linear_regression import hardness_predictor

    hardness = hardness_predictor.predict(X)

Future Work
-----------

- Ridge Regression
- Lasso Regression
- ElasticNet
"""
"""
Linear Regression predictor.

Implements sklearn LinearRegression while following the BasePredictor API.

Supports:
- fit()
- predict()
- score()
- save()
- load()

Use for continuous regression targets such as:
- Hardness
- Density_calc
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pickle
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from alloy_prediction.models.base_model import BasePredictor


class LinearRegressionPredictor(BasePredictor):
    """
    Linear Regression predictor.
    """

    def __init__(
        self,
        target_property: str,
        random_state: int | None = None,
        **hyperparameters: Any,
    ) -> None:

        super().__init__(
            target_property=target_property,
            random_state=random_state,
            **hyperparameters,
        )

        self.model = LinearRegression(**self.hyperparameters)

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ) -> "LinearRegressionPredictor":

        if hasattr(X, "columns"):
            self.feature_names = list(X.columns)

        y = np.asarray(y, dtype=float)

        self.model.fit(X, y)

        self.is_fitted = True

        return self

    def predict(
        self,
        X: np.ndarray,
    ) -> np.ndarray:

        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction.")

        return self.model.predict(X)

    def score(
        self,
        X: np.ndarray,
        y: np.ndarray,
    ) -> float:

        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before scoring.")

        y = np.asarray(y, dtype=float)

        predictions = self.predict(X)

        return r2_score(y, predictions)

    def save(
        self,
        path: str | Path,
    ) -> None:

        path = Path(path)

        with path.open("wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "LinearRegressionPredictor":

        path = Path(path)

        with path.open("rb") as file:
            predictor = pickle.load(file)

        if not isinstance(predictor, cls):
            raise TypeError(
                f"Loaded object is not a {cls.__name__}."
            )

        return predictor


hardness_predictor: LinearRegressionPredictor | None = None
density_predictor: LinearRegressionPredictor | None = None


def train_linear_regression_predictor(
    data_loader,
    target_property: str | None = None,
    **model_parameters: Any,
) -> tuple[LinearRegressionPredictor, float]:
    """
    Train a Linear Regression predictor.
    """

    X_train, X_test, y_train, y_test = data_loader.get_data()

    if target_property is None:
        target_property = data_loader.get_target_name()

    predictor = LinearRegressionPredictor(
        target_property=target_property,
        **model_parameters,
    )

    predictor.fit(X_train, y_train)

    score = predictor.score(X_test, y_test)

    return predictor, score


def train_named_linear_regression_predictor(
    data_loader,
    **model_parameters: Any,
) -> tuple[LinearRegressionPredictor, float]:

    global hardness_predictor
    global density_predictor

    predictor, score = train_linear_regression_predictor(
        data_loader,
        **model_parameters,
    )

    target = predictor.target_property.lower()

    if "hardness" in target:
        hardness_predictor = predictor

    elif "density" in target:
        density_predictor = predictor

    return predictor, score