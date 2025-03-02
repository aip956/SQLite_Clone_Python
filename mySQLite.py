import csv
import os

class MySqliteRequest:
    def __init__(self):
        self.table_name = None
        self.columns = []
        self.conditions = {}
        self.join_info = None
        self.order_by = None
        self.insert_data = None
        self.update_data = None
        self.query_type = None

    def from_table(self, table_name):
        """ Specifies the table (CSV file) to use."""
        self.table_name = table_name
        return self
    
    def select(self, colums):
        """Specifies the columns to retrieve."""
        self.query_type = "SELECT"
        self.columns = columns if isinstance(columns, list) else [columns]

    def where(self, column_name, value):
        """Adds a filtering condition."""
        self.contitions[column_name] = value
        return self
    
    def join(self, column_on_db_a, filename_db_b, column_on_db_b):
        """ Joins another CSV file. """
        self.join_info = (column_on_db_a, filename_db_b, column_on_db_b)
        return self
    
    def order(self, order, column_name):
        """ Orders results in asceinding or descending order. """
        self.order_by = (column_name, order)
        return self
    
    def insert(self, data):
        """ Specifies data for INSERT queries. """
        self.insert_data = data
        return self
    
    def update(self, table_name):
        """ Specifies table for updating rows. """
        self.query_type = "UPDATE"
        self.table_name = table_name
        return self
    
    def set(self, data):
        """ Specifies data to update in UPDATE queries. """
        self.update_data = data
        return self
    
    def delete(self):
        """ Deletes rows matchign the WHERE condition. """
        self.query_type = "DELETE"
        return self
    
    def run(self):
        """ Executes the built query. """
        if not self.table_name:
            raise ValueError("Table name not specified")
        
        if self.query_type == "SELECT":
            return self._execute_select()
        elif self.query_type == "INSERT":
            self._execute_insert()
        elif self.query_type == "UPDATE":
            self._execute_update()
        elif self.query_type == "DELETE":
            self._execute_delete()
        else:
            raise ValueError("Invalid query type")
        
    def _execute_select(self):
        """ Executes a SELECT query. """
        results = []

        with open(self.table_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if self.conditions and not all(row[col] == str(val) for col, val in self.conditions.items()):
                    continue # Skip rows that don't match WHERE condition
                
                selected_row = {col: row[col] for col in self.columns} if self.columns else row
                results.append(selected_row)

        if self.order_by:
            column, order = self.order_by
            results.sort(key=lambda x:x[column], reverse=(order == "DESC"))

        return results
        
    def _execute_insert(self):
        """ Executes an INSERT query. """
        file_exists = os.path.exists(self.table_name)
        with open(self.table_name, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.insert_data.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(self.insert_data)

    def _execute_update(self):
        """ Executes an UPDATE query. """
        rows = []
        with open(self.table_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(row[col] == str(val) for col, val in self.conditions.items()):
                    row.update(self.update_data)
                rows.append(row)
        
        with open(self.table_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def _execute_delete(self):
        """ Executes a DELETE query"""
        rows = []
        with open(self.table_name, "r" newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not all (row[col] == str(val) for col, val in self.conditions.items()):
                    rows.append(row)

        with open(self.table_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)