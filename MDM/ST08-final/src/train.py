# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 09:21:48 2020

@author: pvillalba
"""

from z_utils.PCA import PCA
import pandas as pd
import pickle
import os
import sys

def train(json_data,
          s_model, 
          predictors=None,
          categoricals=None,
          n_components=-1,
          n_comp_criteria=0.95,
          scale=True,
          cleansing = 'extreme',
          algorithm='SVD',
          tol_variance_filter=1e-05):
    """Principal Component Analysis training

    Parameters
    ----------
    json_data : str
        A JSON with data to train.

    s_model: str
        The path where the model will be stored.

    predictors : list, optional (default=None)
        The list of variables to take into account for model training.

    categoricals : list, optional (default=None)
        The list of categorical variables.

    n_components : int, optional (default=-1)
        If -1 the components will be computed automatically
        If >0 the model will be fit with n_components

    n_comp_criteria : float or string, optional (default=0.9)
        Criteria for the selection of the number of components:
            - If it is a number between [0,1] it specifies the minimum value of
              R2 that the model must achieve. That is, the model must have the 
              minimum number of components that give the specified value of R2
            - If it is "Q2" then the number of components will be computed
              automatically by corss-validation based on Q2 "evolution"

    scale : boolean, optional (default=True)
        Wether to scale to unit variance and zero-mean or not

    cleansing : string, optional (default='none')
        Must be one of the following:
            'none': no data cleansing is done at all
            'extreme': remove obs with SPE (or T2) greater than 3*UCL
            'full': remove obs with SPE (or T2) greater than 3*UCL and remove 
                    highest values in SPE (or T2) until having a 5% of 
                    out-of-control observations

    algorithm : string, optional (default='SVD')
        Algorithm to compute PCA. Must be one of the following:
            'SVD': Singular Value Decomposition
            'NIPALS': Nonlinear Iterative Partial Least Squares
        With SVD all the components must be calculated even though the higher
        ones are not needed, while NIPALS computes the components iteratively.
        SVD is usually faster for little datasets and NIPALS is more suitable
        for large datasets

    tol_variance_filter: float, optional (default=1e-05)
        Removes features with coefficient of variation less than 
        tol_variance_filter. This avoids problems with constant features or 
        features with low variance which are not useful for the model
        
    Returns
    ----------
        List that contains error info if any error occurs, null otherwise
        R-squared of the predictions

    """
    
    # Read data
    s_error = []
    R2 = []
    try:
        df = pd.read_json(json_data)
        df.fillna(0, inplace=True)
        if predictors:
            df = df[predictors]
        else:
            predictors = df.columns.values.tolist()
        if categoricals:
            # ensure that variables are of "category" class
            for col in categoricals:
                df[col] = df[col].astype('category')
        # Train PCA model
        pca_model = PCA(n_components=n_components, 
                        n_comp_criteria=n_comp_criteria, 
                        scale=scale, 
                        cleansing=cleansing, 
                        algorithm=algorithm,
                        tol_variance_filter=tol_variance_filter)
        pca_model.fit(data=df)
        # Save model
        with open(s_model, 'wb') as file:
            pickle.dump(pca_model, file)
        R2 = pca_model.R2[pca_model.A-1]
            
    except:
        # Get error description
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        s_error = [exc_type, exc_obj, fname, exc_tb.tb_lineno]

    return s_error, R2
