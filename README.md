<h1 align="center">Rice Tracker</h1>
<p>
  Used to track monthly average rice stock and annual regional consumption. This application can also be used to predict future value
</p>

<br/><br/><br/>

<h3>========================== Application Setup ========================== </h3>
<h4>Linux environment with poetry is recommended.</h4>

===== If you are linux user, follow these steps ===== <br/>
Prerequisites:
- Python 3.11
- pip
- poetry

<br/>

Steps: 
1. navigate console to project root directory

2. For nix user, execute command below
> nix-shell <br/>

3. navigate to riceApp
> cd riceApp <br/>

4. Download dependency
> poetry update <br/>

5. Setup database table
>  poetry run python manage.py makemigrations <br/>

6. Reset database and model
> rm db.sqlite3 <br/>
> rm stock.model <br/>
> rm population.model <br/>
> rm consumption.model <br/>

7. Rebuild database
> poetry run python manage.py migrate <br/>

8. Run server
> poetry run python manage.py runserver <br/>

<br/><br/>

==== If you are windows user, follow these steps ===== <br/>
Prerequisites:
- Python 3.11
- pip

<br/>

Steps: 

1. Open cmd and navigate to project root directory

2. navigate to riceApp
> cd riceApp <br/>

3. Download dependency
> pip install Django <br/>
> pip install matplotlib <br/>
> pip install scikit-learn <br/>
> pip install pandas <br/>
> pip install statsmodel <br/>

4. Setup database table
> python manage.py makemigrations <br/>

5. Reset database and model
> del db.sqlite3 <br/>
> del stock.model <br/>
> del population.model <br/>
> del consumption.model <br/>

6. Rebuild database
> python manage.py migrate <br/>

7. Run server
> python manage.py runserver <br/>

<br/><br/><br/>
<h3>========================== API Entry ========================== </h3>

<br/> > insert-stock-bulk
<br/> Description: Used to input stock data by csv file
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; file : csv File -> File 
<br/>

<br/> > insert-stock
<br/> Description: Used to input stock data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : month -> Integer
<br/> &nbsp; &nbsp; param1 : year -> Integer
<br/> &nbsp; &nbsp; param2 : average Stock -> Integer

<br/> > update-stock
<br/> Description: Used to update stock data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : month -> Integer
<br/> &nbsp; &nbsp; param1 : year -> Integer
<br/> &nbsp; &nbsp; param2 : average Stock -> Integer

<br/> > delete-stock
<br/> Description: Used to delete stock data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : month -> Integer
<br/> &nbsp; &nbsp; param1 : year -> Integer

<br/> > fetch-stock
<br/> Description: Used to view historical stock data and predict several future value
<br/> Method: GET / POST
<br/> Parameter:

<br/> > insert-consumption-bulk
<br/> Description: Used to input consumption data by csv file
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; file : csv File -> File 
<br/>

<br/> > insert-consumption
<br/> Description: Used to input consumption data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : year -> Integer
<br/> &nbsp; &nbsp; param1 : population -> Integer
<br/> &nbsp; &nbsp; param2 : consumption rate -> Float

<br/> > update-consumption
<br/> Description: Used to update consumption data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : year -> Integer
<br/> &nbsp; &nbsp; param1 : population -> Integer
<br/> &nbsp; &nbsp; param2 : consumption rate -> Float

<br/> > delete-consumption
<br/> Description: Used to delete consumption data
<br/> Method: POST
<br/> Parameter:
<br/> &nbsp; &nbsp; param0 : year -> Integer

<br/> > fetch-consumption
<br/> Description: Used to view historical consumption data and predict several future value
<br/> Method: GET / POST
<br/> Parameter:
