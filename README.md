# wallet
A reusable app to keep your money in check.

# Features
You can simple add income/expense or upload an excel sheet for multiple transactions.

# ToDo
Display the table with bootstrap datatable. (Easy sort and filter)
Add an option for comments. (Model already has that field, you can change it easily)

# To Run
1. `virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`	
4. `python manage.py makemigrations`
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`
8. `python populate.py`
9. Head over to 127.0.0.1:8000/app/ or localhost:8000/app/
