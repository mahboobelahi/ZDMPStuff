import json


def txtToJson(inputfile,outfile):
    dependencies = []
    with open(inputfile,"r") as packages:#"requirements.txt"
        for pkg in packages:
            pkg = pkg.rstrip().split("==")
            dependencies.append((dict(name= pkg[0],version= pkg[1])))
        dependencies = json.dumps(dependencies,indent=4)
    with open(outfile,"w") as outfile:#"PR_Packages.json"
        outfile.write(dependencies)


# Importing modules
import tensorflow  as tf
import json
import numpy as np


# loading transformer/scaler Object to scale both features between 0 and 1
# Load_scaler = joblib.load('pallet-scaler.save')
# Power_scaler = joblib.load('Power-scaler.save')


def predict(*args,**kwargs):
    """

    :param data: {
  "powerConsumption": num,
  "load": num
}
    :return:
    """
    print(f"Data Type: {type(kwargs)}")
    print(kwargs)
    "model loading and data transfor"
    features_1 = np.array(np.append([kwargs.get("data")["powerConsumption"]],
                                     [kwargs.get("data")["load"]]), ndmin=2)
    model = tf.keras.models.load_model('M_iter3_1.h5', compile=True)
    pred = np.argmax(model.predict(features_1), axis=1) # need to pus that vakue to message bus
    print(pred)
    json_results = json.dumps({"BT_Class":int(pred[0])}, indent=4)
    print(f"[X] {json_results}")
    return json_results
"""
    from predict import predict
    predict({"kwargs": {"powerConsumption": 0.175, "load": 0.73}})
	Sample input
	power 	load
	0.26  	0.13	
	0.81	1	
	0.15	0.07	

"""