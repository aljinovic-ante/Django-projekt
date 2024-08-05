# Student Enrollment System

Web application created using Django framework. Designed for student enrollment system with three user roles: student, professor, and administrator.

# Administrator Role:
-Authentication
-View and modify the list of courses
-Add new courses
-Assign courses to professors
-View list of students and professors
-Add and edit student and professor information
-Create and modify student enrollment records
-View student lists for each course with a "view student list" link

# Professor Role:
-Authentication
-View list of assigned courses
-View student list for each course taught
-Change course status (enrolled, passed, failed)
-Filter students by course status

# Student Role:
-Authentication
-Enroll and withdraw from courses
-System Requirements:

All changes made via POST requests
Ensure application security (password encryption, protection against SQL injection and XSS)
Adjust database structure to include a "roles" table
Implement code in Django framework following MVC (MVT) architecture
Maintain easy extensibility for additional functionalities (e.g., displaying total enrolled ECTS credits)
Focus on functionality, security, usability, and code organization
The enrollment form will display unenrolled and enrolled/passed courses by semester for students and administrators. Menus will be role-specific with restricted access.
