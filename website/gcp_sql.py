import pymysql
import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user

# config = {
#     'user': 'test_user',
#     'password': 'test_password',
#     'host': '34.85.253.183',
#     'client_flags': [ClientFlag.SSL],
#     # 'ssl_ca': 'ssl/server-ca.pem',
#     # 'ssl_cert': 'ssl/client-cert.pem',
#     # 'ssl_key': 'ssl/client-key.pem'
# }

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    # try:
    #     if os.environ.get('GAE_ENV') == 'standard':
    conn = pymysql.connect(user=db_user, password=db_password,
                        unix_socket=unix_socket, db=db_name,
                        cursorclass=pymysql.cursors.DictCursor
                        )
    # except pymysql.MySQLError as e:
        # print(e)

    return conn

def add_active_production(filled_form):
    if len(filled_form["body_repair"]) == 0:
        flash('Please enter body repair info!', category='error') 
    else:
        conn = open_connection()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO active_vehicles (ro, damage_level, date_in, tear_down, initial_estimate, estimate, body_repair) VALUES(%s, %s, %s, %s, %s, %s, %s)', filled_form["ro_string"], filled_form["damage_levels"], filled_form["date_in"], filled_form["tear_down"], filled_form["initial_estimate"], filled_form["estimate_status"], filled_form["body_repair"])
            conn.commit()
            conn.close()
        # new_vehicle = ActiveVehicles(ro=ro_string, damage_level=damage_levels, date_in=datetime.strptime(date_in,"%Y-%m-%d"), tear_down=tear_down, inital_estimate=initial_estimate, estimate=estimate_status, body_repair=body_repair )  #providing the schema for the new car
        # db.session.add(new_vehicle) #adding the note to the database 
        # db.session.commit()
        flash('Car Added!', category='success')
        return redirect(url_for('views.home'))            
