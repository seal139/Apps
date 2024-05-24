Linux environment with poetry is recommended.

<br/><br/>

// -----===== If you are linux user, follow these steps <br/>
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

// -----===== If you are windows user, follow these steps <br/>
Prerequisites:
- Python 3.11
- pip
- poetry

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
