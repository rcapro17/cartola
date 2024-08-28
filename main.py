from flask import Flask, request, redirect, url_for, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

times = []
jogadores = []
times_jogadores = {}


class Time:

    def __init__(self, id_time, nome_time, foto):
        self.id_time = id_time
        self.nome_time = nome_time
        self.foto = foto


class Jogador:

    def __init__(self, id, nome, posicao, numero, id_time, foto):
        self.id = id
        self.nome = nome
        self.posicao = posicao
        self.numero = numero
        self.id_time = id_time
        self.foto = foto


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/add_time', methods=['POST', 'GET'])
def add_time():
    if request.method == 'POST':
        id_time = len(times) + 1
        nome_time = request.form['nome_time']
        foto = request.files['foto']

        if foto and allowed_file(foto.filename):
            filename = f"time_{id_time}_{foto.filename}"
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            time = Time(id_time, nome_time, filename)
            times.append(time)
            times_jogadores[id_time] = []
            return redirect(url_for('list_times'))
    return render_template('add_time.html')


@app.route('/add_jogador', methods=['POST', 'GET'])
def add_jogador():
    if request.method == 'POST':
        id = len(jogadores) + 1
        nome = request.form['nome']
        posicao = request.form['posicao']
        numero = request.form['numero']
        id_time = int(request.form['id_time'])
        foto = request.files['foto']

        if foto and allowed_file(foto.filename):
            filename = f"jogador_{id}_{foto.filename}"
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            jogador = Jogador(id, nome, posicao, numero, id_time, filename)
            jogadores.append(jogador)
            times_jogadores[id_time].append(jogador)
            return redirect(url_for('list_jogadores'))
    return render_template('add_jogador.html', times=times)


@app.route('/list_times')
def list_times():
    return render_template('list_times.html', times=times)


@app.route('/list_jogadores')
def list_jogadores():
    return render_template('list_jogadores.html', jogadores=jogadores)


@app.route('/list_jogadores_time/<int:id_time>')
def list_jogadores_time(id_time):
    jogadores_time = times_jogadores.get(id_time, [])
    time = next((time for time in times if time.id_time == id_time), None)

    if not time:
        return redirect(url_for('list_times'))

    return render_template('list_jogadores_time.html',
                           jogadores=jogadores_time,
                           time=time)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/edit_time/<int:id_time>', methods=['GET', 'POST'])
def edit_time(id_time):
    time_to_edit = next((time for time in times if time.id_time == id_time),
                        None)
    if not time_to_edit:
        return redirect(url_for('list_times'))

    if request.method == 'POST':
        time_to_edit.nome_time = request.form['nome_time']

        foto = request.files['foto']
        if foto and allowed_file(foto.filename):
            filename = f"time_{id_time}_{foto.filename}"
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            time_to_edit.foto = filename

        return redirect(url_for('list_times'))

    return render_template('edit_time.html', time=time_to_edit)


@app.route('/delete_time/<int:id_time>', methods=['POST'])
def delete_time(id_time):
    global times
    global times_jogadores

    times = [time for time in times if time.id_time != id_time]

    if id_time in times_jogadores:
        del times_jogadores[id_time]

    return redirect(url_for('list_times'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
