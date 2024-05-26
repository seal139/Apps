import itertools
import pandas as pd

from joblib                             import dump, load
from sklearn.metrics                    import r2_score
from statsmodels.tsa.statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')

def predict(input1, input2) :

    data           = pd.read_json(input2)
    exogenous_vars = data[['month']] 

    stockModel  = load(input1)
    predictions = stockModel.forecast(
        steps = len(exogenous_vars),  # Forecast the same number of steps as the test data length
        exog  = exogenous_vars
    )

    return predictions.tolist()
#end def

# Create and train new model based on input file and save the model into output file
def train(input, output) :
    data = pd.read_json(input)

    target_data    = data[['avgStock']]     # Stok
    exogenous_vars = data[['month']]   # Bulan

    split_index = int(len(target_data) - 22)

    train_target = target_data[:split_index]
    test_target  = target_data[split_index:]

    train_exog = exogenous_vars[:split_index]
    test_exog  = exogenous_vars[split_index:]

    best_combinationIn = None
    best_return        = float('-inf')

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

            eval  = candidate.forecast(
                steps = len(test_target),  # Forecast the same number of steps as the test data length
                exog  = test_exog
            )

            r2 = r2_score(test_target, eval)

            # Update the best combination and return if the current result is better
            if r2 > best_return:
                best_combinationIn = (p, d, q)
                best_return        = r2
            #end if

        except Exception as e:
            continue
        #end try
    #end for

    p, d, q   = best_combinationIn
    candidate = SARIMAX(
            seasonal       = True,  # Set to True if seasonality is present
            stepwise       = True,
            endog          = target_data,
            exog           = exogenous_vars,
            order          = (p, d, q),  # Adjust the order as needed (p, d, q)
            seasonal_order = (p, d, q, 12)
        ).fit()
    
    dump(candidate, output)
#end def