import numpy as np
import sklearn
from sklearn.metrics.pairwise import euclidean_distances
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt

import my_tf_pkg as mtf

## Data sets
def get_kernel_matrix(x,W,S):
    beta = get_beta_np(S)
    #beta = 0.5*tf.pow(tf.div( tf.constant(1.0,dtype=tf.float64),S), 2)
    Z = -beta*euclidean_distances(X=x,Y=W,squared=True)
    K = np.exp(Z)
    return K

N = 7000
low_x =-2*np.pi
high_x=2*np.pi
X = low_x + (high_x - low_x) * np.random.rand(N,1)
# f(x) = 2*(2(cos(x)^2 - 1)^2 -1
f = lambda x: 2*np.power( 2*np.power( np.cos(x) ,2) - 1, 2) - 1
Y = f(X)

stddev = 1
replace = False # with or without replacement
nb_centers = [4, 8, 16, 24, 48] # number of centers for RBF
colours = ['g','r','c','m','y']
#
rbf_errors = []
rbf_predictions = []
for K in nb_centers:
    indices=np.random.choice(a=N,size=K,replace=replace) # choose numbers from 0 to D^(1)
    subsampled_data_points=X[indices,:] # M_sub x D

    beta = 0.5*np.power(1.0/stddev,2)
    Kern = np.exp(-beta*euclidean_distances(X=X,Y=subsampled_data_points,squared=True))
    (C,_,_,_) = np.linalg.lstsq(Kern,Y)

    Y_pred = np.dot( Kern , C )

    rbf_predictions.append(Y_pred)
    rbf_errors.append(sklearn.metrics.mean_squared_error(Y, Y_pred))

#plt.plot(X, Y,'bo', X, Y_pred, 'ro')
plt.figure(1)
plt.plot(X, Y,'bo', label='Original data', markersize=3)
#plt.plot(X, Y_pred, 'bo', label='Fitted line', markersize=3)
for i, Y_pred in enumerate(rbf_predictions):
    colour = colours[i]
    K = nb_centers[i]
    plt.plot(X, Y_pred, colour+'o', label='RBF'+str(K), markersize=3)
#plt.plot(X, Y_pred, 'bo', label='Fitted line', markersize=3)
# errors
plt.figure(2)
plt.plot(nb_centers, rbf_errors,'b', label='Errors', markersize=3)
plt.plot(nb_centers, rbf_errors,'bo')
#
plt.legend()
plt.show()