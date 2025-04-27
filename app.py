import os
import pandas as pd
from flask import Flask, jsonify, render_template

# Factory to create the Flask app
def create_app():
    app = Flask(__name__)

    # Load datasets
    base_dir = os.path.dirname(os.path.abspath(__file__))
    matches_df = pd.read_csv(os.path.join(base_dir, 'data', 'matches.csv'))
    deliveries_df = pd.read_csv(os.path.join(base_dir, 'data', 'deliveries.csv'))

    # Helper: lowercase a column safely
    def lower_series(df, col):
        return df[col].astype(str).str.lower()

    # Helper: count wickets (exclude run outs)
    def count_wickets(df):
        s = df['player_dismissed'].dropna().astype(str).str.lower()
        return int(s[s != 'run out'].count())

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/api/team/<team_name>')
    def team_record(team_name):
        t = team_name.strip().lower()
        df = matches_df[
            (lower_series(matches_df, 'team1') == t) |
            (lower_series(matches_df, 'team2') == t)
        ]
        if df.empty:
            return jsonify(error="Team not found"), 404
        wins = int(df[lower_series(df, 'winner') == t].shape[0])
        return jsonify(
            team=team_name.strip(),
            matches_played=int(df.shape[0]),
            wins=wins,
            losses=int(df.shape[0] - wins)
        )

    @app.route('/api/team_vs/<team1>/<team2>')
    def team_vs_record(team1, team2):
        t1, t2 = team1.strip().lower(), team2.strip().lower()
        cond = (
            (lower_series(matches_df, 'team1') == t1) &
            (lower_series(matches_df, 'team2') == t2)
        ) | (
            (lower_series(matches_df, 'team1') == t2) &
            (lower_series(matches_df, 'team2') == t1)
        )
        df = matches_df[cond]
        if df.empty:
            return jsonify(error="No matches found between these teams"), 404
        wins1 = int(df[lower_series(df, 'winner') == t1].shape[0])
        wins2 = int(df[lower_series(df, 'winner') == t2].shape[0])
        return jsonify(
            team1=team1.strip(),
            team2=team2.strip(),
            matches=int(df.shape[0]),
            wins_team1=wins1,
            wins_team2=wins2
        )

    @app.route('/api/batsman/<player>')
    def batsman_record(player):
        p = player.strip().lower()
        df = deliveries_df[lower_series(deliveries_df, 'batter') == p]
        if df.empty:
            return jsonify(error="Batsman not found"), 404
        runs = int(df['batsman_runs'].sum())
        balls = int(df.shape[0])
        return jsonify(
            batsman=player.strip(),
            total_runs=runs,
            balls_faced=balls
        )

    @app.route('/api/batsman_vs/<player>/<team>')
    def batsman_vs_record(player, team):
        p, t = player.strip().lower(), team.strip().lower()
        df = deliveries_df[
            (lower_series(deliveries_df, 'batter') == p) &
            (lower_series(deliveries_df, 'bowling_team') == t)
        ]
        if df.empty:
            return jsonify(error="No records for this batsman vs team"), 404
        runs = int(df['batsman_runs'].sum())
        balls = int(df.shape[0])
        return jsonify(
            batsman=player.strip(),
            opponent=team.strip(),
            total_runs=runs,
            balls_faced=balls
        )

    @app.route('/api/bowler/<player>')
    def bowler_record(player):
        p = player.strip().lower()
        df = deliveries_df[lower_series(deliveries_df, 'bowler') == p]
        if df.empty:
            return jsonify(error="Bowler not found"), 404
        wickets = count_wickets(df)
        balls = int(df.shape[0])
        return jsonify(
            bowler=player.strip(),
            total_wickets=wickets,
            balls_bowled=balls
        )

    @app.route('/api/bowler_vs/<player>/<team>')
    def bowler_vs_record(player, team):
        p, t = player.strip().lower(), team.strip().lower()
        df = deliveries_df[
            (lower_series(deliveries_df, 'bowler') == p) &
            (lower_series(deliveries_df, 'batting_team') == t)
        ]
        if df.empty:
            return jsonify(error="No records for this bowler vs team"), 404
        wickets = count_wickets(df)
        balls = int(df.shape[0])
        return jsonify(
            bowler=player.strip(),
            opponent=team.strip(),
            total_wickets=wickets,
            balls_bowled=balls
        )

    return app

# Expose the app for Gunicorn / WSGI
app = create_app()

# For local development
if __name__ == '__main__':
    app.run(debug=True)
