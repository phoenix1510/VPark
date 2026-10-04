from flask import Blueprint, render_template, redirect, url_for , session, flash
from .auth import admin_required 
from app.db.db_operations import (
    delete_admin,get_user_by_id,fetch_all_facilities_of_user, fetch_all_floors, fetch_all_slots,
    add_facility, add_slot, add_floor, remove_floor,
    get_user_owning_facility, get_facility_by_id, remove_facility, edit_facility,
    remove_slot, change_slot_status, get_floor_by_id,
    add_parking_rate, fetch_rates_for_facility, remove_parking_rate
)
from .wtfforms import (Add_Fal_Form, Add_Flo_Form, Remove_Flo_Form, Remove_admin_Form, Remove_fal_Form,
                       Edit_fal_Form, Add_slo_Form, Remove_slo_Form, Edit_status_Form,
                       Add_Rate_Form, Remove_Rate_Form)

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')


# profile route endpoints

@admin_bp.route('/profile',methods=["GET","POST"])
@admin_required
def Profile():
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    remove_admin_form = Remove_admin_Form()
    return render_template('admin_profile.html', current_user = user, remove_admin_form = remove_admin_form)


@admin_bp.route('/profile/delete_admin', methods = ['GET','POST'])
@admin_required
def Remove_admin():
    remove_admin_form = Remove_admin_Form()
    if remove_admin_form.validate_on_submit():
        user_id = session.get('user_id')
        delete_admin(user_id)
        flash('Admin deleted!','success')
        return redirect(url_for('auth.logout'))

# dashboard route endpoints

@admin_bp.route('/dashboard',methods=['GET','POST'])
@admin_required
def admin_dashboard():
    user_id = session.get('user_id')
    username = session.get('username')
    facilities = fetch_all_facilities_of_user(user_id)
    add_fal_form = Add_Fal_Form()
    remove_form = Remove_fal_Form()
    edit_fal_form = Edit_fal_Form()
    return render_template('admin_dashboard.html', facilities= facilities,add_fal_form=add_fal_form,current_user = username, remove_form = remove_form,edit_fal_form = edit_fal_form)

@admin_bp.route('/dashboard/add_facility',methods=['GET','POST'])
@admin_required
def Add_facility():
    user_id = session.get('user_id')
    add_fal_form  = Add_Fal_Form()
    if add_fal_form.validate_on_submit():
        name = add_fal_form.name.data
        address = add_fal_form.address.data
        add_facility(user_id, name, address)
        flash("Facility added successfully! Add some floors to start with!",'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/dashboard/remove_facility', methods = ['GET','POST'])
@admin_required
def Remove_facility():
    user_id = session.get('user_id')
    remove_form = Remove_fal_Form()
    if remove_form.validate_on_submit():
        facility_id = remove_form.facility_id.data
        owner=get_user_owning_facility(facility_id)
        if user_id == owner['user_id']:
            remove_facility(facility_id)
            flash('Facility successfully removed!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Facility does not belong to admin!!', 'danger')
    return redirect(url_for('admin.admin_dashboard'))
        
@admin_bp.route('/dashboard/edit_facility',methods=['GET','POST'])
@admin_required
def Edit_facility():
    edit_fal_form  = Edit_fal_Form()
    if edit_fal_form.validate_on_submit():
        name = edit_fal_form.name.data
        address = edit_fal_form.address.data
        facility_id = edit_fal_form.facility_id.data
        edit_facility(facility_id,name, address)
        flash("Successfully edited details of the facility!",'success')
    return redirect(url_for('admin.admin_dashboard'))


# floor route endpoints

@admin_bp.route('/<int:facility_id>/floors',methods=['GET','POST'])
@admin_required
def Fetch_floors(facility_id):
    username = session.get('username')
    floors = fetch_all_floors(facility_id)
    add_flo_form = Add_Flo_Form()
    remove_flo_form = Remove_Flo_Form()
    facility = get_facility_by_id(facility_id)
    return render_template('floors.html',floors = floors,add_flo_form=add_flo_form,remove_flo_form = remove_flo_form ,facility = facility,current_user =username)

@admin_bp.route('/<int:facility_id>/add_floor',methods=['GET','POST'])
@admin_required
def Add_floor(facility_id):
    floors = fetch_all_floors(facility_id)
    floors_numbers = [floor["floor_number"] for floor in floors]
    add_flo_form = Add_Flo_Form()
    if add_flo_form.validate_on_submit():
        Floor_number = add_flo_form.floor_number.data
        if floors_numbers and (Floor_number in floors_numbers):
            flash("FLoor already exists!",'danger')
        else:
            add_floor(facility_id,Floor_number)
            flash("Floor added!",'success')
            return redirect(url_for('admin.Fetch_floors',facility_id = facility_id))
    return redirect(url_for('admin.Fetch_floors',facility_id= facility_id))

@admin_bp.route('/<int:facility_id>/remove_floor',methods=['GET','POST'])
@admin_required
def Remove_floor(facility_id):
    remove_form = Remove_Flo_Form()
    user_id = session.get('user_id')
    owner = get_user_owning_facility(facility_id)
    if remove_form.validate_on_submit():
        floor_id = remove_form.floor_id.data
        if user_id == owner['user_id']:
            remove_floor(floor_id)
            flash("Succesfully removed floor!",'success')
            return redirect(url_for('admin.Fetch_floors',facility_id = facility_id))
        else:
            flash("Facility does not belong to admin!!",'success')
    return redirect(url_for('admin.Fetch_floors', facility_id = facility_id))

    

#slot route endpoints

@admin_bp.route('/<int:facility_id>/<int:floor_id>/Slots',methods=['GET','POST'])
@admin_required
def Fetch_slots(facility_id,floor_id):
    username = session.get('username')
    add_slo_form = Add_slo_Form()
    remove_slo_form = Remove_slo_Form()
    edit_status_form = Edit_status_Form()
    slots = fetch_all_slots(floor_id)
    floor = get_floor_by_id(floor_id)
    return render_template('Slots.html', current_user=username, add_slo_form=add_slo_form,
                           remove_slo_form=remove_slo_form, edit_status_form=edit_status_form,
                           slots=slots, floor=floor, facility_id=facility_id, floor_id=floor_id)

@admin_bp.route('/<int:facility_id>/<int:floor_id>/add_slot', methods= ['GET','POST'])
@admin_required
def Add_slot(facility_id,floor_id):
    slots = fetch_all_slots(floor_id)
    slots_numbers = [slot['slot_number'] for slot in slots]

    user_id = session.get('user_id')
    owner = get_user_owning_facility(facility_id)

    add_slo_form = Add_slo_Form()
    if add_slo_form.validate_on_submit():
        slot_number = add_slo_form.slot_number.data
        if user_id == owner['user_id']:
            if slot_number in slots_numbers:
                flash('Slot already exists!','danger')
            else:
                add_slot(slot_number,floor_id)
                flash('Successfully added slot!','success')
                return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))
        else:
            flash('Facility does not belong to admin!', 'danger')
    return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))

@admin_bp.route('/<int:facility_id>/<int:floor_id>/remove_slot',methods= ["GET","POST"])
@admin_required
def Remove_slot(facility_id, floor_id):
    user_id = session.get('user_id')
    remove_slo_form = Remove_slo_Form()
    if remove_slo_form.validate_on_submit():
        slot_id = remove_slo_form.slot_id.data
        owner = get_user_owning_facility(facility_id)
        if user_id == owner['user_id']:
            remove_slot(slot_id)
            flash('Succesfully removed parking slot!', 'success')
            return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))
        else:
            flash('Facility does not belong to admin!','danger')
    return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))
@admin_bp.route('/<int:facility_id>/<int:floor_id>/change_status', methods= ['GET','POST'])
@admin_required
def Change_slot_status(facility_id, floor_id):
    user_id = session.get('user_id')
    edit_status_form = Edit_status_Form()
    if edit_status_form.validate_on_submit():
        slot_id = edit_status_form.slot_id.data
        status = edit_status_form.status.data
        owner = get_user_owning_facility(facility_id)
        if user_id == owner['user_id']:
            change_slot_status(slot_id,status)
            flash('Status changed successfully!','success')
            return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))
        else:
            flash('Facility does not belong to admin!','danger')
    return redirect(url_for('admin.Fetch_slots',facility_id = facility_id, floor_id = floor_id))


# ---- rate route endpoints ----

@admin_bp.route('/<int:facility_id>/rate', methods=['GET'])
@admin_required
def Fetch_rates(facility_id):
    username = session.get('username')
    facility = get_facility_by_id(facility_id)
    rates = fetch_rates_for_facility(facility_id)
    add_rate_form = Add_Rate_Form()
    remove_rate_form = Remove_Rate_Form()
    return render_template('rates.html', current_user=username, facility=facility,
                           rates=rates, add_rate_form=add_rate_form,
                           remove_rate_form=remove_rate_form)

@admin_bp.route('/<int:facility_id>/add_rate', methods=['POST'])
@admin_required
def Add_rate(facility_id):
    user_id = session.get('user_id')
    owner = get_user_owning_facility(facility_id)
    add_rate_form = Add_Rate_Form()
    if add_rate_form.validate_on_submit():
        if user_id == owner['user_id']:
            vehicle_type = add_rate_form.vehicle_type.data
            rate_per_hour = add_rate_form.rate_per_hour.data
            add_parking_rate(vehicle_type, rate_per_hour, facility_id)
            flash('Rate added successfully!', 'success')
        else:
            flash('Facility does not belong to admin!', 'danger')
    return redirect(url_for('admin.Fetch_rates', facility_id=facility_id))

@admin_bp.route('/<int:facility_id>/remove_rate', methods=['POST'])
@admin_required
def Remove_rate(facility_id):
    user_id = session.get('user_id')
    owner = get_user_owning_facility(facility_id)
    remove_rate_form = Remove_Rate_Form()
    if remove_rate_form.validate_on_submit():
        if user_id == owner['user_id']:
            rate_id = remove_rate_form.rate_id.data
            remove_parking_rate(rate_id)
            flash('Rate removed successfully!', 'success')
        else:
            flash('Facility does not belong to admin!', 'danger')
    return redirect(url_for('admin.Fetch_rates', facility_id=facility_id))
