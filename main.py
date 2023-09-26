import math
import os
import pyodbc
server = input("Please enter SQL Server's name or IP address:")
server = server

connection_string = "Driver={SQL Server};Server={server};Database=DbArchive_Master;Uid=sa;Pwd=Safa-qc-3;"


# Function to get the size of the file
def get_file_size(filepath):
    return os.path.getsize(filepath)


# Function to connect to the SQL Server database and fetch the FileBody size
def get_sql_filebody_size(bizcode):
    print(bizcode)
    # File name with the ".zip" extension
    original_file_name = bizcode

    # Split the file name based on "_0" to remove the "-0" part
    file_name_without_suffix = original_file_name.split("_0")[0]

    # Remove the ".zip" extension from the file name
    new_file_name = os.path.splitext(file_name_without_suffix)[0]
    print(new_file_name)

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
        print(row)

        if row is not None and row[0] is not None:
            filebody_size = row[0]
            print(filebody_size)
        else:
            filebody_size = 0

        cursor.close()
        connection.close()

        return filebody_size

    except Exception as e:
        print(f"Error fetching SQL FileBody size for BizCode '{bizcode}': {e}")
        return 0


# Replace this with the path to your directory
# C:\Users\Administrator\Desktop\write>
directory = input('Add path of directory : ')
directory_path = directory

if os.path.exists(directory_path) and os.path.isdir(directory_path):
    files = os.listdir(directory_path)

    if len(files) == 0:
        print("The directory is empty.")
    else:
        print("File sizes in the directory (in KB) rounded up:")
        # Sort the files based on size in ascending order
        sorted_files = sorted(files,
                              key=lambda file: math.ceil(get_file_size(os.path.join(directory_path, file))))

        for file in sorted_files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                file_size_bytes = get_file_size(file_path)
                file_size_kb = file_size_bytes
                rounded_file_size_kb = round(file_size_kb)  # Round to two decimal places
                # Get the BizCode from the file name or use the appropriate way to fetch it
                # Replace with the proper way to get BizCode
                bizcode = file.replace(".txt", "")

                # Fetch the FileBody size from the SQL Server database
                filebody_size_sql = get_sql_filebody_size(bizcode)

                # Compare the sizes
                # Use an appropriate threshold value

                if abs(file_size_kb - filebody_size_sql) > 0.5:
                    print(f"in{bizcode} File size and SQL FileBody size do not match."
                          f"File size:{file_size_kb} and SQL FileBody size:{filebody_size_sql}")
                else:
                    continue

            else:
                print(f"{file}: Not a file.")

else:
    print("The specified directory does not exist.")
