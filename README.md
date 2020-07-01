# cheap-matrix-onboarding

A tool allowing users to get invites to private matrix channels.

# Requirements

- A Matrix "service account" with invite privilege on the desired channels
- A GSuite organization
- GSuite OAuth2 credentials

# Install

First, we recommend you create a python virtualenv :

```(bash)
python -m venv .venv
```

Then, execute the following commands :

```(bash)
source .venv/bin/activate
pip install -r requirements.txt
```

The app needs minimal config (`onboard/settings.py`):

```(python)
# Google Auth Backend
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'changeme'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'changeme'

# Matrix Settings
MATRIX_HOMESERVER = 'changeme' # without leading https:// and trailing /_matrix
MATRIX_USERNAME = 'changeme' # just the local part without leading @
MATRIX_PASSWORD = 'changeme'
```

After the database is configured :

```(bash)
./manage.py migrate
./manage.py createsuperuser
```

To start playing with this thing :

```(bash)
./manage.py runserver
```
