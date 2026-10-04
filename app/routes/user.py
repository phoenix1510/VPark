from flask import render_template, redirect, url_for, Blueprint, session, flash , jsonify , request
from app.db.db_operations import (
    get_vehicle_type, get_slot_status, search_facility, fetch_all_vehicle_rates_of_facility,
    end_session, get_session_status, fetch_session, remove_vehicle, get_owner_of_vehicle,
    fetch_rate_used_for_operation, add_parking_session, fetch_vehicles_of_user, add_vehicle,
    get_user_by_id, delete_user, fetch_all_available_slots, change_slot_status, fetch_sessions_of_user
)
from .auth import auth_required
from .wtfforms import Add_vehicle_Form, Remove_user_Form , Remove_vehicle_Form , Finish_parking_Form , Start_parking_Form
from datetime import datetime

user_bp = Blueprint('user',__name__,url_prefix='/user')


# dashboard + profile route endpoints


@user_bp.route('/dashboard', methods=['GET','POST'])
@auth_required
def user_dashboard():
    username = session.get('username')
    return render_template('user_dashboard.html',current_user = username)

@user_bp.route('/profile',methods=["GET","POST"])
@auth_required
def User_profile():
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    remove_user_form = Remove_user_Form()
    return render_template('user_profile.html', current_user = user, remove_user_form = remove_user_form)


@user_bp.route('/profile/delete_user', methods = ['GET','POST'])
@auth_required
def Remove_user():
    remove_user_form = Remove_user_Form()
    if remove_user_form.validate_on_submit():
        user_id = session.get('user_id')
        delete_user(user_id)
        flash('User deleted!','success')
        return redirect(url_for('auth.logout'))


# vehicle endpoints

@user_bp.route('/dashboard/vehicles',methods=['GET','POST'])
@auth_required
def Fetch_vehicles():
    user_id = session.get('user_id')
    vehicles = fetch_vehicles_of_user(user_id)
    add_vehicle_form = Add_vehicle_Form()
    remove_vehicle_form = Remove_vehicle_Form()
    return render_template('vehicles.html', vehicles = vehicles, add_vehicle_form = add_vehicle_form, remove_vehicle_form = remove_vehicle_form)

@user_bp.route('/dashboard/vehicles/add_vehicle', methods=['GET','POST'])
@auth_required
def Add_vehicle():
    user_id = session.get('user_id')
    add_vehicle_form = Add_vehicle_Form()
    if add_vehicle_form.validate_on_submit():
        vehicle_name = add_vehicle_form.vehicle_name.data
        registration_number = add_vehicle_form.registration.data
        vehicle_type = add_vehicle_form.vehicle_type.data
        add_vehicle(vehicle_name,registration_number,user_id,vehicle_type)
        flash('vehicle added successfully!','success')
        return redirect(url_for('user.Fetch_vehicles', add_vehicle_form = add_vehicle_form))
    return redirect(url_for('user.Fetch_vehicles', add_vehicle_form = add_vehicle_form))

@user_bp.route('/dashboard/vehicles/remove_vehicle', methods=['GET','POST'])
@auth_required
def Remove_vehicle():
    user_id = session.get('user_id')
    remove_vehicle_form = Remove_vehicle_Form()
    if remove_vehicle_form.validate_on_submit():
        vehicle_id = remove_vehicle_form.vehicle_id.data
        owner = get_owner_of_vehicle(vehicle_id)
        if user_id == owner['user_id']:
            remove_vehicle(vehicle_id,user_id)
            flash("vehicle successfully deleted!",'success')
            return redirect(url_for('user.Fetch_vehicles',remove_vehicle_form = remove_vehicle_form))
        else:
            flash("vehicle does not belong to user!")
    return redirect(url_for('user.Fetch_vehicles', remove_vehicle_form = remove_vehicle_form))


# existing session user interaction end points 


@user_bp.route('/dashboard/current_sessions',methods=['GET','POST'])
@auth_required
def Fetch_sessions():
    user_id = session.get('user_id')
    sessions = fetch_sessions_of_user(user_id) if user_id else []
    return render_template('sessions.html', sessions = sessions, finish_parking_form = Finish_parking_Form())

@user_bp.route('/dashboard/current_session/finish_session',methods=['GET','POST'])
@auth_required
def Finish_parking():
    finish_parking_form = Finish_parking_Form()
    if finish_parking_form.validate_on_submit():
        session_id = finish_parking_form.session_id.data
        user_id = session.get('user_id')
        exit_time = datetime.now()
        if get_session_status(session_id) == 'active':
            Session = fetch_session(session_id)
            start_time = Session['entry_time']
            rate_used = Session.get('rate_per_hour_used') or Session.get('rate_per_hour_user') or 0
            end_session(session_id, exit_time)
            if Session.get('slot_id'):
                change_slot_status(Session['slot_id'], 'vacant')
            duration = exit_time - start_time
            duration_hours = round(duration.total_seconds() / 3600, 2)
            final_amount = round(duration_hours * rate_used, 2)
            total_minutes = int(duration.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            flash("Session ended!", 'success')
            message = "Session has successfully ended."
            return jsonify({
                'message': message,
                'duration': f'{hours} hour(s) {minutes} minute(s)',
                'duration_hours': duration_hours,
                'final_amount': final_amount
            })
        else:
            flash("Session is already over or cancelled!",'danger')
    else:
        flash("Invalid form submission!",'danger')
    return redirect(url_for('user.Fetch_sessions'))



#user starting session end point

@user_bp.route('/dashboard/search_facility',methods=['GET','POST'])
@auth_required
def Search_facility():
    search_name = request.args.get('search_id', default='a', type=str)
    facilities = search_facility(search_name)
    vehicles = fetch_vehicles_of_user(session.get('user_id'))
    return render_template('user_parking.html',
        facilities=facilities,
        vehicles=vehicles,
        start_parking_form=Start_parking_Form())

@user_bp.route('/dashboard/search_facility/<int:facility_id>', methods=['GET','POST'])
@auth_required
def Check_slots(facility_id):
    parking_rates = fetch_all_vehicle_rates_of_facility(facility_id)
    slots = fetch_all_available_slots(facility_id)
    return jsonify({
        'slots' : slots,
        'parking_rates' : parking_rates
    })

@user_bp.route('/dashboard/Park_start', methods=['GET','POST'])
@auth_required
def Start_parking():
    start_parking_form = Start_parking_Form()
    if start_parking_form.validate_on_submit():
        slot_id = start_parking_form.slot_id.data
        facility_id = start_parking_form.facility_id.data
        vehicle_id = start_parking_form.vehicle_id.data
        status = get_slot_status(slot_id)
        vehicle_type = get_vehicle_type(vehicle_id)

        if status == 'vacant':
            rate_info = fetch_rate_used_for_operation(vehicle_type, facility_id)
            if not rate_info:
                all_rates = fetch_all_vehicle_rates_of_facility(facility_id)
                for r in all_rates:
                    if (r.get('vehicle_type') or '').lower() == (vehicle_type or '').lower():
                        rate_info = r
                        break
                if not rate_info and all_rates:
                    rate_info = all_rates[0]

            rate_id = rate_info['rate_id'] if rate_info else None
            rate_used = rate_info['rate_per_hour'] if rate_info else 0
            entry_time = datetime.now()

            add_parking_session(entry_time, rate_id, rate_used, vehicle_id, slot_id)
            change_slot_status(slot_id, 'occupied')
            flash("Parking session started!", 'success')
            return redirect(url_for('user.Fetch_sessions'))
        else:
            flash(f"Selected slot is no longer vacant (status: {status}).", 'danger')
            return redirect(url_for('user.Search_facility'))
    else:
        for field, errors in start_parking_form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", 'danger')
        return redirect(url_for('user.Search_facility'))


        
# to add reviews and ratings for facilities and slots -- feature in v2
