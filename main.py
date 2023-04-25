from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello_world():
  return render_template('home.html')

@app.route("/calculate", methods=["POST"])
def calculate():
  weight = float(request.form['weight'])
  height = float(request.form['height'])
  bmi = weight / (height**2)
  return render_template("result.html", bmi=bmi)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
