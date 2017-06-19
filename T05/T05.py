import sys
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory, \
    QPushButton, QHBoxLayout, QGroupBox, QDialog, QProgressBar, \
    QGridLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtCore import QTimer, Qt, QEvent, pyqtSignal, QRect
import os
import Imgs
import backend
import math
import random


campeon = ""


class Tienda(QDialog):
    buy = pyqtSignal(tuple)

    def __init__(self, listacomprados, llamadas=0):
        super().__init__()
        self.title = "Tienda League of Progra"
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        self.a = QPushButton(self)
        self.b = QPushButton(self)
        self.c = QPushButton(self)
        self.d = QPushButton(self)
        self.e = QPushButton(self)
        self.f = QPushButton(self)

        if "Arma de mano" not in listacomprados:
            a = llamadas
        if "Arma de distancia" not in listacomprados:
            b = llamadas
        if "Botas" not in listacomprados:
            c = llamadas
        if "Báculo" not in listacomprados:
            d = llamadas
        if "Armadura" not in listacomprados:
            e = llamadas
        if "Carta Earthstone" not in listacomprados:
            f = llamadas

        self.lista_productos = [("Arma de mano", "Daño", 5 + llamadas - a, 2), ("Arma de distancia", "Rango", 5 + llamadas - b, 2),
                                ("Botas", "Rapidez", 2 + llamadas - c, 3)
                                , ("Báculo", "Habilidad", 7 + llamadas - d, 2),
                                ("Armadura", "Daño Recibido", 5 + llamadas - e, 2),
                                ("Carta Earthstone", "Aleatorio", 10 + llamadas - f, 6)]
        self.a.setText("Arma de mano: {} puntos -> Aumenta tu daño inflingido".format(self.lista_productos[0][2]))
        self.b.setText("Arma de distancia: {} puntos -> Aumenta tu rango de ataque".format(self.lista_productos[1][2]))
        self.c.setText("Botas: {} puntos -> Aumenta tu rapidez de movimiento".format(self.lista_productos[2][2]))
        self.d.setText("Báculo: {} puntos -> Potencia tu habilidad especial".format(self.lista_productos[3][2]))
        self.e.setText("Armadura: {} puntos -> Aumenta tu daño inflingido".format(self.lista_productos[4][2]))
        self.f.setText("Carta Earthstone: {} puntos -> Potencia una habilidad aleatoria".format(self.lista_productos[5][2]))
        self.a.move(10, 10*4)
        self.b.move(10, 20*4)
        self.c.move(10, 30*4)
        self.d.move(10, 40*4)
        self.e.move(10, 50*4)
        self.f.move(10, 60*4)
        self.a.clicked.connect(self.buya)
        self.b.clicked.connect(self.buyb)
        self.c.clicked.connect(self.buyc)
        self.d.clicked.connect(self.buyd)
        self.e.clicked.connect(self.buye)
        self.f.clicked.connect(self.buyf)

    def iniUI(self):
        self.setWindowTitle(self.title)
        self.a.show()
        self.b.show()
        self.c.show()
        self.d.show()
        self.e.show()
        self.f.show()

    def buya(self):
        self.buy.emit((1, "Daño", 2))

    def buyb(self):
        self.buy.emit(2, ("Rango", 2))

    def buyc(self):
        self.buy.emit((3, "Rapidez", 3))

    def buyd(self):
        self.buy.emit((4, "Habilidad", 2))

    def buye(self):
        self.buy.emit((5, "Inmunidad", 2))

    def buyf(self):
        a = random.choice(("Habilidad", "Inmunidad", "Rapidez", "Rango", "Daño"))
        self.buy.emit((6, a, 6))


class inicio(QDialog):
    inicio = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.uno = QPushButton(self)
        self.uno.setText("Chau la Hechicera")
        self.dos = QPushButton(self)
        self.dos.setText("Sans")
        self.tres = QPushButton(self)
        self.tres.setText("Hernán el destructor")
        self.uno.move(10, 10 * 4)
        self.dos.move(10, 20 * 4)
        self.tres.move(10, 30 * 4)
        self.title = "League of Progra - Start"
        self.uno.clicked.connect(self.un)
        self.dos.clicked.connect(self.do)
        self.tres.clicked.connect(self.tre)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.uno.show()
        self.dos.show()
        self.tres.show()

    def un(self):
        self.inicio.emit("Chau")

    def do(self):
        self.inicio.emit("Sans")

    def tre(self):
        self.inicio.emit("Hernán")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Legend of Progra'
        self.imagenes = []
        self.deleted = []
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.run)
        self.llamadas_a_tienda = 0
        self.compras = []
        self.holdon = False
        self.campeon = ""
        self.puntos = 0

        self.clock = QTimer()
        self.clock.setSingleShot(False)
        self.clock.setInterval(1000)
        self.time = 0
        self.last = 0
        self.clock.timeout.connect(self.pasar_tiempo)
        self.spwn = 0
        self.edificios = 0
        self.inhibidor_out_amigo = 0
        self.inhibidor_out_enemigo = 0

        self.temp = dict()
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.labels = dict()
        self.pixmaps = dict()
        self.bars = dict()

        self.dicc_todos = dict()
        self.perso_enemigo = random.choice(("Noob", "Normal", "Ragequitter"))
        print(self.perso_enemigo)

        self.threads = []
        self.log_queue = []

        self.w_height = 1000
        self.w_width = 1500
        self.enable = [True, True]
        self.initUI()

    def dict_deleter(self, dicc, key):
        aux = dict()
        for a in dicc:
            k = dicc[a]
            if a != key:
                aux[a] = k
        return aux

    def pasar_tiempo(self):
        self.time += 1
        print("Tick     {}".format(self.time))
        self.spwn = 0
        for a in self.dicc_todos:
            actor = self.dicc_todos[a]
            if actor.counter == -1:
                actor.counter = 0
            actor.siendo_atacado = False
            actor.atacando_a = -1

    def revivir_campeon(self, id):
        for l in self.labels:
            if l == id:
                label = self.labels[l]
                label.show()
                label.setVisible(True)
        for i in self.dicc_todos:
            if i == id:
                campeon = self.dicc_todos[i]
                campeon.waiting = False
                campeon.revival_timer.stop()

    def revivir_inhibidor(self, id):
        for l in self.labels:
            if l == id:
                label = self.labels[l]
                label.show()
                label.setVisible(True)
        for i in self.dicc_todos:
            if i == id:
                inhibidor = self.dicc_todos[i]
                inhibidor.revival_timer.stop()
                if inhibidor.ia[0] == "Amigo":
                    self.inhibidor_out_amigo = 0
                else:
                    self.inhibidor_out_enemigo = 0

    def poblar(self):
        # self.x = backend.Sans(self.imagenes, self.w_height - 200, self.w_width - 200, ("Enemigo", "Auto"), 0)
        # self.y = backend.Subdito(pyqtSignal(tuple), self.imagenes,
        # self.w_height - 500, self.w_width - 500, ("Enemigo", "Auto"), 1)

        self.agregar_actor(backend.Edificio(self.imagenes, "Torre", 450, 450, ("Amigo", "Auto"), 4))
        self.agregar_actor(backend.Edificio(self.imagenes, "Torre", 900, 500, ("Enemigo", "Auto"), 5))
        self.agregar_actor(backend.Edificio(self.imagenes, "Nexo", 100, 100, ("Amigo", "Auto"), 6))
        self.agregar_actor(backend.Edificio(self.imagenes, "Nexo", 1200, 700, ("Enemigo", "Auto"), 7))
        self.agregar_actor(backend.Edificio(self.imagenes, "Inhibidor", 300, 350, ("Amigo", "Auto"), 1))
        self.agregar_actor(backend.Edificio(self.imagenes, "Inhibidor", 1050, 650, ("Enemigo", "Auto"), 2))

        self.agregar_actor(backend.Sans(self.imagenes, 50, 60, ("Amigo", "Teleop"), 3, self.campeon))
        self.agregar_actor(backend.Sans(self.imagenes, 1450, 940, ("Enemigo", "Auto"), 0))

        self.clock.start()
        if len(self.dicc_todos) > 1:
            i = 0
            for ac in self.dicc_todos:
                i += 1
                actor = self.dicc_todos[ac]
                actor.delay = i
                actor.start()
        else:
            if len(self.dicc_todos) > 0:
                for ac in self.dicc_todos:
                    actor = self.dicc_todos[ac]
                    actor.start()

    def agregar_actor(self, actor):
        if actor.id not in self.dicc_todos.keys():
            # o = QThread()
            # actor.moveToThread(o)
            if actor.nombre == "Sans":
                # actor.data0.connect(self.ide0)
                actor.data0.connect(self.ide)
                actor.revive.connect(self.revivir_campeon)
                # actor.aux_obj.connect(self.ide)

            elif actor.nombre == "Pengu":
                # actor.data1.connect(self.ide1)
                actor.data1.connect(self.ide)

            elif actor.tipo == "Edificio":
                actor.data4.connect(self.ide)
                actor.revive.connect(self.revivir_inhibidor)
            # o.start()
            # self.threads.append(o)
            self.dicc_todos[actor.id] = actor
            return actor

    def ide0(self, *args):
        # self.waitpls[1].lock()
        args = args[0]
        if len(self.log_queue) != 0:
            if args[3] != self.log_queue[0][3]:
                self.log_queue.append(args)
            print("SIGNAL IDE TABLERO, CONTENIDO -> {}".format(str(self.log_queue[0])))
        else:
            self.log_queue.append(args)
            print("SIGNAL IDE TABLERO, CONTENIDO -> {}".format(str(self.log_queue[0])))
        if len(self.log_queue) >= 1:
            del self.log_queue[0]
            # self.waitpls[1].unlock()
            # self.waitpls[1] = QMutex()

    def ide1(self, *args):
        # self.waitpls[1].lock()
        args = args[0]
        if len(self.log_queue) != 0:
            if args[3] != self.log_queue[0][3]:
                self.log_queue.append(args)
            print("SIGNAL IDE TABLERO, CONTENIDO -> {}".format(str(self.log_queue[0])))
        else:
            self.log_queue.append(args)
            print("SIGNAL IDE TABLERO, CONTENIDO -> {}".format(str(self.log_queue[0])))
        if len(self.log_queue) >= 1:
            del self.log_queue[0]
            # self.waitpls[1].unlock()
            # self.waitpls[1] = QMutex()

    def run(self):
        QApplication.instance().processEvents()
        # for actor in self.dicc_todos:
        # act = self.dicc_todos[actor]
        if self.holdon is False:
            #self.ruteo()
            self.spawn()
            finish = self.ataquen(self.time)
            if finish == "FINISH":
                for i in self.dicc_todos:
                    ed = self.dicc_todos[i]
                    if ed.tipo == "Edificio":
                        if ed.rango_e == "Nexo" and ed.vida == 0:
                            otro = ""
                            if ed.ia[0] == "Amigo":
                                otro = "Enemigo"
                            elif ed.ia[0] == "Enemigo":
                                otro = "Amigo"
                            print("El equipo {} ha destruido el Nexo {} y ha ganado la partida!".format(ed.ia[0], otro))
                            QApplication.closeAllWindows()
                            return

    def ataquen(self, tiempo):
        poss = dict()
        for o in self.dicc_todos:
            a = self.dicc_todos[o]
            poss[a.position] = a
        for co in poss:
            QApplication.processEvents()
            posicion = co
            actor = poss[co]
            for c in poss:
                pos = c
                ac = poss[c]
                xt = pos[0] - posicion[0]
                yt = pos[1] - posicion[1]
                dis = math.sqrt(xt ** 2 + yt ** 2)
                if self.time != tiempo + 1:
                    if (ac.ia[0] == "Amigo" and actor.ia[0] == "Enemigo") or \
                            (ac.ia[0] == "Enemigo" and actor.ia[0] == "Amigo"):
                        d = True
                        campeon_id = ""
                        if ac.tipo == "Edificio":
                            if ac.rango_e != "Torre":
                                d = False
                        if d:
                            if ac.nombre != "Chau" and ac.counter < ac.vel_ataque and ac.counter != -1\
                                    and dis <= ac.rango and ac.teleop_ahora is False:
                                if ac.tipo == "Edificio":
                                    lock = True
                                    lock1 = True
                                    for c in self.dicc_todos:
                                        cam = self.dicc_todos[c]
                                        if cam.tipo == "Campeón" and cam.ia[0] == ac.ia[0]:
                                            if cam.siendo_atacado is True:
                                                lock = False
                                                if actor.atacando_a == cam.id:
                                                    ac.counter += 1
                                                    actor.siendo_atacado = True
                                                    ac.atacando_a = actor.id
                                                    actor.vida -= ac.daño
                                                    print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                          "HP: {}  {}  Counters:   {}  {}".format(
                                                            ac.nombre, ac.ia[0], ac.id,
                                                            actor.nombre, actor.ia[0], actor.id, ac.id, ac.vida,
                                                            actor.vida, ac.counter, actor.counter))
                                    if lock:
                                        if actor.tipo == "Súbdito":
                                            if actor.tamaño == "Grande":
                                                lock1 = False
                                                ac.counter += 1
                                                ac.atacando_a = actor.id
                                                actor.siendo_atacado = True
                                                actor.vida -= ac.daño
                                                print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   HP: {}  {} "
                                                      " Counters:   {}  {}".format(
                                                        ac.nombre, ac.ia[0], ac.id,
                                                        actor.nombre, actor.ia[0], actor.id, ac.id, ac.vida,
                                                        actor.vida, ac.counter, actor.counter))
                                    if lock1:
                                        if actor.vida < 50:
                                            ac.counter += 1
                                            actor.vida -= ac.daño
                                            ac.atacando_a = actor.id
                                            actor.siendo_atacado = True
                                            print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                  "HP: {}  {}  Counters:   {}  {}".format(
                                                    ac.nombre, ac.ia[0], ac.id,
                                                    actor.nombre, actor.ia[0], actor.id, ac.id, ac.vida,
                                                    actor.vida, ac.counter, actor.counter))
                                elif ac.tipo == "Súbdito":
                                    print("PROCESANDO SUBDITO")
                                    lock = True
                                    for c in self.dicc_todos:
                                        cam = self.dicc_todos[c]
                                        if cam.tipo == "Campeón" and cam.ia[0] == ac.ia[0]:
                                            print("Found campeon")
                                            campeon_id = cam.id
                                            if cam.siendo_atacado is True:
                                                print("Campeón es atacado")
                                                lock = False
                                                if actor.atacando_a == cam.id:
                                                    print("{} DEFENDIENDO A CAMPEÓN".format(ac.id))
                                                    ac.counter += 1
                                                    actor.siendo_atacado = True
                                                    ac.atacando_a = actor.id
                                                    actor.vida -= ac.daño
                                                    print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                          "HP: {}  {}  Counters:   {}  {}".format(
                                                        ac.nombre, ac.ia[0], ac.id,
                                                        actor.nombre, actor.ia[0], actor.id, ac.id, ac.vida,
                                                        actor.vida, ac.counter, actor.counter))
                                    if lock:
                                        for a in self.dicc_todos:
                                            acto = self.dicc_todos[a]
                                            if acto.tipo == "Edificio" and acto.ia[0] != ac.ia[0]:
                                                print("PENGU YENDO A EDIFICIO")
                                                if (ac.ia[0] == "Amigo" and self.inhibidor_out_enemigo == 0)\
                                                        or (ac.ia[0] == "Enemigo" and self.inhibidor_out_amigo == 0):
                                                    if acto.rango_e == "Torre" or acto.rango_e == "Inhibidor":
                                                        ac.counter += 1
                                                        acto.siendo_atacado = True
                                                        ac.atacando_a = acto.id
                                                        acto.vida -= ac.daño
                                                        print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                              "HP: {}  {}  Counters:   {}  {}".format(
                                                                ac.nombre, ac.ia[0], ac.id,
                                                                acto.nombre, acto.ia[0], acto.id, ac.id, ac.vida,
                                                                acto.vida, ac.counter, acto.counter))
                                                        break
                                                elif (ac.ia[0] == "Amigo" and self.inhibidor_out_enemigo == 1)\
                                                        or (ac.ia[0] == "Enemigo" and self.inhibidor_out_amigo == 1):
                                                    if acto.rango_e == "Torre" or acto.rango_e == "Nexo":
                                                        ac.counter += 1
                                                        acto.siendo_atacado = True
                                                        ac.atacando_a = acto.id
                                                        acto.vida -= ac.daño
                                                        print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                              "HP: {}  {}  Counters:   {}  {}".format(
                                                                ac.nombre, ac.ia[0], ac.id,
                                                                acto.nombre, acto.ia[0], acto.id, ac.id, ac.vida,
                                                                acto.vida, ac.counter, acto.counter))
                                                        break

                                else:
                                    ac.counter += 1
                                    actor.vida -= ac.daño
                                    ac.atacando_a = actor.id
                                    actor.siendo_atacado = True
                                    print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   HP: {}  {}  Counters:   {}  {}".format(
                                        ac.nombre, ac.ia[0], ac.id,
                                        actor.nombre, actor.ia[0], actor.id, ac.id, ac.vida,
                                        actor.vida, ac.counter, actor.counter))

                            elif ac.counter >= ac.vel_ataque and dis <= ac.rango:
                                ac.counter = -1
                            elif dis >= ac.rango:
                                if (ac.tipo == "Súbdito" and (actor.tipo == "Edificio" or actor.atacando_a == campeon_id))\
                                        or ac.tipo == "Campeón":
                                    continu = True
                                    if ac.tipo == "Súbdito" and actor.tipo == "Edificio":
                                        if actor.rango_e == "Nexo" and (ac.ia[0] != actor.ia[0]):
                                            if actor.ia[0] == "Amigo" and self.inhibidor_out_amigo != 1:
                                                continu = False
                                            elif actor.ia[0] == "Enemigo" and self.inhibidor_out_enemigo != 1:
                                                continu = False
                                        elif (actor.rango_e == "Torre" or actor.rango_e == "Inhibidor") \
                                                and actor.vida == 0:
                                            continu = False
                                    if ac.ia[1] == "Teleop":
                                        continu = False
                                    if continu:
                                        if ac.position[0] >= actor.position[0]:
                                            m = -ac.rango
                                        else:
                                            m = ac.rango
                                        if ac.position[1] >= actor.position[1]:
                                            mn = -ac.rango
                                        else:
                                            mn = ac.rango
                                        ac.target = (actor.position[0] + m, actor.position[1] + mn)

                        d = True
                        if actor.tipo == "Edificio":
                            if actor.rango_e != "Torre":
                                d = False
                        if d:
                            if actor.nombre != "Chau" and actor.counter < actor.vel_ataque and actor.counter != -1\
                                    and dis <= actor.rango and actor.teleop_ahora is False:
                                if actor.tipo == "Edificio":
                                    lock = True
                                    lock1 = True
                                    for c in self.dicc_todos:
                                        cam = self.dicc_todos[c]
                                        if cam.tipo == "Campeón" and cam.ia[0] == actor.ia[0]:
                                            if cam.siendo_atacado is True:
                                                lock = False
                                                if ac.atacando_a == cam.id:
                                                    actor.counter += 1
                                                    ac.siendo_atacado = True
                                                    actor.atacando_a = ac.id
                                                    ac.vida -= actor.daño
                                                    print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |  "
                                                          " HP: {}  {}  Counters:   {}  {}".format(
                                                            ac.nombre, ac.ia[0], ac.id,
                                                            actor.nombre, actor.ia[0], actor.id, actor.id, ac.vida,
                                                            actor.vida, ac.counter, actor.counter))
                                    if lock:
                                        if ac.tipo == "Súbdito":
                                            if ac.tamaño == "Grande":
                                                lock1 = False
                                                actor.counter += 1
                                                actor.atacando_a = ac.id
                                                ac.siendo_atacado = True
                                                ac.vida -= actor.daño
                                                print(
                                                    "ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                    "HP: {}  {}  Counters:   {}  {}".format(
                                                        ac.nombre, ac.ia[0], ac.id,
                                                        actor.nombre, actor.ia[0], actor.id, actor.id, ac.vida,
                                                        actor.vida, ac.counter, actor.counter))
                                    if lock1:
                                        if ac.vida < 50:
                                            actor.counter += 1
                                            ac.vida -= actor.daño
                                            actor.atacando_a = ac.id
                                            ac.siendo_atacado = True
                                            print(
                                                "ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                "HP: {}  {}  Counters:   {}  {}".format(
                                                    ac.nombre, ac.ia[0], ac.id,
                                                    actor.nombre, actor.ia[0], actor.id, actor.id, ac.vida,
                                                    actor.vida, ac.counter, actor.counter))
                                elif actor.tipo == "Súbdito":
                                    print("PROCESANDO SUBDITO")
                                    lock = True
                                    for c in self.dicc_todos:
                                        cam = self.dicc_todos[c]
                                        if cam.tipo == "Campeón" and cam.ia[0] == actor.ia[0]:
                                            print("Found campeon")
                                            if cam.siendo_atacado is True:
                                                lock = False
                                                if ac.atacando_a == cam.id:
                                                    print("{} DEFENDIENDO A CAMPEÓN".format(actor.id))
                                                    actor.counter += 1
                                                    ac.siendo_atacado = True
                                                    actor.atacando_a = ac.id
                                                    ac.vida -= actor.daño
                                                    print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |  "
                                                          " HP: {}  {}  Counters:   {}  {}".format(
                                                            ac.nombre, ac.ia[0], ac.id,
                                                            actor.nombre, actor.ia[0], actor.id, actor.id, ac.vida,
                                                            actor.vida, ac.counter, actor.counter))
                                    if lock:
                                        for a in self.dicc_todos:
                                            acto = self.dicc_todos[a]
                                            if acto.tipo == "Edificio" and acto.ia[0] != ac.ia[0]:
                                                print("PENGU YENDO A EDIFICIO")
                                                if (actor.ia[0] == "Amigo" and self.inhibidor_out_enemigo == 0) \
                                                        or (actor.ia[0] == "Enemigo" and self.inhibidor_out_amigo == 0):
                                                    if acto.rango_e == "Torre" or acto.rango_e == "Inhibidor":
                                                        actor.counter += 1
                                                        acto.siendo_atacado = True
                                                        actor.atacando_a = acto.id
                                                        acto.vida -= actor.daño
                                                        print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                              "HP: {}  {}  Counters:   {}  {}".format(
                                                                actor.nombre, actor.ia[0], actor.id,
                                                                acto.nombre, acto.ia[0], acto.id, actor.id, actor.vida,
                                                                acto.vida, actor.counter, acto.counter))
                                                        break
                                                elif (actor.ia[0] == "Amigo" and self.inhibidor_out_enemigo == 1) \
                                                        or (actor.ia[0] == "Enemigo" and self.inhibidor_out_amigo == 1):
                                                    if acto.rango_e == "Torre" or acto.rango_e == "Nexo":
                                                        actor.counter += 1
                                                        acto.siendo_atacado = True
                                                        actor.atacando_a = acto.id
                                                        acto.vida -= actor.daño
                                                        print("ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   "
                                                              "HP: {}  {}  Counters:   {}  {}".format(
                                                                actor.nombre, actor.ia[0], actor.id,
                                                                acto.nombre, acto.ia[0], acto.id, actor.id, actor.vida,
                                                                acto.vida, actor.counter, acto.counter))
                                                        break
                                else:
                                    actor.counter += 1
                                    ac.vida -= actor.daño
                                    ac.siendo_atacado = True
                                    actor.atacando_a = ac.id
                                    print(
                                        "ENGAGE:  {}-{}-{}  {}-{}-{}  <{}>  |   HP: {}  {}  Counters:   {}  {}".format(
                                            ac.nombre, ac.ia[0], ac.id,
                                            actor.nombre, actor.ia[0], actor.id, actor.id, ac.vida,
                                            actor.vida, ac.counter, actor.counter))
                            elif actor.counter >= actor.vel_ataque and dis <= actor.rango:
                                actor.counter = -1

                    if ac.vida == 0 and ac.tipo == "Súbdito":
                        self.dicc_todos = self.dict_deleter(self.dicc_todos, ac.id)
                        if str(ac.id) not in self.deleted:
                            ac.waiting = True
                            ac.stop()
                        for l in self.labels:
                            if l == ac.id and l not in self.deleted:
                                label = self.labels[l]
                                label.setVisible(False)
                                label.clear()
                                label.deleteLater()
                                self.deleted.append(l)
                                self.labels = self.dict_deleter(self.labels, l)
                                ac.deleteLater()
                        if actor.tipo == "Campeón" and actor.ia[0] == "Amigo":
                            self.puntos += 1

                    elif ac.vida == 0 and ac.tipo == "Campeón":
                        ac.waiting = True
                        ac.muertes += 1
                        ac.revival_timer.setInterval(10000 * (1.1 ** actor.muertes))
                        if ac.ia[0] == "Amigo":
                            ac.position = (50, 60)
                        else:
                            ac.position = (1450, 940)
                        ac.revival_timer.start()
                        for l in self.labels:
                            if l == ac.id:
                                label = self.labels[l]
                                label.setVisible(False)
                        if actor.tipo == "Campeón" and actor.ia[0] == "Amigo":
                            self.puntos += 5

                    elif ac.vida == 0 and ac.tipo == "Edificio":
                        if ac.rango_e == "Inhibidor":
                            ac.revival_timer.start()
                            if ac.ia[0] == "Amigo":
                                self.inhibidor_out_amigo = 1
                            else:
                                self.inhibidor_out_enemigo = 1
                            for l in self.labels:
                                if l == ac.id:
                                    label = self.labels[l]
                                    label.setVisible(False)
                            if actor.tipo == "Campeón" and actor.ia[0] == "Amigo":
                                self.puntos += 15
                        elif ac.rango_e == "Nexo":
                            return "FINISH"
                        elif ac.rango_e == "Torre":
                            self.dicc_todos = self.dict_deleter(self.dicc_todos, ac.id)
                            if str(ac.id) not in self.deleted:
                                ac.waiting = True
                                ac.stop()
                            for l in self.labels:
                                if l == ac.id and l not in self.deleted:
                                    label = self.labels[l]
                                    label.setVisible(False)
                                    label.clear()
                                    label.deleteLater()
                                    self.deleted.append(l)
                                    self.labels = self.dict_deleter(self.labels, l)
                                    ac.deleteLater()
                            if actor.tipo == "Campeón" and actor.ia[0] == "Amigo":
                                self.puntos += 15

                    if actor.vida == 0 and actor.tipo == "Campeón":
                        actor.waiting = True
                        actor.muertes += 1
                        actor.revival_timer.setInterval(10000 * (1.1 ** actor.muertes))
                        if actor.ia[0] == "Amigo":
                            actor.position = (50, 60)
                        else:
                            actor.position = (1450, 940)
                        actor.revival_timer.start()
                        for l in self.labels:
                            if l == actor.id:
                                label = self.labels[l]
                                label.setVisible(False)
                        if ac.tipo == "Campeón" and ac.ia[0] == "Amigo":
                            self.puntos += 5

                    elif actor.vida == 0 and actor.tipo == "Súbdito":
                        self.dicc_todos = self.dict_deleter(self.dicc_todos, actor.id)
                        if str(actor.id) not in self.deleted:
                            actor.waiting = True
                            actor.stop()
                        for l in self.labels:
                            if l == str(actor.id) and l not in self.deleted:
                                print("pass")
                                print(actor.id)
                                label = self.labels[l]
                                label.setVisible(False)
                                label.clear()
                                label.deleteLater()
                                self.deleted.append(l)
                                self.labels = self.dict_deleter(self.labels, l)
                                actor.deleteLater()
                        if ac.tipo == "Campeón" and ac.ia[0] == "Amigo":
                            self.puntos += 1

                    elif actor.vida == 0 and actor.tipo == "Edificio":
                        if actor.rango_e == "Inhibidor":
                            actor.revival_timer.start()
                            if actor.ia[0] == "Amigo":
                                self.inhibidor_out_amigo = 1
                            else:
                                self.inhibidor_out_enemigo = 1
                            for l in self.labels:
                                if l == actor.id:
                                    label = self.labels[l]
                                    label.setVisible(False)
                            if ac.tipo == "Campeón" and ac.ia[0] == "Amigo":
                                self.puntos += 15
                        elif actor.rango_e == "Nexo":
                            return "FINISH"
                        elif actor.rango_e == "Torre":
                            self.dicc_todos = self.dict_deleter(self.dicc_todos, actor.id)
                            if str(actor.id) not in self.deleted:
                                actor.waiting = True
                                actor.stop()
                            for l in self.labels:
                                if l == actor.id and l not in self.deleted:
                                    label = self.labels[l]
                                    label.setVisible(False)
                                    label.clear()
                                    label.deleteLater()
                                    self.deleted.append(l)
                                    self.labels = self.dict_deleter(self.labels, l)
                                    actor.deleteLater()
                            if ac.tipo == "Campeón" and ac.ia[0] == "Amigo":
                                self.puntos += 15

    def spawn(self):
        if self.time % 10 == 0 and self.time != 0 and self.spwn == 0:
            self.spwn = 1
            ids = []
            grandes_amigos = 0
            chicos_amigos = 0
            grandes_enemigos = 0
            chicos_enemigos = 0
            lista = []
            for a in self.dicc_todos:
                ids.append(a)
            for i in range(0, 10000):
                if i not in ids and i not in self.deleted:
                    QApplication.processEvents()
                    if grandes_amigos < 1:
                        grandes_amigos += 1
                        r = self.agregar_actor(backend.Subdito(self.imagenes,
                                                                30 + 3*i, 20 + i, ("Amigo", "Auto"), i, "Grande"))
                        lista.append(r)
                    elif chicos_amigos < 4:
                        chicos_amigos += 1
                        r = self.agregar_actor(backend.Subdito(self.imagenes,
                                                                5 + i, 5 + i, ("Amigo", "Auto"), i, "Chico"))
                        lista.append(r)
                    elif grandes_enemigos < 1:
                        grandes_enemigos += 1
                        r = self.agregar_actor(backend.Subdito(self.imagenes,
                                                                1400 - i, 900 - i, ("Enemigo", "Auto"), i, "Grande"))
                        lista.append(r)
                    elif chicos_enemigos < 4:
                        chicos_enemigos += 1
                        r = self.agregar_actor(backend.Subdito(self.imagenes,
                                                                1390 - i, 980 - 3*i, ("Enemigo", "Auto"), i, "Chico"))
                        lista.append(r)
                    if chicos_amigos == 4 and chicos_enemigos == 4 and grandes_enemigos == 1 \
                            and grandes_enemigos == 1:
                        break
            if len(lista) > 1:
                n = 0
                for actor in lista:
                    n += 1
                    actor.delay = n
                    print("Spawning subdito {} {}:  {}".format(actor.ia[0], actor.tamaño, actor.position))
                    actor.start()

    def ruteo(self):
        if self.enable[1]:
            lista_rutas = []
            for actoruno in self.dicc_todos:
                actor = self.dicc_todos[actoruno]
                lista_rutas.append((actor.id, actor.rate, actor.position, actor.target, (actor.x, actor.y)))
            if len(lista_rutas) > 1:
                revisadas = []
                for ruta in lista_rutas:
                    x = ruta[2][0] + ruta[4][0] + ruta[1] + 20
                    y = ruta[2][1] + ruta[4][1] + ruta[1] + 20
                    for rutauno in lista_rutas:
                        if ruta != rutauno:
                            xaux = rutauno[2][0] + rutauno[4][0] + rutauno[1]
                            yaux = rutauno[2][1] + rutauno[4][1] + rutauno[1]
                            actores = []
                            tolx = abs(rutauno[4][0] + ruta[4][0])
                            if tolx == 0:
                                tolx = abs(ruta[4][0]) + 10
                            toly = abs(rutauno[4][1] + ruta[4][1])
                            if toly == 0:
                                toly = abs(ruta[4][1]) + 10
                            if abs(x - xaux) <= tolx and abs(y - yaux) <= toly:
                                if (ruta[0], rutauno[0]) not in revisadas:
                                    revisadas.append((ruta[0], rutauno[0]))
                                    revisadas.append((rutauno[0], ruta[0]))
                                    for ac in self.dicc_todos:
                                        actor = self.dicc_todos[ac]
                                        if actor.id == ruta[0]:
                                            actores.append(actor)
                                        elif actor.id == rutauno[0]:
                                            actores.append(actor)
                            if len(actores) == 2:
                                control = True
                                # print("ARREGLANDO RUTA COLISIÓN")
                                # print((ruta[0], x, y, ruta[2]))
                                # print("Revisando ruta con {}".format(rutauno[0]))
                                # print((rutauno[0], xaux, yaux, rutauno[2]))
                                if actores[0].waiting is False and actores[1].waiting is False:
                                    if actores[1].tipo == "Edificio":
                                        if actores[0].tipo == "Edificio":
                                            control = False
                                        else:
                                            a = actores[0]
                                            b = actores[1]
                                            actores = list()
                                            actores.append(b)
                                            actores.append(a)
                                    if control:
                                        actores[0].waiting = True
                                        uno = actores[1].target[0]
                                        dos = actores[1].target[1]
                                        tres = actores[0].target[0]
                                        cuatro = actores[0].target[1]
                                        if abs(y - yaux) <= toly and actores[0].ia[0] != actores[1].ia[0]:
                                            if actores[0].target[0] in range(int(uno) - 4, int(uno) + 4)\
                                                    and actores[0].target[1] in range(int(dos) - 4, int(dos) + 4):
                                                t = dos - cuatro
                                                if t >= 0:
                                                    actores[1].target = (actores[1].target[0], actores[1].target[1]
                                                                         + 1.5*(actores[0].position[1] - actores[1].position[1]))
                                                else:
                                                    actores[1].target = (actores[1].target[0], actores[1].target[1]
                                                                         - 1.5 * (
                                                                         actores[0].position[1] - actores[1].position[1]))
                                            avance = 0
                                            uo = actores[0].target[1]
                                            ds = actores[1].target[1]
                                            while 2*yaux / (200 + toly) - avance > 0 and abs(uo - ds) <= toly:
                                                uo = actores[0].target[1]
                                                ds = actores[1].target[1]
                                                r = 0
                                                if abs(actores[0].position[0] - actores[1].target[0]) \
                                                        in range(toly - 3, toly + 3):
                                                    r = rutauno[1] / 2*(200 + toly)
                                                avance += rutauno[1] / (200 + toly) - r
                                                actores[1].position = (
                                                actores[1].position[0], actores[1].position[1] + rutauno[1]/(200 + toly) - r)
                                            actores[0].waiting = False
                                        if abs(x - xaux) <= tolx and actores[0].ia[0] != actores[1].ia[0]:
                                            if actores[0].target[0] in range(int(uno) - 4, int(uno) + 4) \
                                                    and actores[0].target[1] in range(int(dos) - 4, int(dos) + 4):
                                                t = uno - tres
                                                if t >= 0:
                                                    actores[1].target = (actores[1].target[0] +
                                                                         1.5*(actores[0].position[0] - actores[1].position[0]),
                                                                         actores[1].target[1])
                                                else:
                                                    actores[1].target = (actores[1].target[0] -
                                                                         1.5 * (
                                                                         actores[0].position[0] - actores[1].position[0]),
                                                                         actores[1].target[1])
                                            avance = 0
                                            uno = actores[0].target[0]
                                            dos = actores[1].target[0]
                                            while 2*xaux / (200 + tolx) - avance > 0 and abs(uno - dos) <= tolx:
                                                r = 0
                                                if abs(actores[0].position[1] - actores[1].target[1]) \
                                                        in range(tolx - 3, tolx + 3):
                                                    r = rutauno[1] / 2*(200 + toly)
                                                avance += rutauno[1] / (200 + tolx) - r
                                                actores[1].position = (
                                                actores[1].position[0] + rutauno[1] / (200 + tolx) - r, actores[1].position[1])
                                                uno = actores[0].target[0]
                                                dos = actores[1].target[0]

                                            actores[0].waiting = False
            else:
                self.enable[1] = False

    def setter(self, s):
        self.campeon = s

    def hider(self):
        print("HIDING")
        self.expiry_timer = QTimer()
        self.expiry_timer.setInterval(2000)
        self.expiry_timer.setSingleShot(True)
        self.expiry_timer.timeout.connect(self.hider)
        for coso in self.temp:
            cosa = self.temp[coso]
            cosa.setVisible(False)

    def iniciar(self):
        inici = inicio()
        inici.inicio.connect(self.setter)
        inici.exec_()

    def initUI(self):
        self.iniciar()
        lista = tuple(Imgs.all[1])
        for dire in lista:
            aux = dire.split("\\")
            y = aux[len(aux) - 1]
            q = (y, dire)
            self.imagenes.append(q)

        self.ModGridLayout()
        self.setWindowTitle(self.title)

        self.show()
        self.poblar()
        self.timer.start()

    def ide(self, data):
        # print("RECEIVING TO GRAPH")
        QApplication.processEvents()
        self.showr.setText("Puntos: " + str(self.puntos))
        self.showr.setVisible(True)
        self.showr.show()
        if isinstance(data, tuple):
            if len(data) == 5:
                keys = []
                cmon = True
                for a in self.dicc_todos:
                    actor = self.dicc_todos[a]
                    if actor.id == data[0] and actor.tipo == "Edificio":
                        self.edificios += 1
                        if self.edificios == 6:
                            cmon = False
                if cmon:
                    for i in self.labels:
                        keys.append(str(i))
                    if str(data[0]) not in keys:
                        label = QLabel(str(data[0]), self)
                        bar = QProgressBar(self)
                        self.bars[data[0]] = bar
                        bar.resize(5, data[1][1])
                        label.setGeometry(data[1][0], data[1][1], data[1][0], data[1][1])
                        p = QPixmap(data[2])
                        label.setPixmap(p)
                        label.move(*data[3])
                        bar.setRange(0, data[4])
                        bar.move(data[3][0], data[3][1] + data[1][1] + 5)
                        label.show()
                        label.setVisible(True)
                        bar.raise_()
                        bar.show()
                        bar.setVisible(True)
                        self.labels[str(data[0])] = label
                        self.pixmaps[data[2]] = p
                    else:
                        for ite in self.labels:
                            key = str(ite)
                            if key == str(data[0]):
                                label = self.labels[key]
                                n = 0
                                for i in self.pixmaps:
                                    pix = self.pixmaps[i]
                                    if i == data[2]:
                                        n = 1
                                        label.setPixmap(pix)
                                if n == 0:
                                    p = QPixmap(data[2])
                                    label.setPixmap(p)
                                    self.pixmaps[data[2]] = p
                                label.move(*data[3])
                                label.show()
                                label.setVisible(True)
                                for l in self.bars:
                                    if l == data[0]:
                                        bar = self.bars[l]
                                        bar.move(data[3][0], data[3][1] + data[1][1] + 5)
                                        bar.setValue(data[4])
                                        bar.raise_()
                                        bar.show()
                                        bar.setVisible(True)

            elif len(data) == 3:
                if data[0] == "Sans":
                    # self.expiry_timer.start()
                    movie = QMovie(data[1])
                    if len(self.temp) == 0:
                        print("FIRST TIME SANS SPECIAL")
                        # self.expiry_timer.start()
                        for i in range(0, 4):
                            a = data[2][i]
                            label = QLabel(data[0] + "GasterBlaster", self)
                            label.setMovie(movie)
                            label.show()
                            label.move(*a)
                            label.setVisible(True)
                            self.temp[i] = label
                    else:
                        if not self.expiry_timer.isActive():
                            self.expiry_timer.start()
                        else:
                            self.expiry_timer.stop()
                            self.expiry_timer = QTimer()
                            self.expiry_timer.setInterval(2000)
                            self.expiry_timer.setSingleShot(True)
                            self.expiry_timer.timeout.connect(self.hider)

                        for cosa in self.temp:
                            print("Setting visible")
                            coso = self.temp[cosa]
                            coso.show()
                            coso.setVisible(True)

    def mousePressEvent(self, QMouseEvent):
        pos = (QMouseEvent.x(), QMouseEvent.y())
        for item in self.dicc_todos:
            campeon = self.dicc_todos[item]
            if campeon.tipo == "Campeón" and campeon.ia[0] == "Amigo":
                if campeon.ia[1] == "Teleop":
                    campeon.changesprite = pos
                    campeon.target = pos
                    campeon.automatico = True

    def keyPressEvent(self, e):
        n = e.key()
        QApplication.processEvents()
        if n == Qt.Key_W:
            for c in self.dicc_todos:
                campeon = self.dicc_todos[c]
                if campeon.ia[1] == "Teleop" and campeon.tipo == "Campeón":
                    campeon.cte = 1
                    campeon.active = True
                    campeon.automatico = False
        elif n == Qt.Key_I:
            self.iniciar()

        elif n == Qt.Key_O:
            self.tienda()

        elif n == Qt.Key_P:
            for i in self.dicc_todos:
                actor = self.dicc_todos[i]
                if actor.waiting is True:
                    actor.waiting = False
                elif actor.waiting is False:
                    actor.waiting = True
            if self.holdon is False:
                self.holdon = True
            else:
                self.holdon = False

        elif n == Qt.Key_A:
            for c in self.dicc_todos:
                campeon = self.dicc_todos[c]
                if campeon.ia[1] == "Teleop" and campeon.tipo == "Campeón":
                    campeon.cte = -2
                    campeon.active = True
                    campeon.automatico = False
        elif n == Qt.Key_S:
            for c in self.dicc_todos:
                campeon = self.dicc_todos[c]
                if campeon.ia[1] == "Teleop" and campeon.tipo == "Campeón":
                    campeon.cte = -1
                    campeon.active = True
                    campeon.automatico = False
        elif n == Qt.Key_D:
            for c in self.dicc_todos:
                campeon = self.dicc_todos[c]
                if campeon.ia[1] == "Teleop" and campeon.tipo == "Campeón":
                    campeon.cte = 2
                    campeon.active = True
                    campeon.automatico = False

    def ModGridLayout(self):
        positions = [(i, j) for i in range(20) for j in range(30)]
        names = [str(position) for position in positions]
        done = list()
        for i in positions:
            if i[1] not in done:
                done.append(i[1])
                self.layout.setColumnStretch(i[1], 1)

        # Lo siguiente rellena las posiciones con pasto
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QLabel(name)
            button.setFixedSize(50, 50)
            button.setText(name)
            for img in self.imagenes:
                if "2706961_71630599.jpg" == img[0]:
                    img = QPixmap(img[1])
                    img.scaledToWidth(50)
                    img.scaledToWidth(50)
                    button.setPixmap(img)
                elif "loot.png" == img[0]:
                    pix = QIcon(img[1])
                    F = QPushButton(self)
                    F.setGeometry(230, 30, 50, 50)
                    F.setIcon(pix)
                    F.setVisible(True)
                    F.clicked.connect(self.tienda)
                    F.show()
            h = QPushButton(self)
            h.setGeometry(1430, 30, 50, 50)
            h.setText("Salir al menú")
            h.setVisible(True)
            h.clicked.connect(self.iniciar)
            h.show()
            self.showr = QLabel(self)
            self.showr.setGeometry(750, 950, 100, 50)
            self.showr.setText("Puntos: " + str(self.puntos))
            self.showr.setVisible(True)
            self.showr.raise_()
            self.showr.show()

            self.layout.addWidget(button, *position)

    def tienda(self):
        global campeon
        for i in self.dicc_todos:
            actor = self.dicc_todos[i]
            if actor.ia[0] == "Amigo" and actor.tipo == "Campeón":
                campeon = actor

        def ba():
            global campeon
            actor = campeon
            actor.daño += 2

        def bb():
            global campeon
            campeon.rango += 2

        def bc():
            global campeon
            actor = campeon
            actor.rate += 2

        def bd():
            global campeon
            actor = campeon
            actor.daño += 2

        def be():
            global campeon
            actor = campeon
            actor.daño += 2

        def bf():
            global campeon
            actor = campeon
            a = random.choice("Daño", "Rapidez", "Rango")
            if a == "Daño":
                actor.daño += 6
            elif a == "Rapidez":
                actor.rate += 6
            elif a == "Rango":
                actor.rango += 6
            else:
                actor.daño += 6

        def chooser(tupla):
            n = tupla[0]
            if n == 1:
                ba()
            elif n == 2:
                bb()
            elif n == 3:
                bc()
            elif n == 4:
                bd()
            elif n == 5:
                be()
            elif n == 6:
                bf()

        tienda = Tienda(self.compras, self.llamadas_a_tienda)
        tienda.buy.connect(chooser)

        tienda.exec_()
        self.llamadas_a_tienda += 1
        #tienda.show()


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    # direccion_img = Imgs.all[0]
    # app.addLibraryPath(direccion_img)
    ex = App()
    # ex.tablero.start()
    sys.exit(app.exec_())