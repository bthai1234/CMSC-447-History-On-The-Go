# CMSC-447-Project-Historical-Tours

Historical tours: A web app where users can select historical figures/events and the application will generate a list of sites nearby the user with historical relevance to the selected figure/event. For the sake of simplicity, the MVP of this system will be limited to a small collection of historical figures.

### An example of this App is deployed to a Heroku instance and can be accessed by the following url:  
https://history-on-the-go.herokuapp.com/

### Directions how to run the webapp locally using the django test server:

##### Mac:
1. install virtualenv:  
    `pip install virtualenv`
2. make the virtualenv directory in the root project directory where the file manage.py is:  
    `virtualenv .venv` 
3. Activate the virual environment:  
    `source venv/bin/activate`
4. Install dependancys:  
    `pip install -r ./requirements.txt`
5. download .env file and add the google_API_key in the root project directory 
6. run the following command and go the the url `127.0.0.1:8000` in your browser:  
    `python manage.py runserver`

##### windows:
1. Open your terminal in the root project directory and run the following command:  
    `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
2. install virtualenv:  
    `pip install virtualenv`
3. make the virtualenv directory in the root project directory where the file manage.py is:  
    `python -m virtualenv .venv` 
4. Activate the virual environment:  
    `.venv/Scripts/activate`
5. Install dependancys:  
    `pip install -r ./requirements.txt`
6. download .env file and add the google_API_key in the root project directory:   
7. run the following command and go the the url `127.0.0.1:8000` in your browser:  
    `python manage.py runserver`

### Test Suits:

The django a tests.py file can be found in the tour_app directory and can be ran by calling the following command in the root project directory  
 `python manage.py test tour_app`
 
Tests for the intinerary back end can be ran using:
 `python ./manage.py test tour_app.tests.itineraryTests`

The some of the javascript unit tests for the google maps api implementation can be found the the tour_app\js_tests and can be ran by running the django test server and going to the url below:  
`python manage.py runserver`
`127.0.0.1:8000/tests/map_test`
