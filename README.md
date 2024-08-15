# Course Management System
The Course Management System is a web application built with Flask and SQLAlchemy that allows users to manage courses, enroll in courses, and view grades. The system has separate functionalities for instructors and students, including course creation, enrollment, and profile management.

## Features

- **User Registration & Login**: Users can register and log in with different roles (student or instructor).
- **Instructor Dashboard**:
  - Create new courses.
  - View created courses.
  - Grade students.
  - Edit profile.
- **Student Dashboard**:
  - Enroll in courses.
  - View enrolled courses and grades.
  - Edit profile.
- **Profile Management**: Both students and instructors can update their profiles.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **PostgreSQL**: A powerful, open-source object-relational database system.
- **Werkzeug**: A comprehensive WSGI web application library.


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/course-management-system.git
    ```
2. Navigate to the project directory:
    ```sh
    cd course-management-system
    ```
3. Create a virtual environment:
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
5. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Code Structure

- **`app.py`**: The main application file containing routes, logic for user registration, login, and dashboards.
- **`models.py`**: Contains SQLAlchemy models for the database tables.
- **`.env`**: Configuration file for the database connection string.


## Usage

1. Run the Flask application:
    ```sh
    flask run
    ```
2. Open your web browser and navigate to `http://127.0.0.1:5000`.


## License

This project is licensed under the MIT License. See the [`LICENSE`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2Fc%3A%2FUsers%2FAbdelrahman%20Feteha%2FDesktop%2FCoding%20Projects%2Fworthy%2FFlask_Course_Management_System%2FLICENSE%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%5D "c:\Users\Abdelrahman Feteha\Desktop\Coding Projects\worthy\Flask_Course_Management_System\LICENSE") file for details.
