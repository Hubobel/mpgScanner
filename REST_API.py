import os
import random
from flask import Flask, jsonify

app = Flask(__name__)
fact=[]
pfad = os.path.dirname(__file__)
chuck_file= open(pfad + '/mpg/chuck.rtf','r')
for line in chuck_file:
    fact.append(line)
chuck_file.close()
ran=random.randint(1,len(fact)-1)
fakt={}
a=0
for i in fact:
    fakt[a]=i
    a  =a +1

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/facts', methods=['GET'])
def get_tasks():
    return jsonify({'facts': fakt})

@app.route('/facts/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if len(fact)-1<task_id:
        return jsonify({'error':"Auch Chuck Norris Witze sind begrenzt"})
    return jsonify({'fact': fact[task_id]})
if __name__ == '__main__':
    app.run(host='0.0.0.0')