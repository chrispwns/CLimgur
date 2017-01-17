# What is CLimgur

CLimgur is a command line imgur client built to make sharing images and downloading albums faster with less hassle

CLimgur is built with Python 3.4.3


## Features

Climgur currently only supports uploading files, but downloading files is in the works.

### Requirements
Python 3.4

[imgurpython]()

and an imgur [app ID/Pass]()

# Usage

Add the CLimgur Directory to your PATH

Open CMD

invoke Climgur with the keyword

    imgur

If this is your first run you will be prompted to input an ID/Secret that you got from imgur. 
This is required to use the imgur api.


To upload a single image

    imgur -i "image/on/pc.jpg"
     


    imgur --image "image/on/pc.jpg"
    
To upload an album

    imgur -a "folder/with/images/"



    imgur --album "folder/with/images/"
