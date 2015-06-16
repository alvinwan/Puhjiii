#Puhjiii
Puhjiii is a lightweight content management system. Get it setup on your local system and even for production use in just a matter of seconds.

##Why Puhjiii?
Puhjiii was designed to make developers' lives easier; drag-and-drop in HTML statics, and Puhjiii will automatically allow users to customize content through a UI. In this way, clients can edit the page's content without touching a single line of code. Even better, developers can port statics into a CMS, without touching a single line of code.

With simple customizations -- doable by both developers and clients -- the website can also be transformed into a fully-fledged blogging platform. Common elements across pages can be synchronized, and with a few more plugins, clients can add comments, statistics and more.

Now, Puhjiii is a lightweight CMS. Truth be told, it's not built to be extensive and all-encompassing. On the same note, dragging-and-dropping files to make a deployable CMS is pretty exciting.

##Installation

**Short Version**

1. Clone this repository and switch into the directory `git clone git@github.com:alvinwan/Puhjiii.git && cd puhjiii`.
2. Check that Python3 and MongoDB are installed `source check.sh`. If either is missing, see [Python3 Downloads](https://www.python.org/downloads/) or [Mongodb Official Guides](http://docs.mongodb.org/manual/installation/#installation-guides).
3. Run the installation `source install.sh`.

> To ensure that the system works as promised, run `env/bin/py.test tests`.

**Long Version**
In case something goes wrong, attempt these steps one by one.

1. Clone this repository `git clone git@github.com:alvinwan/Puhjiii.git`.
2. Change into the directory `cd puhjiii`.
3. Setup a new virtual environment: `python3 -m venv env`.
4. Start the virtual environment: `source env/bin/activate`.
5. Create a new directory for the datastore `mkdir env/db`.
6. Install all requirements `pip install -r requirements.txt`.
7. Build default settings `python3 setup.py build`.
8. Launch the server daemon `mongod --dbpath env/db &`.
9. Launch the server itself `env/bin/python run.py`.
10. When finished, stop mongodb using `mongo 127.0.0.1/admin --eval "db.shutdownServer()"`.

*Only steps 3, 9, and 10 are required for starting server in the future.*

## Getting Started

To start server, use `source activate.sh`. Point your browser to 'http://localhost:5000' and your local installation of Puhjiii is now running.

##Puhjiii Features
Here are existing features, packed into this tiny program:

Editing Webpages
+ upload and import new templates
+ click anywhere on rendered page to edit content
+ convert elements into repeatable items (e.g., post, comment)
+ convert elements into reusable partials (e.g., header, footer)
+ access the code directly, when needed
- drag-and-drop to rearrange elements on page
- copy-and-paste or delete elements

Website Management
+ add a new "mold" for a new type of content (e.g., "mold" for all posts)
+ add a specific item for a "mold" (e.g., a post)
+ add pages based on existing or new templates with a custom URL
+ login and register users
+ install plugins to enhance functionality

##More

For more information, see the official Puhjiii website at [braiiin.com/puhjiii](http://braiiin.com/puhjiii), and here is the [chubby bird](http://drbl.in/oRxN) that started it all.

##Developers

*Plugin Development*
Each plugin is composed of the following:

```
plugins/
    __init__.py : plugin description, adopted directory name, list of all requirements
    forms.py : all forms, using WTForms
    libs.py : all classes needed for plugin functionality
    models.py : all models, using MongoEngine
    views.py : all views, using Flask and Werkzeug
    [component].py : generates context for a specific Nest panel
    
templates/
    [component].html : template for Nest panel
```

Plugins may add views to one of three Blueprints: public, nest, or auth.