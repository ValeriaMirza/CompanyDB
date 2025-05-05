import re
import docx
import psycopg2
import sys
import os
from db_utils import get_cursor, close_connection


sys.stdout.reconfigure(encoding='utf-8')

doc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'codelist.docx'))


conn, cursor = get_cursor()


def extract_table_data(doc_path):
    doc = docx.Document(doc_path)
    table_data = []
    
  
    for table in doc.tables:
        for row in table.rows:
            
            row_data = [cell.text.strip() for cell in row.cells]
            table_data.append(row_data)
    
    return table_data

table_data = extract_table_data(doc_path)


for row in table_data:
    if len(row) >= 3: 
        code = row[1]  
        industry_name = row[2] 

        
        if not code.isdigit():
            continue 

 
        cursor.execute('INSERT INTO "Industry" (code, name) VALUES (%s, %s)', (code, industry_name))


close_connection(conn, cursor)

print("Industries imported to PostgreSQL successfully.")
