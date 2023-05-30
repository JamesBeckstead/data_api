import subprocess
import os


class MySubProcessDBCreation:
    # Set the values of the variables
    db_pass = "admin123"
    dir_path =  os.path.abspath(".")
    p_sql = "C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe"
    db_path = 'C:\\Users\\jtbec\\Documents\\code\\python\\prestonV_api\\app\\scripts\\db_create.sql'
    # C:\Users\jtbec\Documents\code\python\prestonV_api\app\scripts\db_create.sql

    def run_db_create_command(self):
        file = os.path.join(self.dir_path, 'app', 'scripts', 'db_create.sql')
        if os.path.isfile(file):
            # Call the psql command using subprocess
            subprocess.call([self.p_sql, '-h', 'localhost', f'user_passwd="{self.db_pass}"', '-U', 'postgres', '-d', 'postgres', 'james_preston', '-f', "C:/Users/jtbec/Documents/code/python/prestonV_api/app/scripts/db_create.sql"])


    def create_user_on_db(self):
        # Set the values of the variables
        username = "new_user"
        password = "new_password"

        path = 'C:\\Program Files\\PostgreSQL\\15\\bin\\createuser.exe'
        subprocess.call([path, '--interactive', '--pwprompt', '-P', '-e', '-d', '-r', '-s', username])