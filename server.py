from inspect import signature
import os, socket, shutil
import webbrowser
from os import remove
from typing import Counter
from flask import Flask, render_template, request, send_file
from flask_caching import Cache
from werkzeug.utils import secure_filename, redirect
from tqdm.auto import tqdm


Counter = 0
Signal = False

nombre_equipo = socket.gethostname()
a = str(socket.gethostbyname(socket.gethostname()))

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)
#'C:/Users/Greg707/Documents/- proyectos/Servidor Python/Disco/'
app.config["UPLOAD_FOLDER"] = "../Servidor Python/Disco/"
FILE_DISC = app.config["UPLOAD_FOLDER"]
status = 50

def carge_bar(filename):
    sizefile = os.stat("./Disco/"+filename).st_size
    j = sizefile
    print(f"archivo: {filename}"+f" Peso: {sizefile}")
    for i in tqdm(range(j)):
        status = i
        print(end='\r')

    

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    # os.system(r'rundll32.exe powrprof.dll,SetSuspendState Hibernate')

@app.route('/')
def mostrar_cont():
    if Counter > 0:
        Signal = True
    else:
        Signal = False
    dir = FILE_DISC

    with os.scandir(dir) as ficheros:
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
    return render_template('server.html',ficheros=ficheros, signal_changes = Signal, status = status)

@app.route("/upload", methods=["POST"])
def uploader():
    if request.method == "POST":
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        Counter + 1
        carge_bar(filename)
        
    return redirect('/')

@app.route('/download_file/<filename>')
def return_files_tut(filename):
    file_path = FILE_DISC + filename
    print(file_path)
    mostrar_cont()
    return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/remove_file/<filename>')
def remove_file(filename):
    file_path = FILE_DISC + filename
    print(file_path)
    try:
        remove(file_path)
        Counter + 1
    except:
        print("no hay archivo")
    return redirect('/')

@app.route('/apagar')
def apagar():
    cache.delete_memoized(mostrar_cont)
    shutdown_server()
    return redirect('/')

if __name__ == '__main__':
    # webbrowser.open_new_tab("http://"+a+":8000")
    app.run(debug=False, host="192.168.193.133", port="8000")
    