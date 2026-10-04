# all operations of database that will be used by the app
from .init_db import open_db


# ----auth operation----


def get_user_by_email(email):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from users where email = %s'
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def insert_user_into_db(name, email , password_hash, phone, role):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into users(name , email, password_hash, phone_number, role) values (%s, %s, %s , %s, %s)'
    cursor.execute(query, (name , email , password_hash, phone, role))
    db.commit()
    cursor.close()


# ----all admin operations----

def delete_admin(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from users where user_id = %s'
    cursor.execute(query,(user_id,))
    db.commit()
    cursor.close()

def get_user_by_id(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from users where user_id = %s'
    cursor.execute(query,(user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def fetch_all_facilities_of_user(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from facility where user_id = %s'
    cursor.execute(query,(user_id,))
    user_facilities = cursor.fetchall()
    cursor.close()
    return user_facilities

def fetch_all_floors(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from floor where facility_id = %s'
    cursor.execute(query,(facility_id,))
    floors = cursor.fetchall()
    cursor.close()
    return floors

def fetch_all_slots(floor_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from parking_slot where floor_id = %s'
    cursor.execute(query,(floor_id,))
    slots = cursor.fetchall()
    cursor.close()
    return slots

def add_facility(user_id,name,address):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into facility(facility_name, user_id, address) values(%s,%s,%s)'
    cursor.execute(query,(name, user_id,address))
    db.commit()
    cursor.close()

def get_facility_by_id(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from facility where facility_id = %s'
    cursor.execute(query, (facility_id,))
    facility = cursor.fetchone()
    cursor.close()
    return facility

def get_floor_by_id(floor_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from floor where floor_id = %s'
    cursor.execute(query, (floor_id,))
    floor = cursor.fetchone()
    cursor.close()
    return floor

def add_floor(facility_id, number):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into floor(floor_number, facility_id) values(%s,%s)'
    cursor.execute(query,(number,facility_id))
    db.commit()
    cursor.close()

def remove_floor(floor_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from floor where floor_id = %s'
    cursor.execute(query, (floor_id,))
    db.commit()
    cursor.close()

def add_slot(slot_number,floor_id):
    db= open_db()
    cursor = db.cursor(dictionary= True)
    query = 'insert into parking_slot(slot_number, floor_id) values(%s,%s)'
    cursor.execute(query,(slot_number, floor_id))
    db.commit()
    cursor.close()

def remove_slot(slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from parking_slot where slot_id = %s'
    cursor.execute(query,(slot_id,))
    db.commit()
    cursor.close()

def change_slot_status(slot_id, status):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'update parking_slot set status = %s where slot_id = %s'
    cursor.execute(query,(status,slot_id))
    db.commit()
    cursor.close()


def add_parking_rate(vehicle_type, rate_per_hour,facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into parking_rate(vehicle_type, rate_per_hour, facility_id) values(%s,%s,%s)'
    cursor.execute(query,(vehicle_type,rate_per_hour,facility_id))
    db.commit()
    cursor.close()

def fetch_rates_for_facility(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from parking_rate where facility_id = %s'
    cursor.execute(query, (facility_id,))
    rates = cursor.fetchall()
    cursor.close()
    return rates

def remove_parking_rate(rate_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from parking_rate where rate_id = %s'
    cursor.execute(query, (rate_id,))
    db.commit()
    cursor.close()

def make_unavailable(slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = "update parking_slot set status = 'unavailable' where slot_id = %s"
    cursor.execute(query,(slot_id,))
    db.commit()
    cursor.close()

def get_user_owning_facility(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = "select user_id from facility where facility_id = %s"
    cursor.execute(query,(facility_id,))
    user_id = cursor.fetchone()
    cursor.close()
    return user_id 

def remove_facility(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = "delete from facility where facility_id = %s"
    cursor.execute(query,(facility_id,))
    db.commit()
    cursor.close()

def edit_facility(facility_id,name,address):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'update facility set facility_name = %s , address = %s where facility_id = %s'
    cursor.execute(query,(name,address,facility_id))
    db.commit()
    cursor.close()


# ----all user operation----

def fetch_vehicles_of_user(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from vehicle where user_id = %s'
    cursor.execute(query,(user_id,))
    vehicles=cursor.fetchall()
    cursor.close()
    return vehicles

def add_vehicle(name, regis_number, user_id, type):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into vehicle(vehicle_name, registration_number,user_id,vehicle_type) values(%s,%s,%s,%s)' 
    cursor.execute(query,(name, regis_number,user_id,type))
    db.commit()
    cursor.close()


def fetch_all_facilities():
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from facility'
    cursor.execute(query)
    facilities=cursor.fetchall()
    cursor.close()
    return facilities

def fetch_all_available_slots(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select ps.slot_id, ps.slot_number, ps.status, f.floor_number from parking_slot ps inner join floor f on ps.floor_id=f.floor_id where f.facility_id = %s and ps.status = %s order by f.floor_number, ps.slot_number'
    cursor.execute(query,(facility_id,'vacant'))
    slots=cursor.fetchall()
    cursor.close()
    return slots 

def fetch_rate_used_for_operation(vehicle_type,facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select rate_id,rate_per_hour from parking_rate where vehicle_type = %s and facility_id = %s'
    cursor.execute(query,(vehicle_type,facility_id))
    rate=cursor.fetchone()
    cursor.close() 
    return rate


def add_parking_session(entry_time,rate_id, rate_used, vehicle_id, slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into parking_session(entry_time, rate_id, rate_per_hour_used, vehicle_id, slot_id) values(%s, %s, %s, %s, %s)'
    cursor.execute(query, (entry_time, rate_id, rate_used, vehicle_id, slot_id))
    db.commit()
    cursor.close()

def delete_user(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from user where user_id = %s'
    cursor.execute(query, (user_id,))
    db.commit()
    cursor.close()

def get_owner_of_vehicle(vehicle_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select user_id from vehicle where vehicle_id = %s'
    cursor.execute(query, (vehicle_id,))
    owner = cursor.fetchone()
    cursor.close()
    return owner

def remove_vehicle(vehicle_id,user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'delete from vehicle where vehicle_id = %s and user_id = %s'
    cursor.execute(query,(vehicle_id,user_id))
    db.commit()
    cursor.close()

def fetch_session(session_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from parking_session where session_id = %s'
    cursor.execute(query,(session_id,))
    session = cursor.fetchone()
    cursor.close()
    return session

def get_session_status(session_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select status from parking_session where session_id = %s'
    cursor.execute(query,(session_id,))
    status = cursor.fetchone()
    cursor.close()
    return status['status']

def end_session(session_id, exit_time):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'update parking_session set exit_time = %s, status = %s where session_id = %s'
    cursor.execute(query,(exit_time,'completed',session_id))
    db.commit()
    cursor.close()

def fetch_all_vehicle_rates_of_facility(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from parking_rate where facility_id = %s'
    cursor.execute(query, (facility_id,))
    rates = cursor.fetchall()
    cursor.close()
    return rates

def search_facility(search_term):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = "select * from facility where facility_name like %s"
    cursor.execute(query, ('%' + search_term + '%',))
    facilities = cursor.fetchall()
    cursor.close()
    return facilities

def get_slot_status(slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select status from parking_slot where slot_id = %s'
    cursor.execute(query,(slot_id,))
    row = cursor.fetchone()
    cursor.close()
    return row['status'] if row else None

def fetch_sessions_of_user(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = '''
        select ps.*, v.vehicle_name, v.registration_number, v.vehicle_type
        from parking_session ps
        join vehicle v on ps.vehicle_id = v.vehicle_id
        where v.user_id = %s
        order by ps.entry_time desc
    '''
    cursor.execute(query, (user_id,))
    sessions = cursor.fetchall()
    cursor.close()
    return sessions

def get_vehicle_type(vehicle_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select vehicle_type from vehicle where vehicle_id = %s'
    cursor.execute(query,(vehicle_id,))
    vehicle_type = cursor.fetchone()
    cursor.close()
    return vehicle_type['vehicle_type']
