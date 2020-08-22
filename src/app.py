from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
#pasamos la configuracion de donde esta la base de datos
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root@localhost/flaskmysql'
#configuracion por defecto para q no me pase un warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
#instancia a la base de datos
db=SQLAlchemy(app)
# para realizar el esquema usamos una instancia de marshmallow
ma= Marshmallow(app)
#creamos un task que viene desde la base de datos creamos la tabla
class Task (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60),unique=True)    
    description = db.Column(db.String(120))

    def __init__(self, titulo ,descripcion):
        self.title = titulo
        self.description = descripcion

#despues de definir nuestra base de datos lo creamos las tablas atraves del metodo create_all
db.create_all()

class TaskEschema(ma.Schema):
    class Meta:
        fields = ('id', 'title' ,'description')
task_schema = TaskEschema()
tasks_schema = TaskEschema(many = True)

@app.route('/task', methods = ['POST'])
def create_task():
#para recibir los datos que viene del cliente
    title = request.json['title']
    description = request.json['description']
#creamos la tares
    new_task = Task(title,description)
#ahora guardo mi esquema new_task  a mi base de datos
    db.session.add(new_task)
    db.session.commit()
# mostramos al cliente que guardo en su base de datos
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods = ['GET'])
def get_tasks():
#devuelve todas las tares y lo guardo
    all_tasks = Task.query.all()
#para consultar los tasks  utilizo tasks  esquemna, retorno una lista de los esquemas
    result = tasks_schema.dump(all_tasks)
#lo visualizo en formato json
    return jsonify(result)

@app.route('/tasks/<id>', methods = ['GET'])
def get_task(id):
#consulto el esquema que tenga el id pasado por ruta
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods = ['PUT'])
def update_task(id):
#consulto el esquema que tenga el id pasado por ruta
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']
    
    task.title = title
    task.description = description
    
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods = ['DELETE'])
def delete_task(id):
#consulto el esquema que tenga el id pasado por ruta
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)
#esto se tiene que borrar
if __name__ =='__main__':
    app.run(debug=True)