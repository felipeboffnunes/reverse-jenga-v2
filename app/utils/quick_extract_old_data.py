# import csv
# import json
# import sqlite3
#
# # File paths
# CSV_FILE = 'tower_1.csv'
# JL_FILE = '../data/books.jl'
# DB_NAME = 'books_database.db'
#
# # Read CSV and write to JL file
# def csv_to_jl(csv_file, jl_file):
#     with open(csv_file, 'r', encoding='utf-8') as csvf, open(jl_file, 'w', encoding='utf-8') as jlf:
#         reader = csv.DictReader(csvf)
#         for row in reader:
#             data = {
#                 'Author': row['Author'],
#                 'Title': row['Title'],
#                 'Pages': row['Pages'],
#                 'ISBN-13': row['ISBN-13'],
#                 'Language': row['Language']
#             }
#             json.dump(data, jlf)
#             jlf.write('\n')
#
# # Create a new table in the database
# def create_book_table():
#     with sqlite3.connect(DB_NAME) as conn:
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS book_info (
#                 Author TEXT,
#                 Title TEXT,
#                 Pages INTEGER,
#                 ISBN_13 TEXT,
#                 Language TEXT
#             )
#         """)
#
# # Read JL file and insert data into database
# def insert_data_from_jl(jl_file):
#     with sqlite3.connect(DB_NAME) as conn, open(jl_file, 'r', encoding='utf-8') as jlf:
#         cursor = conn.cursor()
#         for line in jlf:
#             data = json.loads(line)
#             cursor.execute("""
#                 INSERT INTO book_info (Author, Title, Pages, ISBN_13, Language)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (data['Author'], data['Title'], data['Pages'], data['ISBN-13'], data['Language']))
#
# # Main execution
# csv_to_jl(CSV_FILE, JL_FILE)
# create_book_table()
# insert_data_from_jl(JL_FILE)