
# Help
# 1. Train
# frcast.py train [training csv] [output]
# return: {void}

# 2. Predict
# frcast.py predict [model] [exogenous csv] 
# return: [array of predicted stock

#Example: Train and predict
# frcast.py train history.csv regmodel
# frcast.py predict regmodel exogenous.csv

# Historical csv format must have 3 column and not nullable
# ----------------------------------------------------------- 
# | Month | Year | Square root of avg stock |
# -----------------------------------------------------------

# ----------- Function  -----------

import itertools
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from joblib                             import dump, load
from sklearn.metrics                    import r2_score
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')

def draw(model, input1, input2, output) :
    train_target   = pd.read_csv(input1).iloc[:, 2] 
    exogenous_vars = pd.read_csv(input2).iloc[:, [0]] 

    stockModel  = load(model)
    predictions = stockModel.forecast(
        steps = len(exogenous_vars),  # Forecast the same number of steps as the test data length
        exog  = exogenous_vars
    )


    plt.figure(figsize=(20, 6))
    plt.plot(train_target.index, train_target, label='Historical Data')
    plt.plot(predictions.index, predictions, label='Predicted Data', linestyle='--')

    plt.xticks(range(0, 1+len(train_target) + len(predictions), 6))
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    
    plt.savefig(output)  

def predict(input1, input2) :

    data           = pd.read_csv(input2)
    exogenous_vars = data.iloc[:, [0]] 

    stockModel  = load(input1)
    predictions = stockModel.forecast(
        steps = len(exogenous_vars),  # Forecast the same number of steps as the test data length
        exog  = exogenous_vars
    )

    print(predictions.tolist())

# Create and train new model based on input file and save the model into output file
def train(input, output) :
    data = pd.read_csv(input)

    target_data    = data.iloc[:, 2]    # Stok
    exogenous_vars = data.iloc[:, [0]]  # Bulan

    split_index = int(len(target_data) - 22)

    train_target = target_data[:split_index]
    test_target = target_data[split_index:]

    train_exog = exogenous_vars[:split_index]
    test_exog = exogenous_vars[split_index:]

    best_combinationIn = None
    best_return = float('-inf')

    # Iterate over all possible combinations of values for a, b, c, p, q, and r
    for p, d, q in itertools.product(range(3), repeat=3):

        # Model
        try :
            candidate = SARIMAX(
                seasonal       = True,  # Set to True if seasonality is present
                stepwise       = True,
                endog          = train_target,
                exog           = train_exog,
                order          = (p, d, q),  # Adjust the order as needed (p, d, q)
                seasonal_order = (p, d, q, 12)
            ).fit()

            eval = candidate.forecast(
            steps = len(test_target),  # Forecast the same number of steps as the test data length
            exog  = test_exog
            )

            r2 = r2_score(test_target, eval)

            # Update the best combination and return if the current result is better
            if r2 > best_return:
                best_combinationIn = (p, d, q)
                best_return = r2
        except Exception as e:
            continue

    p, d, q = best_combinationIn
    candidate = SARIMAX(
                seasonal       = True,  # Set to True if seasonality is present
                stepwise       = True,
                endog          = target_data,
                exog           = exogenous_vars,
                order          = (p, d, q),  # Adjust the order as needed (p, d, q)
                seasonal_order = (p, d, q, 12)
            ).fit()
    
    dump(candidate, output)


import sys

exec = sys.argv[0] # prints python_script.py
comm = sys.argv[1] 

if comm == "train" :
    train(sys.argv[2], sys.argv[3])
elif comm == "predict" :
    predict(sys.argv[2], sys.argv[3])
elif comm == "draw" :
    draw(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])