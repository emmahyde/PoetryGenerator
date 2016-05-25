# Poetry Generator
### Amy D'Entremont and Emma Hyde
###### Under Dr. Hava Siegelmann

### Installation

In order to get the poetry generator to run, you need Python 3.
Using bash shell with Python 3, navigate to the download directory and enter `python3 generator.py`. 
This will generate a poem from the ASCII input (default `input.txt` is Electric Kool Aid Acid Test, found in the same directory. This can be changed to any book-length input).
This task takes between 15 seconds and 10 minutes depending on your CPU power and the length of the input.

PLEASE NOTE: the generator cannot handle non-ASCII symbols or pound signs. Please replace all of these with spaces before attempting to use it.

### Flask Server Implementation

Using the app.py file, you can run the main method through a Flask app.
This will require Flask to be fully installed on your machine or server.
Use the Flask default instructions to get this to function correctly. 
The ability of the server to run this as a threaded application may require some modification, but this implementation functions fully on a local server with one user.

### Report

The report describes the history of the poetry generator, the various forms our generator went through, future concepts and a general observational piece on if computers can truly produce art.