from flask import Flask, request, jsonify, render_template, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)
database_url = "postgresql://web_postgresql_w2wm_user:WE9n3h8BO5KQG4NXfhe8tO4afgZETitD@dpg-cvngq97fte5s73ccdnrg-a.oregon-postgres.render.com/web_postgresql_w2wm"
# Database connection
def get_db_connection():
    connection = psycopg2.connect(
        host="dpg-cvngq97fte5s73ccdnrg-a", 
        dbname="web_postgresql_w2wm",  
        user="web_postgresql_w2wm_user",  
        password="WE9n3h8BO5KQG4NXfhe8tO4afgZETitD"  
    )
    return connection

# Initialize the database by running SQL script
def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    with open("database.sql", "r") as sql_file:
        sql_script = sql_file.read()
    
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)
    
    connection.commit()
    cursor.close()
    connection.close()

# Run the database initialization (if needed)
# initialize_database()

# Routes
@app.route('/')
def home():
    return render_template('index.html')

# Route to display the HTML form
@app.route('/add-project', methods=['GET'])
def add_project_form():
    return render_template('projects.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add_project', methods=['POST'])
def add_project():
    try:
        # Get data from the form
        data = request.get_json()
        title = data['title']
        description = data['description']
        image_url = data.get('image_url', '')  # Optional
        github_link = data.get('github_link', '')  # Optional
        
        # Insert data into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO projects (title, description, image_url, github_link) VALUES (%s, %s, %s, %s)", 
            (title, description, image_url, github_link)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({"message": "Project added successfully!"}), 201  # Send JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/project-list', methods=['GET'])
def get_projects():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, description, image_url, github_link FROM projects")
        projects = cursor.fetchall()
        
        # List of project dictionaries
        projects_list = [
            {"id": proj[0], "title": proj[1], "description": proj[2], "image_url": proj[3], "github_link": proj[4]}
            for proj in projects
        ]
        
        cursor.close()
        connection.close()
        
        # Pass the projects list to the template
        return render_template('project-list.html', projects=projects_list)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/contact', methods=['POST'])
def save_message():
    data = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
            (data['name'], data['email'], data['message'])
        )
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": "Message received"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
