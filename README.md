# wallet
A reusable app to keep your money in check.

# Features
You can simply add income/expense or upload an excel sheet for multiple transactions. You can also download your income/expenses in an excel sheet.

# Update
- Added calendar for date picking while adding income/expenses. (24-12-2017)
- Removed unused css and js scripts for fast loading.(24-12-2017)
- Fixed some other bugs(24-12-2017)

# ToDo
- Display the table with bootstrap datatable. (Easy sort and filter)
- Add an option for comments. (Model already has that field, you can change it easily)
- Improve front-end :(
- Add option to download in a specific time range.
- Proper form heading

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
