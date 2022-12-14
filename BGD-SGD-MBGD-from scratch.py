import seaborn as sns
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
import random
# %matplotlib inline

df = pd.read_csv("Assignment_2_SoccerPlayers.csv",header=None)

X = df.iloc[1:501, 12:15].to_numpy()
y = df.iloc[1:501, 7].to_numpy()

sc=StandardScaler()
X_transform=sc.fit_transform(X)
# splitting the data
x_train, x_test, y_train, y_test = train_test_split(X_transform, y, test_size = 0.2, random_state = 10)

"""# Batch Gradient Descent"""

def batch_predicted_y(weight,x,intercept): #prediction = wx +b 
    y_lst=[]
    for i in range(len(x)):
        y_lst.append(weight@x[i]+intercept)
    return np.array(y_lst)
    
# linear loss 
def batch_loss(y,y_predicted):  # MSE calculation--> 1/n* sum of y(actual)-y(predicted) **2
    n=len(y)
    s=0
    for i in range(n):
        s+=(y[i]-y_predicted[i])**2
    return (1/n)*s

#derivative of loss w.r.t weight
def batch_dlbydw(x,y,y_predicted): # 2/n* sum of (-xi(y actual - y predicted))
    s=0
    n=len(y)
    for i in range(n):
        y[i] = float(y[i])
        s+= -x[i]*(y[i]-y_predicted[i])
    return (2/n)*s
    

# derivative of loss w.r.t bias # 2/n * sum of (-(y actual - y predicted))
def batch_dlbydb(y,y_predicted):
    n=len(y)
    s=0
    for i in range(len(y)):
        s+=-(y[i]-y_predicted[i])
    return (2/n) * s
     
# Batch gradient function
def batch_gradient_descent(x,y):
    weight_vector=np.random.randn(x.shape[1])
    intercept=0
    epoch = 2000
    n = len(x)
    linear_loss=[]
    learning_rate = 0.001
 
    for i in tqdm(range(epoch)):
        
        y_predicted = batch_predicted_y(weight_vector,x,intercept)      # calculate prediction         
        weight_vector = weight_vector - learning_rate *batch_dlbydw(x,y,y_predicted)          # caluclate weight vector     
        intercept = intercept - learning_rate * batch_dlbydb(y,y_predicted) # calculate intercept or bias
        linear_loss.append(batch_loss(y,y_predicted)) # calculate loss
        
    #plot    
    plt.plot(np.arange(1,epoch),linear_loss[1:])
    plt.title("Loss vs Epoch")
    plt.xlabel("Number of Epoch")
    plt.ylabel("Loss")
    
    return weight_vector,intercept

w,b=batch_gradient_descent(x_train,y_train)
print("For Training Set")

w,b=batch_gradient_descent(x_test,y_test)
print("For Testing Set")

print('Final Weights from Batch Gradient Descent',w)
print('Final Bias from Batch Gradient Descent',b)

def predict(inp): # function to create dataframe of predicted values
    df_pred=pd.DataFrame()
    df_pred["y_actual"]=y
    y_lst=[]
    for i in range(len(inp)):
        y_lst.append(w@inp[i]+b)
    y_pred=  y_lst
    df_pred["y_predicted"]=np.round(y_pred,1)
    return df_pred

#predicted dataframe
df_predic=predict(X_transform)
df_predic

"""# Stochastic Gradient Descent"""

def stoch_predicted_y(weight,x,intercept): #prediction = wx +b 
    return weight@x+intercept    

# linear loss
def stoch_loss(y,y_predicted): # MSE calculation--> (y(actual)-y(predicted))**2
    s=(y-y_predicted)**2
    return s

#derivative of loss w.r.t weight # 2* (-xi(y actual - y predicted))
def stoch_dlbydw(x,y,y_predicted):
    s=-x*(y-y_predicted)
    return 2*s
    

# derivative of loss w.r.t bias #2 * (-(y actual - y predicted))
def stoch_dlbydb(y,y_predicted):
    s=-(y-y_predicted)
    return 2*s
        
        
# gradient function
def stoch_gradient_descent(x,y):
    weight_vector=np.random.randn(x.shape[1])
    intercept=0
    epoch = 5000
    n = len(x)
    linear_loss=[]
    learning_rate = 0.000001
    n_iter=[]
    loss_iter = []
    count=1
    
    for i in tqdm(range(epoch)):
        
        for j in range(n):
            random_index = random.randint(0,n-1) # taking a random index
            x_sample = x[random_index] # getting X values for that random index
            y_sample = y[random_index] # getting Y values for that random index
            y_predicted = stoch_predicted_y(weight_vector,x_sample,intercept)  # calculate prediction
            # updation of weight and bias for every record
            weight_vector = weight_vector - learning_rate *stoch_dlbydw(x_sample,y_sample,y_predicted)  # calculate Weight vector
            intercept = intercept - learning_rate * stoch_dlbydb(y_sample,y_predicted) # calculate intercept or bias
            loss_iter.append(stoch_loss(y_sample,y_predicted)/n) 
            n_iter.append(count)
            count+=1 
        linear_loss.append(stoch_loss(y_sample,y_predicted)/n)     # calculate loss
        
   #plot for Epoch  
    plt.ticklabel_format(style='plain')
    plt.plot(np.arange(1,epoch),linear_loss[1:])
    plt.title("Loss vs Epoch")
    plt.xlabel("Number of Epoch")
    plt.ylabel("Loss")
    plt.show()
    # Set axes limit

    #plot for iterations
    #plt.ticklabel_format(style='plain')
    plt.plot(n_iter,loss_iter)
    plt.xlabel("Number of Iterations")
    plt.ylabel("Loss")
    plt.title("Loss vs Iterations")  
    plt.show() 

    
    return weight_vector,intercept

print("For Training Set")
w,b=stoch_gradient_descent(x_train,y_train)

print("For Testing Set")
w,b=stoch_gradient_descent(x_test,y_test)

print('Final Weights from Stochastic Gradient Descent',w)
print('Final Bias from Stochastic Gradient Descent',b)

#predicted Dataframe
df_predic=predict(X_transform)
df_predic

"""# Mini Batch Gradient Descent"""

def mbgd_predicted_y(weight,x,intercept): #prediction = wx +b 
    y_lst=[]
    for i in range(len(x)):
        y_lst.append(weight@x[i]+intercept)
    return np.array(y_lst)
    
# linear loss
def mbgd_loss(y,y_predicted): # MSE cal--> 1/total count(12) * sum of 12 values of the minibatch for(y(actual)-y(predicted))**2
    n=len(y)
    batch_sz =12
    s=0
    for i in range(n):
        s+=(y[i]-y_predicted[i])**2
    return (1/batch_sz)*s

#derivative of loss w.r.t weight # 2/total count(12) * sum of 12 values of mini batch for (-xi(y actual - y predicted))
def mbgd_dlbydw(x,y,y_predicted):
    s=0
    batch_sz =12
    n=len(y)
    for i in range(n):
        y[i] = float(y[i])
        s+=-x[i]*(y[i]-y_predicted[i])
    return (2/batch_sz)*s
    

# derivative of loss w.r.t bias #2/total count(12) * sum of 12 values of mini batch for(-(y actual - y predicted))
def mbgd_dlbydb(y,y_predicted):
    n=len(y)
    batch_sz =12
    s=0
    for i in range(n):
        s+=-(y[i]-y_predicted[i])
    return (2/batch_sz) * s          
        
# gradient function
def mini_batch_gradient_descent(x,y):
    weight_vector=np.random.randn(x.shape[1])
    intercept=0
    epoch = 2000
    n = len(x)
    linear_loss=[]
    learning_rate = 0.0001
    n_iter=[]
    count=1
    batch_size=12 # mini batch size is 12 
    loss_iter = []
    for i in tqdm(range(epoch)):
        
        for j in range(int(n/batch_size)): # int(500/12)
            random_index=np.random.choice(x.shape[0],batch_size,replace=False) #batch size of 12
            x_sample = x[random_index] # choosing 12 x values 
            y_sample = y[random_index] # choosing 12 y values 
            y_predicted = mbgd_predicted_y(weight_vector,x_sample,intercept)  # calculate prediction
            # updation of weight and bias for every batch size
            weight_vector = weight_vector - learning_rate *mbgd_dlbydw(x_sample,y_sample,y_predicted)   # calculate Weight vector
            intercept = intercept - learning_rate * mbgd_dlbydb(y_sample,y_predicted) # calculate intercept or bias                  
            linear_loss.append(mbgd_loss(y_sample,y_predicted)) # calculate loss
            n_iter.append(count)
            count+=1        
        loss_iter.append(mbgd_loss(y_sample,y_predicted))    # calculate loss
        
   #plot for Epoch    
    plt.plot(np.arange(1,epoch),loss_iter[1:])
    plt.title("Loss vs Epoch")
    plt.xlabel("Number of Epoch")
    plt.ylabel("Loss")
    plt.show()
    #plot    
    plt.plot(n_iter,linear_loss)
    plt.xlabel("Number of Iterations")
    plt.ylabel("Loss")
    plt.title("Loss vs Iterations")    
    plt.show()
    return weight_vector,intercept

print("For Training Set")
w,b=mini_batch_gradient_descent(x_train,y_train)

print("For Testing Set")
w,b=mini_batch_gradient_descent(x_test,y_test)

print('Final Weights from Mini-Batch Gradient Descent',w)
print('Final Bias from Mini-Batch Gradient Descent',b)

#predicted Dataframe
df_predic=predict(X_transform)
df_predic

