# You are tasked with developing a video sorting function that sorts a list of videos alphabetically by their titles using the merge sort algorithm. This application will help users organize their video collections more efficiently. You should use the previous assignment project.

# TODO 1 - Implement the merge sort algorithm in Python to sort videos by their titles..
from flask import Flask, jsonify, render_template_string, request
from flask_marshmallow import Marshmallow
from connect_to_vid_db import get_db_connection

app = Flask(__name__)
ma = Marshmallow(app)

def merge_sort_videos(video_list):
    if len(video_list) > 1:
        mid = len(video_list) // 2
        left_half = video_list[:mid]
        right_half = video_list[mid:]

        # Recursively sort both halves
        merge_sort_videos(left_half)
        merge_sort_videos(right_half)

        i = j = k = 0

        # Merge the sorted halves
        while i < len(left_half) and j < len(right_half):
            # Access the first element of the tuple, which is the title
            if left_half[i][0].lower() < right_half[j][0].lower():
                video_list[k] = left_half[i]
                i += 1
            else:
                video_list[k] = right_half[j]
                j += 1
            k += 1

        # Check for any remaining elements
        while i < len(left_half):
            video_list[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            video_list[k] = right_half[j]
            j += 1
            k += 1

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search for a Video</title>
    </head>
    <body>
        <h1>Sort Your Videos</h1>
        <a href="/sort_videos"><button type="button">Sort Videos</button></a>
    </body>
    </html>
    ''')

@app.route('/sort_videos', methods=['GET'])
def sort_videos():
    print("Connecting to database...")
    conn = get_db_connection()
    print("Connected!")
    cursor = conn.cursor()

    print("Executing query...")
    query = "SELECT title FROM Video"
    cursor.execute(query)
    videos = cursor.fetchall()
    print(f"Fetched {len(videos)} videos.")

    cursor.close()
    conn.close()

    print("Starting merge sort...")
    print(f"Fetched videos: {videos}")
    merge_sort_videos(videos)
    print("Merge sort completed.")

    # Create an HTML string to display the sorted video titles
    html_output = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sorted Videos</title>
    </head>
    <body>
        <h1>Sorted Videos</h1>
        <ul>
    '''

    for video in videos:
        html_output += f'<li>{video[0]}</li>'

    html_output += '''
        </ul>
        <a href="/"><button type="button">Back to Home</button></a>
    </body>
    </html>
    '''

    return render_template_string(html_output)


if __name__ == "__main__":
    app.run(debug=True, port=5001)