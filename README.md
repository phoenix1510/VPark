# VPark — Smart Parking Management System



\

VPark is a web-based parking management system built using **Flask and MySQL**.

The project has separate areas for **parking users** and **facility administrators**. Users can find parking facilities, check available slots, register their vehicles, start and end parking sessions, and view their parking history. Administrators can manage their facilities, floors, parking slots, and vehicle-based parking rates.

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [How It Works](#how-it-works)
* [Database](#database)
* [Project Structure](#project-structure)
* [Setup](#setup)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Environment Variables](#environment-variables)
  * [Database Setup](#database-setup)
  * [Running the Application](#running-the-application)
* [Routes](#routes)
* [Future Plans](#future-plans)
* [License](#license)

---

## Features

### For Users

* Search for parking facilities by name or address.
* Check available parking slots for a facility.
* Select a vehicle from the user's registered vehicles.
* Start a parking session by selecting an available slot.
* Track an active parking session.
* Calculate the parking cost based on the duration and vehicle type.
* End a parking session and view the final bill.
* Add and remove vehicles from a personal garage.
* Manage the user account.

### For Administrators

* Create, edit, and remove parking facilities.
* Add and remove floors for a facility.
* Add and manage parking slots on each floor.
* Change the status of individual slots:

  * `vacant`
  * `occupied`
  * `unavailable`
* Set hourly parking rates for different vehicle types.
* Update or remove existing rates.
* Manage the administrator profile.
* Protected admin routes to prevent unauthorized access.

---

## Tech Stack

| Part                 | Technology             |
| -------------------- | ---------------------- |
| Backend              | Python, Flask          |
| Forms                | Flask-WTF, WTForms     |
| Database             | MySQL                  |
| Database Driver      | mysql-connector-python |
| Templates            | Jinja2                 |
| Frontend             | HTML, CSS, JavaScript  |
| Client-side Requests | Fetch API              |
| Password Hashing     | Werkzeug               |
| Icons                | SVG icons              |
| Fonts                | Google Fonts           |

---

## How It Works

The application is divided into three main parts:

```text
Browser
   │
   ├── Authentication
   │
   ├── User Portal
   │
   └── Admin Portal
          │
          ▼
    Flask Application
          │
          ▼
    Database Operations
          │
          ▼
        MySQL
```

Flask handles the application routes and user authentication. The user and admin sections have their own blueprints, while database-related operations are kept in a separate database layer.

Forms use **Flask-WTF**, including CSRF protection for form submissions.

---

## Database

VPark uses a MySQL database named `parking_db`.

The main tables are:

* **`users`** — Stores user accounts, contact details, and roles.
* **`facility`** — Stores parking facilities.
* **`floor`** — Stores the floors belonging to each facility.
* **`parking_slot`** — Stores individual parking slots and their current status.
* **`parking_rate`** — Stores hourly parking rates for different vehicle types.
* **`vehicle`** — Stores vehicles registered by users.
* **`parking_session`** — Stores parking sessions, including entry time, exit time, vehicle, slot, rate, and session status.

The tables are connected using foreign keys where required.

---

## Project Structure

```text
VPark/
│
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── db_operations.py
│   │   ├── init_db.py
│   │   └── schema.sql
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── user.py
│   │   └── wtfforms.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── admin_dashboard.css
│   │   │   ├── admin_profile.css
│   │   │   ├── user_dashboard.css
│   │   │   ├── user_parking.css
│   │   │   ├── vehicles.css
│   │   │   └── sessions.css
│   │   │
│   │   └── js/
│   │       ├── admin_dashboard.js
│   │       ├── user_parking.js
│   │       ├── vehicles.js
│   │       └── sessions.js
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── admin_login.html
│   │   ├── signup.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_profile.html
│   │   ├── user_dashboard.html
│   │   ├── user_parking.html
│   │   ├── vehicles.html
│   │   ├── sessions.html
│   │   └── user_profile.html
│   │
│   └── __init__.py
│
├── run.py
├── requirements.txt
└── README.md
```

---

## Setup

### Prerequisites

Make sure you have the following installed:

* Python 3.10 or newer
* MySQL Server 8.0 or newer
* Git

### Installation

Clone the repository:

```bash
git clone https://github.com/phoenix1510/VPark.git
cd VPark
```

Create a virtual environment:

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-super-secret-key-change-me

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=parking_db
```

Replace the MySQL password with the password for your local MySQL installation.

---

### Database Setup

Create the database and tables using the provided schema:

```bash
mysql -u root -p < app/db/schema.sql
```

You can also run the contents of `app/db/schema.sql` using MySQL Workbench or another MySQL client.

---

### Running the Application

Start the Flask development server:

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000/
```

---

## Routes

### Authentication

| Endpoint            | Method    | Purpose           |
| ------------------- | --------- | ----------------- |
| `/auth/login`       | GET, POST | User login        |
| `/auth/login/admin` | GET, POST | Admin login       |
| `/auth/signup`      | GET, POST | User registration |
| `/auth/logout`      | GET       | Log out           |

### Admin

| Endpoint                                | Method    | Purpose                |
| --------------------------------------- | --------- | ---------------------- |
| `/admin/dashboard`                      | GET, POST | Admin dashboard        |
| `/admin/dashboard/add_facility`         | POST      | Add a facility         |
| `/admin/dashboard/edit_facility`        | POST      | Edit a facility        |
| `/admin/dashboard/remove_facility`      | POST      | Remove a facility      |
| `/admin/<facility_id>/floors`           | GET, POST | Manage facility floors |
| `/admin/<facility_id>/<floor_id>/Slots` | GET, POST | Manage parking slots   |
| `/admin/<facility_id>/rate`             | GET       | View parking rates     |
| `/admin/<facility_id>/add_rate`         | POST      | Add a parking rate     |
| `/admin/profile`                        | GET, POST | Admin profile          |
| `/admin/profile/delete_admin`           | POST      | Delete admin account   |

### User

| Endpoint                                         | Method | Purpose                      |
| ------------------------------------------------ | ------ | ---------------------------- |
| `/user/dashboard`                                | GET    | User dashboard               |
| `/user/dashboard/search_facility`                | GET    | Search for facilities        |
| `/user/dashboard/search_facility/<id>`           | GET    | Get facility slots and rates |
| `/user/dashboard/Park_start`                     | POST   | Start a parking session      |
| `/user/dashboard/current_sessions`               | GET    | View parking sessions        |
| `/user/dashboard/current_session/finish_session` | POST   | Finish a parking session     |
| `/user/dashboard/vehicles`                       | GET    | Manage vehicles              |
| `/user/dashboard/vehicles/add_vehicle`           | POST   | Add a vehicle                |
| `/user/dashboard/vehicles/remove_vehicle`        | POST   | Remove a vehicle             |
| `/user/profile`                                  | GET    | User profile                 |
| `/user/profile/delete_user`                      | POST   | Delete user account          |

---

## Future Plans

Some features that could be added in a future version:

* [ ] Facility ratings and reviews
* [ ] Revenue and parking occupancy analytics
* [ ] More detailed parking history and reports

---

## License

This project is distributed under the MIT License. See `LICENSE` for more information.
