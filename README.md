# Weather station

## Setup (first time only)

1. Clone the source into a directory called "weather_station" inside the current directory
```git clone https://github.com/bebosudo/weather_station weather_station```

2. Move into the directory
```cd weather_station```

3. Create a new python3 virtualenv in a folder called "venv"
```virtualenv -p /usr/bin/python3 venv```

4. Activate the virtualenv just created
```. venv/bin/activate```

You can verify that this step took place correctly by noticing the "(venv)" string prepended to your prompt.

5. Install Django
```pip install django```

6. Create and populate the "secret_things" module
```echo "SECRET_KEY='supersecretkey'" > weather_station_website/secret_things.py```

7. Run the test suite
```./manage.py test -k```

8. Deactivate the virtualenv
```deactivate```

## Run the project

1. Move to the "weather_station" directory

2. Activate the virtualenv
```. venv/bin/activate```

3. Run the server
```./manage.py runserver```

4. Don't forget to deactivate the virtualenv after you've finished
```deactivate```
