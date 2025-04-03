from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(host="localhost", user="root", passwd="admin123")
cursor = db.cursor()

def initialize_database():
    with open("database.sql", "r") as sql_file:
        sql_script = sql_file.read()
    
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)
    
    db.commit()

# Run the database initialization
initialize_database()

# Connect to portfolio_db after initialization
db.select_db("portfolio_db")

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
        cursor.execute("INSERT INTO projects (title, description, image_url, github_link) VALUES (%s, %s, %s, %s)", 
                       (title, description, image_url, github_link))
        db.commit()
        
        return jsonify({"message": "Project added successfully!"}), 201  # Send JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/project-list', methods=['GET'])
def get_projects():
    try:
        cursor.execute("SELECT id, title, description, image_url, github_link FROM projects")
        projects = cursor.fetchall()
        
        # List of project dictionaries
        projects_list = [
            {"id": proj[0], "title": proj[1], "description": proj[2], "image_url": proj[3], "github_link": proj[4]}
            for proj in projects
        ]
        
        # Pass the projects list to the template
        return render_template('project-list.html', projects=projects_list)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/contact', methods=['POST'])
def save_message():
    data = request.json
    cursor.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                   (data['name'], data['email'], data['message']))
    db.commit()
    return jsonify({"message": "Message received"}), 201

if __name__ == '__main__':
    app.run(debug=True)
