# Assignment Submission DBMS 
The main objective of this project is to build a backend-only system (without frontend UI) that automates the process of managing courses, students, assignments, and submissions. The project uses MySQL to store structured data and Python scripts to perform operations such as creating the database schema, seeding initial data, inserting submissions, displaying pending submissions, and detecting late submissions. Even without a graphical interface, the system efficiently captures the core workflow of an academic submission portal.
The project has been implemented using a modular approach. The db_helper.py file centralizes the database connection settings, ensuring that any script can connect to MySQL easily. The create_schema.py script is responsible for constructing all required tables such as users, courses, assignments, enrollments, submissions, and grades. Each table has proper primary keys, foreign keys, and unique constraints. This ensures data consistency, reduces duplication, and maintains referential integrity between students, their courses, and their assignment submissions.

For demonstration purposes, a seed_data.py script is included. It automatically inserts sample users (one instructor and two students), creates a course, adds them into enrollments, and generates one sample assignment with a deadline. This helps in quickly initializing the database for viva or testing. The most important feature of the project—the assignment submission process—is implemented in submit_demo.py. This script simulates how a student uploads a file. It copies the file to the uploads folder and inserts a new row into the submissions table, also marking whether the submission is late based on the assignment’s due date.

To support teachers, an additional script called list_pending.py identifies which students have not yet submitted a particular assignment. This uses a LEFT JOIN operation to compare enrollments with submissions, making it easy to see defaulters or pending work. Similarly, the late_submissions.py script highlights which students submitted after the deadline. In real educational platforms, these functionalities are essential for transparency and progress tracking.



Follow the README instructions below.

1. Install XAMPP and start MySQL from XAMPP Control Panel.
2. Open this folder in VS Code.
3. In VS Code Terminal:
   - `python -m venv venv`
   - `venv\Scripts\activate`
   - `pip install -r requirements.txt`
4. Run `python scripts/create_schema.py`
5. Run `python scripts/seed_data.py`
6. Put a file named `sample_submission.pdf` in the project root (or the script will create a placeholder).
7. Run `python scripts/submit_demo.py`
8. Run `python scripts/list_pending.py` and `python scripts/late_submissions.py`
