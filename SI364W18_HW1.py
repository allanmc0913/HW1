## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

#I worked alone on this project.  I referred to the requests library for documentation to make REST API calls (http://docs.python-requests.org/en/master/)
#I referred to discussion and class code for help with form actions and methods (GET, POST)
#For Problem 4, I used the OMDB API documentation (http://www.omdbapi.com) for help making calls to their movie/tv database
#I used Stack Overflow to see how to check if a checkbox is checked in Flask (https://stackoverflow.com/questions/20941539/how-to-get-if-checkbox-is-checked-on-flask)


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def welcome():
    return '<h1>Welcome to SI364!</h1>'



## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }
## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!
@app.route('/movie/<moviename>')
def movie_data(moviename):
    r = requests.get('https://itunes.apple.com/search?term=' + moviename + '&media=movie')
    obj = r.json()
    return '<div>{}</div>'.format(obj)



## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
@app.route('/question')
def fav_num():
    s = """<!DOCTYPE html>
    <html>
    <body>
    <form action="/result" method="get">
      Enter your favorite number:<br>
      <input type="text" name="fav">
      <br>
      <input type="submit" value="Submit">
    </form>
    </body>
    </html>"""
    return s

@app.route('/result', methods = ['POST', 'GET'])
def display_data():
    if request.method == 'GET':
        twicenum = int(request.args.get('fav')) * 2

        return '<h1>Double your favorite number is {}.</h1>'.format(str(twicenum))



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.


@app.route('/problem4form')
def form_exchange():
    s = """<!DOCTYPE html>
    <html>
    <body>
    <h1>Movie/TV Show Search</h1>
    <form action="/problem4form" method="post">
      <div>
        <h2>Enter a title to search:</h2>
        <input type="text" name="title" id="title">
      </div>
      <div>
        <h2>Specify Type:</h2>
        
        <label for="tv">
            <input type="checkbox" name="tv" id="tv" value="tv">TV Show
        </label>
        <label for="movie">
            <input type="checkbox" name="movie" id="movie" value="movie">Movie
        </label>
      </div>
      <div>
        <h2>Plot Length:</h2>
        
        <label for="short">
            <input type="checkbox" name="short" id="short" value="short">Short
        </label>
        <label for="full">
            <input type="checkbox" name="full" id="full" value="full">Full
        </label>
      </div>
      
      <br>
      <input type="submit" value="Submit">
    </form>
    </body>
    </html>"""
    return s
@app.route('/problem4form', methods = ['POST', 'GET'])
def display_omdb():
    if request.method == 'POST':
        base_url="http://www.omdbapi.com/?apikey=ceb2160f&"
        if len(request.form.getlist('tv')) != 0:
            if len(request.form.getlist('short')) != 0:
                new_url = base_url + "t=" + request.form['title'] + "&type=series&plot=short"
            else:
                new_url = base_url + "t=" + request.form['title'] + "&type=series&plot=full"
        if len(request.form.getlist('movie')) != 0:
            if len(request.form.getlist('short')) != 0:
                new_url = base_url + "t=" + request.form['title'] + "&type=movie&plot=short"
            else:
                new_url = base_url + "t=" + request.form['title'] + "&type=movie&plot=full"


        r = requests.get(new_url)
        obj = r.json()
        try:
            title = request.form['title']
            actors = obj['Actors']
            genre = obj['Genre']
            plot = obj['Plot']
            awards = obj['Awards']

        except:
            pass

        return '<h1>Summary for {}</h1>' \
               '<br>' \
               '<div><strong>Actors</strong>: {}</div>' \
               '<div><strong>Plot</strong>: {}</div>' \
               '<div><strong>Genre</strong>: {}</div>' \
               '<div><strong>Awards</strong>: {}</div>'.format(title, actors, plot, genre, awards)


if __name__ == '__main__':
    app.run()
