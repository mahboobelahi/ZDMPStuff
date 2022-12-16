
import tensorflow as tf
import tensorflow.experimental.numpy as tnp
import joblib,json
tnp.experimental_enable_numpy_behavior()
def predict(**data_in):
    """

    :param data: {
  "powerConsumption": num,
  "load": num
}
    :return:
    """
    print(f"Data Type: {type(data_in)}")
    print(data_in)
    "model loading and data transfor"
    model = tf.keras.models.load_model('M_iter3_1.h5', compile=True)
   
    #model = joblib.load("model.pkl")
    
    features_1 = tnp.array(tnp.append([data_in.get("data")["powerConsumption"]],
                                     [data_in.get("data")["load"]]), ndmin=2)
    pred = tnp.argmax(model.predict(features_1), axis=1) # need to pus that vakue to message bus
    json_results = {"BT_Class":int(pred[0])} #AIAR will dumps python dict to JSONstring
    print(type(json_results))
    return json_results

predict(**{"data": {"powerConsumption": 0.75, "load": 0.73}})