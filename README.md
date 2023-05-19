# CACTAS Program

## Table of Contents
* [Software Information](#software-information)
* [Project Overview](#project-overview)
* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)
* [License](#license)


## Software Information
**Software Name:** CACTAS Program<br/>
**Latest Software Version:** v.1.0

## Project Overview
**Team Members:** Jenna Kim, Dhruv Shah, Thuytien Chu, Alexander Choe

The goal of our project is to design a program that can characterize qualitative and quantitative morphologic features of calcific plaque. Using machine learning algorithms, we automatically identify calcific plaque in the carotid artery visible in CTA scans and perform image segmentation on them. We then train the algorithm to determine useful features about the plaque, such as its estimated risk to the patient to lead to a stroke, and then create another program to calculate its manual features such as the number, size, and volume. This program would be able to be used as the groundwork to simplify further research tasks in identifying critical features of plaque, such as determining causal relationships between a given feature and estimated risk. The current version (1.0) of this software uses 2D UNet, 2D and 3D Swin UNETR for image segmentation, Random Forest and CNN for risk estimation, and the Mahotas library for manual features.

## Installation

**Fork our github repository:**
```
git clone git@github.com:jiehyunjkim/cs410_upenn.git [local directory]
```

**Data:** <br/> Change the DATAPATH at ```experiments - cactus- util.py - load() - DATAPATH``` to your own local directory. The size of npy file should be 512 by 512.

Open the terminal:<br/>

**Install conda:** https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html<br/>

From terminal, go to your local github fork directory and run the following steps. 
To create the environment necessary to run the program:
```
conda env create -f environment.yml
conda install notebook
jupyter--notebook --generate-config
vi /home/[YourUsername]/.jupyter/jupyter_notebook_config.py
```

Uncomment and populate the following fields within the file using your IP address and an arbitrary port number:
```
c.NotebookApp.ip = ‘0.0.0.0’
c.NotebookApp.open_browser = False
c.NotebookApp.port = YOUR_PORT_NUMBER
```
Lastly, to start up the environment and notebook:
```
conda activate CACTAS
jupyter notebook
```

At this point, you should have access to all the program files, visible within the Jupyter Notebook environment, where you can also run them.

## Usage

**Image segmentation:** [keras_2d_unet_usingAPI_v1.ipynb](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/keras_2d_unet_usingAPI_v1.ipynb)<br/>
[keras_swinUnetr_full_v11.ipynb](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/keras_swinUnetr_full_v11.ipynb)<br/>
[3D Swin UNETR]()<br/>
**Risk estimation:** [RandomForest.ipynb](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/RandomForest.ipynb)<br/>
[CNN.ipynb](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/CNN.ipynb)<br/>
**Manual Features:** [upenn_plaque_features_oo_v1.py](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/upenn_plaque_features_oo_v1.py)<br/>

## Examples
Here is an example of output of 2D UNet: <br/>
<img src="https://drive.google.com/uc?id=1_dJ1mKtbxw2RwG6fSvnVBvIOrn6HscQy"
     alt="unet_result"
     style="display: block; margin-right: auto; margin-left: auto; width: 40%;" /><br/>
2D Swin UNETR: <br/>
<img src="https://drive.google.com/uc?id=1PRS8ZBuPxTA7uaLFgKA82vwgInwAGNbg"
     alt="2dswinunet_result"
     style="display: block; margin-right: auto; margin-left: auto; width: 40%;" /><br/>
3D Swin UNETR: <br/>
<img src="https://drive.google.com/uc?id=1TA8ywcK_O2q9hO2pJeZDqb2WknphPeix"
     alt="3dswinunet_result"
     style="display: block; margin-right: auto; margin-left: auto; width: 40%;" /><br/>
Random Forest: <br/>
<img src="https://drive.google.com/uc?id=1lp7lJ43KiYIL7VYEMZF0UQvTIMJ-vhoO"
     alt="RF"
     style="display: block; margin-right: auto; margin-left: auto; width: 40%;" /><br/>
     
An example of running manual features and what its output looks like can be found [here](https://github.com/jiehyunjkim/cs410_upenn/blob/master/experiments/manual_features_videotest.ipynb).<br/>

## License 
This project is licensed under the MIT License - see the [LICENSE](https://github.com/jiehyunjkim/cs410_upenn/blob/master/LICENSE.md) file for details.
