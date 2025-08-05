import csv
positions = ('K', 'TE', 'RB', 'WR', 'QB', 'DEF')
# Define classes to hold the data
from collections import defaultdict

def create_position_dictionary(player_stats):
    """
    Create a dictionary with positions as keys and arrays of players as values,
    sorted by points in descending order.

    :param player_stats: List of PlayerStats objects
    :return: Dictionary with positions as keys and sorted player arrays as values
    """
    position_dict = defaultdict(list)

    # Group players by position
    for player in player_stats:
        position_dict[player.position].append(player)

    # Sort players in each position by points in descending order
    for position in position_dict:
        position_dict[position].sort(key=lambda p: p.points, reverse=True)

    return position_dict

class PlayerStats:
    def __init__(self, player_key, full_name, position, team, points):
        self.player_key = player_key
        self.full_name = full_name
        if ',' in position:
            position_options = position.split(',')
            self.position = next((pos for pos in positions if pos in position_options), position_options[0])
        else:
            self.position = position
        self.team = team
        self.points = float(points)  # Convert points to float

    def __repr__(self):
        return f"PlayerStats({self.full_name}, {self.position}, {self.team}, {self.points})"


class DraftPick:
    def __init__(self, pick, round, manager, player, position):
        self.pick = int(pick)
        self.round = int(round)
        self.manager = manager
        self.player = player
        self.position = position

    def __repr__(self):
        return f"DraftPick({self.pick}, {self.round}, {self.manager}, {self.player}, {self.position})"

# Helper function to read and clean files
def clean_file_contents(filename):
    with open(filename, "r") as file:
        contents = file.read().replace("\x00", "")  # Remove all null characters
    return contents.splitlines()


# Load the tab-separated file into an array of PlayerStats objects
def load_tab_separated_file(filename):
    player_stats = []
    lines = clean_file_contents(filename)
    reader = csv.reader(lines, delimiter="\t")
    next(reader)  # Skip header
    for row in reader:
        player_stats.append(PlayerStats(*row))
    return player_stats


# Load the CSV file into an array of DraftPick objects
def load_csv_file(filename):
    draft_picks = []
    lines = clean_file_contents(filename)
    reader = csv.DictReader(lines)
    for row in reader:
        #print(row)
        if(row["pos"].find(',')!=-1):
            position_options = row["pos"].split(',')
            position = next((pos for pos in positions if pos in position_options), position_options[0])
        else:
            position = row["pos"]
        draft_picks.append(DraftPick(row["pick"], row["round"], row["manager"], row["player"], position))
    return draft_picks

def find_player_points(player_name, position, position_dict):
    """
    Find the points of a player by their name and position using the position dictionary.

    :param player_name: The full name of the player to search for.
    :param position: The position of the player.
    :param position_dict: Dictionary with positions as keys and lists of PlayerStats as values.
    :return: The points of the player if found, or None if the player does not exist.
    """
    # Ensure the position exists in the dictionary
    if position in position_dict:
        for player in position_dict[position]:
            if player.full_name.lower() == player_name.lower():
                return player.points
    return None

def compare_draft_picks(draft_picks, position_dict):
    """
    Compare each draft pick to the best remaining player in the position dictionary.

    :param draft_picks: List of DraftPick objects, sorted by draft order.
    :param position_dict: Dictionary with positions as keys and lists of PlayerStats as values.
    """
    print("manager,round,pick,player,position,points,best_alternative,best_alternative_points,point_difference,was_best_pick")

    pick_ratings = {}
    for draft_pick in draft_picks:
        is_best_pick = 0
        # Verify that the position exists in the dictionary and has remaining players
        if draft_pick.position in position_dict and position_dict[draft_pick.position]:
            # Get the best remaining player for the position
            best_option = position_dict[draft_pick.position][0]
            if best_option.full_name == draft_pick.player: # if they picked the best option, we're looking at their best alternative.
                #print("Picked Best Available Player.")
                best_option = position_dict[draft_pick.position][1]
                is_best_pick=1
            picked_points = find_player_points(draft_pick.player, draft_pick.position, position_dict)
            #print(f"Points: {picked_points} vs {best_option.points}")

            if(picked_points == None):
                #print(f"Could not find {draft_pick.player} at {draft_pick.position}")
                picked_points = 0
            # Determine point difference (assuming draft pick points aren't available)
            point_difference = picked_points - best_option.points
            # Print comparison results
            #print(f"Draft Pick: {draft_pick.player} ({draft_pick.position})")
            #print(f"Best Alternate Option: {best_option.full_name}, {point_difference:.2f} points to {draft_pick.manager}")                
            if draft_pick.manager in pick_ratings:
                pick_ratings[draft_pick.manager] += point_difference
            else:
                pick_ratings[draft_pick.manager] = point_difference
            # Remove the draft pick from the position dictionary
            position_dict[draft_pick.position] = [
                player for player in position_dict[draft_pick.position] if player.full_name != draft_pick.player
            ]
            print(f"{draft_pick.manager},{draft_pick.round},{draft_pick.pick},{draft_pick.player},{draft_pick.position},{picked_points},{best_option.full_name},{best_option.points},{point_difference:.2f},{is_best_pick}")
        # else:
        #     print(f"Draft Pick: {draft_pick.player} ({draft_pick.position})")
        #     print(f"No remaining options for position {draft_pick.position}.")
    return pick_ratings

def print_pick_ratings(pick_ratings):
    """
    Print the contents of the pick_ratings hashmap in a readable format.

    :param pick_ratings: Dictionary with manager names as keys and their cumulative points difference as values.
    """
    print("Pick Ratings:")
    for manager, points in pick_ratings.items():
        print(f"Manager: {manager}, Total Points Difference: {points:.2f}")

# Example usage
if __name__ == "__main__":
    # Replace these filenames with the actual paths to your files
    tab_separated_file = "player_stats2.tsv"
    csv_file = "draftresults.csv"

    # Load data
    player_stats = load_tab_separated_file(tab_separated_file)
    draft_picks = load_csv_file(csv_file)


    # # Print results
    # print("Player Stats:")
    # for player in player_stats:
    #     print(player)

    # print("\nDraft Picks:")
    # for pick in draft_picks:
    #     print(pick)
    # Create position dictionary
    position_dict = create_position_dictionary(player_stats)

    # Print results
    # for position, players in position_dict.items():
    #     print(f"Position: {position}")
    #     for player in players:
    #         print(f"  {player}")

    draftratings = compare_draft_picks(draft_picks,position_dict)
    print_pick_ratings(draftratings)

