Linux environment with poetry is recommended.

// -----===== If you are linux user, follow these steps
Prerequisites:
1. Python 3.11
2. pip
3. poetry


- navigate console to project root directory

1. For nix user, execute command below
> nix-shell

2. navigate to riceApp
> cd riceApp

3. Download dependency
> poetry update

4. Setup database table
>  poetry run python manage.py makemigrations

5. Reset database and model
> rm db.sqlite3
> rm stock.model
> rm population.model
> rm consumption.model

6. Rebuild database
> poetry run python manage.py migrate

7. Run server
> poetry run python manage.py runserver


// -----===== If you are windows user, follow these steps
Prerequisites
1. Python 3.11
2. pip

- Open cmd and navigate to project root directory

1. navigate to riceApp
> cd riceApp

2. Download dependency
> pip install Django
> pip install matplotlib
> pip install scikit-learn
> pip install pandas
> pip install statsmodel

3. Setup database table
> python manage.py makemigrations

4. Reset database and model
> del db.sqlite3
> del stock.model
> del population.model
> del consumption.model

5. Rebuild database
> python manage.py migrate

6. Run server
> python manage.py runserver
