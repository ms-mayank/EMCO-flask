from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///EMCO.db"

db = SQLAlchemy(app)

class Emco(db.Model):
  sno = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(200), nullable = False)
  company_name = db.Column(db.String(200), nullable = False)
  linkedin = db.Column(db.String(200), nullable = False)
  email = db.Column(db.String(200), nullable = False)
  phone = db.Column(db.String(200), nullable = False)

  def __repr__(self):
    return f"{self.name}-{self.company_name}-{self.linkedin}-{self.email}-{self.phone}"

with app.app_context():
  db.create_all()


@app.route('/', methods=["GET","POST"])
def create():
  if request.method == "POST":
    name = request.form['name']
    company_name = request.form['company_name']
    linkedin = request.form['linkedin']
    email = request.form['email']
    phone = request.form['phone']
    data = Emco(name=name, company_name=company_name, linkedin=linkedin,email=email,phone=phone)
    db.session.add(data)
    db.session.commit()
  dataall=Emco.query.all()
  return render_template("index.html",dataall=dataall)

@app.route("/delete/<int:sno>")
def delete(sno):
  data = Emco.query.filter_by(sno=sno).first()
  db.session.delete(data)
  db.session.commit()
  return redirect("/")

@app.route("/update/<int:sno>", methods=["GET","POST"])
def update(sno):
  if request.method == "POST":
    name = request.form['name']
    company_name = request.form['company_name']
    linkedin = request.form['linkedin']
    email = request.form['email']
    phone = request.form['phone']
    data = Emco.query.filter_by(sno=sno).first()
    data.name = name
    data.company_name = company_name
    data.linkedin =linkedin
    data.email = email
    data.phone = phone
    db.session.add(data)
    db.session.commit()
    return redirect('/')
  data = Emco.query.filter_by(sno=sno).first()
  print(data.name)
  return render_template("update.html",data=data)


