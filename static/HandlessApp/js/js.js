var idAction = 0;
var acoesArray = [];

function handleCancelar() {
    window.location.reload();
}

function getControleMouse() {
    fetch(`${window.origin}/getcontrolemouse`, {
        method: 'POST'
    })
    .then(resp => resp.json())
    .then((result) => {
        chkBox = document.getElementById('inputControlaMouse');
        if (result.result == 1) {
            chkBox.checked = true;
        } else {
            chkBox.checked = false;
        }
    });
}

function handleCalibra() {
    fetch(`${window.origin}/calibra`, {
        method: 'POST'
    })
    .then(resp => resp.json())
    .then((result) => {
        if (result.status == 'ok') {
            alert('calibrando');
        } else {
            alert('erro');
        }
    });
}

function handleCalibraMouse() {
    fetch(`${window.origin}/calibramouse`, {
        method: 'POST'
    })
    .then(resp => resp.json())
    .then((result) => {
        if (result.status == 'ok') {
            alert('calibrando');
        } else {
            alert('erro');
        }
    });
}

function handleParaPrograma() {
    fetch(`${window.origin}/paraprograma`, {
        method: 'POST'
    })
    .then(resp => resp.json())
    .then((result) => {
        alert('parando a execução');
        window.close();
    });
}

function handleControlaMouse() {
    chkMouse = document.getElementById('inputControlaMouse').checked;

    fetch(`${window.origin}/controlemouse`, {
        method: 'POST',
        body: chkMouse.toString()
    })
    .then(resp => resp.json())
    .then((result) => {
        if (result.status == 'ok') {
            if (chkMouse) {
                alert('calibrando');
            } else {
                alert('parando o controle do mouse')
            }
        } else {
            alert('erro');
        }
    });
}

function handleCancelar() {
    window.location.reload();
}

function handleSalvar() {
    let objSave = [];
    acoesArray.forEach(element => {
        let arrayExpression = [];
        let arrayThreshold = [];
        let arrayCalibra = [];
        let arrayCompara = [];
        Object.values(element.ExprAction).forEach(Exp => {
            if (Exp.optExpressions.value == 'piscouDireito' || Exp.optExpressions.value == 'piscouEsquerdo') {
                arrayCompara.push('>');
            } else {
                arrayCompara.push('<');
            }
            arrayExpression.push(Exp.optExpressions.value);
            arrayThreshold.push(Exp.threshold.value);
            arrayCalibra.push(-1);
        });
        let acao = element.actionOpt.value;
        let params = [];
        if (acao == 'calibra') {
            acao = 'calibra';
        } else if (acao == 'moveMouse') {
            params.push(element.paramInput1.value);
            params.push(element.paramInput2.value);
        } else if (acao == 'aperte') {
            let arrElTeclas = element.apertTeclas;
            Object.values(arrElTeclas).forEach(elTec => {
                params.push(elTec.tecla.value);
            });
        } else {
            params.push(element.paramInput.value);
        }

        if (acao == 'holdDown' && element.paramCheck) {
            var segundAcao = 'release';
        }

        objSave.push([arrayExpression, arrayThreshold, acao, arrayCalibra, arrayCompara, false, 0, params, 0, segundAcao])
    });
    let prt = new aguarde();
    prt.show();

    let objFetch = {objSave}
    let send = new FormData;

    send.append("newConfig", JSON.stringify(objFetch));

    fetch(`${window.origin}/setAcoes`, {
        method: 'POST',
        body: JSON.stringify(objFetch)
    })
    .then(resp => resp.json())
    .then((result) => {
        prt.hide();
    });
}

class expressionSelectorClass {
    constructor(linhaPai, adicionaElemento, arrayConteiner, objId, expBase, thresholdBase) {
        this.id = objId;
        
        this.expBase = expBase;

        this.linha = linhaPai;
        this.arrayConteiner = arrayConteiner;

        this.celula = document.createElement('td');
        this.celula.className = 'celulaExpression';
        this.linha.insertBefore(this.celula, adicionaElemento);

        this.divExpression = document.createElement('div');
        this.divExpression.className = 'divExpression';
        this.celula.appendChild(this.divExpression);

        this.imgExpressions = document.createElement('img');
        this.imgExpressions.className = 'imgExpressions';
        this.imgExpressions.src = "/static/HandlessApp/img/face_neutra.png";
        this.divExpression.appendChild(this.imgExpressions);

        this.divThreshold = document.createElement('div');
        this.divThreshold.className = 'thresholddiv';
        this.divExpression.appendChild(this.divThreshold);

        this.thresholdText = document.createElement('p');
        this.thresholdText.className = 'textThreshold';
        this.thresholdText.innerHTML = 'Sensibilidade: ';
        this.divThreshold.appendChild(this.thresholdText);

        this.threshold = document.createElement('input');
        this.threshold.className = 'threshold';
        this.threshold.type = 'range';
        this.threshold.min = 0.1;
        this.threshold.max = 10;
        this.threshold.step = 0.05;
        this.threshold.value = 1;
        this.divThreshold.appendChild(this.threshold);

        this.optExpressions = document.createElement('select');
        this.optExpressions.className = 'optExpressions';
        this.optExpressions.name = 'optExpressions';
        this.optExpressions.innerHTML = `<select class="optExpression"true>
            <option disabled selected value=""></option>
            <option value="ergueuSombrancelhaEsquerda">Erguer a Sobrancelha Esquerda</option>
            <option value="ergueuSombrancelhaDireita">Erguer a Sobrancelha Direita</option>
            <option value="piscouEsquerdo">Piscar o Olho Esquerdo</option>
            <option value="piscouDireito">Piscar o Olho Direito</option>
            <option value="esticouBocaEsquerdo">Esticar Lado Esquerdo da Boca</option>
            <option value="esticouBocaDireito">Esticar Lado Direito da Boca</option>
            <option value="abriuBoca">Abrir a Boca</option>
        </select>`;

        this.divExpression.appendChild(this.optExpressions);

        this.expressionsDestroyer = document.createElement('div');
        this.expressionsDestroyer.className = 'destroyExpressionDiv';
        this.divExpression.appendChild(this.expressionsDestroyer);

        this.expressionsDestroyerText = document.createElement('p');
        this.expressionsDestroyerText.className = 'destroyActionText';
        this.expressionsDestroyerText.innerHTML = 'X';
        this.expressionsDestroyer.appendChild(this.expressionsDestroyerText);

        this.width = (this.optExpressions.getBoundingClientRect().right - this.optExpressions.getBoundingClientRect().left) + 30;

        this.celula.style.width = this.width+'px';

        this.optExpressions.addEventListener('change', () => {
            this.imgExpressions.src = "/static/HandlessApp/img/" + this.optExpressions.value + ".png";
        });

        this.expressionsDestroyer.addEventListener('click', () => {
            this.celula.remove();
            delete this.arrayConteiner[this.id];
        });

        if (expBase != null) {
            this.optExpressions.value = expBase;
            this.imgExpressions.src = "/static/HandlessApp/img/" + expBase + ".png";
            this.threshold.value = thresholdBase;
        }
    }
}

class teclaActionClass {
    constructor(linhaPai, adicionaElemento, arrayConteiner, objId, tecla) {
        this.id = objId;
        
        this.linha = linhaPai;
        this.arrayConteiner = arrayConteiner;
        
        this.celula = document.createElement('td');
        this.celula.className = 'celulaTecla';
        this.linha.insertBefore(this.celula, adicionaElemento);
        
        this.tecla = document.createElement('input');
        this.tecla.className = 'teclaHolder';
        this.tecla.type = 'text';
        this.celula.appendChild(this.tecla);

        this.celulaDestroyer = document.createElement('td');
        this.celulaDestroyer.className = 'celulaTeclaDestroyer';
        this.linha.insertBefore(this.celulaDestroyer, adicionaElemento);

        this.destroyer = document.createElement('p');
        this.destroyer.className = 'teclaDestroyer';
        this.destroyer.innerHTML = '−';
        this.celulaDestroyer.appendChild(this.destroyer);

        this.tecla.addEventListener('keydown', (e) => {
            e.preventDefault();
            var keynum = e.key;
            if (keynum == 'Meta') {
                keynum = 'Win';
            }
            this.tecla.value = (keynum.toLowerCase());
        });
        this.destroyer.addEventListener('click', () => {
            this.celula.remove();
            this.celulaDestroyer.remove();
            
            delete this.arrayConteiner[this.id];
        });

        if (tecla != null) {
            this.tecla.value = tecla;
        }
    }
}

class action {
    constructor(adicionaActionElemento, objBase) {
        this.id = idAction;
        idAction++;

        var tabelaAcoes = document.getElementById('tableConfig');

        this.linha = document.createElement('tr');
        tabelaAcoes.insertBefore(this.linha, adicionaActionElemento);

        this.actionHolder = document.createElement('div');
        this.actionHolder.className = 'actionHolder';

        this.actionTitle = document.createElement('div');
        this.actionTitle.className = 'actionTitle';

        this.actionHolder.appendChild(this.actionTitle);

        this.actionText = document.createElement('p');
        this.actionText.className = 'actionTitleText';
        this.actionText.innerHTML = 'Ação: ';

        this.actionTitle.appendChild(this.actionText);

        this.actionOpt = document.createElement('select');
        this.actionOpt.className = 'actionActionOpt';
        this.actionOpt.name = 'actionOpt';
        this.actionOpt.innerHTML = `<option disabled selected value=""></option>
        <option value="clica">clicar</option>
        <option value="moveMouse">mover o mouse</option>
        <option value="holdDown">segurar o botão do mouse</option>
        <option value="release">soltar o botão do mouse</option>
        <option value="abra">abrir aplicativo</option>
        <option value="pesquise">pesquisar</option>
        <option value="aperte">apertar teclas</option>
        <option value="digite">digitar texto</option>`;
        
        this.actionTitle.appendChild(this.actionOpt);

        this.destroyDiv = document.createElement('div');
        this.destroyDiv.className = 'destroyActionDiv';
        this.actionTitle.appendChild(this.destroyDiv);

        this.destroyActionText = document.createElement('p');
        this.destroyActionText.className = 'destroyActionText';
        this.destroyActionText.innerHTML = 'X';
        this.destroyDiv.appendChild(this.destroyActionText);

        var width = 0;

        this.scrollParamDiv = document.createElement('div');
        this.scrollParamDiv.className = 'scrollParamDiv';
        this.actionTitle.appendChild(this.scrollParamDiv);
        
        this.paramDiv = document.createElement('div');
        this.paramDiv.className = 'paramDiv';
        this.scrollParamDiv.appendChild(this.paramDiv);

        this.scrollExpressionDiv = document.createElement('div');
        this.scrollExpressionDiv.className = 'scrollExpressionDiv';
        this.actionTitle.appendChild(this.scrollExpressionDiv);
        
        this.actionHolder.appendChild(this.scrollExpressionDiv);

        this.actionExpressionsDiv = document.createElement('div');
        this.actionExpressionsDiv.className = 'actionExpressionsDiv';

        this.scrollExpressionDiv.appendChild(this.actionExpressionsDiv);

        this.expressionsTable = document.createElement('table');
        this.expressionsTable.className = 'expressionsTable';

        this.actionExpressionsDiv.appendChild(this.expressionsTable);

        this.linhaExpression = document.createElement('tr');
        this.expressionsTable.appendChild(this.linhaExpression);

        this.celulaAddExpression = document.createElement('td');
        this.celulaAddExpression.className = 'celulaAddExpression';
        this.linhaExpression.appendChild(this.celulaAddExpression);

        this.divAddExpression = document.createElement('div');
        this.divAddExpression.className = 'divAddExpression';
        this.celulaAddExpression.appendChild(this.divAddExpression);
        
        this.addExpression = document.createElement('p');
        this.addExpression.className = 'addAcao';
        this.addExpression.innerHTML = '+';
        this.divAddExpression.appendChild(this.addExpression);

        this.idExpression = 0;

        this.linha.appendChild(this.actionHolder);

        this.ExprAction = {};

        this.apertTeclas = {};

        this.actionOpt.addEventListener('change', (evt) => {
            this.paramDiv.innerHTML = '';
            let vlr = this.actionOpt.value
            if (vlr == 'digite') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Texto a ser digitado: ';
                this.paramDiv.appendChild(this.paramText);

                this.paramInput = document.createElement('input');
                this.paramInput.className = 'paramTexto';
                this.paramInput.type = 'text';
                this.paramInput.name = 'param';
                this.paramInput.placeholder = 'texto';
                this.paramDiv.appendChild(this.paramInput);
            } else if (vlr == 'pesquise') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Pesquisa: ';
                this.paramDiv.appendChild(this.paramText);

                this.paramInput = document.createElement('input');
                this.paramInput.className = 'paramTexto';
                this.paramInput.type = 'text';
                this.paramInput.name = 'param';
                this.paramInput.placeholder = 'texto';
                this.paramDiv.appendChild(this.paramInput);
            } else if (vlr == 'abra') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Aplicativo: ';
                this.paramDiv.appendChild(this.paramText);

                this.paramInput = document.createElement('input');
                this.paramInput.className = 'paramTexto';
                this.paramInput.type = 'text';
                this.paramInput.name = 'param';
                this.paramInput.placeholder = 'aplicativo';
                this.paramDiv.appendChild(this.paramInput);
            } else if (vlr == 'moveMouse') {
                this.paramText1 = document.createElement('p');
                this.paramText1.className = 'textParam';
                this.paramText1.innerHTML = 'X: ';
                this.paramDiv.appendChild(this.paramText1);

                this.paramInput1 = document.createElement('input');
                this.paramInput1.className = 'paramNumber';
                this.paramInput1.type = 'number';
                this.paramInput1.name = 'param';
                this.paramInput1.placeholder = 'x';
                this.paramDiv.appendChild(this.paramInput1);

                this.paramText2 = document.createElement('p');
                this.paramText2.className = 'textParam';
                this.paramText2.innerHTML = 'Y: ';
                this.paramDiv.appendChild(this.paramText2);

                this.paramInput2 = document.createElement('input');
                this.paramInput2.className = 'paramNumber';
                this.paramInput2.type = 'number';
                this.paramInput2.name = 'param';
                this.paramInput2.placeholder = 'y';
                this.paramDiv.appendChild(this.paramInput2);
            } else if (vlr == 'holdDown') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Botão: ';
                this.paramDiv.appendChild(this.paramText);

                this.paramInput = document.createElement('select');
                this.paramInput.className = 'paramSelect';
                this.paramInput.name = 'param';
                this.paramInput.innerHTML = `<option value="left">esquerdo</option>
                <option value="right">direito</option>
                <option value="middle">meio</option>`;
                this.paramDiv.appendChild(this.paramInput);

                this.paramCheck = document.createElement('input');
                this.paramCheck.type = 'checkbox';
                this.paramCheck.name = 'release';
                this.paramCheck.value = 'release';
                this.paramCheck.id = 'release'+this.id;
                this.paramDiv.appendChild(this.paramCheck);
                
                this.paramLabel = document.createElement('label');
                this.paramLabel.htmlFor = 'release'+this.id;
                this.paramLabel.innerHTML = ' Soltar quando parar a expressão ';
                this.paramDiv.appendChild(this.paramLabel);
            } else if (vlr == 'release') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Botão: ';
                this.paramDiv.appendChild(this.paramText);
                
                this.paramInput = document.createElement('select');
                this.paramInput.className = 'paramSelect';
                this.paramInput.name = 'param';
                this.paramInput.innerHTML = `<option value="left">esquerdo</option>
                <option value="right">direito</option>
                <option value="middle">meio</option>`;
                this.paramDiv.appendChild(this.paramInput);
            
            } else if (vlr == 'clica') {
                this.paramText = document.createElement('p');
                this.paramText.className = 'textParam';
                this.paramText.innerHTML = 'Botão: ';
                this.paramDiv.appendChild(this.paramText);
                
                this.paramInput = document.createElement('select');
                this.paramInput.className = 'paramSelect';
                this.paramInput.name = 'param';
                this.paramInput.innerHTML = `<option value="left">esquerdo</option>
                <option value="right">direito</option>
                <option value="middle">meio</option>`;
                this.paramDiv.appendChild(this.paramInput);
            } else if (vlr == 'aperte') {
                this.apertTeclas = {};
                this.idTecla = 0;

                this.paramTable = document.createElement('table');
                this.paramTable.className = 'paramTable';
    
                this.paramDiv.appendChild(this.paramTable);
                
                this.paramLinha = this.paramTable.insertRow();
                
                this.paramColunaAdd = this.paramLinha.insertCell();
                this.paramColunaAdd.className = 'paramColunaAdd';
                this.paramColunaAdd.innerHTML = `<p class="paramColunaAddText">+</p>`;
                this.paramColunaAdd.addEventListener('click', () => {
                    width = (this.destroyDiv.getBoundingClientRect().left - this.actionOpt.getBoundingClientRect().right - 15);
                    this.scrollParamDiv.style.maxWidth = width+'px';

                    this.apertTeclas[this.idTecla] = new teclaActionClass(this.paramLinha, this.paramColunaAdd, this.apertTeclas, this.idTecla);
                    this.idTecla += 1;
                });
            }
        });

        this.divAddExpression.addEventListener('click', () => { 
            this.ExprAction[this.idExpression] = new expressionSelectorClass(this.linhaExpression, this.celulaAddExpression, this.ExprAction, this.idExpression, null, null);
            this.idExpression += 1;
        });

        this.destroyDiv.addEventListener('click', () => {
            this.linha.remove();
            acoesArray.splice(acoesArray.indexOf(this), 1);
        });

        if (objBase != null) {
            this.actionOpt.value = objBase[2];
            this.actionOpt.dispatchEvent(new Event('change'));
            setTimeout(() => {
                if (objBase[2] == 'moveMouse') {
                    this.paramInput1.value = objBase[7][0];
                    this.paramInput2.value = objBase[7][1];
                } else if (objBase[2] == 'aperte') {
                    objBase[7].forEach(elTec => {
                        this.apertTeclas[this.idTecla] = new teclaActionClass(this.paramLinha, this.paramColunaAdd, this.apertTeclas, this.idTecla, elTec);
                        this.idExpression += 1;
                    });
                } else {
                    this.paramInput.value = objBase[7][0];
                }
    
                if (objBase[3] == 'holdDown') {
                    if (objBase[9] == 'release') {
                        this.paramCheck.checked = true;
                    }
                }
    
                for (let i = 0; i < objBase[0].length; i++) {
                    this.ExprAction[this.idExpression] = new expressionSelectorClass(this.linhaExpression, this.celulaAddExpression, this.ExprAction, this.idExpression, objBase[0][i], objBase[1][i]);
                    this.idExpression += 1;
                }
            }, 100);
        }
    }
}

function getAcoes() {
    event.preventDefault();

    let prt = new aguarde();

    prt.show();
    let send = new FormData;

    fetch(`${window.origin}/getAcoes`, {
        method: 'POST',
        body: send
    })
    .then(resp => resp.json())
    .then((result) => {
        result.forEach(element => {
            acoesArray.push(new action(linhaAdd, element));
        });
        var tabelaAcoesEvent = document.getElementById('tableConfig');

        var linhaAdd = document.createElement('tr');
        tabelaAcoesEvent.appendChild(linhaAdd);

        var divAddAcao = document.createElement('div');
        divAddAcao.className = 'divAddAcao';
        linhaAdd.appendChild(divAddAcao);
        
        var addAcao = document.createElement('p');
        addAcao.className = 'addAcao';
        addAcao.innerHTML = '+';
        divAddAcao.appendChild(addAcao);
        
        divAddAcao.addEventListener('click', () => {
            acoesArray.push(new action(linhaAdd, null));
        });
        
        prt.hide();
    });
}