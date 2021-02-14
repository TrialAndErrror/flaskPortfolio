from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('resume/home.html')


@app.route('/about')
def about():
    return render_template('resume/home/about.html')


@app.route('/projects')
def projects():
    return render_template('resume/portfolio/portfolio.html')


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
