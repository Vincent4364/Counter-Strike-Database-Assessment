from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "CS_DATA.db"


def create_connection(db_filename):
    try:
        connection = sqlite3.connect(db_filename)
        return connection
    except Error as e:
        print(e)
        return None


@app.route('/')
def render_home_page():
    return render_template('index.html')


@app.route('/display')
def render_leaderboard_page():
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    data_list = cursor.fetchall()
    connection.close()

    return render_template('display.html', data=data_list)


@app.route('/display')
def render_major_league_page():
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query)
    data_list = cursor.fetchall()
    connection.close()

    return render_template('display.html', data=data_list)


@app.route('/search', methods=['GET', 'POST'])
def render_search_page():
    if request.method == 'POST':
        look_up = request.form['Search']
        search_term = look_up
        title = "Search for: '" + look_up + "'"
        look_up = "%" + look_up + "%"

        query = """
        SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
        FROM player_stats
        WHERE player_name LIKE ? OR teams_played_in LIKE ? OR country LIKE ?
        """
        connection = create_connection(DATABASE)
        cursor = connection.cursor()
        cursor.execute(query, (look_up, look_up, look_up))
        data_list = cursor.fetchall()
        connection.close()

        no_results = len(data_list) == 0

        return render_template('display.html', data=data_list, search_term=search_term, no_results=no_results)

    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
