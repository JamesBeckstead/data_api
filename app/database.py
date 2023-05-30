from flask import Flask
from models.models import engine, DATABASE_URL, Base
from command_line import MySubProcessDBCreation as DBC




class Database:

    def __init__(self, remove_tables=False):
        self.remove_tables = remove_tables

    def delete_all_tables(self):
        """Find all tables and drops them"""
        conn = engine.connect()
        result = conn.exec_driver_sql(
            "SELECT table_name FROM information_schema.tables where table_schema = 'homework';"
        )
        tables = [row[0] for row in result.fetchall()]

        for table in tables:
            conn.exec_driver_sql(f"DROP TABLE IF EXISTS homework.{table} CASCADE;")
            conn.commit()
        conn.close()

    def create_tables(self):
        # creates all tables in postgres database
        Base.metadata.create_all(engine)

    def create_database(self):
        """Creates database in postgresql"""
        DBC().run_db_create_command()
        self.create_user()

    def create_user(self):
        """
            Creates a user on the database
            hard coded to use the following values
            -username=new_user
            -password=new_password
        """
        DBC().create_user_on_db()

    def drop_database(self):
        """Drops database in postgresql"""
        query = 'DROP DATABASE james_preston;'
        conn = engine.connect()
        conn.exec_driver_sql(query)
        conn.commit()
        conn.close()


    def main(self):
        """Creates Flask app context""" 
        # self.create_database()
        self.create_tables()
        if self.remove_tables:
            self.delete_all_tables()
            # self.drop_database()



if __name__=='__main__':
    d = Database()
    d.main()
