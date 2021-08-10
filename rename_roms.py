from xml.etree.ElementTree import ElementTree
import os
import datetime
import re
import sys

minimum_rating = 49
roms_folder = "x:\\"
#roms_folder = "y:\\roms\\"
IGNORED_FOLDERS = ('snap', 'mixart', 'media')


def get_node_value(root, name):
    element = root.find(name)
    if element == None:
        return ""
    return str(element.text)


def set_node_value(root, name, value):
    element = root.find(name)
    if element != None:
        element.text = value


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


def get_formatted_date(value):
    if value != None:
        value = str(datetime.datetime.strptime(value, '%Y%m%dT%H%M%S').date())
    return " "+get_formatted_value(value)


def get_formatted_value(value):
    if value != None:
        return "("+value+")"
    return ""


def read_gamelist(file):
    print("Reading "+file+"...")
    tree = ElementTree()
    tree.parse(file)
    folder = os.path.dirname(file)
    games = tree.findall(".//game")
    for game in games:
        path = os.path.basename(get_node_value(game, ".//path"))
        name = get_node_value(game, ".//name")
        name = re.sub("[/\\?*|\"]", "", name)
        developer = get_node_value(game, ".//developer")
        developer = re.sub("[/\\?*|\"]", "", developer)
        developer = get_formatted_value(developer)
        name = name.replace(developer, "").strip()
        extension = os.path.splitext(path)[1]
        new_path = ("./"+name + " "+ developer).strip()+extension
        new_path = new_path.replace(":", " -").replace("  ", " ")
        if os.path.basename(new_path).lower() == path.lower():
            continue
        set_node_value(game, ".//path", new_path)
        path_file = get_node_file(folder, path)
        if os.path.isfile(path_file):
            new_path_file = get_node_file(folder, new_path)
            print("Renaming '" + path_file + "' to '"+new_path+"'")
            try:
                if os.path.isfile(new_path_file):
                    suffix = ".DUPLICATE"
                    while os.path.isfile(new_path_file+suffix):
                        suffix += "1"
                    os.rename(path_file, new_path_file+suffix)
                else:
                    os.rename(path_file, new_path_file)
            except:
                    print("Oops!", sys.exc_info()[0], "occurred.")
                    print()
    tree.write(file)


def main(folder_path):
    read_files(folder_path)


if __name__ == "__main__":
    main(roms_folder)
