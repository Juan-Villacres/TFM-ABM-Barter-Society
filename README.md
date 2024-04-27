Here I use agent based models to model a society that exchanges goods and services based on digital barter regulated by Here you can find a group of files where I provide different ways to model a society that exchanges goods and services based on digital barter regulated by the Lotka-Volterra equations (LV). 

Description of the files:

Final_LV_RF_con_contador: This file integrates a random forest model to the agent based model (ABM) in order to emulate the preferences of people involved in bartering. The ABM uses the LV equations for the case of mutualism in order to decide which person is going to receive a goood or service--when there are many persons interested in the same good or service.

RFTrueque: This contains the random forest model implemented in the file 'Final_LV_RF' which is trained with the file shopping_behaviour_updated.csv (from Kaggle). 

SustitutoConv: Here I design a surrogate of the ABM based on convolutional neural networks.

SustitutoLSTM: In this file I design a surrogate of the ABM based on recurrent neural networks with LSTM. 

TFM2: Here I implement the classic SugarScape model by means of the lybrary MESA in Python.

TruequeNetlogo: I modified NetLogo's model 'Simply Economy' to modelate a digital barter that is not regulated by the LV equations.

mutualismo_competencia: In this file I desing twoe different models of barter. One regulated by means of the LV equations for the case of competition, and the other regulated by the LV equations for the case of mutualism. Also, I analyze the benefits of each model in terms of the decrease of monopoly. 

A general result of this project is that a society that base their exchange of goods and services by means of digital barter can avoid the monopoly if such barter is regulated by the LV equations for the case of mutualism

 

