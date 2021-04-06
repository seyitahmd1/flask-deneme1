from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask.helpers import url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////Users/Seyit/Desktop/Python/ToDo/todo.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    todos= ToDo.query.all()
    return render_template("index.html",todos=todos)

@app.route('/add',methods=["POST"])
def addTodo():
    title=request.form.get("title")
    newTodo=ToDo(title=title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/complete/<string:id>')
def completeTodo(id):
    todo =ToDo.query.filter_by(id=id).first()
    if todo.complete==True:
        todo.complete=False
    else:
        todo.complete=True
    db.session.commit()

    return redirect(url_for("index"))

@app.route('/delete/<string:id>')
def deleteTodo(id):
    todo= ToDo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ =="__main__":
    db.create_all()
    app.run(debug=True)