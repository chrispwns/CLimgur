import os
import sys
from requests import exceptions
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

"""
    Need to add a way to store client id and secret to separate (encrypted?) file.

    MUST
    initialize the client in a class or it runs auto
"""


class Client():

    def __init__(self, client_id, client_secret, cred_dir):
        self.supported_types = [".jpg", ".jpeg", ".png", ".apng", ".tiff", ".pdf", ".xcf"]

        try:
            self.client = ImgurClient(client_id, client_secret)
        except ImgurClientError:
            print("Invalid ID or Secret.")
            os.remove(cred_dir)
            sys.exit(0)


class SingleFile(Client):
    """ Upload a single file to imgur if it exists. """
    def __init__(self, client, path_to_file):
        super(Client, self).__init__()
        client = client.client
        try:
            f = open(path_to_file)
            f.close()
            print("uploading " + path_to_file)
            url = client.upload_from_path(path_to_file, anon=True)
            print("\nFile uploaded at: " + url['link'])

        except FileNotFoundError:
            print("File not found. Check that the file exists.")
        except PermissionError:
            print("Permission Denied, check that you have sufficient privilege to access the folder.")
        except exceptions as e:
            print(e)


class Album(Client):
    """ Upload all supported files in a folder to an album"""
    def __init__(self, client, album_dir):
        super(Client, self).__init__()
        self.client = client.client
        self.supported_types = client.supported_types
        self.album_dir = album_dir
        self.album = self.client.create_album(fields={'title': 'bot test'})
        self.config = {'album': self.album['deletehash']}
        self.upload()

    def upload(self):
        """
        Upload all images in folder to imgur album if they exist
            and are a supported file type
        """
        try:
            list_of_files = [file for file in os.listdir(self.album_dir)]

            for i in range(len(list_of_files)):
                file = self.album_dir + "/" + list_of_files[i] # create full path of file
                for j in range(len(self.supported_types)):
                    if self.supported_types[j] in file:
                        self.percent_display(i, len(list_of_files))
                        file_too_large = Utilities.max_size(file)
                        if not file_too_large:
                            self.client.upload_from_path(file, config=self.config, anon=True)
            self.percent_display(1, 1)  # upload is 100%
            print("\nAlbum uploaded at: http://www.imgur.com/a/" + self.album['id'])

        except (FileNotFoundError, PermissionError):
            if FileNotFoundError:
                print(print("Directory not found. Check that Directory exists"))
            else:
                print("Permission Denied, check that you have sufficient privilege to access the folder.")
        except ImgurClientError as e:
            print(e.error_message)
            print(e.status_code)

    @staticmethod
    def percent_display(current_index, max_index):
        """
        Calculate and display a percentage in the terminal
        :param current_index: Current file index.
        :param max_index: Number of files in directory.
        :return: current_index Incremented
        """
        percent = (current_index / max_index) * 100
        # write percent to output stream and push it to terminal
        sys.stdout.write("\r[Uploading: %d%%" % percent + "] ")
        sys.stdout.flush()

    def warn_too_many_files(self):
        """ Warn the user about albums larger than 50 images """


class Utilities():
    @staticmethod
    def max_size(file):
        """
        Determines whether a file is too large to be uploaded to imgur.
        :param file:
        :return: True if too large/False is not too large
        """
        max_static_size = 20000000  # 20Mb. Max size for standard "static" file formats
        max_anim_size = 200000000  # 200Mb. Max size for animated file formats
        file_size = os.stat(file).st_size

        if (".gif" in file or ".apng" in file) and file_size >= max_anim_size:
            sys.stdout.write(str(" " + file + " exceeds the 200mb limit for '.gif' and '.apng' files. Skipping"))
            sys.stdout.flush()
            return True
        elif file_size >= max_static_size:
            sys.stdout.write(str(" " + file + " exceeds the 20mb limit for non-animated files. Skipping"))
            sys.stdout.flush()
            return True
        else:
            return False
