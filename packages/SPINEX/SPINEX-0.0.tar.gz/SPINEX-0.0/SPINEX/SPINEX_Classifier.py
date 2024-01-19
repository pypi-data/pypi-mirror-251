import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import AdaBoostClassifier, StackingClassifier, BaggingClassifier
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
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils import check_X_y, check_array


from data_preprocessor import DataPreprocessor


class SPINEXClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, n_neighbors=5, distance_threshold=0.05, distance_threshold_decay=0.95, ensemble_method=None, preprocessor=None, metric='euclidean'):
        self.n_neighbors = n_neighbors
        self.distance_threshold = distance_threshold
        self.distance_threshold_decay = distance_threshold_decay
        self.ensemble_method = ensemble_method
        self.preprocessor = preprocessor
        self.metric = metric
        self.feature_combination_size = None
        self.X_train_ = None
        self.y_train_ = None
        self.eps = 1e-8
    
    def fit(self, X, y, sample_weight=None):
        X, y = check_X_y(X, y)
        self.classes_ = np.unique(y)
        self.X_train_ = X
        self.y_train_ = y

        one_hot_encoder = OneHotEncoder(sparse_output=False)
        self.y_train_one_hot_ = one_hot_encoder.fit_transform(y.reshape(-1, 1))

        self.class_prior_ = np.bincount(y) / len(y)

        if self.ensemble_method == 'bagging':
            self.model_ = BaggingClassifier(estimator=SPINEXClassifier(ensemble_method=None),
                                            n_estimators=10, random_state=42)
        elif self.ensemble_method == 'boosting':
            self.model_ = AdaBoostClassifier(estimator=SPINEXClassifier(ensemble_method=None),
                                             n_estimators=10, random_state=42)
        elif self.ensemble_method == 'stacking':
            estimators = [('spinex1', SPINEXClassifier(ensemble_method=None)), 
                          ('spinex2', SPINEXClassifier(ensemble_method=None))]
            self.model_ = StackingClassifier(estimators=estimators, 
                                             final_estimator=LogisticRegression())
        else:
            self.model_ = None

        if self.model_ is not None:
            self.model_.fit(X, y, sample_weight)

        return self

    def _calculate_feature_combination_distances(self, instances, train_instances):
        # Calculate the distances between instances and train_instances based on feature combinations
        feature_combinations = list(combinations(range(min(train_instances.shape[1], instances.shape[1])), self.feature_combination_size))
        distances = np.zeros((instances.shape[0], train_instances.shape[0]))
        for comb in feature_combinations:
            comb_distance = np.sqrt(np.sum((train_instances[:, comb] - instances[:, comb][:, np.newaxis]) ** 2, axis=-1))
            distances += comb_distance
        overall_distance = distances / len(feature_combinations)
        return overall_distance

    def calculate_weights(self, distances):
        # Compute the weights based on the distances using the Gaussian kernel function
        sigma = np.mean(distances)
        weights = np.exp(-distances ** 2 / (2 * sigma ** 2))
        return weights

    def predict_proba(self, X):
        if self.preprocessor:
            X = self.preprocessor.auto_select_features(X)

        if self.model_ is not None:
            probabilities = self.model_.predict_proba(X)
        else:
            distances = pairwise_distances(X, self.X_train_, metric=self.metric)
            nearest_indices = np.argpartition(distances, self.n_neighbors, axis=1)[:, :self.n_neighbors]
            decayed_distance_threshold = self.distance_threshold * self.distance_threshold_decay
            nearest_distances = distances[np.arange(distances.shape[0])[:, None], nearest_indices]
            weights = 1 / (nearest_distances + decayed_distance_threshold)

            weights = weights[:, :, None]  # Add an extra dimension to match with y_train_one_hot_
            weighted_votes = self.y_train_one_hot_[nearest_indices] * weights
            weighted_votes = np.sum(weighted_votes, axis=1)  # Sum across the n_neighbors axis

            # Normalize the weighted votes to obtain probabilities
            probabilities = weighted_votes / np.sum(weighted_votes, axis=1, keepdims=True)

        return probabilities

    def predict(self, X):
        if self.preprocessor:
            X = self.preprocessor.auto_select_features(X)

        distances = pairwise_distances(X, self.X_train_, metric=self.metric)
        nearest_indices = np.argpartition(distances, self.n_neighbors, axis=1)[:, :self.n_neighbors]
        decayed_distance_threshold = self.distance_threshold * self.distance_threshold_decay
        nearest_distances = distances[np.arange(distances.shape[0])[:, None], nearest_indices]
        weights = 1 / (nearest_distances + decayed_distance_threshold)

        weights = weights[:, :, None]
        weighted_votes = self.y_train_one_hot_[nearest_indices] * weights
        weighted_votes = np.sum(weighted_votes, axis=1)

        weighted_votes = np.atleast_2d(weighted_votes)

        if self.model_ is not None:
            predictions = self.model_.predict(X)
        else:
            predictions = self.classes_[np.argmax(weighted_votes, axis=1)]

        return predictions

    def predict_contributions(self, X, instances_to_predict=None):
        if instances_to_predict is None:
            instances_to_predict = range(X.shape[0])

        # Use only selected features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Calculate overall predictions (probability) for selected instances
        final_probabilities = self.predict_proba(X[instances_to_predict])

        # Define a function to calculate contributions for each feature
        def compute_contributions(i):
            # Prediction with the feature excluded (set to zero or mean value)
            X_excluded = X.copy()
            X_excluded[:, i] = 0  # You may replace this with mean imputation
            excluded_probabilities = self.predict_proba(X_excluded[instances_to_predict])

            # Contribution of the feature
            feature_contributions = final_probabilities - excluded_probabilities
            return feature_contributions

        # Calculate contributions for each feature in parallel
        with ThreadPoolExecutor() as executor:
            contributions = list(executor.map(compute_contributions, range(X.shape[1])))

        # Calculate pairwise interaction effects
        interaction_effects = []
        for i in range(X.shape[1]):
            interaction_effects_row = []
            for j in range(X.shape[1]):
                if i == j:
                    interaction_effects_row.append(np.zeros_like(final_probabilities))
                    continue
                # Interaction effect of features i and j
                interaction_effect = final_probabilities - contributions[i] - contributions[j]
                interaction_effects_row.append(interaction_effect)
            interaction_effects.append(interaction_effects_row)

        # Combine interaction effects into an array
        interaction_effects = np.array(interaction_effects, dtype=object)

        return final_probabilities, np.array(contributions), interaction_effects

    def get_feature_importance(self, X, instances_to_explain=None):
        """Get feature importance and interaction effects for the given instances."""
        if instances_to_explain is None:
            instances_to_explain = range(X.shape[0])
        
        # Use only selected features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Contribution of each feature to the model's predictions for each instance
        predictions, contributions, interaction_effects = self.predict_contributions(X)
        # Calculate the contribution of each feature
        feature_importances = np.mean(np.abs(contributions), axis=(1, 2))

        # Calculate the interaction effects
        interaction_effects = np.zeros((X.shape[1], X.shape[1]))
        for i in range(X.shape[1]):
            for j in range(i+1, X.shape[1]):
                interaction_effect = np.mean(np.abs(predictions - contributions[:, i] - contributions[:, j]), axis=0)
                interaction_effects[i, j] = interaction_effect
                interaction_effects[j, i] = interaction_effect

        return feature_importances, interaction_effects

    def get_global_interaction_effects(self, X, instances_to_explain=None):
        """Get the average interaction effects for the given instances."""
        if instances_to_explain is None:
            instances_to_explain = range(X.shape[0])
        
        # Use only selected features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Contribution of each feature to the model's predictions for each instance
        predictions, contributions, _ = self.predict_contributions(X)

        # Calculate the interaction effects
        avg_interaction_effects = np.zeros((X.shape[1], X.shape[1]))
        for i in range(X.shape[1]):
            for j in range(i+1, X.shape[1]):
                # Interaction effect of features i and j for each class
                interaction_effect_per_class = np.abs(predictions - contributions[i] - contributions[j])
                # Average interaction effect across classes and samples
                interaction_effect = np.mean(interaction_effect_per_class)
                avg_interaction_effects[i, j] = interaction_effect
                avg_interaction_effects[j, i] = interaction_effect

        return avg_interaction_effects

    def feature_combination_impact_analysis(self, X):
        # Use only selected or prioritized features
        selected_features = self.X_train_.shape[1]
        X = X[:, :selected_features]

        # Calculate the base predictions (probability) for the entire dataset
        base_probabilities = self.predict_proba(X)

        # Initialize an empty dictionary to store the impact of each feature combination
        feature_combination_impact = {}

        # Define a function to calculate the impact of a feature combination
        def compute_combination_impact(comb):
            # Exclude features in the current combination and calculate new predictions (probability)
            X_excluded = X.copy()
            X_excluded[:, comb] = 0  # You may replace this with mean imputation
            excluded_probabilities = self.predict_proba(X_excluded)

            # Calculate the impact of the current feature combination
            impact = np.mean(np.abs(base_probabilities - excluded_probabilities))
            return comb, impact

        # Iterate over possible feature combinations in parallel
        n_features = X.shape[1]
        with ThreadPoolExecutor() as executor:
            for combination_size in range(1, n_features + 1):
                all_combinations = itertools.combinations(range(n_features), combination_size)
                impacts = executor.map(compute_combination_impact, all_combinations)
                # Store the impact of each feature combination
                feature_combination_impact.update(impacts)

        # Sort feature combinations by their impact
        sorted_combinations = sorted(feature_combination_impact.items(), key=lambda x: x[1], reverse=True)

        return sorted_combinations

    def get_params(self, deep=True):
        return {
            'n_neighbors': self.n_neighbors,
            'distance_threshold': self.distance_threshold,
            'distance_threshold_decay': self.distance_threshold_decay,
            'ensemble_method': self.ensemble_method,
            'preprocessor': self.preprocessor,  # Data preprocessor instance
            'metric': self.metric
        }

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
