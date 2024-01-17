# Enderbyte Programs Internal Libraries

This is a set of libraries used by Enderbyte Programs software. These libraries will be re-used.

The public is welcome to use this if you find it useful

## Files Index

epadvertisements	Enderbyte Programs Advertisement. Get and show enderbyte programs advertisements

epappdata		A class of JSON-based appdata, read and write included

epdoc			Reader for Enderbyte Programs Documentation format

epprodkey		Generation and verification of Enderbyte Programs style product keys

pngdim			Calculate PNG dimensions without PIL

# Documentation

## epadvertisements

### Variables

POST_MESSAGE		A message shown after the advertisement. Meant to be set to "buy x to remove"

ADLIB_BASE		The link to the advertisement list in plaintext

ADS			A list of advertisements

### gen_adverts(message="")

message (str, optional): The POST_MESSAGE you want

gen_adverts sends a request to the adlib, downloads the ads and populates the ADS list.

### class Advertisement(url,msg)

url is the url associated with the ad

msg is the message shown to the user (the ad content).

Advertisement class controls advertisements. You propbably won't have to run the init yourself, as gen_adverts do it for you

**show(stdscr)**

stdscr is a curses window object.

Shows a cursesplus pop up with the associated ad

**public variables**

url,msg

## epappdata

### Variables

WINDOWS		If the user is on a Microsoft Windows Operating system

APP_NAME	The name of your app

### register_app_name(name)

name (str) is the name of your app. IT MUST BE CALLED BEFORE INITIALIZING AN APP DATA FILE as it will be used to choose a path for your app data

### class AppDataFile

This class behaves like a dictionary except with read and write options to commit to a disk

**init(name)**

name is the name of the individual file. name is defaulted to data

Initialize a new App Data File. A directory is chosen and created at this stage.

**setdefault(data)**

data is a dictionary. It sets what default data should be used if the current data is empty or corrupt.

**load** 

Returns dictionary

Loads the data from the file path if it exists and returns it as a dictionary. The internal dictionary is also populated. The user is free to use the AppDataFile. THIS MUST BE CALLED BEFORE WRITING!

**update(data:dict)**

The internal dictionary within the ApPDatFile object is completely replaced with data

**write**

Write app data to the disk

** The functions __getitem__, keys, values, items, and __setitem__ function like a dictionary and thus, require no documentation**

***VARIABLES***

path		The file path

default		Default data

data		Internal dictionary

## epdoc

### Variables

(none)

### class EPDocFile

An object for Enderbyte Programs Documentation Files

***VARIABLES***

textblocks	Raw blocks of text based on chapter

text		Raw data from file

name		The application name

**init(filetext,programname)**

filetext is the raw text of the documentation

programname is the application name

*Warning, you should not be calling this directly. Use `load_from_text` or `load_from_file` on the module level*

**load**

Must be called. Processes the data and generates chapters

**read_from_name(stdscr,block_name)**

Show the text in cursesplus textview based on a provided name

stdscr is a curses window object

block_name is the chapter name you wish to see

**read_from_index(stdscr,index)**

Show the text in cursesplus textview based on an index

stdscr is a curses window object

index is the index you wish to read

**show_documentation(stdscr)**

Interactively show the documentation

stdscr is a curses window object

### load_from_text(text,name)

Wrapper to EPDocFile.__init__

### load_from_file(file,name)

Read the file and return an EPDocFile. Set program name to `name`

## epprodkey

### Variables

DATA	The list of valid product keys

### class ProductKey

Data storage class for a product key

**init(s)**

S is the string representation of the key

***VARIABLES***

s	String representation of the key
hex	SHA512 representation

### generate_product_key

Generate and return a ProductKey

### load_data(url)

Load a key list from the url

### check(inputs:str)

returns boolean

Check if the provided raw string is a valid key

## pngdim

### is_png_image(data in bytes)

Check if the provided bytes are a valid PNG image

### class PNGImage

**__init__(data)**

Load PNG images based on byte data

***VARIABLES***

data	Raw data

width	Image Width

height	Image Height

**is_valid_minecraft_server_image**

Checks if image is a valid minecraft icon (64x64)

### load(file)

Load the path provided and return a PNGImage
