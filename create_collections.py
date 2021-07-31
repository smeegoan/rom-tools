from xml.etree.ElementTree import ElementTree
import os

minimum_rating = 49
roms_folder = "x:\\"
collections_folder = "w:\\"
roms_folder_in_collection = "/home/pi/RetroPie/roms/"
IGNORED_FOLDERS = ('snap', 'mixart', 'media','genesis','segacd')
keywords = {"batman": "batman",
            "castlevania": "castlevania",
            "contra": "contra",
            "crashbandicoot": "crash bandicoot",
            "donkeykong": "donkey kong",
            "dragonball": "dragon ball",
            "finalfight": "final fight",
            "fatalfury": "fatal fury",
            "finalfantasy": "final fantasy",
            "formula1": ["grand prix", "f1 ", "formula 1"],
            "fzero": "fzero",
            "goldenaxe": "golden axe",
            "jurassicpark": "jurassic park",
            "kingoffighters": "king of fighters",
            "mario": "mario ",
            "megaman": "mega man",
            "metalslug": "metal slug",
            "metroid": "metroid",
            "mortalkombat": "mortal kombat",
            "ninja": "ninja",
            "princeofpersia": "prince of persia",
            "puzzle": ["puzzle", "tetris"],
            "quake": "quake",
            "racing": ["racing", "nascar", "racer"],
            "rally": "rally",
            "rayman": "rayman",
            "residentevil": "resident evil",
            "robocop": "robocop",
            "silenthill": "silent hill",
            "simpsons": "simpsons",
            "soccer": ["soccer","world cup"],
            "sonic": "sonic ",
            "spiderman": ["spiderman","spider-man"],
            "starwars": "star wars",
            "streetfighter": "street fighter",
            "skate": ["tonny hawk","skate"],
            "superman": "superman",
            "tennis": "tennis",
            "tombraider": "tomb raider",
            "zelda": "zelda"}
collections = {}
WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'


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


def name_contains_keywords(name, keywords):
    if isinstance(keywords, list):
        for keyword in keywords:
            if keyword in name:
                return True
    else:
        return keywords in name
    return False


def read_gamelist(file):
    print("Reading "+file+"...")
    tree = ElementTree()
    tree.parse(file)
    folder = os.path.basename(os.path.dirname(file))
    games = tree.findall(".//game")
    for game in games:
        name = get_node_value(game, ".//name").lower()
        for collection in keywords:
            if name_contains_keywords(name, keywords[collection]):
                path = roms_folder_in_collection+folder + "/" + \
                    os.path.basename(get_node_value(game, ".//path"))
                if not collection in collections:
                    file = os.path.join(collections_folder,
                                        "custom-"+collection+".cfg")
                    if os.path.exists(file):
                        reader = open(file, 'r')
                        collections[collection] = reader.readlines()
                    else:
                        collections[collection] = list()
                collections[collection].append(path+UNIX_LINE_ENDING)


def main(folder_path):
    read_files(folder_path)
    for collection in collections:
        lines = list(set(collections[collection]))
        file = os.path.join(collections_folder, "custom-"+collection+".cfg")
        writer = open(file, 'w', newline=UNIX_LINE_ENDING)
        writer.writelines(lines)
        writer.close()
        print("Wrote " + file + ": " +
              str(len(lines)) + " games")


if __name__ == "__main__":
    main(roms_folder)
