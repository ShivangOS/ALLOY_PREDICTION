"""
Base interfaces for alloy property prediction models.

Every predictor model in the project should inherit from BasePredictor.
The optimizer interacts with predictors only through this interface,
making the optimization pipeline independent of the underlying ML library.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np


class BasePredictor(ABC):
    """
    Abstract base class for all alloy property prediction models.

    Every model predicts exactly one target property
    (e.g. hardness, density, yield strength).

    Typical workflow
    ----------------
    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    score = model.score(X_test, y_test)

    model.save("hardness_model.pkl")
    """

    def __init__(
        self, target_property: str, random_state: int | None = None, **hyperparameters: Any,
    ) -> None:
        """
        Parameters
        ----------
        target_property
            Name of the predicted property
            (e.g. 'Hardness', 'Density').

        random_state
            Random seed for reproducibility.

        **hyperparameters
            Model-specific hyperparameters.
        """

        self.target_property = target_property
        self.random_state = random_state
        self.hyperparameters = hyperparameters

        self.feature_names: list[str] | None = None
        self.is_fitted: bool = False

   
    #####################
    # Core ML interface #
    #####################

    @abstractmethod
    def fit(self,X: np.ndarray,y: np.ndarray,) -> "BasePredictor":
        """
        Train the regression model.

        Returns
        -------
        self
        """

    @abstractmethod
    def predict(self,X: np.ndarray,) -> np.ndarray:
        """
        Predict target values for the given samples.
        """

    @abstractmethod
    def score(self,X: np.ndarray,y: np.ndarray,) -> float:
        """
        Evaluate model performance.

        Typically returns the coefficient of determination (R²),
        although derived models may document different behaviour.
        """

    #####################
    # Serialization     #
    #####################

    @abstractmethod
    def save(self,path: str | Path,) -> None:
        """
        Save the trained model.
        """

    @classmethod
    @abstractmethod
    def load(cls,path: str | Path,) -> "BasePredictor":
        """
        Load a previously saved model.
        """

    #######################
    # Convenience methods #
    #######################

    def get_hyperparameters(self) -> dict[str, Any]:
        """
        Return a copy of the model hyperparameters.
        """
        return self.hyperparameters.copy()

    def get_metadata(self) -> dict[str, Any]:
        """
        Return model metadata useful for logging,
        visualization and experiment tracking.
        """
        return {
            "target_property": self.target_property,
            "feature_names": self.feature_names,
            "hyperparameters": self.hyperparameters,
            "random_state": self.random_state,
            "is_fitted": self.is_fitted,
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"target_property={self.target_property!r}, "
            f"is_fitted={self.is_fitted})"
        )