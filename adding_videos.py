from connect_to_vid_db import get_db_connection, Error

conn = get_db_connection()
if conn is not None:
    try:
        cursor = conn.cursor()

        sql = "INSERT INTO Video (id, title, release_year, runtime) VALUES (%s, %s, %s, %s)"

        values = video_titles = [
            (1, 'Inception', 2010, '02:28:00'),
            (2, 'The Matrix', 1999, '02:16:00'),
            (3, 'Interstellar', 2014, '02:49:00'),
            (4, 'The Godfather', 1972, '02:55:00'),
            (5, 'Pulp Fiction', 1994, '02:34:00')
        ]

        cursor.executemany(sql, values)
        conn.commit()
        print(cursor.rowcount, "Videos added successfully.")
    except Error as e:
        print(f"Error adding videos: {e}")
        conn.rollback()

