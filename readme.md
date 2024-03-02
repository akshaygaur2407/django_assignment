## Description

This is the assignment to extract the data feom swiggy API and return the relevant fields in the form of csv.
Please use postman to send the resturant id and receive the csv data, here is a sample postman requestr:- http://127.0.0.1:8000/myapp/fetch_and_extract_menu/?restaurant_id=37968

## Installation
Clone the repository:


```python
git clone https://github.com/your_username/django_assignment.git
```

## Install dependencies:

```python
pip install -r requirements.txt
```

## Navigate to the project directory:

```python
cd myproject
```
## Run the Django development server:

```python
python manage.py runserver
```
Access the application in your postman, here is the sample url:- http://127.0.0.1:8000/myapp/fetch_and_extract_menu/?restaurant_id=37968.

## Running Tests
To run the unit tests for the project:

```python
python manage.py test myapp.test_views
```
