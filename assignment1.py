from datetime import timedelta
from flask import Flask, jsonify, render_template_string, request
from flask_marshmallow import Marshmallow
from marshmallow import fields
from connect_to_vid_db import get_db_connection, Error

app = Flask(__name__)
ma = Marshmallow(app)


class VideoSchema(ma.Schema):
    title = fields.String(required=True)
    release_year = fields.Integer(required=True)
    runtime = fields.Integer(required=True)

    class Meta:
        fields = (
            "id",
            "title",
            "release_year",
            "runtime"
        )


video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)
conn = get_db_connection()


def binary_search(video_list, title):
    left, right = 0, len(video_list) - 1
    title = title.lower()
    results = []

    while left <= right:
        mid = (left + right) // 2
        mid_title = video_list[mid]['title'].lower()

        if mid_title == title:
            results.append(video_list[mid])
            i = mid - 1
            while i >= 0 and video_list[i]['title'].lower() == title:
                results.insert(0, video_list[i])
                i -= 1
            i = mid + 1
            while i < len(video_list) and video_list[i]['title'].lower() == title:
                results.append(video_list[i])
                i += 1
            break
        elif mid_title < title:
            left = mid + 1
        else:
            right = mid - 1

    return results


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
        <h1>Search for a Video</h1>
        <form action="/search_video" method="get">
            <label for="title">Video Title:</label>
            <input type="text" id="title" name="title" required>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    ''')


@app.route('/search_video', methods=['GET'])
def search_video():
    title = request.args.get('title')
    if not title:
        return jsonify({"message": "No search term provided."}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id, title, release_year, runtime FROM Video"
    cursor.execute(query)
    video_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    video_rows.sort(key=lambda x: x['title'])

    result = binary_search(video_rows, title)

    if not result:
        return jsonify({"message": "No results found."}), 404

    for row in result:
        if isinstance(row['runtime'], timedelta):
            row['runtime'] = str(row['runtime'])

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)