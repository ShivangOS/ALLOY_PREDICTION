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