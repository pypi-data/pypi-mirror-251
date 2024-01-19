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
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, r2_score, make_scorer, roc_auc_score, log_loss, accuracy_score



class DataPreprocessor:
    def __init__(self, n_features_to_select=None, use_auto_select_features=False,
                 use_local_search=False, prioritized_features=None,
                 missing_data_method='mean_imputation', outlier_handling_method='z_score_outlier_handling',
                 exclude_method='zero', random_state=None):  # Add random_state parameter
        self.n_features_to_select = n_features_to_select
        self.use_auto_select_features = use_auto_select_features
        self.use_local_search = use_local_search
        self.prioritized_features = prioritized_features
        self.missing_data_method = missing_data_method
        self.outlier_handling_method = outlier_handling_method
        self.exclude_method = exclude_method
        self.random_state = random_state  # Set random_state as instance variable
        self.selected_features_ = None  # Initialize the attribute 

    def fit(self, X, y):
        if self.use_auto_select_features:
            # Define the feature selection model
            model = LogisticRegression(random_state=self.random_state)  # Use the random_state attribute
            # Set n_features_to_select to 'auto' if self.n_features_to_select is None
            n_features_to_select = 'auto' if self.n_features_to_select is None else self.n_features_to_select
            # Fit the SequentialFeatureSelector
            self.feature_selector_ = SequentialFeatureSelector(
                model, n_features_to_select=n_features_to_select, direction='forward', scoring='accuracy', tol=None
            )
            self.feature_selector_.fit(X, y)

    def auto_select_features(self, X, y=None):
        # If use_auto_select_features is True, transform the data using the stored feature selector
        if self.use_auto_select_features:
            X = self.feature_selector_.transform(X)
            self.selected_features_ = self.feature_selector_.get_support(indices=True)
        
        # If prioritized_features are provided, validate indices and select only those features
        if self.prioritized_features is not None:
            # Get the total number of features in the transformed matrix
            total_features = X.shape[1]
            
            # Validate indices and filter out invalid ones
            valid_indices = [idx for idx in self.prioritized_features if idx < total_features]
            
            # Select features using valid indices
            X = X[:, valid_indices]
            self.selected_features_ = np.array(valid_indices)
            
            # Add this line to print the selected_features_ attribute after it is updated
            print(f"Updated selected_features_: {self.selected_features_}")
            
            # Store the selected feature indices
            self.selected_features_ = valid_indices
            
        # Local search feature selection logic (only run if 'y' is provided during training)
        if self.use_local_search and y is not None:  # Check if 'y' is provided
            model = LogisticRegression()
            
            # Set n_features_to_select to 'auto' if self.n_features_to_select is None
            n_features_to_select = 'auto' if self.n_features_to_select is None else self.n_features_to_select
            
            # Pass n_features_to_select to SequentialFeatureSelector
            sfs = SequentialFeatureSelector(model, n_features_to_select=n_features_to_select,
                                            direction='forward', scoring='accuracy', tol=None)
            
            sfs.fit(X, y)  # Use the 'y' parameter
            X = sfs.transform(X)  # Update the X variable with the selected features
            self.selected_features_ = sfs.get_support(indices=True)  # Store the selected feature indices

        # Correlation-based feature selection logic (skip during prediction)
        elif self.n_features_to_select is not None and not self.use_local_search and y is not None:
            correlations = np.abs(np.corrcoef(X, y, rowvar=False)[-1, :-1])
            top_feature_indices = np.argsort(correlations)[-self.n_features_to_select:]
            X = X[:, top_feature_indices]
            
        return X
    
    def mean_imputation(self, X):
        col_means = np.nanmean(X, axis=0)
        return np.where(np.isnan(X), col_means, X)

    def deletion(self, X, y, missing_values=np.nan):
        not_missing = ~np.isnan(X).any(axis=1)
        return X[not_missing], y[not_missing]

    def z_score_outlier_handling(self, X, y, threshold=3):
        z_scores = np.abs(stats.zscore(X))
        not_outliers = (z_scores < threshold).all(axis=1)
        return X[not_outliers], y[not_outliers]

    def iqr_outlier_handling(self, X, y, k=1.5):
        Q1 = np.percentile(X, 25, axis=0)
        Q3 = np.percentile(X, 75, axis=0)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        not_outliers = np.logical_and(X >= lower_bound, X <= upper_bound).all(axis=1)
        return X[not_outliers], y[not_outliers]

    def handle_missing_data(self, X, y):
        if self.missing_data_method == "mean_imputation":
            return self.mean_imputation(X), y  # y is unchanged
        elif self.missing_data_method == "deletion":
            return self.deletion(X, y)
        elif self.missing_data_method == "none":  # add this condition
            return X, y  # return the data as is
        else:
            raise ValueError("Unsupported missing_data_method. Please use 'mean_imputation', 'deletion' or 'none'.")

    def handle_outliers(self, X, y):
        if self.outlier_handling_method == "z_score_outlier_handling":
            return self.z_score_outlier_handling(X, y)
        elif self.outlier_handling_method == "iqr_outlier_handling":
            return self.iqr_outlier_handling(X, y)
        elif self.outlier_handling_method == "none":  # add this condition
            return X, y  # return the data as is
        else:
            raise ValueError("Unsupported outlier_handling_method. Please use 'z_score_outlier_handling', 'iqr_outlier_handling', or 'none'.")

