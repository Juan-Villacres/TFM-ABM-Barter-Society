Project Description:

This project utilizes agent-based models to simulate a society engaged in digital barter, governed by the Lotka-Volterra equations (LV). The models aim to capture the dynamics of goods and services exchange within this digital barter system.

Description of Files
1) Final_LV_RF_con_contador: Integrates a random forest model into the agent-based model (ABM) to mimic the preferences of participants in bartering. The ABM utilizes LV equations, specifically focusing on mutualism, to determine the allocation of goods or services when multiple individuals express interest in the same item.

2) RFTrueque: Contains the random forest model implemented in 'Final_LV_RF,' trained using the 'shopping_behaviour_updated.csv' dataset from Kaggle.

3) SustitutoConv: Develops a surrogate ABM using convolutional neural networks.

4) SustitutoLSTM: Implements a surrogate ABM based on recurrent neural networks with LSTM architecture.

5) TFM2: Implements the SugarScape model using the MESA library in Python, exploring agent behaviors and resource allocation dynamics.

6) TruequeNetlogo: Adapts NetLogo's 'Simply Economy' model to simulate a digital barter system without LV equation regulation, providing insights into unregulated barter dynamics.

7) mutualismo_competencia: Designs two distinct barter models, one regulated by LV equations for competition and the other for mutualism. Analyzes the benefits of each model in terms of reducing monopoly effects.

Overall Project Insight: The project demonstrates that a society engaging in digital barter can mitigate monopoly tendencies when regulated by LV equations, particularly those governing mutualistic interactions.
 

