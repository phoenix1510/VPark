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


def fetch_all_facilities_of_user(user_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'select * from facility where user_id = %s'
    cursor.execute(query,(user_id,))
    user_facilities = cursor.fetchall()
    cursor.close()
    return user_facilities

def fetch_all_slots(facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'SELECT ps.slot_number, ps.status, f.floor_number FROM parking_slot ps INNER JOIN floor f ON ps.floor_id = f.floor_id WHERE ps.facility_id = %s'
    cursor.execute(query, (facility_id,))
    slots = cursor.fetchall()
    cursor.close()
    return slots

def add_facility(user_id,name,address):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into facility(name, user_id, address) values(%s,%s,%s)'
    cursor.execute(query,(name, user_id,address))
    db.commit()
    cursor.close()

def add_floor(facility_id, number):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into floor(floor_number, facility_id) values(%s,%s)'
    cursor.execute(query,(number,facility_id))
    db.commit()
    cursor.close()

def add_slot(slot_number,floor_id):
    db= open_db()
    cursor = db.cusror(dictionary= True)
    query = 'insert into parking_slot(slot_number, floor_id) values(%s,%s)'
    cursor.execute(query,(slot_number, floor_id))
    db.commit()
    cursor.close()

def add_parking_rate(vehicle_type, rate_per_hour,facility_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into parking_slot(vehicle_type, rate_per_hour, facility_id) values(%s,%s,%s)'
    cursor.execute(query,(vehicle_type,rate_per_hour,facility_id))
    db.commit()
    cursor.close()

def make_unavailable(slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = "modify parking_slot set status = 'unavailable' where slot_id = %s"
    cursor.execute(query,(slot_id,))
    db.commit()


# ----all user operation----


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
    query = 'select ps.slot_number,ps.status, f.floor_number from parking_slot ps inner join floor f on ps.floor_id=f.floor_id where f.facility_id = %s and ps.status = %s'
    cursor.execute(query,(facility_id,'available'))
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


def add_parking_session(entry_time, exit_time,rate_id, rate_used, vehicle_id, slot_id):
    db = open_db()
    cursor = db.cursor(dictionary=True)
    query = 'insert into parking_session(entry_time, exit_time, rate_id, rate_per_hour_used, vehicle_id, slot_id)'
    cursor.execute(query, (entry_time,exit_time, rate_id, rate_used, vehicle_id, slot_id))
    db.commit()
    cursor.close()
