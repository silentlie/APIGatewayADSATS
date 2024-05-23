 # Get the maximum ID from the notices table
        maxID_statement = "SELECT MAX(id) FROM notices"
        cursor.execute(maxID_statement ,)
        max_id_result = cursor.fetchone()
        max_id = max_id_result[0] 
        # Calculate the next report number
        report_number = max_id + 1