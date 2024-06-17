import os
import re

def extract_sql_from_tmdl(file_path):
    start_pattern = re.compile(r'let\s+Source = Odbc\.Query\("dsn=Simba Athena", "')
    end_pattern = re.compile(r'"\),')
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    start_match = start_pattern.search(content)
    end_match = end_pattern.search(content)
    
    if start_match and end_match:
        start_index = start_match.end()
        end_index = end_match.start()
        sql_query = content[start_index:end_index]
        return sql_query
    return None

def process_tmdl_files(directory):
    tmdl_files = [f for f in os.listdir(directory) if f.endswith('.tmdl')]
    for tmdl_file in tmdl_files:
        file_path = os.path.join(directory, tmdl_file)
        sql_query = extract_sql_from_tmdl(file_path)
        if sql_query:
            sql_file_path = os.path.splitext(file_path)[0] + '.sql'
            with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
                sql_file.write(sql_query)
            print(f'SQL query extracted and saved to {sql_file_path}')
        else:
            print(f'No SQL query found in {file_path}')

if __name__ == "__main__":
    directory = r'C:\Users\JorgeNavarro'
    process_tmdl_files(directory)
