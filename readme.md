# Folder Structure
- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. Repo ships with one required for testing.
- `application` is where our application code is
- `static/style.css` Custom CSS. You can edit it. Its empty currently
- `templates` - Default flask templates folder
- `migrate` - Migration data
- `venv` - Virtual Environment
- ` api.yaml` - API file
- ` app.py` - API file
- ` requirements.txt` - Requirements file



First create Virtual Environment 
- $ python -m venv .venv
Activate Virtual Environment
- $ source .env/bin/activate
Run the app.py file
- $ python3 app.py