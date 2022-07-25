# be-sks-dosen
This is the temporary README for this file

## Purpose
This repository serves as a backend for the `sks-dosen` project. The purpose of the project is to group the lecturers based on performance.<br>
The used programming language here is python with framework flask.

## How to start the program?

### Step 1: Install requirements
Installing requirements using requirements.txt<br>
`pip install -r requirements.txt`

### Step 2: Prepare the database
This step will be configured later on<br>
Run your database at `localhost:3306`<br>
Use admin access (username:`root` and no password)<br>
Create empty database `db-sks-dosen`

### Step 2: Run db migrate
Run the database migration<br>
`flask db init`<br>
`flask db migrate`<br>
`flask db upgrade`

### Step 3: Run the program
`flask run`
