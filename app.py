from flask import Flask, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy  
from flask import Flask, request, redirect, url_for, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Course, Enrollment, Grade, db, Profile
import os

#DATABASE_TYPE = 'enter your database type'
#USERNAME = 'username'
#PASSWORD = 'password'
#DATABASE = 'name of the database'
#SQLALCHEMY_DATABASE_URI = f'{DATABASE_TYPE}://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE}'

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")  #connect to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # Disables modification tracking for performance reasons.
app.secret_key = '34762346234sdg'

db.init_app(app)    #initialize the database object 

def create_tables():
    with app.app_context():     #is used to run the database commands within the application context.
        db.create_all()
        db.session.commit()
    print("All tables created successfully")


# Main page with login form and registration button
@app.route('/')
def main_page():
    return render_template('login.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        name = request.form['name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']
        
        # Check if the username already exists
        existing_user = User.query.filter_by(UserName=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        # Create and add User
        user = User(UserName=username, Password=password, Role=role)
        db.session.add(user)
        
        # Commit to generate UserID for Profile
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while committing user: {e}")
            flash('An error occurred while registering user')
            return redirect(url_for('register'))
        
        # Create and add Profile
        profile = Profile(UserID=user.UserID, Name=name, Birthdate=birthdate, Gender=gender)
        db.session.add(profile)
        
        # Commit the Profile addition
        try:
            db.session.commit()
            print(f"User {username} and Profile created successfully")
            return redirect(url_for('main_page'))
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred while committing profile: {e}")
            flash('An error occurred while creating profile')
            return redirect(url_for('register'))
    
    return render_template('register.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['submit'] == 'signup':
            return redirect(url_for('register'))
        else:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(UserName=username).first()
            if user and check_password_hash(user.Password, password):
                session['user_id'] = user.UserID  # Store user_id in session
                if user.Role == 'student':
                    return redirect(url_for('student_dashboard'))
                else:
                    return redirect(url_for('instructor_dashboard'))
            else:
                flash('Invalid username or password')
                return redirect(url_for('main_page'))
    return render_template('login.html')


# Instructor Dashboard
@app.route('/instructor_dashboard', methods=['GET', 'POST'])
def instructor_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    if request.method == 'POST':
        if 'create_course' in request.form:
            flash('Course Created Successfully')
            return redirect(url_for('create_course'))
        elif 'view_courses' in request.form:
            return redirect(url_for('view_courses'))
        elif 'grade_student' in request.form:
            flash('Student has been graded successfully')
            return redirect(url_for('grade_student'))
        elif 'logout' in request.form:
            session.pop('user_id', None)
            return redirect(url_for('main_page'))
        elif 'edit' in request.form:
            flash('Profile Updated Successfully')
            return redirect(url_for('edit_profile'))
        
    if request.method == 'GET':
        return render_template('instructor_dashboard.html', user_id=user_id)


# Create a new course (Instructor only)
@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('instructor_dashboard'))
        
        if 'submit' in request.form:
            title = request.form['title']
            description = request.form['description']
            schedule = request.form['schedule']
            
            course = Course(Title=title, Description=description, Schedule=schedule, UserID=user_id)
            db.session.add(course)
            try:
                db.session.commit()
                flash('Course has been added successfully!')
                return redirect(url_for('instructor_dashboard'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {e}')
                return redirect(url_for('create_course'))
    
    return render_template('create_course.html', user_id=user_id)


# View courses (Instructor only)
@app.route('/view_courses')
def view_courses():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    # Query to get all courses and join with User table to get instructor names
    courses = db.session.query(Course, User.UserName).join(User, Course.UserID == User.UserID).all()
    
    return render_template('view_courses.html', courses=courses)

#Grade a student (Instructor only)
@app.route('/grade_student', methods=['GET', 'POST'])
def grade_student():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    if request.method == 'POST':
        if 'course_id' in request.form:
            course_id = request.form['course_id']
            # Fetch students enrolled in the selected course
            enrollments = db.session.query(Enrollment, User.UserName).join(User, Enrollment.UserID == User.UserID).filter(Enrollment.CourseID == course_id).all()
            return render_template('grade_student.html', course_id=course_id, enrollments=enrollments)
        elif 'assign_grade' in request.form:
            enrollment_id = request.form['enrollment_id']
            grade_value = request.form['grade']
            grade = Grade(EnrollmentID=enrollment_id, Grade=grade_value)
            db.session.add(grade)
            try:
                db.session.commit()
                flash('Grade assigned successfully')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while assigning the grade')
            return redirect(url_for('instructor_dashboard'))

    # Fetch courses taught by the instructor
    courses = db.session.query(Course).filter_by(UserID=user_id).all()
    return render_template('select_course.html', courses=courses)


###########Student Dashboard
@app.route('/student_dashboard', methods=['GET', 'POST'])
def student_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    if request.method == 'POST':
        if 'enroll_course' in request.form:
            return redirect(url_for('enroll_course'))
        elif 'view_courses' in request.form:
            return redirect(url_for('view_enrolled_courses'))
        elif 'edit_profile' in request.form:
            return redirect(url_for('edit_profile'))
        elif 'logout' in request.form:
            session.pop('user_id', None)
            return redirect(url_for('main_page'))
        
    return render_template('student_dashboard.html', user_id=user_id)


# Enroll in a course (Student only)
@app.route('/enroll_course', methods=['GET', 'POST'])
def enroll_course():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in
    
    if request.method == 'POST':
        course_id = request.form['course_id']
        existing_enrollment = Enrollment.query.filter_by(UserID=user_id, CourseID=course_id).first()
        
        if existing_enrollment:
            flash('You are already enrolled in this course.')
        else:
            enrollment = Enrollment(UserID=user_id, CourseID=course_id)
            db.session.add(enrollment)
            try:
                db.session.commit()
                flash('Successfully enrolled in the course!')
            except Exception as e:
                db.session.rollback()
                flash(f'Error occurred: {e}')
        
        return redirect(url_for('enroll_course'))
    
    if request.method == 'GET': #display
        # Query to get all courses with their instructor names
        courses = db.session.query(Course, User).join(User, Course.UserID == User.UserID).all()
        return render_template('enroll_course.html', courses=courses)


# View enrolled courses and grades (Student only)
@app.route('/view_enrolled_courses', methods=['GET'])
def view_enrolled_courses():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in

    # Query to get the enrolled courses for the user
    enrolled_courses = db.session.query(Enrollment, Course, User).join(Course, Enrollment.CourseID == Course.CourseID).join(User, Course.UserID == User.UserID).filter(Enrollment.UserID == user_id).all()
    #this returns a list of tuples, each tuple contains an Enrollment object, Course object, and User object
    
    courses_details = []
    for enrollment, course, instructor in enrolled_courses:
        # Query to get the grade for this course and user
        grade_entry = db.session.query(Grade).filter_by(EnrollmentID=enrollment.EnrollmentID).first()
        course_details = {
            'CourseID': course.CourseID,
            'Title': course.Title,
            'Description': course.Description,
            'Instructor': instructor.UserName,
            'Schedule': course.Schedule,
            'Grade': grade_entry.Grade if grade_entry else 'N/A'
        }
        courses_details.append(course_details)

    return render_template('view_enrolled_courses.html', courses=courses_details)



#Edit Profile (Instructor and Student)
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main_page'))  # Redirect if not logged in

    user = User.query.get(user_id)
    profile = Profile.query.filter_by(UserID=user_id).first()

    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        name = request.form['name']
        birthdate = request.form['birthdate']
        gender = request.form['gender']

        # Update User details
        if password:
            user.Password = generate_password_hash(password)
        user.UserName = user_name
        
        # Update Profile details
        profile.Name = name
        profile.Birthdate = birthdate if birthdate else None
        profile.Gender = gender
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('instructor_dashboard') if user.Role == 'instructor' else url_for('student_dashboard'))

    return render_template('edit_profile.html', user=user, profile=profile)






if __name__ == '__main__':
    create_tables()  # Create tables before starting the app
    app.run(debug=True)