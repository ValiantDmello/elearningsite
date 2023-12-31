# e-learning site (LMS using Django)

## Project Description
This LMS (Learning Management System) project is a web application designed to facilitate online learning and course management using Django. This platform allows users to upload courses, enroll in them, and access educational content in a structured and user-friendly manner.
Link to deployed live server: http://valiant9.pythonanywhere.com/

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Features
* User registration and authentication system.
* Course creation and management for instructors.
* Course enrollment for students.
* Users can buy premium plan or buy individuals courses.
* Uploading and viewing course materials.
* Search and categorization of courses.
* Admin panel for site management.

## Getting Started

### Prerequisites
* Python-3.9.18
* VS code (or any other code editor / IDE)

### Installation
1. Clone the repository:
  ```git clone https://github.com/ValiantDmello/elearningsite.git```
2. Navigate to the project directory:
  ```cd elearningsite```
3. Create a virtual environment and activate it:
  ```python -m venv venv```
  ```source venv/bin/activate # On Windows, use venv\Scripts\activate```
4. Install the project dependencies:
  ```pip install -r requirements.txt```
5. Apply database migrations:
  ```python manage.py migrate```
6. Create a superuser (admin) account:
  ```python manage.py createsuperuser```
7. Start the development server:
   ```python manage.py runserver```

Your LMS should now be accessible at http://127.0.0.1:8000/

## Usage
* User can register and login
* User can access the teacher portal and create courses and lessons
* Students can enroll to the courses and veiw its content

## Contributing
If you'd like to contribute to this project, please follow these guidelines:

* Create an issue to discuss proposed changes or improvements.
* Fork the project and create a branch for your feature or fix.
* Make your changes, test them, and submit a pull request with a clear description of your changes.

