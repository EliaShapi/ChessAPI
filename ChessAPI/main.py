from chessdotcom import Client, get_leaderboards, get_player_stats, get_player_game_archives
import pprint
import requests

printer = pprint.PrettyPrinter()

# Set a custom User-Agent
Client.request_config['headers'] = {
    'User-Agent': 'My Python Application. Contact me at eliahush.hanavi@gmail.com'
}


# Fetch and print leaderboards
def print_leaderboards():
    data = get_leaderboards().json
    leaderboards = data["leaderboards"]  # Access the 'leaderboards' dictionary directly

    for category, players in leaderboards.items():
        print(f'Category: {category}')
        if isinstance(players, list):  # Ensure the value is a list of player entries
            for idx, entry in enumerate(players):
                if isinstance(entry, dict) and "username" in entry and "score" in entry:
                    print(f'Rank: {idx + 1} | Username: {entry["username"]} | Rating: {entry["score"]}')
                else:
                    print(f'Skipping entry: {entry} - Invalid format.')
        else:
            print(f'Skipping category {category}: No player data found or invalid format.')



def get_player_rating(username):
    try:
        # Fetch player stats
        response = get_player_stats(username)
        data = response.json

        # Check if 'stats' key is present
        stats = data.get('stats')
        if not stats:
            print(f"No stats found for username '{username}'.")
            return

        categories = ['chess_rapid', 'chess_blitz', 'chess_bullet']
        for category in categories:
            if category in stats:
                print(f"Category: {category}")
                print(f"  Current: {stats[category]['last']['rating']}")
                print(f"  Best: {stats[category]['best']['rating']}")
                print(f"  Record: {stats[category]['record']}")
            else:
                print(f"Category: {category} is not available for this player.")
    except KeyError as e:
        print(f"Key error: {e}. Check the response structure.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")




def debug_player_stats(username):
    try:
        data = get_player_stats(username).json
        print(f"Raw data for username '{username}':\n", data)
    except Exception as e:
        print(f"Error fetching stats for username '{username}': {e}")


def get_most_recent_game(username):
    # Get the player's game archives (assumed to return a dictionary directly)
    data = get_player_game_archives(username)  # No need for .json()

    # Check if 'archives' key exists and is not empty
    if 'archives' in data and data['archives']:
        url = data['archives'][-1]

        # Fetch the games from the URL
        games = requests.get(url).json()  # .json() is valid here since it is a response object

        # Check if 'games' key exists and is not empty
        if 'games' in games and games['games']:
            game = games['games'][-1]
            printer.pprint(game)
        else:
            print("No games found in the most recent archive.")
    else:
        print("No archives found for this user.")


get_most_recent_game('eliahu_hanavi')