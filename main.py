if __name__ == '__main__':
    try:
        import cv2
        import mediapipe as mp
        import math
        from genericpath import isfile
        import asyncio
        import subprocess
        import pyautogui
        import os
        import json
        from threading import Timer
        from PIL import ImageFont, ImageDraw, Image
        import numpy as np
        import sys
    except:
        os.system("pip install -r requirements.txt")

    # Inicializando as soluções de desenho e face_mesh
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    pth = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"
    pht2 = "C:\\Users\\Acer\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs"
    
    mouseBorders = [-1, -1]
    
    # Configuração para desenhar os pontos de referência com cores diferentes
    colors = {
        "sobrancelha direita": (0, 255, 0),  # Verde
        "sobrancelha esquerda": (0, 200, 0),  # Verde escuro
        "olho direito": (0, 0, 255),  # Vermelho
        "iris direita": (50, 50, 255),  # laranja
        "olho esquerdo": (0, 0, 200),  # Vermelho escuro
        "iris esquerda": (30, 30, 200),  # laranja escuro
        "nariz": (255, 0, 0),  # Azul
        "boca interno": (0, 255, 255),  # Amarelo
        "boca externo": (0, 200, 200)  # Amarelo escuro
    }

    positions = {
        # "sobrancelhas": {
        #     "cima":  [156, 70, 63, 105, 66, 107, 55],
        #     "baixo": [35, 124, 46, 53, 52, 65]
        # }
        "sobrancelha direita": [156, 70, 63, 105, 66, 107, 55, 124, 46, 53, 52, 65],
        "sobrancelha esquerda": [383, 300, 293, 334, 296, 336, 285, 353, 276, 283, 282, 295],
        "olho esquerdo": [466, 388, 387, 386, 385, 384, 398, 263, 249, 390, 373, 374, 380, 381, 382, 362],
        "iris esquerda": [468, 469, 470, 471, 472],
        "olho direito": [246, 161, 160, 159, 158, 157, 173, 33, 7, 163, 144, 145, 153, 154, 155, 133],
        "iris direita": [473, 474, 475, 476, 477],
        "nariz": [1, 2, 98, 168, 327],
        "boca interno": [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 78, 95, 88, 178, 87, 14, 317,
                         402, 318, 324, 308],
        "boca externo": [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291, 146, 91, 181, 84, 17, 314, 405,
                         321, 375, 291]
    }

    counters = [
        ['piscouEsquerdo', 0],
        ['piscouDireito', 0],
        ['ergueuSombrancelhaEsquerda', 0],
        ['ergueuSombrancelhaDireita', 0],
        ['abriuBoca', 0],
        ['esticouBocaEsquerdo', 0],
        ['esticouBocaDireito', 0]
    ]
    
    site = subprocess.Popen(['python', 'HandlessApp.py'])
    os.system('start ' + 'http://localhost:8989/')
    

    def loadJson(jsonFile):
        with open(f'{jsonFile}.json') as f:
            return json.load(f)

    dists = loadJson('./static/default/configActions')

    def dist(par):
        distancia = math.sqrt((par[2] - par[0]) ** 2 + (par[3] - par[1]) ** 2)
        return abs(distancia)

    def distX(par):
        distancia = par[2] - par[0]
        return abs(distancia)

    def distY(par):
        distancia = par[3] - par[1]
        return abs(distancia)

    #acoes

    def digite(param):
        pyautogui.write(param[0])

    def aperte(param):
        holdTecs = ['shift', 'alt', 'ctrl', 'capslock']

        def preciona(teclas2):
            if teclas2[0] in holdTecs:
                pyautogui.keyDown(teclas2[0])
                preciona(teclas2[1:])
                pyautogui.keyUp(teclas2[0])
            else:
                pyautogui.press(teclas2[0])

        preciona(param[0])


    def abra(param):
        if (not procuraArquivos(pth, param[0])):
            procuraArquivos(pht2, param[0])


    def pesquise(param):
        pesquisa = 'https://www.google.com/search?q=' + param[0].strip().replace(' ', '%20')
        os.system('start ' + pesquisa)


    def procuraArquivos(param):
        for arquivo in os.listdir(param[0]):
            newpth = param[0] + '\\' + arquivo
            if isfile(newpth):
                if param[1] in arquivo.lower():
                    subprocess.Popen(['call', newpth], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    asyncio.run(maximizar(arquivo[:arquivo.find('.')], param[1]))
                    return True
            else:
                for arq in os.listdir(newpth):
                    newnewpth = newpth + '\\' + arq
                    if isfile(newnewpth):
                        if param[1] in arq.lower():
                            subprocess.Popen(['call', newnewpth], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                             shell=True)
                            asyncio.run(maximizar(arq[:arq.find('.')], param[1]))
                            return True


    async def maximizar(janela, janela2):
        tmp = 0
        while True:
            try:
                if tmp > 20:
                    break
                janelatgt = pyautogui.getWindowsWithTitle(janela)[0]
            except:
                try:
                    for jan in pyautogui.getAllTitles():
                        if janela2.lower() in jan.lower():
                            janela2 = jan
                            break
                    janelatgt = pyautogui.getWindowsWithTitle(janela2)[0]
                except:
                    janelatgt = None
                    await asyncio.sleep(1)
                    tmp += 1
            if janelatgt != None:
                janelatgt.maximize()
                janelatgt.activate()
                break

    def clica(param):
        pyautogui.click(button=param[0])
        
    def moveMouse(param):
        pyautogui.moveTo(param[0], param[1])
        
    def holdDown(param):
        pyautogui.mouseDown(button=param[0])
        
    def release(param):
        pyautogui.mouseUp(button=param[0])

    #funcoes teate

    def piscouEsquerdo(param):
        print('piscou o olho esquerdo')
        counters[0][1] += 1

    def piscouDireito(param):
        print('piscou o olho direito')
        counters[1][1] += 1

    def ergueuSombrancelhaEsquerda(param):
        print('ergueu a sombrancelha esquerda')
        counters[2][1] += 1

    def ergueuSombrancelhaDireita(param):
        print('ergueu a sombrancelha direita')
        counters[3][1] += 1

    def abriuBoca(param):
        print('abriu a boca')
        counters[4][1] += 1

    def esticouBocaEsquerdo(param):
        print('esticou a boca esquerda')
        counters[5][1] += 1

    def esticouBocaDireito(param):
        print('esticou a boca direita')
        counters[6][1] += 1

    def calibra(face):
        for index in range(len(dists)):
            for exp in range(len(dists[index][0])):
                pos = []
                for point in dists[index][0][exp][1]:
                    pos.append(face[point][1].x)
                    pos.append(face[point][1].y)

                func = globals()[dists[index][0][exp][0]]
                result = func(pos)

                dists[index][3][exp] = result
                
    def camCalibra():
        global brk, C
        brk = 0
        C = 4
        
        def cMinus():
            global C
            C -= 1
            if C != 0:
                Timer(1, cMinus).start()
            elif C == 0:
                Timer(1, brkFun).start()
        def brkFun():
            global brk
            brk = 1
            
        Timer(1, cMinus).start()
        while brk == 0:
            W = int(cap.get(3))
            
            ret2, frame2 = cap.read()
            frame2 = cv2.resize(frame2, (1100, 800))
            frame2 = cv2.flip(frame2, 1)

            if not ret:
                print("Não foi possível receber o quadro. Verifique a webcam e tente novamente.")
                break

            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            resultsCalibra = face_mesh.process(frame2)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)
            
            if resultsCalibra.multi_face_landmarks is not None:
                fontpath = "./static/default/arial.ttf"     
                font = ImageFont.truetype(fontpath, 22)
                img_pil = Image.fromarray(frame2)
                draw = ImageDraw.Draw(img_pil)
                _, _, w, h = draw.textbbox((0, 0), 'Faça uma cara neutra: ', font=font)

                tBox = draw.textbbox(((W-w)/2, 50), 'Faça uma cara neutra: ', font = ImageFont.truetype(fontpath, 22)) 
                draw.rectangle(tBox, 'black')
                draw.text(((W-w)/2, 50), 'Faça uma cara neutra: ', font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 

                if C < 4:
                    _, _, w, h = draw.textbbox((0, 0), str(C), font=font)
                    tBox = draw.textbbox(((W-w)/2, 77), str(C), font = ImageFont.truetype(fontpath, 22)) 
                    draw.rectangle(tBox, 'black')
                    draw.text(((W-w)/2, 77), str(C), font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 

                frame2 = np.array(img_pil)
                
                cv2.imshow('Calibração', frame2)
                    
                if cv2.waitKey(5) & 0xFF == 27:  # Pressione 'ESC' para sair
                    cv2.destroyAllWindows()
                    break
        for face_landmarksCalibra in resultsCalibra.multi_face_landmarks:
            landmarksCalibra = list(enumerate(face_landmarksCalibra.landmark))
        calibra(landmarksCalibra)
    
    def camCalibraMouse(mode):
        global brkM, cM1, cM2, landmarksCalibraMouse, xM, yM
        brkM = 0
        cM1 = 4
        cM2 = 0
        landmarksCalibraMouse = 0
        xM = 0
        yM = 0
        
        def cM1Minus():
            global cM1, cM2
            cM1 -= 1
            if cM1 != 0:
                Timer(1, cM1Minus).start()
            elif cM1 == 0:
                Timer(1, cM2Plus).start()
        def cM2Plus():
            global cM1, cM2, mouseBorders, xM, yM
            mouseBorders[cM2] = [xM, yM]
            cM2 += 1
            if cM2 != 2:
                cM1 = 4
                Timer(1, cM1Minus).start()
            elif cM2 == 2:
                Timer(1, brkMFun).start()
        def brkMFun():
            global brkM
            brkM = 1
            
        Timer(1, cM1Minus).start()
        while brkM == 0:
            W = int(cap.get(3))
            
            ret2, frame2 = cap.read()
            frame2 = cv2.resize(frame2, (1100, 800))
            frame2 = cv2.flip(frame2, 1)
            if not ret:
                print("Não foi possível receber o quadro. Verifique a webcam e tente novamente.")
                break

            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            resultsCalibraMouse = face_mesh.process(frame2)
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_RGB2BGR)
            
            if resultsCalibraMouse.multi_face_landmarks is not None:
                for face_landmarksCalibraMouse in resultsCalibraMouse.multi_face_landmarks:
                    landmarksCalibraMouse = list(enumerate(face_landmarksCalibraMouse.landmark))
                
                xM = int(landmarksCalibraMouse[1][1].x * frame2.shape[1])
                yM = int(landmarksCalibraMouse[1][1].y * frame2.shape[0])
                if cM2 == 0:
                    cv2.circle(frame2, (xM, yM), 1, (0, 255, 0), -1)
                if cM2 == 1:
                    if mode == 0:
                        cv2.circle(frame2, (mouseBorders[0][0], mouseBorders[0][1]), 1, (0, 255, 0), -1)
                        cv2.circle(frame2, (xM, yM), 1, (0, 255, 0), -1)
                        cv2.rectangle(frame2, (mouseBorders[0][0], mouseBorders[0][1]), (xM, yM), (0, 255, 0, 20), 2)
                    elif mode == 1:
                        cv2.circle(frame2, (mouseBorders[0][0], mouseBorders[0][1]), int(dist([mouseBorders[0][0], mouseBorders[0][1], xM, yM])), (0, 255, 0), 1)
                fontpath = "./static/default/arial.ttf"     
                font = ImageFont.truetype(fontpath, 22)
                img_pil = Image.fromarray(frame2)
                draw = ImageDraw.Draw(img_pil)
                if cM2 == 0:
                    if mode == 0:
                        _, _, w, h = draw.textbbox((0, 0), 'Mova o pescoço para o canto esquerdo da tela: ', font=font)
                        tBox = draw.textbbox(((W-w)/2, 50), 'Mova o pescoço para o canto esquerdo da tela: ', font = ImageFont.truetype(fontpath, 22)) 
                        draw.rectangle(tBox, 'black')
                        draw.text(((W-w)/2, 50), 'Mova o pescoço para o canto esquerdo da tela: ', font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 
                    elif mode == 1:
                        _, _, w, h = draw.textbbox((0, 0), 'Mova o pescoço para o centro da tela: ', font=font)
                        tBox = draw.textbbox(((W-w)/2, 50), 'Mova o pescoço para o centro da tela: ', font = ImageFont.truetype(fontpath, 22)) 
                        draw.rectangle(tBox, 'black')
                        draw.text(((W-w)/2, 50), 'Mova o pescoço para o centro da tela: ', font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 

                elif cM2 == 1:
                    if mode == 0:
                        _, _, w, h = draw.textbbox((0, 0), 'Mova o pescoço para o canto direito da tela: ', font=font)
                        tBox = draw.textbbox(((W-w)/2, 50), 'Mova o pescoço para o canto direito da tela: ', font = ImageFont.truetype(fontpath, 22)) 
                        draw.rectangle(tBox, 'black')
                        draw.text(((W-w)/2, 50), 'Mova o pescoço para o canto direito da tela: ', font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 
                    elif mode == 1:
                        _, _, w, h = draw.textbbox((0, 0), 'Defina o ponto morto da tela: ', font=font)
                        tBox = draw.textbbox(((W-w)/2, 50), 'Defina o ponto morto da tela: ', font = ImageFont.truetype(fontpath, 22)) 
                        draw.rectangle(tBox, 'black')
                        draw.text(((W-w)/2, 50), 'Defina o ponto morto da tela: ', font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 

                if cM1 < 4:
                    _, _, w, h = draw.textbbox((0, 0), str(cM1), font=font)
                    tBox = draw.textbbox(((W-w)/2, 77), str(cM1), font = ImageFont.truetype(fontpath, 22)) 
                    draw.rectangle(tBox, 'black')
                    draw.text(((W-w)/2, 77), str(cM1), font = ImageFont.truetype(fontpath, 22), fill = (255,255,255,0), align='center') 

                frame2 = np.array(img_pil)
                
                cv2.imshow('Calibração do Mouse', frame2)
                    
                if cv2.waitKey(5) & 0xFF == 27:  # Pressione 'ESC' para sair
                    cv2.destroyAllWindows()
                    break

    def handleDists(face):
        for index in range(len(dists)):
            countExp = 0
            
            for exp in range(len(dists[index][0])):
                pos = []
                for point in dists[index][0][exp][1]:
                    pos.append(face[point][1].x)
                    pos.append(face[point][1].y)

                func = globals()[dists[index][0][exp][0]]
                result = func(pos)

                if dists[index][3][exp] == -1:
                    dists[index][3][exp] = result

                if eval(f'{result} {dists[index][4][exp]} ({dists[index][3][exp]} * {dists[index][1][exp]})'):
                    countExp += 1
                    
            if countExp == len(dists[index][0]):
                dists[index][8] = 0
                if dists[index][6] == 0:
                    dists[index][6] = 1
                    funcExec = globals()[dists[index][2]]
                    funcExec(dists[index][7])
            else:
                dists[index][8] += 1
                if dists[index][8] > 10:
                    dists[index][6] = 0
                    if dists[index][9] != None:
                        funcExec = globals()[dists[index][9]]
                        funcExec(dists[index][7])

    m = 1
    sx = 0  # 1750
    sy = 0  # 1300
    letterSize = 0.35
    mostraCounters = True

    cap = cv2.VideoCapture(0)  # Iniciando a webcam

    # Configurações de face_mesh
    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5,
                               min_tracking_confidence=0.5) as face_mesh:

        while cap.isOpened():
            ret, frame = cap.read()
            w, h = pyautogui.size()
            frame = cv2.resize(frame, (1100, 800))
            frame = cv2.flip(frame, 1)
            if not ret:
                print("Não foi possível receber o quadro. Verifique a webcam e tente novamente.")
                break

            # Convertendo o quadro de BGR para RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Processando o quadro com a solução face_mesh
            results = face_mesh.process(frame)

            # Convertendo o quadro de volta para BGR para desenho
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # if mostraCounters:
            #     ln = 20
            #     for txt, cnt in counters:
            #         cv2.putText(frame, f'{txt}: {cnt}', (50, ln), cv2.FONT_HERSHEY_SIMPLEX, letterSize * 2, (0, 0, 0))
            #         ln += 50

            if results.multi_face_landmarks is not None:
                # cv2.rectangle(frame, (0, 0), (1100, 800), (0, 0, 0), -1)
                for face_landmarks in results.multi_face_landmarks:
                    landmarks = list(enumerate(face_landmarks.landmark))
                    handleDists(landmarks)
                    #for id, lm in landmarks:
                    xNariz, yNariz = int(landmarks[1][1].x * frame.shape[1]), int(landmarks[1][1].y * frame.shape[0])

                        #for name, pos in positions.items():
                            #if id in pos:
                                #cv2.circle(frame, (x, y), 1, colors[name], -1)
                                # cv2.putText(frame, str(id), (int(x * m) - sx, int(y * m) - sy), cv2.FONT_HERSHEY_SIMPLEX, letterSize, colors[name], 1)
                try:
                    with open('./static/default/configRun.json', 'r+') as f:
                        cnf = json.load(f)
                        if cnf['atualiza'] == 1:
                            dists = loadJson('./static/default/configActions')
                            cnf['atualiza'] = 0
                            
                        if cnf['calibra'] == 1:
                            camCalibra()
                            cnf['calibra'] = 0
                            cv2.destroyAllWindows()
                        
                        if cnf['mouseCalibra'] == 1:
                            camCalibraMouse(cnf['modoMouse'])
                            cnf['mouseCalibra'] = 0
                            cv2.destroyAllWindows()
                            
                        if cnf['mouseControl'] == 1:
                            if mouseBorders[0] == -1:
                                camCalibraMouse(cnf['modoMouse'])
                                cv2.destroyAllWindows()
                            else:
                                if cnf['modoMouse'] == 0:
                                    xT, yT = (((xNariz - mouseBorders[0][0]) * w) / (mouseBorders[1][0] - mouseBorders[0][0])), (((yNariz - mouseBorders[0][1]) * h) / (mouseBorders[1][1] - mouseBorders[0][1]))
                                    try:
                                        pyautogui.moveTo((((xNariz - mouseBorders[0][0]) * w) / (mouseBorders[1][0] - mouseBorders[0][0])), (((yNariz - mouseBorders[0][1]) * h) / (mouseBorders[1][1] - mouseBorders[0][1])), 0.1)
                                    except pyautogui.FailSafeException:
                                        site.kill()
                                        cap.release()
                                        cv2.destroyAllWindows()
                                        sys.exit()
                                elif cnf['modoMouse'] == 1:
                                    if dist([mouseBorders[0][0], mouseBorders[0][1], xNariz, yNariz]) > dist([mouseBorders[0][0], mouseBorders[0][1], mouseBorders[1][0], mouseBorders[1][1]]):
                                        try:
                                            pyautogui.move(xNariz - mouseBorders[0][0], yNariz - mouseBorders[0][1], 0.1)
                                        except pyautogui.FailSafeException:
                                            site.kill()
                                            cap.release()
                                            cv2.destroyAllWindows()
                                            sys.exit()

                        if cnf['paraPrograma'] == 1:
                            cnf['paraPrograma'] = 0
                            f.seek(0)
                            f.truncate(0)
                            f.write(json.dumps(cnf))
                            site.kill()
                            cap.release()
                            cv2.destroyAllWindows()
                            sys.exit()
                            
                        f.seek(0)
                        f.truncate(0)
                        f.write(json.dumps(cnf))
                except:
                    with open('./static/default/configRun.json', 'w') as f:
                        f.write('"atualiza": 0, "calibra": 0, "mouseControl": 1, "mouseCalibra": 0, "modoMouse": 1, "paraPrograma":0')
                        
                            
                            
            if cv2.waitKey(5) & 0xFF == 27:  # Pressione 'ESC' para sair
                break

    cap.release()
    cv2.destroyAllWindows()


