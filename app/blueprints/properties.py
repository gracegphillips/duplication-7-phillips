from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd

properties = Blueprint('properties', __name__)

@properties.route('/show_properties')
def show_properties():
    connection = get_db()
    query = """
    SELECT property_id, client_id, address, city, state, zip_code, property_type, house_size, price, shown_date
    FROM properties_shown
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['property_id', 'client_id', 'address', 'city', 'state', 'zip_code', 'property_type', 'house_size', 'price', 'shown_date'])
    df['Actions'] = df['property_id'].apply(lambda id:
      f'<a href="{url_for("properties.edit_property_data", property_id=id)}" class="btn btn-sm btn-info">Edit</a> '
      f'<form action="{url_for("properties.delete_property_data", property_id=id)}" method="post" style="display:inline;">'
      f'<button type="submit" class="btn btn-sm btn-danger">Delete</button></form>'
      )
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False, escape=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    return render_template("properties.html", table=rows_only)

@properties.route('/add_property_data', methods=['GET', 'POST'])
def add_property_data():
    if request.method == 'POST':
        client_id = request.form['client_id']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        property_type = request.form['property_type']
        house_size = request.form['house_size']
        price = request.form['price']
        shown_date = request.form['shown_date']

        connection = get_db()
        query = "INSERT INTO properties_shown (client_id, address, city, state, zip_code, property_type, house_size, price, shown_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (client_id, address, city, state, zip_code, property_type, house_size, price, shown_date))
        connection.commit()
        flash("New property data added successfully!", "success")
        return redirect(url_for('properties.show_properties'))

    return render_template("add_property_data.html")

@properties.route('/edit_property_data/<int:property_id>', methods=['GET', 'POST'])
def edit_property_data(property_id):
    connection = get_db()
    if request.method == 'POST':
        client_id = request.form['client_id']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code']
        property_type = request.form['property_type']
        house_size = request.form['house_size']
        price = request.form['price']
        shown_date = request.form['shown_date']

        query = "UPDATE properties_shown SET client_id = %s, address = %s, city = %s, state = %s, zip_code = %s, property_type = %s, house_size = %s, price = %s, shown_date = %s WHERE property_id = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (client_id, address, city, state, zip_code, property_type, house_size, price, shown_date, property_id))
        connection.commit()
        flash("Property data updated successfully!", "success")
        return redirect(url_for('properties.show_properties'))

    query = "SELECT * FROM properties_shown WHERE property_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (property_id,))
        property_data = cursor.fetchone()

    return render_template("edit_property_data.html", property_data=property_data)

@properties.route('/delete_property_data/<int:property_id>', methods=['POST'])
def delete_property_data(property_id):
    connection = get_db()
    query = "DELETE FROM properties_shown WHERE property_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (property_id,))
    connection.commit()
    flash("Property data deleted successfully!", "success")
    return redirect(url_for('properties.show_properties'))

