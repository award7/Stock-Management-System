import sqlite3
import os

class dbActions():
    def __init__(self, db):
        self.rowid = None
        db_location = os.path.join("C:/Users", os.getlogin(), "Box/Data_Analysis_Transforms/sql", db)
        self.connection = sqlite3.connect(db_location)
        self.cur = self.connection.cursor()


    def __del__(self):
        self.connection.close()


    def build_sql(self, sql_dict):
        # only builds one statement for one table
        sql_function = sql_dict.get('function')
        table = sql_dict.get('table')
        # TODO: fix scrub
        # self.scrub(table)

        # form fields and values to be passed
        non_values = ['table', 'foreign_key']
        fields = ()
        values = ()
        for key, val in sql_dict.items():
            if key not in non_values:
                fields += (key,)
                values += (val,)
            if key == 'foreign_key':
                foreign_key = sql_dict['foreign_key']
                fields += (foreign_key,)
                values += (self.cur.lastrowid,)
        # TODO: pass fields to scrub

        # form sql statement
        placeholders = "?"*len(values)
        placeholders = ','.join(placeholders)
        sql = f"INSERT INTO {table} {fields} VALUES ({placeholders})"

        return sql, values

    def insert_sample(self, **kwargs):
        lst = self.dictionaryBuilder(**kwargs)
        print(int(kwargs.get('quantity')))
        i = 0
        while i < int(kwargs.get('quantity')):
            for table in lst:
                if table == 'grid_table':
                    table['grid_location'] = kwargs.get('grid_location')[i]
                sql, values = self.build_sql(table)
                self.executeCommit(sql, values)
            i += 1

    @staticmethod
    def dictionaryBuilder(**kwargs):
        subjects_table = {
            'table': "subjects",
            'study': kwargs.get('study'),
            'subject_id': kwargs.get('sample_id'),
        }

        visit_table = {
                'table': 'study_visit',
                'visit': kwargs.get('visit'),
                'visit_date': kwargs.get('sample_date'),
                'foreign_key': 'study_id'
            }

        time_point_table = {
            'table': 'time_point',
            'time_point': kwargs.get('time_point'),
            'foreign_key': 'visit_id'
        }

        tubes_table = {
            'table': 'tubes',
            'sample_id': kwargs.get('sample_id'),
            'foreign_key': 'time_point_id'
        }

        grid_table = {
            'table': 'grid',
            'grid_location': kwargs.get('grid_location'),
            'foreign_key': 'sample_id'
        }

        box_color_table = {
            'table': 'box_color',
            'color': kwargs.get('box_color'),
            'foreign_key': 'grid_location_id'
        }

        box_number_table = {
            'table': 'box_number',
            'box_id': kwargs.get('box_id'),
            'foreign_key': 'box_color_id'
        }

        shelf_table = {
            'table': 'shelf',
            'shelf_number': kwargs.get('shelf'),
            'foreign_key': 'box_number_id',
        }

        freezer_table = {
            'table': 'freezer',
            'freezer': kwargs.get('freezer'),
            'foreign_key': 'shelf_id'
        }

        lst = [subjects_table,
               visit_table,
               time_point_table,
               tubes_table,
               grid_table,
               box_color_table,
               box_number_table,
               shelf_table,
               freezer_table]

        return lst

    def show_samples(self):
        sql_dict = {
            'subjects': ('study'),
            'study_visit': ('visit', 'visit_date'),
            'time_point': ('time_point'),
            'tubes': ('sample_id'),
            'grid': ('grid_location'),
            'box_color': ('color'),
            'box_number': ('box_id'),
            'shelf': ('shelf_number'),
            'freezer': ('freezer')
        }

        inner_join_dict = {
            'study_visit': ('subjects.id', 'study_visit.study_id'),
            'time_point': ('study_visit.id', 'time_point.visit_id'),
            'tubes': ('time_point.id', 'tubes.time_point.id'),
            'grid': ('tubes.id', 'grid.sample_id'),
            'box_color': ('grid.id', 'box_color.grid_location_id'),
            'box_number': ('box_color.id', 'box_number.box_color_id'),
            'shelf': ('box_number.id', 'shelf.box_number_id'),
            'freezer': ('shelf.id', 'freezer.shelf_id')
        }

        select_fields = ""
        for key, val in sql_dict.items():
            select_fields += f"{key}.{val}, "

        inner_joins = ""
        for key, val in inner_join_dict.items():
            inner_joins += f"INNER JOIN {key} ON {val[0]} = {val[1]}"

        sql = f"SELECT {select_fields} FROM (subjects) {inner_joins}"

        with self.connection:
            self.connection.execute(sql)

        return self.cur.fetchall()


    def update_sample(name, cost, date):
        # with connection:
        #     cursor.execute("""UPDATE stock SET cost = :cost
        #                 WHERE name = :name""",
        #               {'name': name, 'cost': cost})

        pass


    def update_quantity(name, val,date):
        # with connection:
        #     cursor.execute("SELECT quantity FROM stock WHERE name = :name",{'name': name})
        #     z = cursor.fetchone()
        #     cost = z[0]+val
        #     if cost < 0:
        #         return
        #     cursor.execute("""UPDATE stock SET quantity = :quantity
        #                 WHERE name = :name""",
        #               {'name': name, 'quantity': cost})
        #     a = name.upper() + ' ' + str(z[0]) + ' ' + str(cost) + ' ' + str(date) +' UPDATE '+"\n"
        #     with open("transaction.txt", "a") as myfile:
        #         myfile.write(a)

        pass


    def remove_sample(**kwargs):
        # with connection:
        #     cursor.execute("DELETE from stock WHERE name = :name",
        #               {'name': name})
        #     a = name.upper() + ' ' + 'None' + ' ' + 'None'+' ' + str(date) + ' REMOVE '+"\n"
        #
        #     with open("transaction.txt", "a") as myfile:
        #         myfile.write(a)
        #
        #     connection.commit()

        for key, value in kwargs.items():
            print(f"{key}: {value}")


    def scrub(self, table):
        # TODO: revamp to allow fields to be scrubbed
        tables = self.connection.execute("SELECT name FROM sqlite_master WHERE type='table';")

        if table not in tables:
            raise ValueError(f'Table not found in database: {table}')


    def executeCommit(self, sql, values):
        self.cur.execute(sql, values)
        self.connection.commit()


    def close(self):
        self.connection.close()