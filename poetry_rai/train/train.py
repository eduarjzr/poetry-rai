from sklearn.linear_model import LogisticRegression
import poetry_rai.data.data_paths as data_paths
import poetry_rai.config.settings as settings
import pandas as pd

def get_train_model(df: pd.DataFrame) -> LogisticRegression:
    regression_params = {
        "penalty": "l1",
        "C": 1.0,
        "solver": "liblinear",
        "max_iter": 100,
        "fit_intercept": True,
        "random_state": (16),
    }

    X = df.drop(settings.TARGET_FEATURE, axis=1)
    y = df[settings.TARGET_FEATURE]

    model = LogisticRegression(**regression_params)
    model.fit(X=X, y=y)

    # Assign feature names to the model.
    model.feature_names = X.columns.tolist()

    return model