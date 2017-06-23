import threading
import socket
import os
import random
import time
import pickle

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080
server = ""
emojis = [":poop:", "O:)", ":D", ";)", "8)", "U.U", ":(", "3:)", "o.o", ":v"]


def getter():
    songs = dict()
    salas = dict()
    der = os.path.dirname(os.path.realpath(__file__)) + "/songs/"
    lista = os.listdir(der)
    for o in lista:
        direccion = der + "/{}/".format(o)
        songs[o] = os.listdir(direccion)
    k = 0
    for y in songs:
        h = Sala(y)
        u = Sala(y)
        l = []
        for i in songs[y]:
            l.append(i)
        h.id = k
        u.id = k + 1
        h.songs = l
        u.songs = l
        u.special = True
        salas[y] = (h, u)
        k += 2
    return salas


def trigger(c, dicc):
    global server
    if isinstance(server, Server):
        server.sender(c, dicc)


def second_trigger(dicc):
    global server
    if isinstance(server, Server):
        server.actualizer(dicc)


def third_trihher(value, dicc):
    global server
    if isinstance(server, Server):
        server.timing(value, dicc)


def fourth_trigger(msje, dicc):
    global server
    if isinstance(server, Server):
        print("DELIVERING MESSAGE FROM TRIGGER")
        server.messenger(msje, dicc)


class Sala(threading.Thread):
    def __init__(self, theme):
        threading.Thread.__init__(self)
        self.special = False
        self.theme = theme
        self.songs = []  # lista de tuplas con los objetos de QSong y su puntaje máximo
        self.current = ""
        self.correct = 0
        self.nope = 0
        self.players = dict() # actualmente en la sala
        self.time = 0
        self.id = 0
        self.chat = []

    @property
    def num_players(self):
        return len(self.players)

    @property
    def lapse(self):
        return time.time() - self.time

    def dict_deleter(self, it, dicc):
        aux = dict()
        for a in dicc:
            if a != it:
                aux[a] = dicc[a]
        return aux

    def change_tune(self):
        self.current = self.songs[random.randint(0, len(self.songs) - 1)]
        self.time = time.time()
        for a in self.players:
            pl = self.players[a]
            self.players = self.dict_deleter(a, self.players)
            self.players[a] = (pl[0], False, "N", self.lapse)
        trigger(self.current + "PLAY", self.players)
        pass

    def es_coincidencia(self, argu, lk):
        for a in self.players:
            if a == lk:
                cont = self.players[a]
                if cont[1] is False:
                    if argu == self.current:
                        self.players = self.dict_deleter(a, self.players)
                        puntaje = 100*(20 - self.lapse)
                        self.players[a] = (cont[0] + puntaje, True, "Y", self.lapse)
                        self.correct += 1
                    else:
                        self.players = self.dict_deleter(a, self.players)
                        self.players[a] = (cont[0], True, "N", self.lapse)
                        self.nope += 1
        second_trigger(self.players)
        pass

    def tabla_ranking(self):
        string = ""
        for a in self.players:
            pla = self.players[a]
            if pla[2] == "Y":
                yi = "Clasificado"
            else:
                yi = "Desclasificado"
            st = str(a) + " - Puntaje: " + str(round(float(pla[0]), 2)) + " - " + yi + " - Tiempo respuesta: " \
                 + str(round(float(pla[3]), 2)) + ";"
            string += st
        return string

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

    def emoji_replacer(self, texto, string):
        print("CHATROOM ANALIZE")
        print(texto)
        ind = self.find_str(string, texto)
        if ind != -1 and ind != 0:  # Comprobar si se mandó el carácter de no emoji
            if texto[ind - 1] == "<" and texto[ind + len(texto)] == ">":
                text = texto.replace("<{}>".format(string), string)
                print("CHATROOM FOUND MODIFIED EMOJI CALL")
                return text + "-REPLACED" + string
        return texto

    def send_msjes(self):
        if len(self.chat) != 0:
            print("CHATROOM RECEIVED MESSAGE")
            print(self.chat)
            textoo = self.chat[0]
            del self.chat[0]
            global emojis
            msj = []
            for a in emojis:
                if len(msj) == 0:
                    texto = self.emoji_replacer(textoo, a)
                    msj.append(texto)
                    if len(msj) > 1:
                        del msj[0]
                else:
                    texto = self.emoji_replacer(msj[0], a)
                    msj.append(texto)
                    if len(msj) > 1:
                        del msj[0]
            print("CHATROOM FORMATTED MESSAGE")
            print(msj)
            if len(msj) != 0:
                fin = msj[0]
            else:
                fin = textoo
            print(fin)
            fourth_trigger(fin, self.players)

    def run(self):
        self.change_tune()
        while True:
            third_trihher(str(20 - self.lapse), self.players)
            self.send_msjes()
            if self.lapse >= 20:
                print("Sala {}, especial: {} --- Cambiando canción a {}".format(self.theme, str(self.special), self.current))
                self.change_tune()

    def __str__(self):
        return "Songs:  {}".format(self.songs)


class Server:
    def __init__(self, port, host):
        print("Inicializando servidor...")
        self.host = host
        self.port = port
        self.lock = threading.Lock()
        self.salas = getter()
        self.save = "savefile.txt"
        self.stats = "stats.txt"
        self.users = dict()  # diccionario con tuplas de la forma: (score, socket del cliente)
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        for a in self.salas:
            a = self.salas[a]
            for y in a:
                y.start()
        self.accept_connections()

    def bind_and_listen(self):
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen(5)
        print("Servidor escuchando en {}:{}...".format(self.host, self.port))

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        print("Servidor aceptando conexiones...")
        while True:
            self.saveme()
            client_socket, _ = self.socket_servidor.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    @staticmethod
    def send(value, socket):
        stringified_value = str(value)
        msg_bytes = stringified_value.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        try:
            socket.send(msg_length + msg_bytes)
        except:
            pass

    def sender(self, value, dicc):
        stringified_value = str(value)
        msg_bytes = stringified_value.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        try:
            for a in dicc:
                for b in self.users:
                    if a == b:
                        if isinstance(self.users[b], tuple):
                            socket = self.users[b][1]
                            print("SENDING SONG TO".format(str(socket)))
                            try:
                                socket.send(msg_length + msg_bytes)
                            except:
                                print("No se ha podido enviar información a un socket.")
        except:
            self.sender(value, dicc)

    def dict_deleter(self, item, dicc):
        aux = dict()
        for a in dicc:
            if a != item:
                aux[a] = dicc[a]
        return aux

    def actualizer(self, dicc):
        # Actualiza los puntajes de los jugadores
        print("ACTUALIZANDO PUNTAJES DE JUGADORES")
        dictt = self.users
        for b in dicc:
            for a in dictt:
                if b == a:
                    cont = dictt[a]
                    self.users = self.dict_deleter(a, dictt)
                    self.users[a] = (dicc[b][0], cont[1])
        print("ENVIANDO NUEVOS PUNTAJES")
        try:
            y = self.users
            for a in y:
                c = y[a]
                if isinstance(c, tuple):
                    self.send("PUNTAJE" + str(c[0]), c[1])
        except:
            print("ERROR AT SENDING")
            self.actualizer(dicc)

    def messenger(self, msje, dicc):
        print("SERVER MESSENGER DELIVERING")
        for a in dicc:
            for b in self.users:
                if a == b:
                    if isinstance(self.users[b], tuple):
                        print("DELIVERED: {}".format("MSN" + msje))
                        self.send("MSN" + msje, self.users[b][1])

    def timing(self, value, dicc):
        try:
            for b in dicc:
                for a in self.users:
                    if b == a:
                        if isinstance(self.users[a], tuple):
                            c = self.users[a]
                            self.send("TIEMPO" + str(value), c[1])
        except:
            pass

    def listen_client_thread(self, client_socket):
        print("Servidor conectado a un nuevo cliente...")
        running = True
        i = 0
        while running:
            # MISC
            # LISTENER
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length, byteorder="big")
                response = b""

                while len(response) < response_length:
                    response += client_socket.recv(256)

                received = response.decode()

                if received != "":
                    response = self.handle_command(received, client_socket)
                    self.send(response, client_socket)
            except:
                if i > 20:
                    running = False
                    print("LISTENER THREAD STOPPED")
                i += 1
                pass

    def saveme(self):
        print("SAVING DATA")
        with self.lock:
            user = dict()
            for a in self.users:
                if isinstance(self.users[a], tuple):
                    user[a] = self.users[a][0]
                else:
                    user[a] = self.users[a]
            try:
                with open(self.save, mode="wb") as file:
                    pickle.dump(user, file)
            except:
                pass
            bt = []
            mi = float("Inf")
            ma = 0
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    mi = min(y.nope, mi)
                    ma = max(y.correct, ma)
            tope1 = True
            tope2 = True
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    if y.correct == ma and tope1:
                        if y.special is True:
                            im = "Ecualizador"
                        else:
                            im = "Normal"
                        bt.append((y.theme + " " + im, ma))
                        tope1 = False
                    elif y.nope == mi and tope2:
                        if y.special is True:
                            im = "Ecualizador"
                        else:
                            im = "Normal"
                        bt.append((y.theme + " " + im, mi))
                        tope2 = False
            try:
                with open(self.stats, mode="wb") as fil:
                    pickle.dump(bt, fil)
            except:
                pass

    def handle_command(self, rec, cliente):
        for a in self.salas:
            a = self.salas[a]
            for y in a:
                if not y.isAlive():
                    print("Sala de {} HA SIDO ELIMINADA".format(y.theme))
                    try:
                        salan = Sala(y.theme)
                        salan.id = y.id
                        salan.songs = y.songs
                        salan.special = y.special
                        ind = a.index(y)
                        self.salas = self.dict_deleter(a, self.salas)
                        salan.start()
                        if ind == 0:
                            self.salas[a] = (salan, a[1])
                        else:
                            self.salas[a] = (a[0], salan)
                        print("SALA {} REVIVIDA".format(y.theme))
                    except:
                        print("NO SE PUDO REVIVIR")
        if "USERNAME" in rec:
            rec = rec.replace("USERNAME", "")
            om = 0
            for t in self.users:
                om += 1
                if t == rec:
                    if isinstance(self.users[t], tuple):
                        if self.users[t][0] == 0:
                            return "INVALID"
                    else:
                        print("b")
                        score = self.users[t]
                        self.users = self.dict_deleter(t, self.users)
                        self.users[t] = (score, cliente)
            if om == len(self.users) and len(self.users) != 0:
                self.users[rec] = (0, cliente)
            if len(self.users) == 0:
                self.users[rec] = (0, cliente)
            string = ""
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    l = y.songs
                    for u in l:
                        string += ":" + u
                    string += ":" + str(y.theme) + ":" + str(y.num_players) + ":" + str(y.lapse) + ":" + str(y.id) + ":" + str(y.special) + "SEP"
            self.saveme()
            return "CONFIG" + "SEP" + string
        elif "DEFINE" in rec:
            rec = rec.replace("DEFINE", "")
            data = rec.split(":")
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    if y.id == int(data[0][0]):
                        y.players[str(data[1])] = (self.users[str(data[1])][0], True, "N", 20 - y.lapse)
                        return y.tabla_ranking() + "SETUP"
        elif "OPTION" in rec:
            rec = rec.replace("OPTION", "")
            data = rec.split(":")
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    if y.id == int(data[2]):
                        y.es_coincidencia(data[0], data[1])
                        print("RETURNING RANKING")
                        return y.tabla_ranking() + "RANKING"
        elif "CLOSE" in rec:
            rec = rec.replace("CLOSE", "")
            print("CLOSE REQUEST RECEIVED")
            print(rec)
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    for i in y.players:
                        print("PREPARING ERASE")
                        if rec == i:
                            print("LIMPIANDO USUARIO DE SALA")
                            y.players = y.dict_deleter(rec, y.players)
                            for lo in self.users:
                                loo = self.users[lo]
                                if lo == rec:
                                    print("CLOSING CONNECTION")
                                    loo[1].close()
                                    self.send("DONE", cliente)
        elif "MENSAJE" in rec:
            print("MESSAGE RECEIVED")
            data = rec.replace("MENSAJE", "").split("-")
            print(rec)
            print(data)
            user = data[0]
            msje = data[1]
            for a in self.salas:
                a = self.salas[a]
                for y in a:
                    for t in y.players:
                        if t == user:
                            y.chat.append(msje)
                            print("MESSAGE DELIVERED TO CHATROOM")
                            print(msje)
                            break
        else:
            print("SERVER RECEIVED: {}".format(rec))

if __name__ == "__main__":
    global server
    der = os.path.dirname(os.path.realpath(__file__))
    lista = os.listdir(der)
    dic = dict()
    if "savefile.txt" in lista:
        with open("savefile.txt", mode="rb") as file:
            try:
                dic = pickle.load(file)
            except:
                print("COULD NOT LOAD: EMPTY FILE")
    server = Server(PORT, HOST)
    if len(dic) > 0:
        print("LOADED USERS INTO SERVER")
        server.users = dic
        print(server.users)