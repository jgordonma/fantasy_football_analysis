from yahoofantasy import Context

def print_object_attributes(obj):
    """
    Prints all attributes of an object, including their values.

    :param obj: The object to inspect
    """
    print(f"Attributes of {obj.__class__.__name__} object:\n")
    
    for attribute_name in dir(obj):
        # Skip built-in attributes (those starting with __)
        if not attribute_name.startswith("__"):
            try:
                attribute_value = getattr(obj, attribute_name)
                print(f"{attribute_name}: {attribute_value}")
            except AttributeError:
                print(f"{attribute_name}: (Could not retrieve value)")

ctx = Context()
positions = ('K','TE','RB', 'WR','QB')
leagues = ctx.get_leagues('nfl', 2024)
for league in leagues:
    print("player_key\tfull_name\tposition\tteam\tpoints")
    for player in league.players():
        points = player.get_points()
        if(points > 0):
            position = player.display_position
            print(f"{player.player_key}\t{player.name.full}\t{player.display_position}\t{player.editorial_team_abbr}\t{points}")
            #print_object_attributes(player)