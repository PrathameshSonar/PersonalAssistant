import os

this_file_path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(this_file_path)
ENTIRE_PROJECT_DIR = os.path.dirname(BASE_DIR)


def setName(name):
    name_txt = os.path.join(BASE_DIR, "username", "username.txt")
    with open(name_txt, 'w') as f:
        f.write(name)

    f.close()


def getName():
    name_txt = os.path.join(BASE_DIR, "username", "username.txt")
    name = ""
    with open(name_txt, 'r') as f:
        name = f.read()

    f.close()

    return name
