
# Help
# 1. Train
# regr.py train [training csv] [output1] [output2]
# return: {void}

# 2. Predict
# regr.py predict [model] [input1] [input2] 
# return: [estimated population], [estimated consumption]

#Example: Train and predict
# regr.py train history.csv regmodel1 regmodel2
# regr.py predict regmodel1 regmodel2 2025

# Historical csv format must have 3 column and not nullable
# ----------------------------------------------------------- 
# | Year | Square Root Population | Square Root Consumption |
# -----------------------------------------------------------

# An output prediction has 2 values. Population and Consumtion in format of {population}, {consumption}
# Makes sure to split that value by comma and perform power of 2 to retrieve the actual value (Since the regression is performed by square root)
# input1 came from output1, input2 came from output2. Make sure they are refer to the same file(s). Relative path is prefered

# ----------- Function  -----------

import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from joblib               import dump, load

def predict(input1, input2, year) :

    # Load from file
    populationModel  = load(input1)
    consumptionModel = load(input2)

    # Predict
    population  = populationModel.predict(np.array([[int(year)]]))[0]
    consumption = consumptionModel.predict(np.array([[population]]))[0]

    # Show result
    print(population,', ', consumption)

# Create and train new model based on input file and save the model into output file
def train(input, output1, output2) :

    # Data
    data = pd.read_json(input)

    # Population Model
    xYear       = np.array(data.iloc[:, 0].tolist())
    x1          = xYear.reshape(-1, 1)
    yPopulation = data.iloc[:, 1].tolist()

    populationModel = LinearRegression()
    populationModel.fit(x1, yPopulation)

    # Consumption Model
    xPopulation  = np.array(data.iloc[:, 1].tolist())
    x2           = xPopulation.reshape(-1, 1)
    yConsumption = data.iloc[:, 2].tolist()

    consumptionModel = LinearRegression()
    consumptionModel.fit(x2, yConsumption)

    # Save to file
    dump(populationModel, output1)
    dump(consumptionModel, output2)