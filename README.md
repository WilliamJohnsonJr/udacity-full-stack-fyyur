Fyyur
-----

![Fyyur Screenshot](./fyyur-screenshot.png "Fyyur Screenshot")

Built as part of the Udacity Full Stack Web Developer nanodegree program. See ORIGINAL_README.md for the original README and installation notes.

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

This app requires Python 3.10.19.

# Setup Steps:

1. **Initialize and activate a virtualenv using:**
```
python3 -m venv venv
source ./venv/bin/activate
```
>**Note** - In Windows, the `env` does not have a `bin` directory. Therefore, you'd use the analogous command shown below:
```
source venv/Scripts/activate
```

2. **Install the dependencies:**
```
pip install -r requirements.txt
```

3. **Change `config.py` to connect to your local db:**
To use the current `config.py`, run:
- `createdb fyyur`

It should look like this (fill in your db details where it says `'DB_GOES_HERE'`):
```python
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'DB_GOES_HERE'
```

4. **Migrate your database**
Run: `flask db upgrade`

5. **Run the development server:**
```
FLASK_APP=myapp FLASK_ENV=development python3 app.py
```
