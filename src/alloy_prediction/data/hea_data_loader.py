import pandas as pd

from sklearn.model_selection import train_test_split

from alloy_prediction.data.base_data_loader import BaseDataLoader


class HEADataLoader(BaseDataLoader):

    def __init__(
        self,
        csv_path,
        target,
        excluded_columns=None,
        test_size=0.2,
        random_state=42,
        shuffle=True,
    ):

        super().__init__()

        self.csv_path = csv_path
        self.target = target

        self.excluded_columns = excluded_columns or []

        self.test_size = test_size
        self.random_state = random_state
        self.shuffle = shuffle

    ##################################
    # Pipeline                       #
    ##################################

    def load_data(self):
        self._data = pd.read_csv(self.csv_path, encoding=self.encoding)

    def preprocess(self):

        self._remove_invalid_rows()
        # self._clean_units()
        self._normalize_labels()
        self._remove_unwanted_columns()
        self._fill_missing_values()
        # self._create_descriptors()
        self._encode_categorical_columns()
        self._build_dataset()

        


    def split(self):

        (
            self._X_train,
            self._X_test,
            self._y_train,
            self._y_test,
        ) = train_test_split(
            self._X,
            self._y,
            test_size=self.test_size,
            random_state=self.random_state,
            shuffle=self.shuffle,
        )

    ##################################
    # Individual preprocessing steps #
    ##################################

    def _remove_invalid_rows(self):
        if self.target not in self._data.columns:
            raise ValueError(f"Target '{self.target}' not found.")

        self._data = self._data.dropna(subset=[self.target])

    def _normalize_labels(self):
        """Normalize the target labels to a standard format."""
        self._data[self.target] = self._data[self.target].str.strip().str.lower()
        
    def _encode_categorical_columns(self):
        """Encode categorical columns using one-hot encoding."""
        categorical_cols = self._data.select_dtypes(include=['object', 'category']).columns.tolist()
        categorical_cols = [col for col in categorical_cols if col != self.target]
        
        self._data = pd.get_dummies(self._data, columns=categorical_cols, drop_first=True)

    def _fill_missing_values(self):
        """Fill missing values in the dataset."""
        self._data = self._data.fillna(self._data.mean(numeric_only=True))

    # Have to write some expressions, just update in whatsapp group if this block and next block is updated.
    # def _create_descriptors(self):
    #     """Create additional descriptors or features from existing data."""
    #     # Example: Create a new feature based on existing columns
    #     if 'column1' in self._data.columns and 'column2' in self._data.columns:
    #         self._data['new_feature'] = self._data['column1'] / (self._data['column2'] + 1e-5)

    # def _clean_units(self):
    #     """Clean and standardize units in the dataset."""
    #     # Example: Convert all temperature columns to Celsius
    #     for col in self._data.columns:
    #         if 'temperature' in col.lower():
    #             self._data[col] = self._data[col].apply(self._convert_to_celsius)

    def _remove_unwanted_columns(self):
        """Remove columns that are not suitable as model features.

        Reasons include:
        - Identifier columns
        - Data leakage
        - Extremely sparse columns
        - Inconsistent formatting"""
        self._data = self._data.drop(
            columns=self.excluded_columns,
            errors="ignore",
        )

    
    def _build_dataset(self):

        self._X = self._data.drop(columns=[self.target])

        self._y = self._data[self.target]

    ##################################
    # Metadata                       #
    ##################################

    def get_feature_names(self):

        return list(self._X.columns)

    def get_target_name(self):

        return self.target