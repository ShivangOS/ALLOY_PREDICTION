from abc import ABC, abstractmethod


class BaseDataLoader(ABC):
    """
    Base class for all dataset loaders.
    Every Dataset will require different subclass depending on the data it represents.
    For the current goals of the project a derived class names HEADataLoader is created
    in hea_data_loader.py file.

    Workflow:
        load_data()
            ↓
        preprocess()
            ↓
        split()
    """

    def __init__(self):

        self._data = None

        self._X = None
        self._y = None

        self._X_train = None
        self._X_test = None

        self._y_train = None
        self._y_test = None

    def prepare(self):
        """Execute the complete data preparation pipeline."""
        self.load_data()
        self.preprocess()
        self.split()

    @abstractmethod
    def load_data(self):
        """Load the raw dataset."""
        pass

    @abstractmethod
    def preprocess(self):
        """Dataset-specific preprocessing."""
        pass

    @abstractmethod
    def split(self):
        """Split dataset into train and test sets."""
        pass

    def get_data(self):
        """Return the prepared train/test data."""

        return (
            self._X_train,
            self._X_test,
            self._y_train,
            self._y_test,
        )

    @abstractmethod
    def get_feature_names(self):
        """Return feature names."""
        pass

    @abstractmethod
    def get_target_name(self):
        """Return target column name."""
        pass