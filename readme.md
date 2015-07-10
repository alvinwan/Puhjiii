#Puhjiii
Puhjiii is a lightweight content management system. Get it setup on your local system and even for production use in just a matter of seconds. Made with 100% [Alvin Wan](http://alvinwan.com).

##Why Puhjiii?
Puhjiii was designed to make developers' lives easier; easily add HTML statics, and Puhjiii will give users ample control through a UI. In this way, clients can edit the page's content without touching a single line of code. Even better, developers can port statics into a CMS, without touching a single line of code.

With simple customizations -- doable by both developers and clients -- the website can also be transformed into a fully-fledged blogging platform. Common elements across pages can be synchronized, and with a few more plugins, clients can add comments, statistics and more.

Now, Puhjiii is a lightweight CMS. Truth be told, it's not built to be extensive and all-encompassing. On the same note, dragging-and-dropping files to make a deployable CMS is pretty exciting.

##Who is Puhjiii For?

Despite having a slightly technical installation process, this program is written for freelance web designers and programmers alike. More specifically, it's written for designers that dislike converting statics into workable CMS themes. More importantly, it's designed for users that enjoy an immediate connection with what they're creating, meaning simple click-to-edit and drag-and-drop editing interfaces. With that in mind, I hoped to make this guide and the program's use as clear as possible.

##Installation

###Short Version

1. Clone this repository and switch into the directory `git clone git@github.com:alvinwan/Puhjiii.git && cd puhjiii`.
2. Check that Python3 and MongoDB are installed `source check.sh`. If either is missing, see [Python3 Downloads](https://www.python.org/downloads/) or [Mongodb Official Guides](http://docs.mongodb.org/manual/installation/#installation-guides).
3. Run the installation `source install.sh`.

See "Getting Started" to launch the application.

###Long Version
In case something goes wrong, attempt these steps one by one.

1. Clone this repository `git clone git@github.com:alvinwan/Puhjiii.git`.
2. Change into the directory `cd puhjiii`.
3. Setup a new virtual environment: `python3 -m venv env`.
4. Start the virtual environment: `source env/bin/activate`.
5. Create a new directory for the datastore `mkdir env/db`.
6. Install all requirements `pip install -r requirements.txt`.
7. Build default settings `python3 setup.py build`.
8. Installation is complete.

## Getting Started

###Short Version

1. To start server, use `source activate.sh`.

Point your browser to http://localhost:5000, and your local installation of Puhjiii is now running. When finished, use `CTRL+C`.

> Optionally, run `env/bin/py.test tests` to ensure that the system works as promised.

###Long Version

1. Launch the server daemon `mongod --dbpath env/db &`.
2. Launch the server itself `env/bin/python run.py`.

Point your browser to http://localhost:5000. When finished, hit `CTRL+C`, and stop mongodb using `mongo 127.0.0.1/admin --eval "db.shutdownServer()"`.

##Puhjiii Features
Here are existing features, packed into this tiny program:

###Editing Webpages
+ upload and import new templates
+ click anywhere on rendered page to edit content
+ access the code directly, when needed

###Website Management
+ add a new "mold" for a new type of content (e.g., "mold" for all posts)
+ add a specific item for a "mold" (e.g., a post)
+ add pages based on existing or new templates with a custom URL
+ login and register users
+ install plugins to enhance functionality

##More

Here is the [chubby bird](http://drbl.in/oRxN) that started it all.

##Developers
This section covers relevant code information and is written to address a technically-adept audience.

###Plugin Development
Each plugin is composed of the following:

```
plugins/
    (req) __init__.py : plugin description, adopted directory name, list of all permissions checked
    (opt) forms.py : all forms, using WTForms (optional)
    (opt) libs.py : all classes needed for plugin functionality
    (opt) models.py : all models, using MongoEngine
    (opt) views.py : all views, using Flask and Werkzeug
    (req) [component].py : generates context for a specific Nest panel

templates/
    (req) [component].html : template for Nest panel
```

Plugins may add views to one of three [Flask Blueprints](http://flask.pocoo.org/docs/0.10/blueprints/): public, nest, or auth. To build the admin panel, Puhjiii uses a Nest object. You can load a plugin panel using nest.load_plugin('[plugin].[component]').

- All views should contain a permission_required decorator, imported from server.views which requires the most general plugin permission, named 'access_[plugin]'.
- Each plugin component should then specify the permission required using requires = ['list', 'of', 'permissions']

###Theme Development
Themes can be easily imported from static files; the following covers the basics of writing, importing and customizing themes.

**To prepare** a new Puhjiii-ready theme, simply compress all *files and required directories* into one zip. Do not compress the parent folder. This zip can then distributed and easily imported.

**To import** a new theme, follow these steps, and the said zip -- with all assets and templates -- will be divided, parsed, and saved accordingly.

1. Login at http://your_server_ip/login.
2. Click "Code".
3. Click "Upload".

> "Import" is for individual templates that already prepend relative paths (images, stylesheets, scripts etc.) with /static/public/[destination]. If your local directory, for example, has about.html which includes styles/site.css and you specify a destination "Site" during upload, the full path to the stylesheet would become /static/public/Site/style/site.css.

**To customize** a theme, use all and any of Jinja2-flavored templating. All variable statements -- on top of all other content -- will be made editable through the UI, and other statements will be left as-is.

###Current Development

Puhjiii took just over two weeks to build, but I will most likely not continue maintaining this project. The chubby program is ripe with features, or at least filled with *enough* features that it's achieved its purpose : ameliorate a web designer's pain and still give clients a (disputably) pretty UI. If you are interested in picking up this project, feel free to contact me at hi(at)alvinwan.com.
