import os
import json
try:
    from flask import Flask, render_template, url_for, request
except:
    os.system('pip install flask')

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def HandlessApp():
    return render_template('HandlessApp.html')

@app.route('/getAcoes', methods=['POST'])
def acoes():
    try:
        with open('./static/default/configActions.json', 'r') as f:
            dados = json.load(f)

        response = []
        for i in dados:
            for j in range(len(i[0])):
                if i[0][j][0] == 'dist':
                    if i[0][j][1] == [158, 145]:
                        i[0][j] = 'piscouEsquerdo'
                    elif i[0][j][1] == [385, 374]:
                        i[0][j] = 'piscouDireito'
                elif i[0][j][0] == 'distY':
                    if i[0][j][1] == [65, 168]:
                        i[0][j] = 'ergueuSombrancelhaEsquerda'
                    elif i[0][j][1] == [282, 168]:
                        i[0][j] = 'ergueuSombrancelhaDireita'
                    elif i[0][j][1] == [13, 14]:
                        i[0][j] = 'abriuBoca'
                elif i[0][j][0] == 'distX':
                    if i[0][j][1] == [61, 2]:
                        i[0][j] = 'esticouBocaEsquerdo'
                    elif i[0][j][1] == [291, 2]:
                        i[0][j] = 'esticouBocaDireito'
            response.append(i)

        return json.dumps(response)
    except:
        return '{"result":"config. not found"}'


@app.route('/setAcoes', methods=['POST'])
def setacoes():
    try:
        with open('./static/default/configActions.json', 'w') as f:
            data = request.get_json(force=True)
            dataobj = data['objSave']
            for i in range(len(dataobj)):
                for j in range(len(dataobj[i][0])):
                    if dataobj[i][0][j] == 'piscouEsquerdo':
                        dataobj[i][0][j] = ['dist', [158, 145]]
                    elif dataobj[i][0][j] == 'piscouDireito':
                        dataobj[i][0][j] = ['dist', [385, 374]]
                    elif dataobj[i][0][j] == 'ergueuSombrancelhaEsquerda':
                        dataobj[i][0][j] = ['distY', [65, 168]]
                    elif dataobj[i][0][j] == 'ergueuSombrancelhaDireita':
                        dataobj[i][0][j] = ['distY', [282, 168]]
                    elif dataobj[i][0][j] == 'abriuBoca':
                        dataobj[i][0][j] = ['distY', [13, 14]]
                    elif dataobj[i][0][j] == 'esticouBocaEsquerdo':
                        dataobj[i][0][j] = ['distX', [61, 2]]
                    elif dataobj[i][0][j] == 'esticouBocaDireito':
                        dataobj[i][0][j] = ['distX', [291, 2]]

            f.write(json.dumps(dataobj))
            try:
                with open('./static/default/configRun.json', 'r+') as a:
                    cnf = json.load(a)
                    cnf['atualiza'] = 1
                    a.seek(0)
                    a.truncate(0)
                    a.write(json.dumps(cnf))
            except:
                with open('./static/default/configRun.json', 'w') as a:
                    a.write('{"atualiza": 1, "calibra": 0, "mouseControl": 1, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":0}')

            return '{"result":"ok"}'
    except Exception as e:
        return f'{"result":"error", "error":"{e}"}'

@app.route('/calibra', methods=['POST'])
def calibra():
    try:
        with open('./static/default/configRun.json', 'r+') as a:
            cnf = json.load(a)
            cnf['calibra'] = 1
            a.seek(0)
            a.truncate(0)
            a.write(json.dumps(cnf))
    except:
        with open('./static/default/configRun.json', 'w') as a:
            a.write('{"atualiza": 0, "calibra": 1, "mouseControl": 1, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":0}')

    return '{"status":"ok"}'

@app.route('/calibramouse', methods=['POST'])
def calibramouse():
    try:
        with open('./static/default/configRun.json', 'r+') as a:
            cnf = json.load(a)
            cnf['mouseCalibra'] = 1
            a.seek(0)
            a.truncate(0)
            a.write(json.dumps(cnf))
    except Exception as e:
        with open('./static/default/configRun.json', 'w') as a:
            a.write('{"atualiza": 0, "calibra": 0, "mouseControl": 1, "mouseCalibra": 1, "modoMouse": 1, "paraPrograma":0}')
    return '{"status":"ok"}'

@app.route('/controlemouse', methods=['POST'])
def controlemouse():
    data = 1 if request.data == b'true' else 0
    try:
        with open('./static/default/configRun.json', 'r+') as a:
            cnf = json.load(a)
            cnf['mouseControl'] = data
            a.seek(0)
            a.truncate(0)
            a.write(json.dumps(cnf))
    except:
        with open('./static/default/configRun.json', 'w') as a:
            a.write(f'{{"atualiza": 0, "calibra": 0, "mouseControl": {data}, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":0}}')
    return '{"status":"ok"}'

@app.route('/getcontrolemouse', methods=['POST'])
def getcontrolemouse():
    try:
        with open('./static/default/configRun.json', 'r+') as a:
            cnf = json.load(a)
            ctrlmouse = cnf['mouseControl']
    except:
        with open('./static/default/configRun.json', 'w') as a:
            a.write(f'{{"atualiza": 0, "calibra": 0, "mouseControl": 1, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":0}}')
            ctrlmouse = 1
    return f'{{"result":{ctrlmouse}}}'

@app.route('/paraprograma', methods=['POST'])
def paraprograma():
    try:
        with open('./static/default/configRun.json', 'r+') as a:
            cnf = json.load(a)
            cnf['paraPrograma'] = 1
            a.seek(0)
            a.truncate(0)
            a.write(json.dumps(cnf))
    except:
        with open('./static/default/configRun.json', 'w') as a:
            a.write('{"atualiza": 0, "calibra": 0, "mouseControl": 0, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":1}')
    return '{"status":"ok"}'

app.run(host='localhost', port=8989)