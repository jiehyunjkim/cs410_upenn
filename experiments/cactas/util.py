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

    def load(DATAPATH='/raid/mpsych/CACTAS/DATA/ESUS'):

        images_file = os.path.join(DATAPATH, 'images.npy')
        labels_file = os.path.join(DATAPATH, 'labels_new.npy')

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

        with open("image_data_v3.json", "r") as fp:
            image_data = json.load(fp)
        with open("label_data_v3.json", "r") as fp:
            label_data = json.load(fp)
        
        length = len(images)
        
        
        X_train = images[0:image_data['84']] 
        y_train = labels[0:label_data['84']]
        X_val = images[image_data['84']:]
        y_val = labels[label_data['84']:]

        return X_train, X_val, y_train, y_val

  
    def split_2(images, labels, val_size=0.2):

        X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=val_size, random_state=0)

        return X_train, X_val, y_train, y_val

    
    def augment(X_train, y_train):
        from keras_unet.utils import get_augmented
        
        train_gen = get_augmented(
            X_train, y_train, batch_size=2,
            data_gen_args = dict(
                rotation_range=5.,
                width_shift_range=0.05,
                height_shift_range=0.05,
                shear_range=40,
                zoom_range=0.2,
                horizontal_flip=True,
                vertical_flip=True,
                fill_mode='constant'
            ))

        return train_gen
    
    def create_unet(input_shape):
        from keras_unet.models import custom_unet
        model = custom_unet(
            input_shape=input_shape,
            use_batch_norm=False,
            num_classes=1,
            filters=64,
            dropout=0.2, 
            dropout_change_per_layer=0.0,
            num_layers=4,
            output_activation='sigmoid')

        from keras_unet.metrics import iou, iou_thresholded
        from tensorflow.keras.optimizers import Adam
        
        model.compile(optimizer = Adam(learning_rate=0.001),
              loss='binary_crossentropy', 
              metrics=[iou, iou_thresholded])
        
        return model

    def train_unet(train_gen, X_train, y_train, X_val, y_val, model, epochs=200):
        batch_size = 32
        history = model.fit(X_train,
                            y_train,
                            batch_size = batch_size,
                            epochs=200,
                            validation_data=(X_val, y_val))
        return model, history
    
    def visualize_graph(history):
        from keras_unet.utils import plot_segm_history
        
        vis = plot_segm_history(history)
        
        #return vis
    
    def prediction(X_val, model):
        y_pred = model.predict(X_val)
        
        return y_pred
    
    def visualize_result(X_val, y_val, y_pred):
        from keras_unet.utils import plot_imgs

        plot_imgs(org_imgs=X_val, mask_imgs=y_val, pred_imgs=y_pred, nm_img_to_plot=10)
    
    def evaluate(X_val, y_val, model):
        loss, iou, iou_thresholded = model.evaluate(X_val, y_val)
        
        #return loss, iou, iou_thresholded
    
    
    
    
    
    
    