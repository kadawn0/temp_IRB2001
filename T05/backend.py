from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
import random
import os
import time
import math


class GameAsset:
    def __init__(self):
        self.nombre = ""
        self.delay = 0.3
        self.siendo_atacado = False
        self.atacando_a = -1
        self._vida = 0
        self.__position = (0, 0)
        self.movil = False
        self.waiting = False
        self.tipo = ""
        self.rango = ""
        self.tamaño = ""
        self.teleop_ahora = False
        self.ia = tuple()
        self.img = "default"
        self.id = 0
        self.w = 1500
        self.h = 1000
        self.muertes = 0

        self._target = (0, 0)
        self._changesprite = tuple()

    @property
    def vida(self):
        if self._vida < 0:
            self._vida = 0
        return self._vida

    @vida.setter
    def vida(self, other):
        self._vida = other

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        height = self.h - 55
        width = self.w - 55
        xt = value[0]
        yt = value[1]
        if self.movil is True:
            if 0 <= yt < height and 0 <= xt < width:
                self.__position = value
            elif xt < 0 < yt < height:
                self.__position = (0, yt)
            elif yt < 0 < xt < width:
                self.__position = (xt, 0)
            elif yt >= height and 0 < xt < width:
                self.__position = (xt, height)
            elif yt >= height and xt < 0:
                self.__position = (0, height)
            elif 0 < yt < height and xt >= width:
                self.__position = (width, yt)
            elif xt >= width and yt < 0:
                self.__position = (width, 0)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, other):
        if self.movil:
            if isinstance(other, tuple) or isinstance(other, list):
                self._target = other

    def cambiar_posicion(self, tx=0, ty=0):
        if self.movil is True:
            self.position = (self.__position[0] + tx, self.__position[1] + ty)


class Sans(QTimer, GameAsset):
    aux_obj = pyqtSignal(tuple)
    data0 = pyqtSignal(tuple)
    revive = pyqtSignal(int)

    def __init__(self, imagenes, x, y, ai, id, nombre="Sans"):
        super().__init__()
        # QThread().__init__(self)
        # super().__init__()
        QTimer().__init__(self)
        self.nombre = nombre

        self.hero_sprites = dict()
        self.imagenes = imagenes
        self.ia = ai
        self.x = 51
        self.y = 71
        self.sans_sprite()

        # Estas son las propiedades que se usarán en el resto del juego
        self.movil = True
        self.__position = (0, 0)
        self.position = (x, y)
        self.tipo = "Campeón"
        self.id = id
        self.waiting = False
        self.cte = 0

        if self.nombre == "Sans":
            self._vida = 400
            self.vel_ataque = 30
            self.daño = 1
            self.rango = 40
            self.rate = 3
        elif self.nombre == "Hernán":
            self._vida = 666
            self.vel_ataque = 10
            self.daño = 20
            self.rango = 5
            self.rate = 10
        elif self.nombre == "Chau":
            self._vida = 500
            self.vel_ataque = 10
            self.daño = 5
            self.rango = 40
            self.rate = 30
        self.nombre = "Sans"
        self.counter = 0
        self.automatico = False

        self.revival_timer = QTimer()
        self.revival_timer.setInterval(10000*(1.1**self.muertes))
        self.revival_timer.setSingleShot(False)
        self.revival_timer.timeout.connect(self.revivirme)

        if self.ia[0] == "Amigo":
            self.img = self.hero_sprites["sans_34_right"]
        else:
            self.img = self.hero_sprites["sans_34_left"]

        self._changesprite = tuple()
        self._target = (100, 600)
        self.ciclo = 0
        self.active = True
        self.inmunidad = 0

        self.setInterval(50)
        self.setSingleShot(False)

        #self.timer.blockSignals(False)
        #self.timer.setSingleShot(False)
        self.timeout.connect(self.doit_shia)
        # self.data0.connect(self.ide)
        self.data0.emit((self.id, (self.x, self.y), self.img, self.position, self.vida))

    @property
    def changesprite(self):
        return self._changesprite

    @changesprite.setter
    def changesprite(self, other):
        if self.ia[1] == "Teleop":
            self._changesprite = other
            absolute = (int(other[0] - round(self.position[0], 0)), int(other[1] - round(self.position[1], 0)))
        else:
            self._changesprite = self.target
            absolute = (int(self.target[0] - round(self.position[0],
                                                   0)), int(self.target[1] - round(self.position[1], 0)))
        if absolute[0] < 0 and absolute[1] < 0:
            self.img = self.hero_sprites["sans_34_left_back"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] in range(-3, 3) and absolute[1] < 0:
            self.img = self.hero_sprites["sans_back"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] in range(-3, 3) and absolute[1] > 0:
            self.img = self.hero_sprites["sans_front"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] > 0 and absolute[1] > 0:
            self.img = self.hero_sprites["sans_34_right"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] > 0 and absolute[1] in range(-3, 3):
            self.img = self.hero_sprites["sans_right"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] < 0 and absolute[1] in range(-3, 3):
            self.img = self.hero_sprites["sans_left"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[1] < 0 < absolute[0]:
            self.img = self.hero_sprites["sans_34_right_back"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))
        elif absolute[0] < 0 < absolute[1]:
            self.img = self.hero_sprites["sans_34_left"]
            self.data0.emit((self.id, (51, 71), self.img, self.position, self.vida))

    def revivirme(self):
        print("Reviviendo a Sans {}".format(self.id))
        self.revive.emit(self.id)

    def ide(self, *args):
        print("SIGNAL IDE SANS, contenido -> {}".format(str(args)))

    def special_attack(self):
        gasterblaster = self.hero_sprites["gb_gif_front"]
        self.aux_obj.emit(("Sans", gasterblaster, ((self.position[0] - 150, self.position[1] - 150),
                                                   (self.position[0] + 150, self.position[1] - 150),
                                                   (self.position[0] - 150, self.position[1] + 150),
                                                   (self.position[0] + 150, self.position[1] + 150))))

    def run(self):
        print("SANS LOOP")
        self.sleep(self.delay)
        while True:
            if self.ia[1] == "Teleop":
                self.active = False
            self.doit_shia()
            time.sleep(0.01)

    def doit_shia(self):
        rate = self.rate
        mov = [0, 0]
        QApplication.instance().processEvents()
        if random.random() >= 0.9:
            self.special_attack()
        if self.ia[1] == "Auto":
            self.changesprite = 1
        if self.target[0] == 0 and self.target[1] == 0:
            self.waiting = True
        else:
            self.waiting = False
        if self.waiting is False:
            if self.ia[0] == "Enemigo" or self.automatico or (self.ia[1] == "Teleop" and self.cte != 0):
                if self.ia[0] == "Enemigo" or self.automatico:
                    self.cte = 1
                    if self.target[0] != 0:
                        if self.target[0] > self.position[0]:
                            mov[0] = rate * self.cte
                        elif self.target[0] < self.position[0]:
                            mov[0] = -rate * self.cte

                    if self.target[1] != 0:
                        if self.target[1] > self.position[1]:
                            mov[1] = rate * self.cte
                        elif self.target[1] < self.position[1]:
                            mov[1] = -rate * self.cte
                    self.cambiar_posicion(*mov)
                    self.data0.emit((self.id, (self.x, self.y), self.img, self.position, self.vida))
                    if self.automatico:
                        if abs(self.target[0] - self.position[0]) in range(-4, 4) \
                                and abs(self.target[1] - self.position[1]) in range(-4, 4):
                            self.automatico = False

                if self.ia[0] == "Amigo" and self.active is True:
                    if self.cte % 2 == 0:
                        if self.cte == 2:
                            if self.img == self.hero_sprites["sans_back"] \
                                    or self.img == self.hero_sprites["sans_front"]\
                                    or self.img == self.hero_sprites["sans_right"]\
                                    or self.img == self.hero_sprites["sans_left"]:
                                if self.img == self.hero_sprites["sans_back"] \
                                        or self.img == self.hero_sprites["sans_front"]:
                                        c = -1
                                        d = 1
                                        e = 1
                                        f = 0
                                else:
                                    c = -1
                                    d = -1
                                    f = 1
                                    e = 0
                            else:
                                c = -1
                                d = 1
                                if self.img == self.hero_sprites["sans_34_right_back"] or\
                                        self.img == self.hero_sprites["sans_34_left_back"]:
                                    e = 1
                                else:
                                    if self.img == self.hero_sprites["sans_34_right"] or\
                                            self.img == self.hero_sprites["sans_34_left"]:
                                        e = -1
                                f = 1
                        else:
                            if self.img == self.hero_sprites["sans_back"] or self.img == \
                                    self.hero_sprites["sans_front"] \
                                    or self.img == self.hero_sprites["sans_right"] \
                                    or self.img == self.hero_sprites["sans_left"]:
                                if self.img == self.hero_sprites["sans_back"] \
                                        or self.img == self.hero_sprites["sans_front"]:
                                        c = 1
                                        d = -1
                                        e = 1
                                        f = 0
                                else:
                                    c = 1
                                    d = 1
                                    f = 1
                                    e = 0
                            else:
                                c = 1
                                d = -1
                                if self.img == self.hero_sprites["sans_34_right_back"] or\
                                    self.img == self.hero_sprites["sans_34_left_back"]:
                                    e = 1
                                else:
                                    if self.img == self.hero_sprites["sans_34_right"] or\
                                            self.img == self.hero_sprites["sans_34_left"]:
                                        e = -1
                                f = 1
                        if self.target[0] > self.position[0]:
                            mov[0] = rate * -c * e
                        elif self.target[0] < self.position[0]:
                            mov[0] = -rate * d * e

                        if self.target[1] > self.position[1]:
                            mov[1] = rate * d * f
                        elif self.target[1] < self.position[1]:
                            mov[1] = -rate * - d * f
                        self.cambiar_posicion(*mov)
                        self.data0.emit((self.id, (self.x, self.y), self.img, self.position, self.vida))
                    else:
                        if self.img == self.hero_sprites["sans_back"] or self.img == \
                                self.hero_sprites["sans_front"] \
                                or self.img == self.hero_sprites["sans_right"] \
                                or self.img == self.hero_sprites["sans_left"]:
                                if self.img == self.hero_sprites["sans_right"] \
                                        or self.img == self.hero_sprites["sans_left"]:
                                    e = 1
                                    f = 0
                                else:
                                    f = 1
                                    e = 0
                        else:
                            e = 1
                            f = 1
                        if self.target[0] > self.position[0]:
                            mov[0] = rate*self.cte * e
                        elif self.target[0] < self.position[0]:
                            mov[0] = -rate*self.cte * e

                        if self.target[1] > self.position[1]:
                            mov[1] = rate*self.cte * f
                        elif self.target[1] < self.position[1]:
                            mov[1] = -rate*self.cte * f
                        self.cambiar_posicion(*mov)
                        self.data0.emit((self.id, (self.x, self.y), self.img, self.position, self.vida))
        self.active = False

    def sans_sprite(self):
        for img in self.imagenes:
            im = img[0]
            imi = img[1]
            if "sans_34_right.png" == im:
                self.hero_sprites["sans_34_right"] = imi
            elif "sans_34_left.png" == im:
                self.hero_sprites["sans_34_left"] = imi
            elif "sans_34_left_back.png" == im:
                self.hero_sprites["sans_34_left_back"] = imi
            elif "sans_34_right_back.png" == im:
                self.hero_sprites["sans_34_right_back"] = imi
            elif "sans_left.png" == im:
                self.hero_sprites["sans_left"] = imi
            elif "sans_right.png" == im:
                self.hero_sprites["sans_right"] = imi
            elif "sans_back.png" == im:
                self.hero_sprites["sans_back"] = imi
            elif "sans_front.png" == im:
                self.hero_sprites["sans_front"] = imi

            elif "1_by_495557939-damspo8.png" == im:
                self.hero_sprites["gb_static_front"] = imi
            elif "custom_sans_sprite__gif_by_baysenahiru427-da3ki6d.gif" == im:
                dir = os.path.dirname(__file__) + "\\Imgs\\" + im
                self.hero_sprites["gb_gif_front"] = dir
        self.imagenes = list()


class Subdito(QTimer, GameAsset):
    data1 = pyqtSignal(tuple)

    def __init__(self, imagenes, x, y, ai, id, tamaño):
        super().__init__()
        # QThread.__init__(self)
        QTimer.__init__(self)
        self.nombre = "Pengu"
        # Lo siguiente es para definir los sprites disponibles y poner el inicial
        self.x = 38
        self.y = 38
        self.hero_sprites = dict()
        self.imagenes = imagenes
        self.subdito_sprite()
        self.ia = ai

        if self.ia[0] == "Amigo":
            self.img = self.hero_sprites["pengu_34_right"]
        else:
            self.img = self.hero_sprites["pengu_34_left"]

        # Estas son las propiedades que se usarán en el resto del juego

        self.movil = True
        self.__position = (x, y)
        self.position = (x, y)
        self.tipo = "Súbdito"
        self.id = id
        self.tamaño = tamaño

        if self.tamaño == "Grande":
            self._vida = 60
            self.rate = 4
            self.vel_ataque = 1
            self.daño = 4
            self.rango = 20
        elif self.tamaño == "Chico":
            self._vida = 45
            self.rate = 4
            self.vel_ataque = 1
            self.daño = 2
            self.rango = 5
        self.counter = 0

        self._changesprite = tuple()
        self.ciclo = 0
        self._target = (100, 300)  # coordenadas relativas
        self.waiting = False

        self.setInterval(50)
        self.setSingleShot(False)
        #self.timer.blockSignals(False)
        #self.timer.setSingleShot(False)
        self.timeout.connect(self.do_stuff_timer)

        # self.data1.connect(self.ide)
        # self.start.connect(self.run)
        self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))

    @property
    def changesprite(self):
        return self._changesprite

    @changesprite.setter
    def changesprite(self, other):
        self._changesprite = self.target
        absolute = (int(self.target[0] - round(self.position[0],
                        0)), int(self.target[1] - round(self.position[1], 0)))
        if absolute[0] < 0 and absolute[1] < 0:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_34_left_back"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_34_left_back_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] in range(-3, 3) and absolute[1] < 0:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_back"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_back_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] in range(-3, 3) and absolute[1] > 0:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_front"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_front_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] > 0 and absolute[1] > 0:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_34_right"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_34_right_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] > 0 and absolute[1] in range(-3, 3):
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_right"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_right_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] < 0 and absolute[1] in range(-3, 3):
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_left"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_left_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[1] < 0 < absolute[0]:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_34_right_back"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_34_right_back_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
        elif absolute[0] < 0 < absolute[1]:
            if self.ciclo == 0:
                self.ciclo += 1
                self.img = self.hero_sprites["pengu_34_left"]
            else:
                self.ciclo = 0
                self.img = self.hero_sprites["pengu_34_left_alt"]
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))
    # Ojo... el pengu no se mueve mucho, tiene una
    # secuencia de caminata de dos ciclos (sus patas no se ven!)

    def ide(self, *args):
        print("SIGNAL IDE PENGU, contenido -> {}".format(str(args)))

    def subdito_sprite(self):
        for img in self.imagenes:
            im = img[0]
            imi = img[1]
            if "2.png" == im:
                self.hero_sprites["pengu_34_right"] = imi
            elif "3.png" == im:
                self.hero_sprites["pengu_34_right_alt"] = imi
            elif "11.png" == im:
                self.hero_sprites["pengu_34_left"] = imi
            elif "12.png" == im:
                self.hero_sprites["pengu_34_left_alt"] = imi
            elif "8.1.png" == im:
                self.hero_sprites["pengu_34_left_back"] = imi
            elif "8.png" == im:
                self.hero_sprites["pengu_34_left_back_alt"] = imi
            elif "6.png" == im:
                self.hero_sprites["pengu_34_right_back"] = imi
            elif "7.png" == im:
                self.hero_sprites["pengu_34_right_back_alt"] = imi
            elif "9.png" == im:
                self.hero_sprites["pengu_left"] = imi
            elif "10.png" == im:
                self.hero_sprites["pengu_left_alt"] = imi
            elif "4.png" == im:
                self.hero_sprites["pengu_right"] = imi
            elif "5.png" == im:
                self.hero_sprites["pengu_right_alt"] = imi
            elif "0 (2).png" == im:
                self.hero_sprites["pengu_back"] = imi
            elif "0 (3).png" == im:
                self.hero_sprites["pengu_back_alt"] = imi
            elif "0.png" == im:
                self.hero_sprites["pengu_front"] = imi
            elif "1.png" == im:
                self.hero_sprites["pengu_front_alt"] = imi
        self.imagenes = list()

    def run(self):
        print("PENGU LOOP")
        # self.position = (self.x, self.y)
        self.sleep(self.delay)
        # self.timer.start()
        while True:
            self.do_stuff_timer()
            time.sleep(0.01)

    def do_stuff_timer(self, *args):
        rate = self.rate
        mov = [0, 0]
        self.changesprite = 1
        QApplication.instance().processEvents()
        if self.target[0] == 0 and self.target[1] == 0:
            self.waiting = True
        else:
            self.waiting = False
        if self.waiting is False:
            if abs(self.target[0] - self.position[0]) > 0:
                if self.target[0] > self.position[0]:
                    mov[0] = rate
                elif self.target[0] < self.position[0]:
                    mov[0] = -rate

            if abs(self.target[1] - self.position[1]) > 0:
                if self.target[1] > self.position[1]:
                    mov[1] = rate
                elif self.target[1] < self.position[1]:
                    mov[1] = -rate

            self.cambiar_posicion(*mov)
            self.data1.emit((self.id, (38, 38), self.img, self.position, self.vida))


class Edificio(QTimer, GameAsset):
    data4 = pyqtSignal(tuple)
    revive = pyqtSignal(int)

    def __init__(self, imagenes, rango, x, y, ia, iid):
        super().__init__()
        # QThread().__init__(self)
        # super().__init__()
        QTimer().__init__(self)
        self.tipo = "Edificio"
        self.nombre = rango
        self.rango_e = rango
        self.id = iid
        self.movil = True
        self.ia = ia

        self.sprites = dict()
        self.imagenes = imagenes
        self.ia = ia
        if self.rango_e == "Nexo":
            self.x = 230
            self.y = 245
        elif self.rango_e == "Torre":
            self.x = 150
            self.y = 150
        elif self.rango_e == "Inhibidor":
            self.x = 190
            self.y = 140

        self.fill_sprite()

        self.__position = (0, 0)
        self.position = (x, y)
        self.movil = False

        if self.rango_e == "Torre":
            self._vida = 250
            self.vel_ataque = 1
            self.daño = 30
            self.rango = 40
            self.counter = 0
            self.rate = 0
            if self.ia[0] == "Amigo":
                self.img = self.sprites["sentry"]
            elif self.ia[0] == "Enemigo":
                self.img = self.sprites["sentry_alt"]
        elif self.rango_e == "Nexo":
            self._vida = 1200
            self.vel_ataque = 0
            self.daño = 0
            self.rango = 0
            self.counter = 0
            self.rate = 0
            self.img = self.sprites["nexo"]
        elif self.rango_e == "Inhibidor":
            self._vida = 600
            self.vel_ataque = 0
            self.daño = 0
            self.rango = 0
            self.counter = 0
            self.rate = 0
            self.img = self.sprites["inhibidor"]

            self.revival_timer = QTimer()
            self.revival_timer.setInterval(30000)
            self.revival_timer.setSingleShot(False)
            self.revival_timer.timeout.connect(self.revivirme)

        self.setInterval(50)
        self.setSingleShot(False)
        self.timeout.connect(self.run)

        print("EDIFICIO {} {} ONLINE".format(self.rango_e, self.ia[0]))

    def revivirme(self):
        if self.rango == "Inhibidor":
            print("Respawn de Inhibidor {}".format(self.ia[0]))
            self.revive.emit(self.id)

    def fill_sprite(self):
        for img in self.imagenes:
            im = img[0]
            imi = img[1]
            if "nexo.png" == im and self.rango_e == "Nexo":
                self.sprites["nexo"] = imi
            elif "inhibidor.png" == im and self.rango_e == "Inhibidor":
                self.sprites["inhibidor"] = imi
            elif "sentry.png" == im and self.rango_e == "Torre" and self.ia[0] == "Amigo":
                self.sprites["sentry"] = imi
            elif "sentry_alt.png" == im and self.rango_e == "Torre" and self.ia[0] == "Enemigo":
                self.sprites["sentry_alt"] = imi

    def run(self):
        self.data4.emit((self.id, (self.x, self.y), self.img, self.position, self.vida))