import os
import re

def extract_sql_from_tmdl(file_path):
    start_pattern = re.compile(r'SELECT', re.IGNORECASE)
    end_pattern = re.compile(r'"\s*\),', re.DOTALL)

    with open(file_path, 'r', encoding='utf-8') as file:
        inside_sql = False
        sql_lines = []
        
        for line in file:
            if inside_sql:
                sql_lines.append(line)
                if end_pattern.search(line):
                    inside_sql = False
                    break
            elif start_pattern.search(line):
                inside_sql = True
                sql_lines.append(line)

    if sql_lines:
        sql_query = ''.join(sql_lines)
        sql_query = start_pattern.split(sql_query, 1)[1]  # Remove everything before and including 'SELECT'
        sql_query = end_pattern.sub('', sql_query)  # Remove the end pattern from the extracted query
        return 'SELECT' + sql_query.strip()  # Add 'SELECT' back at the beginning and strip any extra spaces
    
    return None

def process_tmdl_files(directory):
    queries_dir = os.path.join(directory, 'QUERIES')
    os.makedirs(queries_dir, exist_ok=True)
    
    try:
        for root, _, files in os.walk(directory):
            tmdl_files = [f for f in files if f.endswith('.tmdl')]
            for tmdl_file in tmdl_files:
                file_path = os.path.join(root, tmdl_file)
                sql_query = extract_sql_from_tmdl(file_path)
                if sql_query:
                    # Get relative path to the file's directory from the base directory
                    relative_dir = os.path.relpath(root, directory)
                    # Extract the last two parts of the relative path
                    last_two_parts = os.path.join(*relative_dir.split(os.sep)[-3:])
                    # Replace path separators with underscores to create the subdirectory name
                    sub_dir_name = last_two_parts.replace(os.sep, '_')
                    # Create corresponding subdirectory in the QUERIES folder
                    sub_queries_dir = os.path.join(queries_dir, sub_dir_name)
                    os.makedirs(sub_queries_dir, exist_ok=True)
                    
                    sql_file_name = os.path.splitext(tmdl_file)[0] + '.sql'
                    sql_file_path = os.path.join(sub_queries_dir, sql_file_name)
                    with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
                        sql_file.write(sql_query)
                    print(f'SQL query extraída y guardada en {sql_file_path}')
                else:
                    print(f'No se encontró ninguna SQL query en {file_path}')
    except FileNotFoundError:
        print(f"Error: El directorio '{directory}' no existe.")
    except PermissionError:
        print(f"Error: No tienes permiso para acceder al directorio '{directory}'.")

if __name__ == "__main__":
    directory = r'/mnt/c/Users/JorgeNavarro/Documents'
    print(f"Procesando archivos en el directorio: {directory}")
    process_tmdl_files(directory)
