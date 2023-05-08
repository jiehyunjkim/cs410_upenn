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
        labels_file = os.path.join(DATAPATH, 'labels.npy')

        images = np.load(images_file)
        labels = np.load(labels_file)

        images = images.reshape(images.shape[0], images.shape[1],images.shape[2], 1)
        labels = labels.reshape(labels.shape[0], labels.shape[1],labels.shape[2], 1)

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
        num = round(length * (1 - val_size))

        nearest_bigger_value = None
        for value in image_data.values():
            if value > num:
                if nearest_bigger_value is None or value < nearest_bigger_value:
                    nearest_bigger_value = value

        for keys, val in image_data.items():
            if val == nearest_bigger_value:
                key = keys

        X_train = images[0:image_data[key]] 
        y_train = labels[0:label_data[key]]
        X_val = images[image_data[key]:]
        y_val = labels[label_data[key]:]

        return X_train, X_val, y_train, y_val

  
    def split_2(images, labels, val_size=0.2):

        X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=val_size, random_state=0)

        return X_train, X_val, y_train, y_val
    
    def split_3(images, labels, val_size=0.15):
        
        with open("symp_data.json", "r") as fp:
            symp_data = json.load(fp)
        with open("asymp_data.json", "r") as fp:
            asymp_data = json.load(fp)

        diffs = []
        prev_val = None
        for key in sorted(symp_data.keys(), key=int):
            val = symp_data[key]
            if prev_val is not None:
                diff = val - prev_val
                diffs.append(diff)
            prev_val = val


        symp_list = [711]
        result = 711
        for i in diffs:
            result += i
            symp_list.append(result)

        values = list(asymp_data.values()) + symp_list

        length = images.shape[0]
        num = round(length * (1 - val_size))

        nearest_bigger_value = None
        for value in values:
            if value > num:
                if nearest_bigger_value is None or value < nearest_bigger_value:
                    nearest_bigger_value = value

        index = values.index(nearest_bigger_value) 

        X_train = images[0:values[index]] 
        y_train = labels[0:values[index]]
        X_val = images[values[index]:]
        y_val = labels[values[index]:]

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
        
    def boxplot(all_data, labels, y_label='Time [s]', y_lim_min=0, y_lim=1000, 
        title=None, outputdir='/home/jiehyun.kim001/CACTAS/_EXPERIMENTS/', y_zoom=None):
     
        
        matplotlib.rcParams.update({'font.size': 32})
        plt.rc('axes', labelsize=65)    # fontsize of the x and y labels
        plt.rc('legend', fontsize=32)   
        plt.rc('xtick', labelsize=42) 

        # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=1, figsize=(9, 4))
        fig = plt.figure(figsize=(7, 13))
        ax = fig.gca()
        # ax1 = plt.gcf()
        boxprops = dict(color="black",linewidth=1.5)
        medianprops = dict(color="black",linewidth=1.5)
        # rectangular box plot
        bplot1 = plt.boxplot(all_data,
                             vert=True,  # vertical box alignment
                             patch_artist=True,  # fill with color
                             labels=labels,
                             boxprops=boxprops,
                             medianprops=medianprops)  # will be used to label x-ticks

        # fill with colors
        colors = ['#af8dc3', '#7fbf7b']
        # for bplot in (bplot1, bplot2):
        for patch, color in zip(bplot1['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_ylabel(y_label)
        ax.set_ylim(y_lim_min,y_lim)
        # Set y-axis limits if y_zoom parameter is provided
        if y_zoom:
            ax.set_ylim(*y_zoom)

        titleb = title
        if not title:
            titleb = 'figure.pdf'

        filename_pdf = outputdir+'/'+titleb.replace(' ','_').replace(',','')+'.pdf'
        filename_png = outputdir+'/'+titleb.replace(' ','_').replace(',','')+'.png'
        plt.savefig(filename_pdf,bbox_inches='tight')
        plt.savefig(filename_png,bbox_inches='tight')

        if title:
            plt.title(title)

        plt.show()

        print(labels[0], np.mean(all_data[0]),'+/-', np.std(all_data[0]))
        print(labels[1], np.mean(all_data[1]),'+/-', np.std(all_data[1]))

        ttest = stats.ttest_ind(all_data[0],all_data[1])

        print('t_'+str(len(all_data[0]+all_data[1])), '=', str(round(ttest[0],3)), ',p=',str(round(ttest[1],2)))






