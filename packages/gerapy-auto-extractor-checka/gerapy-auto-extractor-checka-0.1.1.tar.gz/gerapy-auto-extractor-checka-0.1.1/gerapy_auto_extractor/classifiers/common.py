
model_name = ["rf", "svm", "adaboost", "xgboost"]
# model_name = ["rf", "svm", "adaboost"]
# model_name = ["rf", "svm"]
# model_name = ["xgboost"]
# model_name = ["svm"]

param_grid = {}
param_grid["rf"] = {
    'n_estimators': [100, 200, 300],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [4, 5, 6, 7, 8],
    'criterion': ['gini', 'entropy']
}
param_grid["svm"] = {
    'C': [0.1, 1, 10, 100], 
    'gamma': [1, 0.1, 0.01, 0.001],
    'kernel': ['linear', 'rbf', 'poly']
}
param_grid["adaboost"] = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 1]
}
param_grid["xgboost"] = {
    'n_estimators': [100, 200, 300],
    # 'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1, 0.2, 0.3],
    'max_depth': [3, 4, 5],
    'min_child_weight': [1, 2, 3],
    # 'min_child_weight': [1, 2],
    'gamma': [0, 0.1, 0.2],
    # 'gamma': [0, 0.1],
    'subsample': [0.8, 0.9, 1]
}