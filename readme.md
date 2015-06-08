#Puhjee
Puhjee is a lightweight content management system. Get it setup on your local system and even for production use in just a matter of seconds.

##Why Puhjee?
Puhjee was designed to make developers' lives easier; drag-and-drop in HTML statics, and Puhjee will automatically allow users to customize content through a UI. In this way, clients can edit the page's content without touching a single line of code. Even better, developers can port statics into a CMS, without touching a single line of code.

With simple customizations -- doable by both developers and clients -- the website can also be transformed into a fully-fledged blogging platform. Common elements across pages can be synchronized, and with a few more plugins, clients can add comments, statistics and more.

Now, Puhjee is an *extremely* lightweight CMS. Truth be told, it's not built to be extensive and all-encompassing. On the same note, dragging-and-dropping files to make a deployable CMS is pretty exciting.

##Installation
1. Clone this repository.
2. Setup a virtualenv named `env` using `virtualenv env -p python3`.
3. Launch the virtualenv `source env/bin/activate`.
4. Install all requirements `pip install -r requirements.txt`.
5. Create a new directory for the datastore `mkdir env/db`.
6. Launch the server daemon `mongod --dbpath env/db`.
7. In a new console, launch the server itself `env/bin/python run.py`.

> To ensure that the system works as promised, run tests using `env/bin/py.test tests`.

##Puhjee Features
Here are existing features, packed into this tiny program:

Editing Statics
- drag-and-drop files in, to add to the website
- click anywhere on rendered page to edit content
- drag-and-drop to rearrange elements on page
- copy-and-paste or delete elements
- convert elements into repeatable templates (e.g., post, header, footer)
+ access the code directly, when needed

Website Management
+ add pages and additional users, based on existing or new templates
+ login and register users
+ install plugins to enhance functionality