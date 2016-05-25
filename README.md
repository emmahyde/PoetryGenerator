# Poetry Generator
### Amy D'Entremont and Emma Hyde
###### Under Dr. Hava Siegelmann

### Installation

In order to get the poetry generator to run, you need Python 3.
Using bash shell with Python 3, navigate to the download directory and enter `python3 generator.py`. 
This will generate a poem from the ASCII input (default `input.txt` is Electric Kool Aid Acid Test, found in the same directory. This can be changed to any book-length input).
This task takes between 15 seconds and 10 minutes depending on your CPU power and the length of the input.

**PLEASE NOTE:** the generator cannot handle non-ASCII symbols or pound signs. Please replace all of these with spaces before attempting to use it.

### Use

The generator contains a main method that calls `file = open('input.txt', 'r+')`. This by default opens the program named `input.txt`. If you would like to use various inputs named different things, you would modify this line of the generator. It is found in `generator.py` on line 349.

### Flask Server Implementation

Using the `app.py` file, you can modify the generator to be controlled by a `HTTP GET` and `POST` method.
This will require Flask to be fully installed on your machine or server.
The `app.py` should be run as the main method, which will imports and calls the `generator.py` functions themselves. 
The flask server utilizes the `templates` folder in order to render the HTML, and then returns the poem as an HTML output with the name of the input file.
In order to deploy this application to a server, [use a coded flask deployment](http://flask.pocoo.org/docs/0.10/deploying/). It is possible to host it using another flask hosting option (Google apps, etc.), but some deployment methods (e.g. Heroku) have a timeout limit and are not able to host this application as the return method takes quite long to return.

**PLEASE NOTE:** The ability of the server to run this as a threaded application may require some modification, but this implementation functions fully on a local server with one user.

### Report

The report describes the history of the poetry generator, the various forms our generator went through, future concepts and a general observational piece on if computers can truly produce art.