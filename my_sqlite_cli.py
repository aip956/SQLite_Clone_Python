import readline
from my_sqlite_request import MySqliteRequest

def parse_query(query):
    """Parses SQL-like commands into structured parts. """
    tokens = query.strip().split()
    command = tokens[0].upper()


    if command == "SELECT":
        #Select column1, column2 FROM table WHERE column = value;
        select_index = tokens.index("SELECT")
        from_index = tokens.index("FROM")

        columns = tokens[select_index + 1: from_index]
        columns = [col.strip(",") for col in columns]

        table_name = tokens[from_index + 1]

        request = MySqliteRequest().from_table(table_name).select(columns)

        # Check for WHERE clause
        if "WHERE" in tokens:
            where_index = tokens.index("WHERE")
            column_name = tokens[where_index + 1]
            value = tokens[where_index + 3].strip("'")
            request = request.where(column_name, value)

        return request.run()
        
    elif command == "INSERT":
        """INSERT INTO table VALUES ('val1, 'val2', 'val2)"""
        table_name = tokens[2]
        values_index = tokens.index("VALUES")
        values = query[values_index + 6].strip("();").split(", ")
        values = [v.strip("'") for v in values]

        request = MySqliteRequest().insert(table_name)

        with open(table_name, "r", newline="") as file:
            headers = file.readline().strip().split(",")




# Read csv file
# Filter rows based on WHERE conditions
# Sort data if ORDER BY used
# Return selected columns

