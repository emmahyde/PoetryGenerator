
from werkzeug import secure_filename
from flask import Flask, request, render_template
from flask_bootstrap3 import Bootstrap

from generator import *


def create_app():
    app = Flask(__name__)
    Bootstrap(app)

    return app

app = create_app()

# UPLOAD_FOLDER = '/Users/Emma/flaskproject/uploads'
ALLOWED_EXTENSIONS = set(['txt'])



# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")


def processing(filename):

    raw_text = open(filename, 'r').read()
    text = Text(raw_text) # seperates words into POS buckets
    grammar = Grammar() # makes CFG

    frame = Frame(grammar,text.tags) # create "frame" of poem: list of lists of POS tags
    frame.add_collocations(text)
    frame.add_big_words(text)
    frame.repeat_nouns()
    for x in range(3):
        frame.add_context_words(text)
    frame.add_first_unfilled(text)
    frame.repeat_nouns()
    frame.add_context_words(text)
    frame.fill_remaining(text)

    # POST METHOD FOR @app.route('/', methods=['POST'])
    # Convert frame.print() to HTML friendly string to be returned to browser
    # replace line breaks with <br>
    # Capitalize first letter of line, lowercase all others (for now)

    poem = ""
    for line in frame.lines:
        first = True
        for word in line:
            if (first):
                poem = poem + word.word.lower().title() + " "
                first = False
            else:
                poem = poem + word.word.lower() + " "
        poem = poem + ' <br> '

    return poem


@app.route('/poem', methods=['GET', 'POST'])
def return_poem():
    if request.method == 'POST':
        print("POSTED.")
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("PROCESSING")
            poem = processing(filename)


            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # url_path = redirect(url_for('uploaded_file', filename=filename))
            # a = 'file uploaded'
            #     "Read file and parse the values into an array?"
            #     "Pass arguments to a Processing function and outputs result into generator)"


            return "<p>Generated from " + filename + ": <br><br>" + poem + "</p"
        else:
            return "Not a text file. Please upload a file with extension .txt."
    else:
        return "Not a file."

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")
