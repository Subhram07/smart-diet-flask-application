from flask import Flask, render_template, request
from replit import db

app = Flask(__name__)


@app.route("/")
def hello_world():
  return render_template('home.html')


@app.route("/calculate", methods=["POST"])
def calculate():
  global bmi
  global name
  global age
  global bmr
  name = request.form.get('full_name')
  age = request.form.get('age')
  weight = request.form.get('weight')
  height = request.form.get('height')
  db['name'] = name
  db['age'] = age
  #print(name)
  #print(age)

  # Check if weight and height are provided and are valid numeric values
  if not weight or not height or not age:
    return render_template('error.html',
                           message="Please provide both weight and height.")
  try:
    name = str(name)
    age = int(age)
    weight = float(weight)
    height = float(height)

  except ValueError:
    return render_template(
      'error.html',
      message="Invalid weight or height value. Please enter a valid number.")

  # Check if weight and height values are within reasonable range
  if weight <= 0 or age <= 0 or age >= 150 or height <= 0 or height >= 4:
    return render_template(
      'error.html',
      message="Invalid weight or height value. Please enter??? a valid number."
    )
  else:
    bmi = weight / (height**2)
    bmi = round(bmi, 1)
    bmr = (10 * weight) + (100 * height * 6.25) - (5 * age) + 5
    bmr = round(bmr)
    db['list_entry'] = [name, age, bmi]
    
    return render_template("transition.html", bmi=bmi , bmr=bmr)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
