from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd
from ..functions import filter_properties


properties = Blueprint('properties', __name__)


@properties.route('/show_properties', methods=['GET', 'POST'])
def show_properties():
    connection = get_db()
    query = """
    SELECT p.property_id, p.client_id, p.address, p.city, p.state, p.zip_code, p.property_type, p.house_size, p.price, p.shown_date, c.name AS client_name
    FROM properties_shown p
    JOIN clients c ON p.client_id = c.client_id
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['property_id', 'client_id', 'address', 'city', 'state', 'zip_code', 'property_type', 'house_size', 'price', 'shown_date', 'client_name'])

    # Retrieve list of client IDs, cities, and states
    client_ids = df['client_id'].unique().tolist()
    client_names = {row['client_id']: row['client_name'] for row in result}
    cities = df['city'].unique().tolist()
    states = df['state'].unique().tolist()

    if request.method == 'POST':
        min_size = request.form.get('min_size')
        max_size = request.form.get('max_size')
        min_price = request.form.get('min_price')
        max_price = request.form.get('max_price')
        client_id = request.form.get('client_id')
        city = request.form.get('city')
        state = request.form.get('state')

        # Convert empty strings to None
        min_size = int(min_size) if min_size else None
        max_size = int(max_size) if max_size else None
        min_price = float(min_price) if min_price else None
        max_price = float(max_price) if max_price else None
        client_id = int(client_id) if client_id else None

        filtered_properties = filter_properties(result, min_size=min_size, max_size=max_size, min_price=min_price, max_price=max_price, client_id=client_id, city=city, state=state)
        df = pd.DataFrame(filtered_properties, columns=['property_id', 'client_id', 'address', 'city', 'state', 'zip_code', 'property_type', 'house_size', 'price', 'shown_date', 'client_name'])

    df['Actions'] = df.apply(lambda row:
        f'<button type="button" class="btn btn-sm btn-info" data-toggle="modal" data-target="#editPropertyModal" data-property-id="{row["property_id"]}" data-client-id="{row["client_id"]}" data-client-name="{row["client_name"]}" data-address="{row["address"]}" data-city="{row["city"]}" data-state="{row["state"]}" data-zip-code="{row["zip_code"]}" data-property-type="{row["property_type"]}" data-house-size="{row["house_size"]}" data-price="{row["price"]}" data-shown-date="{row["shown_date"]}">Edit</button> '
        f'<button type="button" class="btn btn-sm btn-danger" data-toggle="modal" data-target="#deletePropertyModal" data-property-id="{row["property_id"]}">Delete</button>', axis=1
    )
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False, escape=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    # Retrieve list of client IDs and names for the dropdown
    query = "SELECT client_id, name FROM clients"
    with connection.cursor() as cursor:
        cursor.execute(query)
        clients = cursor.fetchall()

    return render_template("properties.html", table=rows_only, client_ids=client_ids, client_names=client_names, cities=cities, states=states, clients=clients)


@properties.route('/add_property_data', methods=['GET', 'POST'])
def add_property_data():
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

        query = "INSERT INTO properties_shown (client_id, address, city, state, zip_code, property_type, house_size, price, shown_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (client_id, address, city, state, zip_code, property_type, house_size, price, shown_date))
        connection.commit()
        flash("New property data added successfully!", "success")
        return redirect(url_for('properties.show_properties'))

    # Retrieve list of client IDs and names
    query = "SELECT client_id, name FROM clients"
    with connection.cursor() as cursor:
        cursor.execute(query)
        clients = cursor.fetchall()

    return render_template("properties.html", clients=clients)




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

