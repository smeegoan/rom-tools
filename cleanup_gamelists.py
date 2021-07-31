from xml.etree.ElementTree import ElementTree
import os

minimum_rating = 49
roms_folder = "x:\\"
#roms_folder = "y:\\roms\\"
IGNORED_FOLDERS = ('snap', 'mixart', 'media','genesis','segacd')


def delete_file(file, soft=False):
    if file != None and os.path.exists(file):
        try:
            if soft:
                print("Manually delete "+file+".TODELETE")
                os.rename(file, file+".TODELETE")
            else:
                print("Deleting "+file+"...")
                os.remove(file)
        except:
            print("Error deleting "+file)


def get_node_value(root, name):
    element = root.find(name)
    if element == None:
        return None
    return element.text


def read_files(folder_path):
    for entry in os.listdir(folder_path):
        # Create full path
        path = os.path.abspath(os.path.join(folder_path, entry))
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(path):
            if not path.endswith(IGNORED_FOLDERS):
                read_files(path)
        else:
            if path.endswith("gamelist.xml"):
                read_gamelist(path)


def get_node_file(folder, value):
    if value != None:
        return os.path.abspath(os.path.join(folder, value))
    return None


def safe_getsize(file):
    if file != None and os.path.exists(file):
        return os.path.getsize(file)
    return 0


def read_gamelist(file):
    ids = {}
    print("Reading "+file+"...")
    tree = ElementTree()
    tree.parse(file)
    folder = os.path.dirname(file)
    games = tree.findall(".//game")
    remove_list = list()
    for game in games:
        if len(game.attrib) > 0:
            id = game.attrib["id"]
        else:
            id = "0"
        rating = get_node_value(game, "rating")
        path = get_node_file(folder, get_node_value(game, ".//path"))
        if rating != None:
            rating = float(rating)*100
        else:
            rating = 0
        if rating > 0 and rating < minimum_rating:
            name = get_node_value(game, ".//name")
            print(name + " has low rating: " + str(rating) + "%")
            delete_game(folder, remove_list, game, path)
        elif not os.path.exists(path):
            print(path + " is missing")
            delete_game(folder, remove_list, game, path)
        elif id in ids:
            print(path + " is a duplicate of " + ids.get(id))
            delete_game(folder, remove_list, game, path)
        elif id != "0" and not is_multi_disc(path):  # ignore multi disc
            ids[id] = path
    root = tree.getroot()
    for game in remove_list:
        root.remove(game)
    tree.write(file)


def is_multi_disc(path):
    return not "disc " in path and not "cd " in path and not path.endswith(".m3u")


def delete_game(folder, remove_list, game, path):
    remove_list.append(game)
    image = get_node_file(folder, get_node_value(game, ".//image"))
    video = get_node_file(folder, get_node_value(game, ".//video"))
    file_size = safe_getsize(image)
    file_size += safe_getsize(video)
    file_size += safe_getsize(path)
    file_size = round(file_size/1048576, 2)
    delete_file(video)
    delete_file(image)
    delete_file(path, True)
    print("Freed " + str(file_size) + "MB")


def main(folder_path):
    read_files(folder_path)


if __name__ == "__main__":
    main(roms_folder)
