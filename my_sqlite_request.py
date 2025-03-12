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
    
    def select(self, columns):
        """Specifies the columns to retrieve."""
        self.query_type = "SELECT"
        # If * is given, store None to indicate selecting all columns
        if columns == "*":
            self.columns = None
        else:
            self.columns = columns if isinstance(columns, list) else [columns]
        return self
    
    def where(self, column_name, value):
        """Adds a filtering condition."""
        self.conditions[column_name] = value
        return self
    
    def join(self, column_on_db_a, filename_db_b, column_on_db_b):
        """ Joins another CSV file. """
        self.join_info = (column_on_db_a, filename_db_b, column_on_db_b)
        return self
    
    def order(self, order, column_name):
        """ Orders results in asceinding or descending order. """
        self.order_by = (column_name, order)
        return self
    
    def insert(self, table_name):
        """ Specifies table for inserting data. """
        self.query_type = "INSERT"
        self.table_name = table_name
        return self
    def values(self, data):
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
            return self._execute_insert()
        elif self.query_type == "UPDATE":
            return self._execute_update()
        elif self.query_type == "DELETE":
            return self._execute_delete()
        else:
            raise ValueError("Invalid query type")
        
    def _execute_select(self):
        """ Executes a SELECT query. """
        results = []

        with open(self.table_name, "r", newline="") as file:
            reader = csv.reader(file)
            headers = next(reader) # Read the first row manually
            # Remove first empty column and strip spaces from header
            headers = [header.strip() for header in headers[1:]]
            # Read the actal data, skipping first col
            # reader = csv.DictReader(file, fieldnames=headers)
            reader = csv.reader(file)

            # Clean up fieldnames; remove empty first column and strip spaces
            # reader.fieldnames = [header.strip() for header in reader.fieldnames if header.strip()]

            for row in reader:
                row = row[1:] # Remove first column
                row_dict = dict(zip(headers, row)) # Map headers to row data

                # row = {key: value for key, value in row.items() if key} # Remove empty keys
                # Apply WHERE conditions if they exist
                if self.conditions and not all(row_dict[col] == str(val) for col, val in self.conditions.items()):
                    continue # Skip rows that don't match WHERE condition
                # If self.columns is None, select all columns

                # selected_row = row if self.columns is None else {col: row[col] for col in self.columns} 

                selected_row = row_dict if self.columns is None else {col: row_dict[col] for col in self.columns} 
                results.append(selected_row)

        # Apply ORDER BY if specified
        if self.order_by:
            column, order = self.order_by
            results.sort(key=lambda x: x[column], reverse=(order == "DESC"))

        return results
        
    def _execute_insert(self):
        """ Executes an INSERT query. """
        if not self.insert_data:
            raise ValueError("No data provided for INSERT")
        
        file_exists = os.path.exists(self.table_name)
        last_index = -1

        # Open in "r" mode first to get last index
        if file_exists and os.stat(self.table_name).st_size > 0:
            with open(self.table_name, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None) # Skip header
                for row in reader:
                    if row and row[0].isdigit(): # Ensure not empty row
                        last_index = int(row[0]) # First column is index
        
        # Assing a new ind num (increment from last row)
        new_index = last_index + 1

        # Add the index to the new row
        new_row = {"id": new_index, **self.insert_data} # Merge ID with insert data

        with open(self.table_name, "a", newline="") as file: # Open in "a" (append) mode to write
            writer = csv.DictWriter(file, fieldnames=["id"] + list(self.insert_data.keys())) # Ensure id is first
            
            # Write headers if file is empty
            if not file_exists or os.stat(self.table_name).st_size == 0:
                writer.writeheader() # Write header only if file is empty

            writer.writerow(new_row)
        return f"Inserted: {new_row}"

    def _execute_update(self):
        """ Executes an UPDATE query. """
        if not self.update_data:
            raise ValueError("No data provided for UPDATE")
        
        rows = []
        updated_count = 0 # Count updated rows

        with open(self.table_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            for row in reader:
                if self.conditions and all(str(row.get(col, "")) == str(val) for col, val in self.conditions.items()):
                    row.update(self.update_data) # Apply updates
                    updated_count += 1
                rows.append(row)
        # Only update file if changes were made
        if updated_count > 0:
            with open(self.table_name, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames) # Use correct fieldnames
                writer.writeheader()
                writer.writerows(rows) # All rows have valid keys
        return f"Update {updated_count} rows"
    
    def _execute_delete(self):
        """ Executes a DELETE query"""
        rows = []
        with open(self.table_name, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not all (row[col] == str(val) for col, val in self.conditions.items()):
                    rows.append(row)

        with open(self.table_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)