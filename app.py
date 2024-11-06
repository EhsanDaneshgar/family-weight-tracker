from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'Leon@2022'  # Required for flashing messages

# Database connection configuration

DB_CONFIG = {
    'DRIVER': '{ODBC Driver 17 for SQL Server}',  # or '{ODBC Driver 18 for SQL Server}' if that's installed
    'SERVER': 'EHSAN_DANESHGAR',  # the name of your server
    'DATABASE': 'FamilyWeightTracker',  # replace with the actual database name you are connecting to
    'Trusted_Connection': 'yes',  # enables Windows Authentication
    'Encrypt': 'yes',  # matches the "Mandatory" encryption setting
    'TrustServerCertificate': 'yes'  # corresponds to the checkbox "Trust server certificate"
}

#conn_str = ';'.join(f'{k}={v}' for k, v in DB_CONFIG.items())
def get_db_connection():
    conn_str = ';'.join(f'{k}={v}' for k, v in DB_CONFIG.items())
    return pyodbc.connect(conn_str)

# Create the templates folder and add this HTML file
"""
templates/index.html:
<!DOCTYPE html>
<html>
<head>
    <title>Family Weight Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .flash-message {
            padding: 10px;
            margin: 10px 0;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 4px;
            color: #155724;
        }
    </style>
</head>
<body>
    <h1>Family Weight Tracker</h1>
    
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for message in messages %}
                <div class="flash-message">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <form method="POST" action="{{ url_for('add_measurement') }}">
        <div class="form-group">
            <label for="date">Date:</label>
            <input type="date" id="date" name="date" required>
        </div>
        
        <div class="form-group">
            <label for="person">Person:</label>
            <select id="person" name="person" required>
                <option value="Ehsan">Ehsan</option>
                <option value="Mahtab">Mahtab</option>
                <option value="Leon">Leon</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="weight">Weight (kg):</label>
            <input type="number" id="weight" name="weight" step="0.1" required>
        </div>
        
        <button type="submit">Add Measurement</button>
    </form>

    <h2>Recent Measurements</h2>
    <table>
        <thead>
            <tr>
                <th>Date</th>
                <th>Person</th>
                <th>Weight (kg)</th>
            </tr>
        </thead>
        <tbody>
            {% for measurement in measurements %}
            <tr>
                <td>{{ measurement.MeasurementDate.strftime('%Y-%m-%d') }}</td>
                <td>{{ measurement.PersonName }}</td>
                <td>{{ "%.1f"|format(measurement.Weight) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MeasurementDate, PersonName, Weight 
        FROM WeightMeasurements 
        ORDER BY MeasurementDate DESC, PersonName
    """)
    measurements = cursor.fetchall()
    conn.close()
    return render_template('index.html', measurements=measurements)

@app.route('/add', methods=['POST'])
def add_measurement():
    date = request.form['date']
    person = request.form['person']
    weight = request.form['weight']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO WeightMeasurements (MeasurementDate, PersonName, Weight)
            VALUES (?, ?, ?)
        """, (date, person, weight))
        conn.commit()
        flash('Measurement added successfully!')
    except Exception as e:
        flash(f'Error adding measurement: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)