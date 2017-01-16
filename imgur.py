"""
CLimgur is a command line imgur upload client.
add CLimgur to your path and then upload files like this:

    single file: imgur -upload "path/to/file.png"
    album upload: imgur -album "path/to/folder"

once the file is uploaded a link will be in the command line.

"""
import argparse
import os
from credentials import get, set
from upload import upload


def main():
    """
    get command line options and upload the file(s) accordingly
    :return: None
    """
    parser = argparse.ArgumentParser()
    options = parser.add_mutually_exclusive_group()
    options.add_argument("-i", "--image", help="Upload a single file to imgur")
    options.add_argument("-a", "--album", help="Upload all images in directory to imgur as an album")
    args = parser.parse_args()

    # Attempt to get credentials from file. If unavailable set credentials from user
    login = get.get_creds()
    cred_dir = os.path.dirname(os.path.abspath(__file__)) + "\credentials\credentials.cred"
    if not login:
        login = set.set_creds()
    client = upload.Client(login[0], login[1], cred_dir)

    print(args.image)
    if args.image:
        upload.SingleFile(client, args.image)
    elif args.album:
        upload.Album(client, args.album)
    else:
        print("No commands input.\n[-h] [-help] for a list of commands.")


if __name__ == "__main__":
    main()
