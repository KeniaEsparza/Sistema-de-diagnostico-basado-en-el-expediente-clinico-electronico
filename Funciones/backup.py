import subprocess
import os
import firebase_admin
from firebase_admin import credentials, storage
import google.api_core.exceptions
from datetime import datetime
from os import remove

# MySQL database configuration
db_host = 'localhost'
db_user = 'root'
db_password = 'contra'
db_name = 'diagnostico_auto'

def backup():
    # Backup file path and name
    backup_path = os.path.abspath(os.getcwd()) + '\\Funciones\\'
    print(backup_path)
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d") # format the date as YYYY-MM-DD
    print(date_string)
    backup_file = db_name + date_string + '.sql'

    # Run the mysqldump command to create backup
    backup_cmd = f'mysqldump -u {db_user} -p{db_password} -h {db_host} {db_name} > {backup_path}{backup_file}'
    subprocess.run(backup_cmd, shell=True)

    path = os.path.abspath(os.getcwd()) + '\\Funciones\\backup-682e1-firebase-adminsdk-1qlg6-4a99c0658f.json'
    print(path)

    cred = credentials.Certificate(path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'backup-682e1.appspot.com'
    })

    path = backup_path + backup_file
    print("Este es el path")
    print(path)

    try:
        bucket = storage.bucket('backup-682e1.appspot.com')
        blob = bucket.blob(f'backup-682e1.appspot.com/{ backup_file }')
        blob.upload_from_filename(path)
    except google.api_core.exceptions.NotFound as error:
        print(f'Error: {error}')
        
    remove(path)
    
    # Close Firebase app
    firebase_admin.delete_app(firebase_admin.get_app())