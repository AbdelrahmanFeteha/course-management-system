from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the ORM classes
class Profile(db.Model):
    __tablename__ = 'Profile'

    ProfileID = db.Column(db.Integer, primary_key=True)   # This will auto increment
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False) 
    Name = db.Column(db.String(100), nullable=False)
    Birthdate = db.Column(db.Date, nullable=True)
    Gender = db.Column(db.String(1), nullable=False)
    
    # Define relationships
    user = db.relationship('User', back_populates='profile')
    
class User(db.Model):
    __tablename__ = 'User'
    
    UserID = db.Column(db.Integer, primary_key=True)      # This will auto increment
    Password = db.Column(db.String(250), nullable=False)
    UserName = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(10), nullable=False)
    
    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='user')
    course = db.relationship('Course', back_populates='user')
    profile = db.relationship('Profile', back_populates='user')

class Course(db.Model):
    __tablename__ = 'Courses'
    
    CourseID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    Schedule = db.Column(db.Date, nullable=True)  
    Title = db.Column(db.String(100), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='course')
    enrollment = db.relationship('Enrollment', back_populates='course')
    
    def __repr__(self):
        return f"Course ID: {self.CourseID} Course Title: {self.Title} Course Description: {self.Description} Course Teacher: {self.user.UserName}"
    
class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    
    EnrollmentID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey('Courses.CourseID'), nullable=False)
    EnrollmentDate = db.Column(db.Date, default=db.func.current_date())
    
    # Relationships
    user = db.relationship('User', back_populates='enrollment')
    course = db.relationship('Course', back_populates='enrollment')
    grade = db.relationship('Grade', back_populates='enrollment')

class Grade(db.Model):
    __tablename__ = 'Grade'
    
    GradeID = db.Column(db.Integer, primary_key=True)
    EnrollmentID = db.Column(db.Integer, db.ForeignKey('Enrollment.EnrollmentID'), nullable=False)
    Grade = db.Column(db.Float, nullable=False)

    # Relationships
    enrollment = db.relationship('Enrollment', back_populates='grade')
