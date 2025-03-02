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

    