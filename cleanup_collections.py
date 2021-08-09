import os

find_path = "/home/pi/RetroPie/roms/"
replace_path = "x:\\"
collection_folder = "w:\\"
WINDOWS_LINE_ENDING = '\r\n'
UNIX_LINE_ENDING = '\n'
IGNORED_FOLDERS = ('snap', 'mixart', 'media')

def delete_file(file):
    if file != None and os.path.exists(file):
        print("Deleting "+file+"...")
        os.remove(file)


def read_files(folder_path):
    # Iterate over all the entries
    for entry in os.listdir(folder_path):
        # Create full path
        path = os.path.abspath(os.path.join(folder_path, entry))
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(path):
            if not path.endswith(IGNORED_FOLDERS):
                read_files(path)
        else:
            if path.endswith(".delete"):
                delete_collection(path)
            if path.endswith(".cfg"):
                update_collection(path)


def get_node_file(folder, value):
    if value != None:
        return os.path.abspath(os.path.join(folder, value))
    return None


def safe_getsize(file):
    if file != None and os.path.exists(file):
        return os.path.getsize(file)
    return 0

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

def delete_collection(file):
    print("Reading "+file+"...")
    reader = open(file, 'r')
    lines = reader.readlines()
    file_size = 0

    for line in lines:
        rom = os.path.abspath(line.strip().replace(find_path, replace_path))
        if os.path.exists(rom):
            file_size += safe_getsize(rom)
            delete_file(rom, True)

    file_size = round(file_size/1048576, 2)
   # delete_file(file)
    if file_size>0:
        print("Total size: " + str(file_size)+" MB")


def update_collection(file):
    print("Reading "+file+"...")
    reader = open(file, 'r', encoding='utf-8')
    lines = reader.readlines()

    remove_list = list()
    for line in lines:
        rom = os.path.abspath(line.strip().replace(find_path, replace_path))
        if not os.path.exists(rom):
            print("Rom not found: "+rom)
            remove_list.append(line)

    if len(remove_list) > 0:
        lines = [x for x in lines if x not in remove_list]
        writer = open(file, 'w', newline=UNIX_LINE_ENDING, encoding='utf-8')
        writer.writelines(lines)
        writer.close()


def main(folder_path):
    read_files(folder_path)


if __name__ == "__main__":
    main(collection_folder)
