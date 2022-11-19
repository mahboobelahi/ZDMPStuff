# Importing modules
import pandas as pd
import numpy as np
from collections import Counter
#%matplotlib inline
import matplotlib.pyplot as plt
from tensorflow import keras
#######################
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
from keras.regularizers import l2
# %matplotlib inline


df= pd.read_csv("traningData_349.csv")
print(df.describe())
################
# #Saving Scalar for real-time usage
# import joblib

# scaler_filename =[ "Power-scaler.save","pallet-scaler.save","custom-Power-scaler.save"]
# data_frame = [ df[['Power (W)']],df[['Load Alias']],df[['Power (W)']] ]
# for data,name in zip(data_frame,scaler_filename): 

#     if name=="custom-Power-scaler.save":
#         scaler = MinMaxScaler()
#         x_sample = [220, 320]
#         scaler.fit(np.array(x_sample)[:, np.newaxis])
#         #scaler.fit(data)
#         joblib.dump(scaler, name) 
#         print('If: ',scaler.data_max_,scaler.data_min_)
#     else:
#         scaler = MinMaxScaler()
#         scaler.fit(data)
#         joblib.dump(scaler, name) 
#         #scaler = joblib.load(name)
#         print(scaler.data_max_,scaler.data_min_)


# scaler = MinMaxScaler()
# df['Normalized_Power']=scaler.fit_transform(df[['Power (W)']])
# df['Normalized_Belt_Tension']=scaler.fit_transform(df[['%Belt Tension']])
# df['Normalized_Load']=scaler.fit_transform(df[['Load Alias']])

# df['Normalized_Power']=round(df['Normalized_Power'],2)
# df['Normalized_Belt_Tension']=round(df['Normalized_Belt_Tension'],2)
# df['Normalized_Load']=round(df['Normalized_Load'],2)

## Coustomize Power(W)  and Belt Tension scaling.
# scaler = MinMaxScaler()
# x_sample = [220, 320]
# scaler.fit(np.array(x_sample)[:, np.newaxis])
# #df['NNNormalized_Power']= scaler.fit_transform(df[['Power (W)']])
# df['NNNormalized_Power']=scaler.transform(df[['Power (W)']])
# df['NNNormalized_Power']=round(df['NNNormalized_Power'],2)


#df['NNormalized_Power']= round((df[['Power (W)']]-df[['Power (W)']].min())/(320-df[['Power (W)']].min()),2)
#df.to_csv('s_Measurements10.csv',index=False)


#print(np.allclose(df['NNNormalized_Power'], df['NNormalized_Power']))
#print(scaler.data_max_,scaler.data_min_)
# choices=[1,2,3,4,5,6,7,8,9] #[1,1,1,1,1,1,1,2,3,4],[1,1,1,1,1,1,1,2,2,3]
# conditions= [
#             df['%Belt Tension'].eq(0),df['%Belt Tension'].eq(15),df['%Belt Tension'].eq(30),
#             df['%Belt Tension'].eq(45),df['%Belt Tension'].eq(60),df['%Belt Tension'].eq(70),
#             df['%Belt Tension'].eq(75),df['%Belt Tension'].eq(85),df['%Belt Tension'].eq(95)
#             ]
# df['Class9'] = np.select(conditions, choices, default= df['%Belt Tension'])

# df.to_csv('s_Measurements10.csv',index=False)
# df= pd.read_csv("s_Measurements10.csv")



# helper functions
def plot_accuracy(history_dict,i):
    
    plt.style.use('fivethirtyeight')
    plt.rcParams['figure.figsize'] = (10.0, 7.0)
    
    acc_values = history_dict['accuracy']
    val_acc_values = history_dict['val_accuracy']

    epochs = range(1, len(acc_values) + 1)

    plt.plot(epochs, acc_values, 'bo', label="Training Accuracy")
    plt.plot(epochs, val_acc_values, 'r', label="Validation Accuracy")

    plt.title(f'Training and Validation Accuraccy_{i}')
    plt.yticks(np.arange(0,1.2,0.1))
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.savefig(f'T_V_Validation_{i}.png',bbox_inches='tight')

    plt.show()
    
    
def plot_loss(history_dict,i):
    
    plt.style.use('fivethirtyeight')
    plt.rcParams['figure.figsize'] = (10.0, 7.0)
    
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']

    epochs = range(1, len(loss_values) + 1)
    plt.rcParams['figure.figsize'] = (10.0, 7.0)
    plt.plot(epochs, loss_values, 'ro', label="Training Loss")
    plt.plot(epochs, val_loss_values, 'b', label="Validation Loss")
    plt.yticks(np.arange(0,1.2,0.1))
    plt.title(f'Training and Validation Loss_{i}')
    plt.xlabel('Epochs')
    plt.ylabel('Loss Value')
    plt.legend()
    plt.savefig(f'T_V_Loss_{i}.png',bbox_inches='tight')

    plt.show()


#train test split
def train_test(df,features,T_class=3):
    
    if T_class == 9:
        one_hot_encode = to_categorical(df['Class_9'])

    elif T_class ==4:
        one_hot_encode = to_categorical(df['Class_4'])
        print('HERERRR\n',one_hot_encode)
    
    elif T_class ==3:
        one_hot_encode = to_categorical(df['Class_3'])
        print('HERERRR\n',one_hot_encode)

    else:
        print(f'Wrong class value.....\nAllowed Classes are {3,4,9}!')
        
        return {"TT_split":f'Wrong class value.....\nAllowed Classes are {3,4,9}!'}

    X=np.array(df[features])
    #type(X)
    X_train, X_test, y_train, y_test = train_test_split(X,one_hot_encode, test_size=0.33, random_state=42)

    X_train= np.array(X_train)
    X_test= np.array(X_test)

    print(f'{type(X_train)} ,{X_train.shape}, {type(X_train)} , {X_test.shape}')
    print(f'{type(y_train)} ,{y_train.shape}, {type(y_train)},{y_test.shape}')

    return {"TT_split":( X_train, X_test, y_train, y_test)}

#NN model
def NN_model(model_architecture=[10,10,10,10]):
    
    #build model
    model = Sequential()
    model.add(Dense(model_architecture[0], input_dim=2, activation='relu',kernel_regularizer=l2(0.01)))
    model.add(Dense(model_architecture[1], activation='relu',kernel_regularizer=l2(0.01)))
    model.add(Dense(model_architecture[2], activation='relu',kernel_regularizer=l2(0.01)))
    model.add(Dense(model_architecture[3], activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def fit_model(model,split,i,epocs=100):
    
    X_train, X_test, y_train, y_test= split.get("TT_split")
    # fit model
    history = model.fit(X_train,
                   y_train,
                   epochs=epocs,
                   batch_size=10,
                   validation_data=(X_test, y_test))
    
    model.save(f'M_iter3_{i}.h5') #using h5 extension
    return history

def prdict_Tension_class(model,i,features,T_class=4):
    
    df_test= pd.read_csv('testData_349.csv')
    nn=np.random.randint(500, size=100)

    X_Test= np.array(df_test[features])
    
    if T_class == 9:

        y_Test=np.array(to_categorical(df_test[f'Class_{T_class}']))
        results = model.evaluate(X_Test, y_Test)
        
        #class prediction
        pred = model.predict(X_Test[nn]) 
        pred = np.argmax(pred, axis = 1)
        True_label = np.argmax(y_Test[nn],axis = 1)
        accuracy_score( True_label,pred )
        load = df_test['Load Alias'][nn] #(X_Test[nn][:,1]*16).astype(int)
        
        power = df_test['Power (W)'][nn]
        tem_df=df_test.loc[nn,['Load Alias','Power (W)','%Belt Tension',f'Class_{T_class}']]
        tem_df['Pred_BT_Class'] = pred

        tem_df.to_csv(f'pred{T_class}_{i}.csv',index=False)

        return (T_class,results[0],results[1],pred,True_label,load,power)
        
    elif T_class == 4:
        
        y_Test=np.array(to_categorical(df_test[f'Class_{T_class}']))
        results = model.evaluate(X_Test, y_Test)
        
        #class prediction
        pred = model.predict(X_Test[nn]) 
        pred = np.argmax(pred, axis = 1)
        True_label = np.argmax(y_Test[nn],axis = 1)
        accuracy_score( True_label,pred )
        
        load = df_test['Load Alias'][nn]
        power = df_test['Power (W)'][nn]
        
        tem_df=df_test.loc[nn,['Load Alias','Power (W)','%Belt Tension',f'Class_{T_class}']]
        tem_df['Pred_BT_Class'] = pred

        tem_df.to_csv(f'pred{T_class}_{i}.csv',index=False)
        
        return (T_class,results[0],results[1],pred,True_label,load,power)
        
    elif T_class == 3:
        
        y_Test=np.array(to_categorical(df_test[f'Class_{T_class}']))
        results = model.evaluate(X_Test, y_Test)
        
        #class prediction
        pred = model.predict(X_Test[nn]) 
        pred = np.argmax(pred, axis = 1)
        True_label = np.argmax(y_Test[nn],axis = 1)
        accuracy_score( True_label,pred )
        
        load = df_test['Load Alias'][nn]
        power = df_test['Power (W)'][nn]
        
        tem_df=df_test.loc[nn,['Load Alias','Power (W)','%Belt Tension',f'Class_{T_class}']]
        tem_df['Pred_BT_Class'] = pred

        tem_df.to_csv(f'pred{T_class}_{i}.csv',index=False)
        
        return (T_class,results[0],results[1],pred,True_label,load,power)
    
    else:

        return f'Wrong class value.....Allowed Classes are {3,4,9}!'

# holds test data evaluation and predicted belt tension class 
cashe ={} # printing Average Loss and Accuracy

# reading trainiing data file
df_train= pd.read_csv("traningData_349.csv")
T_class = 3
epocs = 150
features= ['NNNormalized_Power','Normalized_Load']

# list contains number of hidden and output layer nodes
model_architecture = [10,10,6,4]
#if isinstance(split.get("TT_split"),tuple):
    
# build and compile model
model = NN_model(model_architecture)
    
"""
    For loop for getting average loss and accuracy
"""
for i in range(10):

    # spliting the data into train-test data 
    print(f'Splitting data {i+1}.\n')

    split = train_test(df_train,features,T_class)
    #X_train, X_test, y_train, y_test= split.get("TT_split")
    if isinstance(split.get("TT_split"),tuple):
        # fit model
        history = fit_model(model,split,i+1,epocs)

        # getting loss and accuracy for training and validation data
        history_dict = history.history
        print(history_dict.keys())

        # Plotting losses 
        plot_loss(history_dict,i+1)

        # Training and Validation Accuracy
        plot_accuracy(history_dict,i+1)

        res = prdict_Tension_class(model,i+1,features,T_class)


        if f'class_{T_class}' not in cashe:

            cashe[f'class_{T_class}'] = dict(
                            [('loss',[res[1]]), ('accuracy',[res[2]]),
                            ('true_classes',[res[3]]),('pred_classes', [res[4]]),
                             ('load',[res[5]]),('power',[res[6]])]
                             )
        else:
            temp = cashe.get(f'class_{T_class}')
            temp['loss'].append(res[1])
            temp['accuracy'].append(res[2])
            temp['true_classes'].append(res[3])
            temp['pred_classes'].append(res[4])
            temp['load'].append(res[5])
            temp['power'].append(res[6])
            #(T_class,results[0],results[1],True_label,pred,load,power)
    
    else:
        print(split.get("TT_split"))
        #print(prdict_Tension_class(1))
        
print(cashe.get(f'class_{T_class}'))  

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (7.0, 5.0)

plt.scatter(np.arange(1,len(cashe.get('class_4')['accuracy'])+1),
           cashe.get('class_4')['accuracy'],label='Accuracy' )

plt.plot(5.5,np.sum((cashe.get('class_4')['accuracy']))/len(cashe.get('class_4')['accuracy']),
         marker='o', linestyle='none', markersize=10,color='k',label='Average Accuracy')
#plt.yticks(np.arange(0.978,0.987,0.001))
plt.xticks(np.arange(1, 11,1))
plt.title(f'Accuracy of Model on Test Data',color='#4390cb')
plt.xlabel('Number of Iterations',color='#4390cb')
plt.ylabel('Model Accuracy per Interation',color='#4390cb')
plt.legend(loc=1,bbox_to_anchor=(1.40,1))
plt.savefig(f'Model_1_Accuracy.png',bbox_inches='tight')

plt.show()


plt.scatter(np.arange(1,len(cashe.get('class_4')['loss'])+1),
           cashe.get('class_4')['loss'],label='Loss per Iteration' )

plt.plot(5.5,np.sum((cashe.get('class_4')['loss']))/len(cashe.get('class_4')['loss']),
         marker='o', linestyle='none', markersize=10,color='k',label='Average Loss')
#plt.yticks(np.arange(0.059,0.133,0.01))
plt.xticks(np.arange(1, 11,1))
plt.title(f'Loss of Model on Test Data',color='#4390cb')
plt.xlabel('Number of Iterations',color='#4390cb')
plt.ylabel('Model Loss per Interation',color='#4390cb')
plt.legend(loc=1, bbox_to_anchor=(1,1))
plt.savefig(f'Model_1_Loss.png',bbox_inches='tight')
plt.show()