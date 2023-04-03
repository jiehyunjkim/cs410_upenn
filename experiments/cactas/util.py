import os
import mahotas as mh
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy
from sklearn import metrics
from scipy import stats
from sklearn.model_selection import train_test_split
import json


class Util:

  def load(DATAPATH='/Users/jiehyun/Jenna/UMassBoston/Research/CACTAS/_EXPERIMENTS/data'):

    images_file = os.path.join(DATAPATH, 'images.npy')
    labels_file = os.path.join(DATAPATH, 'labels.npy')

    images = np.load(images_file)
    labels = np.load(labels_file)

    images = images.reshape(images.shape[0],images.shape[1],images.shape[2],1)
    labels = labels.reshape(labels.shape[0],labels.shape[1],labels.shape[2],1)

    return images, labels
  

  def shuffle(images, labels):

    p = np.random.permutation(len(images))
    images = images[p]
    labels = labels[p]

    return images, labels
  
  def normalize(images, labels):

    images = images.astype(np.float32)
    labels = labels.astype(np.float32)

    for i in range(images.shape[0]):
        
        images[i] = (images[i] - images[i].min()) / (images[i].max() - images[i].min()) # normalize individually
        
    return images, labels
  
  def split_1(images, labels, val_size=0.2):

    with open("data/image_data_v3.json", "r") as fp:
      image_data = json.load(fp)
    with open("data/label_data_v3.json", "r") as fp:
      label_data = json.load(fp)

    X_train = images[0:image_data['84']] 
    y_train = labels[0:label_data['84']]
    X_val = images[image_data['84']:]
    y_val = labels[label_data['84']:]

    return X_train, X_val, y_train, y_val

  
  def split_2(images, labels, val_size=0.2):

    X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=val_size, random_state=0)

    return X_train, X_val, y_train, y_val



