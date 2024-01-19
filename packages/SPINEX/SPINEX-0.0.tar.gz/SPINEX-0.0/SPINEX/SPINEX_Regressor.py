import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import BaggingRegressor, AdaBoostRegressor, GradientBoostingRegressor, StackingRegressor
from scipy import stats
import math
from scipy import stats
from sklearn.impute import SimpleImputer
import itertools
from itertools import combinations
import pickle
from sklearn.feature_selection import SelectFromModel, SequentialFeatureSelector
from scipy.spatial import distance
from sklearn.metrics import pairwise_distances, r2_score
from sklearn.metrics.pairwise import euclidean_distances
from concurrent.futures import ThreadPoolExecutor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils import check_X_y, check_array
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score, make_scorer, roc_auc_score, log_loss, accuracy_score
from sklearn.linear_model import ElasticNet
from scipy.spatial.distance import cdist
from sklearn.base import clone
from joblib import Parallel, delayed


class SPINEXRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, n_neighbors=5, distance_threshold=0.05, distance_threshold_decay=0.95, ensemble_method='None',
                 n_features_to_select=None, auto_select_features=False,
                 use_local_search=False, prioritized_features=None,
                 missing_data_method='mean_imputation', outlier_handling_method='z_score_outlier_handling',
                 exclude_method='zero'):
        self.n_neighbors = n_neighbors
        self.distance_threshold = distance_threshold
        self.distance_threshold_decay = distance_threshold_decay
        self.ensemble_method = ensemble_method
        self.n_features_to_select = n_features_to_select
        self.auto_select_features = auto_select_features
        self.use_local_search = use_local_search
        self.prioritized_features = prioritized_features
        self.missing_data_method = missing_data_method
        self.outlier_handling_method = outlier_handling_method
        self.exclude_method = exclude_method
        self.feature_combination_size = None
        self.X_train_ = None
        self.y_train_ = None
        self.eps = 1e-8
        self.feature_combinations = None
        self.internal_call = False  # Initialize the flag as False
        self.model = None

    def _auto_select_features(self, X, y):
        selected_features = None

        if self.use_local_search:
            # Local search feature selection logic
            model = LinearRegression()
            # Set n_features_to_select='auto' and tol=None to avoid the warning
            n_features_to_select = 'auto' if self.n_features_to_select is None else self.n_features_to_select
            sfs = SequentialFeatureSelector(model, n_features_to_select=n_features_to_select,
                                            direction='forward', scoring='neg_mean_squared_error', tol=None)
            if y is not None:
                sfs.fit(X, y)
            X_new = sfs.transform(X)
            selected_features = sfs.get_support(indices=True)

        elif self.n_features_to_select is not None and not self.use_local_search:
            correlations = np.abs(np.corrcoef(X, y, rowvar=False)[-1, :-1])
            top_feature_indices = np.argsort(correlations)[-self.n_features_to_select:]
            X_new = X[:, top_feature_indices]
            selected_features = top_feature_indices

        else:
            X_new = X

        return X_new, selected_features

    def fit(self, X, y):
        # External call: Apply ensemble logic (if specified) and train the model
        if not self.internal_call:
            # Perform feature selection if auto_select_features is True
            if self.auto_select_features:
                X, self.selected_features_ = self._auto_select_features(X, y)

            # Set the training data attributes
            self.X_train_ = X.copy()
            self.y_train_ = y.copy()

            # Dynamically determine the feature combination size (n) based on the number of features
            n_features = X.shape[1]
            self.feature_combination_size = math.ceil(n_features / 2)

            # Ensure that the combination size does not exceed the number of features
            self.feature_combination_size = min(self.feature_combination_size, n_features)
            self.feature_combinations = list(combinations(range(min(self.X_train_.shape[1], X.shape[1])), self.feature_combination_size))

            if self.ensemble_method == 'bagging':
                base_model = SPINEXRegressor(auto_select_features=self.auto_select_features, ensemble_method='None')  # Set other parameters as needed
                self.model = BaggingRegressor(estimator=base_model, n_estimators=10, random_state=42)
                self.internal_call = True  # Set the flag to True for internal call
                self.model.fit(X, y)
                self.internal_call = False  # Set the flag back to False for future external calls
            elif self.ensemble_method == 'boosting':
                base_model = SPINEXRegressor(auto_select_features=self.auto_select_features, ensemble_method='None')  # Set other parameters as needed
                self.model = AdaBoostRegressor(estimator=base_model, n_estimators=10, random_state=42)
                self.internal_call = True  # Set the flag to True for internal call
                self.model.fit(X, y)
                self.internal_call = False  # Set the flag back to False for future external calls
            elif self.ensemble_method == 'stacking':
                estimators = [('model1', SPINEXRegressor(ensemble_method='None')),
                              ('model2', SPINEXRegressor(ensemble_method='None'))]
                meta_estimator = ElasticNet()
                self.model = StackingRegressor(estimators=estimators, final_estimator=meta_estimator)
                self.internal_call = True  # Set the flag to True for internal call
                self.model.fit(X, y)
                self.internal_call = False  # Set the flag back to False for future external calls
            else:
                # No ensemble case (use SPINEX directly)
                self.model = None
                # Include the fitting logic directly here
                # Use the existing logic from your original fit method
                # ...
        return self

    def _calculate_feature_combination_distances(self, instances, train_instances):
        def calculate_combination_distance(comb):
            #comb_distance = np.sqrt(np.sum((train_instances[:, comb] - instances[:, comb][:, np.newaxis]) ** 2, axis=-1)) Euclidean 
            comb_distance = np.sum(np.abs(train_instances[:, comb] - instances[:, comb][:, np.newaxis]), axis=-1) #Manhattan
            return comb_distance

        distances = np.zeros((instances.shape[0], train_instances.shape[0]))

        # Parallelize the loop
        comb_distances = Parallel(n_jobs=-1)(delayed(calculate_combination_distance)(comb) for comb in self.feature_combinations)

        for comb_distance in comb_distances:
            distances += comb_distance

        overall_distance = distances / len(self.feature_combinations)
        return overall_distance

    def predict(self, X):
        # Check types and shapes
        assert isinstance(X, np.ndarray)
        assert len(X.shape) == 2
        assert isinstance(self.y_train_, np.ndarray)
        assert len(self.y_train_.shape) == 1
        
        # Check if ensemble logic was applied
        if self.model is not None:
            if self.auto_select_features:
                X = X[:, self.selected_features_]  # Use the ensemble model for prediction
            predictions = self.model.predict(X)
        else:
            # No ensemble case (use SPINEX directly)
            # Calculate distances based on feature combinations for all instances in X
            distances = self._calculate_feature_combination_distances(X, self.X_train_)
            # Find the indices of the k-nearest neighbors for all instances in X
            sorted_indices = np.argsort(distances, axis=1)
            nearest_indices = sorted_indices[:, :self.n_neighbors]
            # Calculate the weighted average of the target values of nearest neighbors
            nearest_distances = np.take_along_axis(distances, nearest_indices, axis=1)
            # Apply distance threshold decay
            decayed_distance_threshold = self.distance_threshold * self.distance_threshold_decay
            weights = 1 / (nearest_distances + decayed_distance_threshold)
            nearest_targets = self.y_train_[nearest_indices]
            predictions = np.sum(nearest_targets * weights, axis=1) / np.sum(weights, axis=1)

        # Ensure predictions is a 1D array
        predictions = np.atleast_1d(predictions)
        assert len(predictions.shape) == 1
        return predictions

    def predict_contributions(self, X, instances_to_predict=None):
        if instances_to_predict is None:
            instances_to_predict = range(X.shape[0])
        
        # Use only selected features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Check if ensemble logic was applied
        if self.model is not None:
            contributions = []
            for estimator in self.model.estimators_:
                _, est_contributions, _ = estimator.predict_contributions(X[instances_to_predict])
                contributions.append(est_contributions)
            contributions = np.mean(contributions, axis=0)
            return contributions
        else:

            # Make overall predictions for selected instances
            final_predictions = self.predict(X[instances_to_predict])

        # Calculate feature contributions
        contributions = []
        for i in range(X.shape[1]):
            # Prediction with the feature excluded (set to zero or mean value)
            X_excluded = X.copy()
            X_excluded[:, i] = 0  # You may replace this with mean imputation
            excluded_predictions = self.predict(X_excluded[instances_to_predict])

            # Contribution of the feature
            feature_contributions = final_predictions - excluded_predictions
            contributions.append(feature_contributions)

        # Combine contributions into an array
        contributions = np.array(contributions).T

        # Calculate pairwise interaction effects
        interaction_effects = []
        for i in range(X.shape[1]):
            interaction_effects_row = []
            for j in range(X.shape[1]):
                if i == j:
                    interaction_effects_row.append(0)
                    continue
                # Prediction with both features i and j excluded
                X_excluded = X.copy()
                X_excluded[:, i] = 0
                X_excluded[:, j] = 0
                excluded_predictions = self.predict(X_excluded[instances_to_predict])

                # Interaction effect of features i and j
                interaction_effect = final_predictions - excluded_predictions - contributions[:, i] - contributions[:, j]
                interaction_effects_row.append(interaction_effect)
            interaction_effects.append(interaction_effects_row)

        # Combine interaction effects into an array
        interaction_effects = np.array(interaction_effects, dtype=object)

        return final_predictions, contributions, interaction_effects

    def get_feature_importance(self, X, instances_to_explain=None):
        if instances_to_explain is None:
            instances_to_explain = range(X.shape[0])
        
        # Use only selected features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Check if ensemble logic was applied
        if self.model is not None:
            feature_importances = []
            interaction_effects_list = []
            for estimator in self.model.estimators_:
                # Get feature importances and interaction effects for each base estimator
                est_importances, est_interaction_effects = estimator.get_feature_importance(X, instances_to_explain)
                feature_importances.append(est_importances)
                interaction_effects_list.append(est_interaction_effects)
            return feature_importances, interaction_effects_list
        else:
            # Contribution of each feature to the model's predictions for each instance
            predictions, contributions, interaction_effects = self.predict_contributions(X)

            # Calculate the contribution of each feature
            feature_importances = np.mean(np.abs(contributions), axis=0)

            # Calculate the interaction effects
            interaction_effects = np.zeros((X.shape[1], X.shape[1]))
            for i in range(X.shape[1]):
                for j in range(i+1, X.shape[1]):
                    interaction_effect = np.mean(predictions - contributions[:, i] - contributions[:, j])
                    interaction_effects[i, j] = interaction_effect
                    interaction_effects[j, i] = interaction_effect

            return feature_importances, interaction_effects

    def _handle_missing_data(self, X, y):
        if self.missing_data_method == 'mean_imputation':
            col_means = np.nanmean(X, axis=0)
            return np.where(np.isnan(X), col_means, X), y  # Return y unchanged
        elif self.missing_data_method == 'deletion':
            not_missing = ~np.isnan(X).any(axis=1)
            return X[not_missing], y[not_missing]
        else:
            raise ValueError("Unsupported missing_data_method. Please use 'mean_imputation' or 'deletion'.")

    def _handle_outliers(self, X, y):
        if self.outlier_handling_method == 'z_score_outlier_handling':
            z_scores = np.abs(stats.zscore(X))
            not_outliers = (z_scores < 3).all(axis=1)
            return X[not_outliers], y[not_outliers]
        elif self.outlier_handling_method == 'iqr_outlier_handling':
            Q1 = np.percentile(X, 25, axis=0)
            Q3 = np.percentile(X, 75, axis=0)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            not_outliers = np.logical_and(X >= lower_bound, X <= upper_bound).all(axis=1)
            return X[not_outliers], y[not_outliers]
        else:
            raise ValueError("Unsupported outlier_handling_method. Please use 'z_score_outlier_handling' or 'iqr_outlier_handling'.")

    def get_global_interaction_effects(self, X):
        # Use only selected or prioritized features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Check if ensemble logic was applied
        if self.model is not None:
            avg_interaction_effects_list = []
            for estimator in self.model.estimators_:
                # Get average interaction effects for each base estimator
                est_avg_interaction_effects = estimator.get_global_interaction_effects(X)
                avg_interaction_effects_list.append(est_avg_interaction_effects)
            return avg_interaction_effects_list
        else:
            # Calculate the contribution of each feature to the model's predictions for the entire dataset
            predictions, contributions, interaction_effects = self.predict_contributions(X)

            # Calculate the average interaction effects for all pairs of features
            avg_interaction_effects = np.zeros((X.shape[1], X.shape[1]))
            for i in range(X.shape[1]):
                for j in range(i+1, X.shape[1]):
                    # Interaction effect of features i and j
                    interaction_effect = np.mean(interaction_effects[i][j])
                    avg_interaction_effects[i, j] = interaction_effect
                    avg_interaction_effects[j, i] = interaction_effect

            return avg_interaction_effects

    def feature_combination_impact_analysis(self, X):
        # Use only selected or prioritized features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Check if ensemble logic was applied
        if self.model is not None:
            feature_combination_impact_list = []
            for estimator in self.model.estimators_:
                # Get feature combination impact analysis for each base estimator
                est_feature_combination_impact = estimator.feature_combination_impact_analysis(X)
                feature_combination_impact_list.append(est_feature_combination_impact)
            return feature_combination_impact_list
        else:
            def calculate_combination_impact(comb, X, base_predictions, model):
                X_excluded = X.copy()
                X_excluded[:, comb] = 0  # You may replace this with mean imputation
                excluded_predictions = model.predict(X_excluded)
                impact = np.mean(np.abs(base_predictions - excluded_predictions))
                return comb, impact

            # Calculate the base predictions for the entire dataset
            base_predictions = self.predict(X)

            # Initialize an empty dictionary to store the impact of each feature combination
            feature_combination_impact = {}

            # Iterate over possible feature combinations
            n_features = X.shape[1]

            # Parallelize the loop
            combination_impacts = Parallel(n_jobs=-1)(delayed(calculate_combination_impact)(comb, X, base_predictions, self) for comb in itertools.chain.from_iterable(
                itertools.combinations(range(n_features), combination_size) for combination_size in range(1, n_features + 1)))

            # Sort feature combinations by their impact
            sorted_combinations = sorted(combination_impacts, key=lambda x: x[1], reverse=True)

            return sorted_combinations


    def get_params(self, deep=True):
        return {
            'n_neighbors': self.n_neighbors,                          #The number of nearest neighbors to consider in the SPINEX model. It determines how many neighbors to use when making predictions.
            'distance_threshold': self.distance_threshold,
            'distance_threshold_decay':self.distance_threshold_decay,
            'ensemble_method': self.ensemble_method,                #The ensemble method to use. It can be set to "bagging", "boosting", or None. Bagging and boosting are ensemble techniques that combine multiple base models to improve prediction accuracy.
            'n_features_to_select': self.n_features_to_select,        #The number of features to select when auto_select_features is set to True. It specifies how many features to retain during automatic feature selection.
            'auto_select_features': self.auto_select_features,        #A boolean flag indicating whether to automatically select features. If True, the model will automatically select a subset of features based on their importance.
            'use_local_search': self.use_local_search,                #A boolean flag indicating whether to use local search for feature selection. If True, the model will perform a local search to find the best subset of features.
            'prioritized_features': self.prioritized_features,        #A list of prioritized features. If auto_select_features is False, the model will only consider the features specified in this list.
            'missing_data_method': self.missing_data_method,          #The method for handling missing data. It can be set to "mean_imputation" or "deletion".
            'outlier_handling_method': self.outlier_handling_method,  #The method for handling outliers. It can be set to "z_score_outlier_handling" or "iqr_outlier_handling".
            'exclude_method': self.exclude_method                     #The method for excluding features when calculating contributions. It can be set to "zero" or "mean".
        }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

def imputation(X, statistic='mean'):
    """
    Fill missing values with a given statistic (mean, median, or mode).
    
    Parameters:
    X (np.array): Input data.
    statistic (str): The statistic to use for imputation. Options: 'mean', 'median', 'mode'. Default is 'mean'.
    
    Returns:
    np.array: The array with missing values replaced.
    """
    # Input validation
    assert isinstance(X, np.ndarray), "Input data should be a numpy array."
    assert statistic in ['mean', 'median', 'mode'], "Invalid statistic. Choose from 'mean', 'median', 'mode'."

    # Compute the chosen statistic
    if statistic == 'mean':
        stat_values = np.nanmean(X, axis=0)
    elif statistic == 'median':
        stat_values = np.nanmedian(X, axis=0)
    elif statistic == 'mode':
        stat_values = stats.mode(X, nan_policy='omit').mode
    
    # Return the array with missing values replaced
    return np.where(np.isnan(X), stat_values, X)


def deletion(X, y, missing_values=np.nan):
    """
    Removes rows in both X and y where X has missing values.

    Parameters:
    X (np.array): Input features.
    y (np.array): Target variable.
    missing_values: The values to be considered as "missing". Default is np.nan.

    Returns:
    Tuple[np.array, np.array]: Tuple of arrays (X, y) with rows containing missing values removed.
    """
    # Input validation
    assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray), "X and y should be numpy arrays."

    not_missing = ~np.isnan(X).any(axis=1)
    return X[not_missing], y[not_missing]


def z_score_outlier_handling(X, y, threshold=3):
    """
    Removes outliers from X and y using Z-score method.

    Parameters:
    X (np.array): Input features.
    y (np.array): Target variable.
    threshold (float): The Z-score threshold to use for detecting outliers. Default is 3.

    Returns:
    Tuple[np.array, np.array]: Tuple of arrays (X, y) with outliers removed.
    """
    # Input validation
    assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray), "X and y should be numpy arrays."
    assert threshold > 0, "Threshold should be a positive number."

    z_scores = np.abs(stats.zscore(X))
    not_outliers = (z_scores < threshold).all(axis=1)
    return X[not_outliers], y[not_outliers]


def iqr_outlier_handling(X, y, k=1.5):
    """
    Removes outliers from X and y using IQR method.

    Parameters:
    X (np.array): Input features.
    y (np.array): Target variable.
    k (float): The multiplier for IQR. Default is 1.5.

    Returns:
    Tuple[np.array, np.array]: Tuple of arrays (X, y) with outliers removed.
    """
    # Input validation
    assert isinstance(X, np.ndarray) and isinstance(y, np.ndarray), "X and y should be numpy arrays."
    assert k > 0, "k should be a positive number."

    Q1 = np.percentile(X, 25, axis=0)
    Q3 = np.percentile(X, 75, axis=0)
    IQR = Q3 - Q1
    lower_bound = Q1 - k * IQR
    upper_bound = Q3 + k * IQR
    not_outliers = np.logical_and(X >= lower_bound, X <= upper_bound).all(axis=1)
    return X[not_outliers], y[not_outliers]


def normalize_importances(importances):
    return importances / np.sum(importances)