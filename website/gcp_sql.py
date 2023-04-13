import os
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from datetime import datetime
from flask_login import login_required, current_user
from google.cloud.sql.connector import Connector ## COMMENT OUT FOR APP ENGINE 
import pymysql ## COMMENT OUT FOR APP ENGINE
from website.sql_connection import connect_with_connector
import sqlalchemy
#UNCOMMENT BELOW FOR APP ENGINE DEPLOYMENT
### INITIALIZE DB 
def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    return connect_with_connector()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

pool = init_connection_pool() # == db in github

### ADD VEHICLED TO ACTIVE PRODUCTION ###
def add_active_production(filled_form):
    ###TODO: if body repair empty not working
    if filled_form["body_repair"] == "None":
        flash('Please enter body repair info!', category='error')
        return redirect(url_for('views.home')) 
    else:
        with pool.connect() as cursor:
            insert_stmt = sqlalchemy.text('INSERT INTO active_vehicles_table (ro, damage_level, date_in, tear_down, inital_estimate, estimate, body_repair) VALUES(:ro, :damage_level, :date_in, :tear_down, :inital_estimate, :estimate, :body_repair)')
            
            cursor.execute(insert_stmt, parameters={"ro": filled_form["ro_string"], "damage_level": filled_form["damage_levels"], "date_in":filled_form["date_in"], "tear_down": filled_form["tear_down"], "inital_estimate": filled_form["initial_estimate"], "estimate": filled_form["estimate_status"], "body_repair": filled_form["body_repair"]  }) 
            cursor.commit()
            result = cursor.execute(sqlalchemy.text("SELECT * from active_vehicles_table")).fetchall()
            print (result)
            cursor.close()

        flash('Car Added!', category='success')
        return redirect(url_for('views.home'))            
### DISPLAY ACTIVE PRODUCTION TABLE ###
def display_active_production():
    display_all = sqlalchemy.text("SELECT * from active_vehicles_table")
    with pool.connect() as cursor:
        execution = cursor.execute(display_all)
        result = execution.fetchall()
    return result

### REMOVE FROM ACTIVE PRODUCTION TABLE ###
def remove_active_production(ro_removed):
    with pool.connect() as cursor:
        print("placeholder")
        cursor.execute(sqlalchemy.text("DELETE FROM `active_vehicles_table` WHERE `ro`=:ro"),parameters={"ro": ro_removed})
        cursor.commit()
        cursor.close()
    flash('RO successfully removed', category='success')        
    return redirect(url_for('views.active_production')) 