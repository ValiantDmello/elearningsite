## Project Description
This LMS (Learning Management System) project is a web application designed to facilitate online learning and course management using Django. This platform allows users to upload courses, enroll in them, and access educational content in a structured and user-friendly manner.

## Features
* User registration and authentication system.
* Course creation and management for instructors.
* Course enrollment for students.
* Uploading and viewing course materials.
* Search and categorization of courses.
* Admin panel for site management.

## Getting Started

### Prerequisites
* Python-3.9.18
* VS code (or any other code editor / IDE)

### Installation
1. Clone the repository:
  ```git clone https://github.com/yourusername/your-lms-project.git```
2. Navigate to the project directory:
  ```cd your-lms-project```
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
