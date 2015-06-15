#Puhjiii
Puhjiii is a lightweight content management system. Get it setup on your local system and even for production use in just a matter of seconds.

##Why Puhjiii?
Puhjiii was designed to make developers' lives easier; drag-and-drop in HTML statics, and Puhjiii will automatically allow users to customize content through a UI. In this way, clients can edit the page's content without touching a single line of code. Even better, developers can port statics into a CMS, without touching a single line of code.

With simple customizations -- doable by both developers and clients -- the website can also be transformed into a fully-fledged blogging platform. Common elements across pages can be synchronized, and with a few more plugins, clients can add comments, statistics and more.

Now, Puhjiii is a ightweight CMS. Truth be told, it's not built to be extensive and all-encompassing. On the same note, dragging-and-dropping files to make a deployable CMS is pretty exciting.

##Installation
1. Clone this repository.
2. Setup a virtualenv named `env` using `virtualenv env -p python3`.
3. Launch the virtualenv `source env/bin/activate`.
4. Install all requirements `pip install -r requirements.txt`.
5. Create a new directory for the datastore `mkdir env/db`.
6. Launch the server daemon `mongod --dbpath env/db`.
7. In a new console, launch the server itself `env/bin/python run.py`.

> To ensure that the system works as promised, run tests using `env/bin/py.test tests`.

##Getting Started
1. Click "Tell me about you."
2. Fill out your desired administrator account information.
3. Complete information about your database; leave empty for defaults.
4. Click "Launch".
5. Setup is complete.

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

