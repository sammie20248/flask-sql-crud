from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'inventory' # Database name is already correct from the image

mysql = MySQL(app)

# HOME/READ - Displays all items and handles search
@app.route('/')
def read():
    cur = mysql.connection.cursor()
    search = request.args.get('search')
    # Select all relevant columns from the gerioea_store table
    if search:
        # Search by name using LIKE operator
        cur.execute("SELECT id, name, description, size, cost, material, brand, category, weight, active_status, phone_number FROM gerioea_store WHERE name LIKE %s", ('%' + search + '%',))
    else:
        # Fetch all items if no search query
        cur.execute("SELECT id, name, description, size, cost, material, brand, category, weight, active_status, phone_number FROM gerioea_store")
    data = cur.fetchall()

    # Calculate total inventory value based on the 'cost' column (index 4)
    # Assuming total value is the sum of costs for all items, as there's no quantity/price columns in the provided schema
    total_value = sum(item[4] for item in data) if data else 0 

    cur.close()
    return render_template('index.html', items=data, search=search, total_value=total_value)

# CREATE - Handles adding new items
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Retrieve form data for all columns in gerioea_store
        name = request.form['name']
        description = request.form['description']
        size = request.form['size']
        cost = request.form['cost']
        material = request.form['material']
        brand = request.form['brand']
        category = request.form['category']
        weight = request.form['weight']
        active_status = request.form['active_status']
        phone_number = request.form['phone_number']

        # Basic validation for required fields: name and cost
        if not name or not cost: 
            flash('Name and cost are required.', 'danger')
            return redirect(url_for('create'))

        cur = mysql.connection.cursor()
        # Insert new item into gerioea_store with all collected data
        cur.execute("INSERT INTO gerioea_store (name, description, size, cost, material, brand, category, weight, active_status, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, description, size, cost, material, brand, category, weight, active_status, phone_number))
        mysql.connection.commit() # Commit changes to the database
        cur.close()
        flash('Item added successfully!', 'success')
        return redirect(url_for('read'))
    return render_template('create.html')

# UPDATE - Handles updating existing items
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Retrieve updated form data for all columns
        name = request.form['name']
        description = request.form['description']
        size = request.form['size']
        cost = request.form['cost']
        material = request.form['material']
        brand = request.form['brand']
        category = request.form['category']
        weight = request.form['weight']
        active_status = request.form['active_status']
        phone_number = request.form['phone_number']

        # Basic validation for required fields: name and cost
        if not name or not cost: 
            flash('Name and cost are required.', 'danger')
            return redirect(url_for('update', id=id))

        # Update the item in gerioea_store based on its ID
        cur.execute("UPDATE gerioea_store SET name=%s, description=%s, size=%s, cost=%s, material=%s, brand=%s, category=%s, weight=%s, active_status=%s, phone_number=%s WHERE id=%s",
                    (name, description, size, cost, material, brand, category, weight, active_status, phone_number, id))
        mysql.connection.commit() # Commit changes to the database
        cur.close()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('read'))

    # Fetch item details to pre-fill the update form when accessed via GET
    cur.execute("SELECT id, name, description, size, cost, material, brand, category, weight, active_status, phone_number FROM gerioea_store WHERE id = %s", (id,))
    item = cur.fetchone()
    cur.close()
    return render_template('update.html', item=item)

# DELETE - Handles deleting items
@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    # Delete item from gerioea_store based on its ID
    cur.execute("DELETE FROM gerioea_store WHERE id = %s", (id,))
    mysql.connection.commit() # Commit changes to the database
    cur.close()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('read'))

if __name__ == '__main__':
    app.run(debug=True) # Run the Flask app in debug mode
