from organizer import organize_folder


def main():

    folder = input("Welchen Ordner möchtest du organisieren?\n> ")

    organize_folder(folder)


if __name__ == "__main__":
    main()