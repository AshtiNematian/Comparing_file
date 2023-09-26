import os
import pyodbc


# Define the connection string
server = input("Please enter SQL Server's name or IP address:")
server = server  # Replace with your SQL Server's name or IP address
database = 'r'  # Replace with the name of your database
username = ''  # Replace with your SQL Server username
password = ''  # Replace with your SQL Server password

# Create the connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}}' \
                    f';SERVER={server};DATABASE={database};UID={username};PWD={password}'


# Function to get the size of the file
def get_file_size(filepath):
    return os.path.getsize(filepath)


# Function to connect to the SQL Server database and fetch the FileBody size
def get_sql_filebody_size(bizcode):
    # File name with the ".zip" extension
    original_file_name = bizcode

    # Split the file name based on "_0" to remove the "-0" part
    file_name_without_suffix = original_file_name.split("_0")[0]

    # Remove the ".zip" extension from the file name
    new_file_name = os.path.splitext(file_name_without_suffix)[0]

    # Output the new file name
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        sql_query = f"""
              SELECT
              ROUND([PackSize] * 1024,0) AS size_in_kb,
              Bizcode
              FROM
              [Archive_Storage] 
              WHERE
              BizCode = '{new_file_name}';
              """

        cursor.execute(sql_query)
        row = cursor.fetchone()

        if row is not None and row[0] is not None:
            filebody_size = row[0]
        else:
            filebody_size = 0

        cursor.close()
        connection.close()

        return filebody_size

    except Exception as e:
        print(f"Error fetching SQL FileBody size for BizCode '{bizcode}': {e}")
        return 0


# Replace this with the path to your directory
# r"C:\Users\NematianA\Desktop\asnad"
directory = input('Add path of directory : ')
directory_path = directory

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    files = os.listdir(directory_path)

    if len(files) == 0:
        print("The directory is empty.")
    else:
        print("File sizes in the directory (in KB) rounded up:")
        # Sort the files based on size in ascending order
        sorted_files = sorted(files, key=lambda file: get_file_size(os.path.join(directory_path, file)))

        for file in sorted_files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                file_size_bytes = get_file_size(file_path)
                file_size_kb = file_size_bytes / 1024
                print(f"{file}: {file_size_kb:.2f} KB")

                # Get the BizCode from the file name or use the appropriate way to fetch it
                # Replace with the proper way to get BizCode
                bizcode = file.replace(".txt", "")

                # Fetch the FileBody size from the SQL Server database
                filebody_size_sql = get_sql_filebody_size(bizcode)

                # Compare the sizes
                # Use an appropriate threshold value
                if abs(file_size_kb - filebody_size_sql) > 0.5:
                    print("File size and SQL FileBody size do not match.")
                else:
                    print("File size and SQL FileBody size match.")

            else:
                print(f"{file}: Not a file.")
else:
    print("The specified directory does not exist.")
