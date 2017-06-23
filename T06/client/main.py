import threading
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory, \
    QPushButton, QVBoxLayout, QGroupBox, QDialog, QProgressBar, \
    QGridLayout, QLabel, QLineEdit, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap, QMovie, QFont
from PyQt5.QtCore import QTimer, Qt, QEvent, pyqtSignal, QRect
from PyQt5.QtMultimedia import QSound
import sys
import random
import os
import time
import pickle


HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
emojis = ["ApoopA", "OA)", "AD", "B)", "8)", "U.U", "A(", "3A)", "o.o", "Av"]  # A = :, B = ;
emoji = [":poop:", "O:)", ":D", ";)", "8)", "U.U", ":(", "3:)", "o.o", ":v"]


class Client(QWidget):
    def __init__(self, port, host):
        QWidget.__init__(self)
        print("Inicializando cliente...")
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user = ""
        self.id_sala = ""
        self.salas = []
        self.options = []
        self.current = ""
        self.butons = []
        self.replies = 0
        self.order = ""
        self.removal = False
        self.songs = dict()
        self.ranking = ""
        self.force_close = False
        self.puntaje = 0
        self.steppers = [True, True, True, True, True, True, True, True]
        self.initi = False
        self.emojis = self.get_emojis()
        self.initUI()

    @property
    def parameters(self):
        return [self.host, self.port, self.user, self.order]

    def get_emojis(self):
        global emojis, emoji
        dicc = dict()
        der = os.path.dirname(os.path.realpath(__file__))
        for a in emojis:
            derr = der + "\\" + a + ".png"
            print(derr)
            pix = QPixmap(derr)
            diro = emoji[emojis.index(a)]
            dicc[diro] = pix.scaled(30,30,Qt.KeepAspectRatio)
        return dicc

    def initUI(self):
        self.setWindowTitle("PrograPop")
        self.e1 = QLineEdit()
        self.e2 = QLabel()
        self.e2.setText("Bienvenido a PrograPop")
        self.e1.setFont(QFont("Arial", 20))

        self.e1.returnPressed.connect(self.okfunc)
        flo = QFormLayout()
        self.ley = flo

        der = os.path.dirname(os.path.realpath(__file__))
        der = der.replace(r"\client", "")
        der += r"\server"
        lista = os.listdir(der)
        dic = dict()
        lis = []
        if "savefile.txt" in lista:
            with open(der + r"\savefile.txt", mode="rb") as file:
                try:
                    dic = pickle.load(file)
                except:
                    print("COULD NOT LOAD: EMPTY FILE")
        if "stats.txt" in lista:
            with open(der + r"\stats.txt", mode="rb") as file:
                try:
                    lis = pickle.load(file)
                except:
                    print("COULD NOT LOAD: EMPTY FILE")

        self.ley.addRow("   Username:", self.e1)
        self.ley.addRow("   ", self.e2)
        self.eaux = QWidget(self)
        lay = QVBoxLayout(self)
        inserted = False
        if len(dic) != 0:
            tii = QLabel(self)
            tii.setText("RANKING DE JUGADORES")
            lay.addWidget(tii)
            inserted = True
            au = []
            for a in dic:
                b = dic[a]
                au.append(float(b))
            new = sorted(au, reverse=True)
            for a in dic:
                b = dic[a]
                if b == new[0]:
                    lab = QLabel(self)
                    lab.setText("Usuario {}     Puntaje: {}".format(a, b))
                    lay.addWidget(lab)
                    if len(new) != 0:
                        del new[0]
            if len(new) != 0:
                for a in dic:
                    b = dic[a]
                    if b == new[0]:
                        lab = QLabel(self)
                        lab.setText("Usuario {}     Puntaje: {}".format(a, b))
                        lay.addWidget(lab)
                        if len(new) != 0:
                            del new[0]
        if len(lis) != 0:
            tii = QLabel(self)
            tii.setText("SALAS DESTACADAS")
            lay.addWidget(tii)
            inserted = True
            if len(lis) > 1:
                a = lis[0]
                b = lis[1]
                if a[1] >= b[1]:
                    lab = QLabel(self)
                    lab.setText(a[0] + " con más respuestas. Total: " + str(a[1]))
                    lay.addWidget(lab)
                    lob = QLabel(self)
                    lob.setText(b[0] + " con más respuestas erróneas o no usada. Total: " + str(b[1]))
                    lay.addWidget(lob)
                else:
                    lab = QLabel(self)
                    lab.setText(b[0] + " con más respuestas. Total: " + str(b[1]))
                    lay.addWidget(lab)
                    lob = QLabel(self)
                    lob.setText(a[0] + " con más respuestas erróneas o no usada. Total: " + str(a[1]))
                    lay.addWidget(lob)
        if len(lis) == 0 and len(dic) == 0:
            lab = QLabel(self)
            lab.setText("No hay ranking ni estadísticas porque no hay datos del juego.")
            self.ley.addRow("   ", lab)
        if inserted:
            self.eaux.setLayout(lay)
            self.ley.addRow("   ", self.eaux)
            self.butons.append(self.eaux)
        self.setLayout(self.ley)
        self.setGeometry(100, 100, 400, 500)
        self.show()

    def okfunc(self):
        print("SETTING USER {}".format(str(self.e1.text())))
        self.initi = True
        self.user = str(self.e1.text())
        try:
            self.connect_to_server()
            self.listen()
            self.repl()
        except:
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    def okfunco(self):
        print("SETTING USER {}".format(str(self.e1.text())))
        self.user = str(self.e1.text())
        self.send(self.parameters[2] + "USERNAME")
        self.replies += 1

    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor...")

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def send(self, msg):
        msg_bytes = msg.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        self.socket_cliente.send(msg_length + msg_bytes)
        self.steppers[2] = True
        self.steppers[4] = True
        if "CLOSE" in msg:
            return "DONE"

    def listen_thread(self):
        i = 0
        listen = True
        while listen:
            try:
                response_bytes_length = self.socket_cliente.recv(4)
                response_length = int.from_bytes(response_bytes_length, byteorder="big")
                response = b""

                while len(response) < response_length:
                    response += self.socket_cliente.recv(256)
                self.steppers[4] = True
                self.steppers[2] = True
                self.steppers[5] = True
                self.steppers[6] = True
                self.steppers[7] = True
                if response.decode() != "":
                    self.order = response.decode()
                    if "TIEMPO" in self.order:
                        s = self.order.split("TIEMPO")
                        if len(s) > 1:
                            ss = s[1][0:5]
                            self.order = "TIEMPO" + ss
                    if self.current != "" and "PLAY" in self.order:
                        print("\nSTOPPING CURRENT at emergency")
                        self.songs[self.current].stop()
                    if "MSN" in self.order:
                        print("RECEIVED MESSAGE!!")
                    # print("{}\n>>> ".format(self.order), end="")
            except:
                if i > 20:
                    listen = False
                    self.force_close = True
                    QApplication.closeAllWindows()
                    print("Cliente desconectado!")
                i += 1

    def closeEvent(self, event):
        go = True
        try:
            tr = self.send("CLOSE" + self.parameters[2])
            if tr == "DONE":
                print("Closing connection")
                time.sleep(5)
                self.socket_cliente.close()
        except:
            if self.initi is True and self.force_close is False:
                go = False
        if go:
            event.accept()  # let the window close
            exit()
        else:
            event.ignore()

    def opt_sender(self):
        sender = self.sender()
        for a in self.options:
            if sender == a[0]:
                option = a[1]
                print("SENDING OPTION")
                self.send(str(option) + ":" + self.parameters[2] + ":" + self.id_sala + "OPTION")
                pass

    def sel_sender(self):
        sender = self.sender()
        texto = sender.text().split(":")[0].replace("Sala ", "").replace(" de", "")
        self.send(str(texto) + ":" + str(self.user) + "DEFINE")
        self.id_sala = str(texto[0])
        for i in self.salas:
            QApplication.processEvents()
            tup = i[3]
            if tup == str(texto[0]):
                chosen = []
                for a in self.butons:
                    try:
                        self.ley.removeRow(a)
                    except:
                        pass
                k = 1
                n = self.ley.rowCount()
                while k < n:
                    k += 1
                    self.ley.removeRow(k)
                self.e2 = QLabel()
                self.e2.setText("Elige el artista de la canción actual!")
                self.ley.addRow("   ", self.e2)
                self.e3 = QLabel(self)
                self.e3.setText("Puntaje actual: " + str(self.puntaje))
                self.ley.addRow("   ", self.e3)
                lif = 0
                while len(chosen) < len(i[5]):
                    p = random.choice(i[5])
                    if p not in chosen:
                        lif += 1
                        chosen.append(p)
                        p.replace(".wav", "")
                        p.replace(".mp3", "")
                        uno = p
                        p = p.split("-")
                        fin = p[0].strip(" ").strip("_").replace("_", " ")
                        pu = QPushButton(self)
                        pu.setText(fin)
                        pu.clicked.connect(self.opt_sender)
                        self.options.append((pu, uno))
                        self.ley.addRow("   ", pu)
                self.setGeometry(100, 100, 100 + lif*10, 50*lif + 50)
                self.show()
                QApplication.processEvents()
                # self.send("REPEAT")

    def chat_grupo_ini(self):
        print("SETTING CHAT GRUPAL")
        self.chat = QFormLayout(self)
        wid = QWidget(self)
        layu = QVBoxLayout(self)
        msje_bienvenida = QLabel(self)
        msje_bienvenida.setText("Bienvenido al chat de grupo!")
        layu.addWidget(msje_bienvenida)
        wid.setLayout(layu)
        self.chat.addRow(wid)
        self.boxx = QLineEdit(self)
        self.boxx.setFont(QFont("Arial", 12))
        self.boxx.returnPressed.connect(self.send_msjs)
        self.ley.addRow(self.chat)
        self.ley.addRow(self.boxx)
        print("CHAT DONE!")

    def send_msjs(self):
        texto = self.boxx.text()
        self.send("MENSAJE" + self.user + "-" + texto)
        print("SENDING MESSAGE")
        print(texto)

    def find_str(self, s, char):
        index = 0

        if char in s:
            c = char[0]
            for ch in s:
                if ch == c:
                    if s[index:index + len(char)] == char:
                        return index

                index += 1

        return -1

    def repl(self):
        print("------ Consola ------\n>>> ", end="")
        while True:
            QApplication.processEvents()
            if self.replies == 0:
                self.send(self.parameters[2] + "USERNAME")
                self.replies += 1
            else:
                if self.order == "INVALID" and self.steppers[0]:
                    self.e1.returnPressed.connect(self.okfunco)
                    self.e2.setText("Username ocupado. Escriba otro.")
                    QApplication.processEvents()
                    pass
                elif "CONFIG" in self.order and self.steppers[1]:
                    self.steppers[0] = False
                    self.e1.setReadOnly(True)
                    order = self.order.replace("CONFIG", "")
                    salas = order.split("SEP")
                    self.puntaje = 0
                    aux = []
                    for a in salas:
                        i = 0
                        aux1 = []
                        sala = a.split(":")
                        if sala != ['']:
                            while i < len(sala) - 6:
                                i += 1
                                if sala[i] != ['']:
                                    aux1.append(sala[i])
                            aux.append((sala[i + 1], sala[i + 2], sala[i + 3], sala[i + 4], sala[i + 5], aux1))
                    self.salas = aux
                    self.e2.setText("Elija una sala para comenzar a jugar")
                    self.e3 = QLabel(self)
                    self.e3.setText("Puntaje actual: " + str(self.puntaje))
                    self.ley.addRow("   ", self.e3)
                    for a in self.salas:
                        art = ""
                        chosen = []
                        while len(chosen) < 2:
                            p = random.choice(a[5])
                            if p not in chosen:
                                chosen.append(p)
                                p.replace(".wav", "")
                                p.replace(".mp3", "")
                                p = p.split("-")
                                fin = p[0].strip(" ").strip("_").replace("_", " ")
                                art += fin + "    "
                        if a[4] == "False":
                            tin = "Ecualizador"
                        else:
                            tin = "Normal"
                        stri = "Sala {} {} {}, Jugadores: {}, Segundos restantes: {}, Artistas: {}".format(a[3],
                                                                                                        a[0], tin, a[1], str(round(float(a[2]), 1)), art)
                        push = QPushButton(str(a[3]), self)
                        push.setText(stri)
                        push.clicked.connect(self.sel_sender)
                        self.butons.append(push)
                        self.ley.addRow("   ", push)
                        QApplication.processEvents()
                    self.show()
                    self.steppers[1] = False
                    self.e3.setText("Puntaje actual: " + str(self.puntaje))
                elif "RANKING" in self.order and self.steppers[2]:
                    print("RECEIVED RANKING")
                    if self.removal is False:
                        print()
                        self.ley.removeRow(self.ley.count() - 3) # estaba en -1
                        self.removal = True
                    else:
                        self.ley.removeRow(self.ley.count() - 1)
                    aux = QWidget(self)
                    rank = QVBoxLayout(self)
                    title = QLabel(self)
                    title.setText("ESTADÍSTICAS DE SALA")
                    rank.addWidget(title)
                    ordah = self.order.replace("RANKING", "")
                    master = ordah.split(";")
                    print("RANKING: {}".format(ordah))
                    for ti in master:
                        if ti != "":
                            r = QLabel(self)
                            r.setText(ti)
                            rank.addWidget(r)
                    aux.setLayout(rank)
                    self.ranking = aux
                    self.ley.addRow("   ", aux)
                    se = ordah.split(" - ")[1].split(":")[1].strip(" ")
                    self.e3.setText("Puntaje actual: {}".format(se))
                    self.show()
                    self.steppers[2] = False
                    pass
                elif "SETUP" in self.order and self.steppers[3]:
                    aux = QWidget(self)
                    rank = QVBoxLayout(self)
                    title = QLabel(self)
                    title.setText("ESTADÍSTICAS DE SALA")
                    rank.addWidget(title)
                    ordah = self.order.replace("SETUP", "")
                    master = ordah.split(";")
                    for ti in master:
                        if ti != "":
                            r = QLabel(self)
                            r.setText(ti)
                            rank.addWidget(r)
                    aux.setLayout(rank)
                    self.ranking = aux
                    self.ley.addRow("   ", aux)
                    self.chat_grupo_ini()  # NUEVO
                    self.show()
                    self.steppers[3] = False
                elif "PLAY" in self.order and self.steppers[4]:
                    if self.current != "":
                        print("\nSTOPPING CURRENT at emergency 2")
                        self.songs[self.current].stop()
                    order = self.order.replace("PLAY", "")
                    if order not in self.songs:
                        der = os.path.dirname(os.path.realpath(__file__))
                        der = der.replace(r"\client", "")
                        der += r"\server\songs"
                        lista = os.listdir(der)
                        for o in lista:
                            direccion = der + "\{}".format(o)
                            if order in os.listdir(direccion):
                                print(order)
                                sound = QSound(direccion + "/" + order)
                                self.songs[order] = sound
                                if self.current != "":
                                    print("STOPPING CURRENT at creation")
                                    self.songs[self.current].stop()
                                self.current = order
                                print("PLAYING NEW SONG")
                                self.songs[self.current].play()
                    else:
                        if not self.songs[self.current].isFinished():
                            print("STOPPING CURRENT at repetition")
                            self.songs[self.current].stop()
                        print("PLAYING REPEATED SONG")
                        self.songs[order].play()
                    self.steppers[4] = False
                elif "PUNTAJE" in self.order and self.steppers[5]:
                    print("CAMBIANDO PUNTAJE")
                    self.steppers[5] = False
                    ol = self.order.replace("PUNTAJE", "")
                    self.e3.setText("Puntaje actual: {}".format(ol))
                    QApplication.processEvents()
                elif "TIEMPO" in self.order and self.steppers[6]:
                    self.steppers[6] = False
                    ol = self.order.replace("TIEMPO", "")
                    ol = str(round(float(ol), 2))
                    r = self.e3.text().split("-")
                    if len(r) > 1:
                        y = r[0].strip(" ")
                    else:
                        y = r[0]
                    self.e3.setText(y + " - Tiempo restante: " + ol)
                    QApplication.processEvents()
                elif "MSN" in self.order and self.steppers[7]:
                    self.steppers[7] = False
                    print("MSN RECEIVER")
                    order = self.order.replace("MSN", "")
                    data = order.split("-")
                    if len(data) == 1:
                        print("SINGLE MESSAGE")
                        widgets = []
                        mensaje = data[0]
                        wid = QWidget(self)
                        layu = QVBoxLayout(self)
                        msj = QLabel(self)
                        go1 = True
                        global emoji
                        for b in emoji:
                            ind = self.find_str(b, mensaje)
                            if ind != -1:
                                go1 = False
                                if len(mensaje) > 0:
                                    print("CREATING MESSAGE")
                                    i = 0
                                    aux = ""
                                    for let in mensaje:
                                        if i <= len(b) - 1:
                                            i += 1
                                            aux += let
                                    mensaje = mensaje.replace(aux, "")
                                    if len(mensaje) != 0:
                                        label = QLabel(self)
                                        label.setText(aux)
                                        widgets.append(label)
                                        pix = self.emojis[b]
                                        lab = QLabel(self)
                                        lab.resize(30, 30)
                                        lab.setPixmap(pix)
                                        widgets.append(lab)
                                    else:
                                        pix = self.emojis[b]
                                        lab = QLabel(self)
                                        lab.setPixmap(pix)
                                        widgets.append(lab)
                        if go1:
                            msj.setText(data[0])
                            layu.addWidget(msj)
                        else:
                            for w in widgets:
                                print(str(isinstance(w, QPixmap)))
                                layu.addWidget(w)
                        wid.setLayout(layu)
                        if self.chat.count() > 10:
                            self.chat.removeRow(0)
                            self.chat.removeRow(1)
                        self.chat.addRow(wid)
                    else:
                        print("MESSAGE WITH EXCEPTIONS")
                        ignore = []
                        widgets =[]
                        mensaje = data[0]
                        notas = data[1:len(data)-1]
                        print(data)
                        print(notas)
                        while len(notas) != 0:
                            nota = notas[0].replace("REPLACED", "")
                            del notas[0]
                            ignore.append(nota)
                        print(ignore)
                        global emoji
                        for b in emoji:
                            ind = self.find_str(b, mensaje)
                            if ind != -1:
                                go = True
                                for g in ignore:
                                    if g == b:
                                        print("GOT TO IGNORE at {}".format(b))
                                        go = False
                                        break
                                if go:
                                    if len(mensaje) > 0:
                                        print("CREATING MESSAGE")
                                        print(mensaje[0, ind - 1])
                                        print(mensaje[ind, len(mensaje) - 1])
                                        label = QLabel(self)
                                        label.setText(mensaje[0, ind - 1])
                                        widgets.append(label)
                                        pix = self.emojis[b]
                                        lab = QLabel(self)
                                        lab.setPixmap(pix)
                                        widgets.append(lab)
                                        mensaje = mensaje[ind, len(mensaje) - 1]
                        print("ADDING CONVERSATION")
                        wid = QWidget(self)
                        layu = QVBoxLayout(self)
                        for y in widgets:
                            layu.addWidget(y)
                        wid.setLayout(layu)
                        if self.chat.count() > 10:
                            self.chat.removeRow(0)
                            self.chat.removeRow(1)
                        self.chat.addRow(wid)
                        print("MSN DONE!!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Client(PORT, HOST)
    sys.exit(app.exec_())