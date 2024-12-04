from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import get_db
import pandas as pd
from ..functions import filter_by_name


clients = Blueprint('clients', __name__)


@clients.route('/show_clients', methods=['GET', 'POST'])
def show_clients():
    connection = get_db()
    query = """
    SELECT client_id, name, email, phone
    FROM clients
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['client_id', 'name', 'email', 'phone'])

    # Retrieve list of client names, emails, and phones
    client_names = df['name'].tolist()
    client_emails = df['email'].tolist()
    client_phones = df['phone'].tolist()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        filtered_clients = filter_by_name(result, name=name, email=email, phone=phone)
        df = pd.DataFrame(filtered_clients, columns=['client_id', 'name', 'email', 'phone'])

    df['Actions'] = df['client_id'].apply(lambda id:
    f'<button type="button" class="btn btn-sm btn-info" data-toggle="modal" data-target="#editClientModal" data-client-id="{id}">Edit</button> '
    f'<button type="button" class="btn btn-sm btn-danger" data-toggle="modal" data-target="#deleteClientModal" data-client-id="{id}">Delete</button>'
)
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=False, escape=False)
    rows_only = table_html.split('<tbody>')[1].split('</tbody>')[0]

    return render_template("clients.html", table=rows_only, client_names=client_names, client_emails=client_emails, client_phones=client_phones)



@clients.route('/add_client_data', methods=['GET', 'POST'])
def add_client_data():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        connection = get_db()
        query = "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, (name, email, phone))
        connection.commit()
        flash("New client data added successfully!", "success")
        return redirect(url_for('clients.show_clients'))

    return render_template("add_client_data.html")


@clients.route('/edit_client_data', methods=['POST'])
def edit_client_data():
    client_id = request.form['client_id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    connection = get_db()
    query = "UPDATE clients SET name = %s, email = %s, phone = %s WHERE client_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (name, email, phone, client_id))
    connection.commit()
    flash("Client data updated successfully!", "success")
    return redirect(url_for('clients.show_clients'))


@clients.route('/delete_client_data/<int:client_id>', methods=['POST'])
def delete_client_data(client_id):
    connection = get_db()
    query = "DELETE FROM clients WHERE client_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (client_id,))
    connection.commit()
    flash("Client data deleted successfully!", "success")
    return redirect(url_for('clients.show_clients'))



