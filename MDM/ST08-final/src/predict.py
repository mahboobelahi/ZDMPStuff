# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 09:22:28 2020

@author: pvillalba
"""

import pandas as pd
import pickle
import json

def predict(json_data,s_model):
    """Principal Component Analysis predictions

    Parameters
    ----------
    json_data : str
        A JSON with data to predict.

    s_model: str
        The path where the model is stored.
    
        
    Returns
    ----------
        A JSON with the following information:
            "result": wether the observation is 'Under control', 'Anomaly (SPE)',
                      'Anomaly (T2)', 'Anomaly (SPE+T2)'
            "payload": contains the following fields:
                "UCL_SPE": Upper Control Limit for Squared Prediction Error
                "SPE": value of Squared Prediction Error
                "SPE_contrib": dictionary with SPE contributions (one per variable)
                "UCL_T2": Upper Control Limit for T2 Hotelling statistic
                "T2": value of T2 Hotelling statistic
                "T2_contrib": dictionary with T2 contributions (one per variable)
        
    """

    # Load model
    with open(s_model, 'rb') as file:
        model = pickle.load(file)
    # Load data
    df = pd.DataFrame(json_data, index=[0])
    # We will assume that the first column is the index, that should be a timestamp
    df.set_index(df.columns.values[0], inplace=True)
    df.fillna(0, inplace=True)    
    # Make predictions
    pred = model.predict(data=df)

    # Check if observation is inside control limits
    SPE = pred.SPE[0]
    T2 = pred.T2[0]
    # Get control limits ...
    UCL_SPE = model.UCL_SPE[0]
    UCL_T2 = model.UCL_T2[0]
    # Check if it is under control ...
    if SPE>UCL_SPE and T2>UCL_T2:
        s_result = 'Anomaly (SPE+T2)'
    elif SPE>UCL_SPE:
        s_result = 'Anomaly (SPE)'
    elif T2>UCL_T2:
        s_result = 'Anomaly (T2)'
    else:
        s_result = 'Under control'

    # export results as JSON
    data = {"result": s_result,
            "payload":{
                    "UCL_SPE": model.UCL_SPE[0],
                    "SPE": SPE,
                    "SPE_contrib": pred.SPE_contrib.iloc[0].to_dict(),
                    "UCL_T2": model.UCL_T2[0],
                    "T2": T2,
                    "T2_contrib": pred.T2_contrib.iloc[0].to_dict()
                    }
                }
    json_results = json.dumps(data, indent=4)
    return json_results
