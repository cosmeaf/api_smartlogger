import sqlite3
import psycopg2

# Configurações do SQLite
sqlite_db_path = 'db.sqlite3'

# Configurações do PostgreSQL
pg_host = 'localhost'
pg_dbname = 'smartlogger'
pg_user = 'superuser'
pg_password = 'Canela_32Canela_32'

# Conectar ao SQLite
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# Conectar ao PostgreSQL
pg_conn = psycopg2.connect(host=pg_host, dbname=pg_dbname, user=pg_user, password=pg_password)
pg_cursor = pg_conn.cursor()

# Obter todas as tabelas do SQLite, ignorando tabelas de sistema
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    columns = sqlite_cursor.fetchall()

    column_names = [column[1] for column in columns]
    column_names_str = ', '.join([f'"{col}"' for col in column_names])

    # Extrair dados do SQLite
    sqlite_cursor.execute(f'SELECT {column_names_str} FROM "{table_name}";')
    rows = sqlite_cursor.fetchall()

    # Inserir dados no PostgreSQL
    for row in rows:
        placeholders = ', '.join(['%s'] * len(row))
        insert_query = f'INSERT INTO {table_name} ({column_names_str}) VALUES ({placeholders}) ON CONFLICT DO NOTHING'
        
        try:
            pg_cursor.execute(insert_query, row)
        except psycopg2.errors.UniqueViolation:
            pg_conn.rollback()
            update_query = f'UPDATE {table_name} SET {", ".join([f"{col} = %s" for col in column_names])} WHERE id = %s'
            pg_cursor.execute(update_query, row + (row[0],))
        pg_conn.commit()

# Fechar conexões
sqlite_conn.close()
pg_conn.close()
