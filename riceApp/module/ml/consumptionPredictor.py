import pandas as pd

from sklearn.linear_model import LinearRegression
from joblib               import dump, load

def predict(input1, input2, year) :

    # Load from file
    populationModel  = load(input1)
    consumptionModel = load(input2)

    # Predict
    population  = populationModel.predict([[int(year)]])[0]
    consumption = consumptionModel.predict([population])[0]

    # Show result
    return [population[0], consumption[0]]
#end def

# Create and train new model based on input file and save the model into output file
def train(input, output1, output2) :

    # Data
    data = pd.read_json(input)

    xYear        = data[['year']]
    yPopulation  = data[['population']]
    zConsumption = data[['consumptionRate']]

    # Population Model
    populationModel = LinearRegression()
    populationModel.fit(xYear, yPopulation)

    # Consumption Model
    consumptionModel = LinearRegression()
    consumptionModel.fit(yPopulation, zConsumption)

    # Save to file
    dump(populationModel, output1)
    dump(consumptionModel, output2)
#end def