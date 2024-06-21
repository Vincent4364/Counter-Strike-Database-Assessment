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
def render_display_page():
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


@app.route('/top_players/rating/<rating>')
def render_top_players_by_rating_page(rating):
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    WHERE rating > ?
    ORDER BY rating DESC
    LIMIT 10
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (rating, ))
    data_list = cursor.fetchall()
    connection.close()

    return render_template('top_players.html', data=data_list)

@app.route('/top_players/kd/<kd>')
def render_top_players_by_kd_page(kd):
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    WHERE kd_ratio > ?
    ORDER BY kd_ratio DESC
    LIMIT 10
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (kd,))
    data_list = cursor.fetchall()
    connection.close()

    return render_template('top_players.html', data=data_list)

@app.route('/top_players/total_kills/<total_kills>')
def render_top_players_by_total_kills_page(total_kills):
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    WHERE total_kills > ?
    ORDER BY total_kills DESC
    LIMIT 10
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (total_kills, ))
    data_list = cursor.fetchall()
    connection.close()

    return render_template('top_players.html', data=data_list)


@app.route('/top_players/headshot/<headshot>')
def render_top_players_by_headshot_percentage_page(headshot):
    query = """
    SELECT rating, headshot_percentage, kd_ratio, teams_played_in, country, player_name, total_kills
    FROM player_stats
    WHERE headshot_percentage > ?
    ORDER BY headshot_percentage DESC
    LIMIT 10
    """
    connection = create_connection(DATABASE)
    cursor = connection.cursor()
    cursor.execute(query, (headshot, ))
    data_list = cursor.fetchall()
    connection.close()

    return render_template('top_players.html', data=data_list)


@app.route('/top_players')
def render_top_players_page():
    return render_template('top_players.html')


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
