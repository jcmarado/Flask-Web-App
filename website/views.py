from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, ActiveVehicles
from . import db
import json
from datetime import datetime
from .gcp_sql import add_active_production, display_active_production, remove_active_production

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/active-production', methods=['GET', 'POST'])
def active_production():
    if request.method == 'POST':
        filled_form = {
            'ro_string': request.form.get('ro'),
            'damage_levels': request.form.get('damage_level'),
            'date_in': request.form.get('date_in'),
            'tear_down': request.form.get('tear_down'),
            'initial_estimate': request.form.get('initial_estimate'),
            'estimate_status': request.form.get('estimate_status'),
            'body_repair': request.form.get('body_repair')
        }
        add_active_production(filled_form)
    ### END IF ###
    display = display_active_production()
    return render_template("active_production.html", user=current_user, data=display)

@views.route('/delete-vehicle', methods=['POST'])
def delete_active_production():
   delete_form = request.form.get("ro_1")
   first_ro = request.form.get('ro1')
   scnd_ro = request.form.get('ro2')

   print(delete_form)
    # noteId = note['noteId']
    # note = Note.query.get(noteId)
    # if note:
    #     if note.user_id == current_user.id:
    #         db.session.delete(note)
    #         db.session.commit()

   return render_template("active_production.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
