import sys
import sqlite3
import datetime
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QButtonGroup
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QVBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QTimer
import random


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_zone_map.ui', self)
        self.setWindowTitle("Сапёр")
        self.fon_pixmap_main = QPixmap('picture_fon.jpg')
        self.fon.setPixmap(self.fon_pixmap_main)
        self.exit_btn.clicked.connect(app.quit)
        self.play_btn.clicked.connect(self.translate)
        self.top_btn.clicked.connect(self.translate)
        self.setting_btn.clicked.connect(self.translate)
        self.profile_btn.clicked.connect(self.translate)
        self.text_for_label()
        self.text_for_profile()

    def text_for_profile(self):
        with open("winner.txt", "rt", encoding="utf8") as f:
            text = f.read().split("\n")
            if text[-2] == "+":
                string = "Вход выполнен в аккаунт!"
                self.label_2.setText("Имя: " + text[-1])
            else:
                string = "Гость"
                self.label_2.setText("Имя: пользователь" + str(1 + int(text[0].split(" ")[1])))
            self.statusBar().showMessage(string)

    def text_for_label(self):
        s = False
        with open('settings.txt', 'rt', encoding="utf8") as f:
            string = f.read().split("\n")[0].split(";")
            if len(string) != 5:
                s = True
                string = ["0", "8", "8", "10", "Новичок"]
        if s:
            f = open('settings.txt', 'w', encoding="utf8")
            print(";".join(string), file=f)
            f.close()
        text = ["Тип игры:" + string[4], "Поле:" + str(string[1]) + "x" + str(string[2]),
                "Мин:" + str(string[3])]
        self.label.setStyleSheet("""font: bold italic;""")
        self.label.setText("\n".join(text))

    def translate(self):
        string = self.sender().text()
        if string == "Профиль":
            with open("winner.txt", "rt", encoding="utf8") as f:
                text = f.read().split("\n")
                text = text[-2]
            if text == "+":
                msg = QMessageBox(self)
                msg.setWindowTitle("Пользователь")
                msg.setText("В аккаунт был сделан вход! Выйти?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                button = msg.exec()
                if button == QMessageBox.Yes:
                    self.w = Profile()
                else:
                    return
            else:
                self.w = Profile()
        elif string == "Начать":
            self.w = Game_zone()
        elif string == "Настройки":
            self.w = Setting_zone()
        elif string == "Топ":
            self.w = Top_game()
        self.w.show()
        self.close()


class Profile(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аккаунт")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonRegister = QPushButton("Register", self)
        self.buttonNew = QPushButton("Exit", self)
        self.buttonLogin.clicked.connect(self.login_acc)
        self.buttonRegister.clicked.connect(self.register_acc)
        self.buttonNew.clicked.connect(self.now)
        self.profi = {}
        with open('winner.txt', 'rt', encoding="utf8") as f:
            s = f.read().split("\n")
            self.kolvo = int(s[0].split(" ")[1])
            for i in range(1, self.kolvo + 1):
                d = s[i].split(" --- ")
                self.profi[d[0]] = d[1]
        layout = QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        layout.addWidget(self.buttonRegister)
        layout.addWidget(self.buttonNew)

    def now(self):
        with open("winner.txt", 'rt', encoding="utf8") as f:
            text = f.read().split("\n")
        if text[-2] == "+":
            text = text[0:-2]
        with open("winner.txt", 'w', encoding="utf8") as f:
            print("\n".join(text), file=f)
        self.close()

    def login_acc(self):
        if len(self.textName.text()) != 0 and len(self.textPass.text()) != 0:
            if self.textName.text() in self.profi.keys():
                if self.textPass.text() == self.profi[self.textName.text()]:
                    with open("winner.txt", 'a', encoding="utf8") as f:
                        f.write("+")
                        f.write("\n")
                        f.write(self.textName.text())
                    self.close()
                else:
                    QMessageBox.warning(self, 'Error', "Пароль не подходит")
            else:
                QMessageBox.warning(self, 'Error', "Нету такого аккаунта")
        else:
            QMessageBox.warning(self, 'Error', "Текст?")

    def register_acc(self):
        if len(self.textName.text()) != 0 and len(self.textPass.text()) != 0:
            name = str(self.check_password(self.textName.text()))
            pas = str(self.check_password(self.textPass.text()))
            d = 0
            if name == "ok":
                for i in self.profi:
                    if i == self.textName.text():
                        d = 1
                        break
                if d != 1:
                    if pas == "ok":
                        self.profi[self.textName.text()] = self.textPass.text()
                        self.zapis()
                        self.close()
                    else:
                        QMessageBox.warning(self, 'Error', pas)
                else:
                    QMessageBox.warning(self, 'Error', "Такое имя уже есть")
            else:
                QMessageBox.warning(self, 'Error', name)
        else:
            QMessageBox.warning(self, 'Error', "Текст?")

    def zapis(self):
        with open("winner.txt", 'w', encoding="utf8") as f:
            print(str("users: " + str(self.kolvo + 1)), file=f)
            for i, j in self.profi.items():
                print(" --- ".join([i, j]), file=f)
            f.write("+")
            f.write("\n")
            f.write(self.textName.text())

    def check_password(self, password):
        try:
            s = password
            digit = set("1234567890")
            word = {"йцукенгшщзхъфывапролджэёячсмитьбю",
                    "qwertyuiopasdfghjklzxcvbnm"}
            if len(s) < 9:
                raise Exception("Длина <9")
            b, c = 0, 0
            for i in word:
                if set(i) & set(s) and b == 0:
                    b += 1
                if set(i.upper()) & set(s) and c == 0:
                    c += 1
            if c + b < 2:
                raise Exception("разные регистры")
            if not digit & set(s):
                raise Exception("нету цифр")
            return "ok"
        except Exception as e:
            return e

    def closeEvent(self, s):
        self.w = MainWindow()
        self.w.show()


class Top_game(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('top_zone_map.ui', self)
        self.setWindowTitle("Топ")
        self.exit_btn.clicked.connect(self.return_move)
        self.comboBox.activated[str].connect(self.pokaz)
        self.con = sqlite3.connect("saper.db")
        self.pokaz("Новичок 8х8")

    def closeEvent(self, event):
        self.con.close()

    def pokaz(self, text):
        s = 'SELECT * FROM users ORDER BY "{}" NULLS LAST'.format(text)
        cur = self.con.cursor()
        result = cur.execute(s).fetchall()
        self.tw_top.setRowCount(len(result))
        self.tw_top.setColumnCount(len(result[0]))
        self.tw_top.setHorizontalHeaderLabels([description[0] for description in cur.description])
        self.tw_top.verticalHeader().setVisible(False)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tw_top.setItem(i, j, QTableWidgetItem(str(val)))

    def return_move(self):
        self.con.close()
        self.w = MainWindow()
        self.w.show()
        self.close()


class Game_zone(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('game_zone_map.ui', self)
        self.setWindowTitle("Сапёр")
        with open('settings.txt', 'r',
                  encoding='utf8') as f:
            string = f.read().split("\n")[0].split(";")
            self.rasmer = [int(string[2]) + 1, int(string[1]) + 1, int(string[3])]
        self.vsego_min = self.rasmer[2]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.setInterval(1000)  # 1 sec
        self.time = 0
        self.peremennya = [True, True, True]
        self.lcdNumber.display(str(self.vsego_min))
        self.tocki = []
        self.postroika_button()
        self.mest_rp = ()
        self.mest_rp_spis = []
        self.pole = []
        self.flag_ = []
        self.win = 0
        self.svet_toka = {"1": "color : blue;",
                          "2": "color : green;",
                          "3": "color : red;",
                          "4": "color : darkBlue;",
                          "5": "color : brown;",
                          "6": "color : cyan;",
                          "7": "color : black;",
                          "8": "color : white;"}
        self.pushButton_2.clicked.connect(self.restart_game)
        self.pushButton_3.clicked.connect(self.smena)
        self.pushButton.clicked.connect(self.return_move)
        [j.clicked.connect(self.game) for i in self.tocki for j in i]

    def showTime(self):
        self.lcdNumber_2.display(self.time)
        self.time += 1

    def game(self):
        for y, i in enumerate(self.tocki):
            for x, j in enumerate(i):
                if j == self.sender():
                    self.mest_rp = y, x
                    break
        if self.peremennya[2]:
            self.timer.start()
            self.start_game()
            self.otcritie()
            return
        if not self.peremennya[0] and not self.peremennya[2]:
            self.set_flag()
        else:
            string = self.sender().text()
            if "50" == string:
                self.game_over()
                return
            if " " not in string:
                self.otcritie_pos()

    def vivod(self):
        for i, j in self.mest_rp_spis:
            toka = self.tocki[i][j].text()
            if toka == "50":
                continue
            if toka == " ":
                continue
            self.tocki[i][j].setStyleSheet("color: notransparent;")
            self.tocki[i][j].setStyleSheet("font-weight: bold")
            if toka in self.svet_toka:
                self.tocki[i][j].setStyleSheet(self.svet_toka[toka])
            if toka == "0":
                self.tocki[i][j].setText("")
            self.tocki[i][j].setEnabled(False)
        self.mest_rp_spis = []
        b = 0
        for i in self.tocki:
            for j in i:
                if j.isEnabled():
                    b += 1
        if b == self.rasmer[2]:
            self.timer.stop()
            self.zapis_winner()
            self.win = 1
            self.restart_game()

    def zapis_winner(self):
        with open('winner.txt', 'rt', encoding="utf8") as f:
            dd = f.read().split("\n")
            kolvo = int(dd[0].split(" ")[1])
            if len(dd) == kolvo + 2:
                name_ = "Пользователь" + str(kolvo)
            else:
                name_ = dd[-1]
        with open('settings.txt', 'r', encoding='utf8') as f:
            text = f.read().split("\n")[0].split(";")
            if text[-1] != "Настраиваемый":
                mest = text[-1] + " " + text[1] + "х" + text[2]
            else:
                mest = text[-1]
        time = str(datetime.timedelta(seconds=self.time))
        if len(time) > 9:
            time = time[8:]
        else:
            time = "0" + time
        proverka = {"Новичок 8х8": 2,
                    "Любитель 16х16": 3,
                    "Профессионал 30х16": 4,
                    "Настраиваемый": 5}
        data = ""
        string = "SELECT * FROM users where name = '{}'".format(name_)
        self.connection = sqlite3.connect("saper.db")
        cursor = self.connection.cursor()
        for i in cursor.execute(string):
            data = i
        if len(data) != 0:
            time_old = data[proverka[mest]]
            if not time_old or time_old == "00:00:00":
                string = "UPDATE users SET '{}' = '{}' WHERE name = '{}'".format(mest, time, name_)
            elif time_old > time:
                string = "UPDATE users SET '{}' = '{}' WHERE name = '{}'".format(mest, time, name_)
            else:
                self.connection.close()
                return
        else:
            string = 'INSERT INTO users(name, "{}") VALUES("{}", "{}");'.format(mest, name_, time)
        cursor.execute(string)
        self.connection.commit()
        self.connection.close()

    def otcritie_pos(self):
        key = False
        b = self.poisk_tochki(*self.mest_rp)
        for i, j in b:
            if self.tocki[i][j].text() == "0":
                take = [(i, j)]
                self.mest_rp_spis.append((i, j))
                key = True
                break
        if key:
            while True:
                proverka = self.mest_rp_spis.copy()
                if len(take) == 0:
                    break
                for i in take:
                    for j in self.poisk_tochki(*i):
                        if j not in self.mest_rp_spis:
                            self.mest_rp_spis.append(j)
                take = []
                for i in self.mest_rp_spis:
                    if i in proverka:
                        continue
                    if self.tocki[i[0]][i[1]].text() == "0":
                        take.append(i)
        self.mest_rp_spis.append(self.mest_rp)
        self.vivod()

    def otcritie(self):
        take = [self.mest_rp]
        self.mest_rp_spis.append(self.mest_rp)
        while True:
            proverka = self.mest_rp_spis.copy()
            if len(take) == 0:
                break
            for i in take:
                for j in self.poisk_tochki(*i):
                    if j not in self.mest_rp_spis:
                        self.mest_rp_spis.append(j)
            take = []
            for i in self.mest_rp_spis:
                if i in proverka:
                    continue
                if self.tocki[i[0]][i[1]].text() == "0":
                    take.append(i)
        self.vivod()

    def poisk_tochki(self, i, j):
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        result = []
        for dy, dx in offsets:
            ny, nx = i + dy, j + dx
            if ny in range(self.rasmer[0]) and nx in range(self.rasmer[1]):
                result.append((ny, nx))
        return result

    def set_flag(self):
        string = self.tocki[self.mest_rp[0]][self.mest_rp[1]].text()
        if string == " ":
            self.tocki[self.mest_rp[0]][self.mest_rp[1]].setStyleSheet(
                "background-image : none;")
            s = []
            for i in self.flag_:
                if i[0] == self.mest_rp[0] and i[1] == self.mest_rp[1]:
                    string = i[2]
                else:
                    s.append(i)
            self.flag_ = s.copy()
            self.tocki[self.mest_rp[0]][self.mest_rp[1]].setText(string)
            self.tocki[self.mest_rp[0]][self.mest_rp[1]].setStyleSheet(
                "color: transparent;")
            self.vsego_min += 1
        else:
            self.flag_.append([self.mest_rp[0], self.mest_rp[1], string])
            self.tocki[self.mest_rp[0]][self.mest_rp[1]].setStyleSheet(
                "background-image : url(flag_text.png);")
            self.tocki[self.mest_rp[0]][self.mest_rp[1]].setText(" ")
            self.vsego_min -= 1
        self.lcdNumber.display(str(self.vsego_min))

    def start_game(self):
        for i in range(self.rasmer[0]):
            s = []
            for j in range(self.rasmer[1]):
                s.append(0)
            self.pole.append(s)
        for i in range(self.rasmer[2]):
            b = [random.randint(1, self.rasmer[0]), random.randint(1, self.rasmer[1])]
            while self.pole[b[0] - 1][b[1] - 1] == 50 or (b[0] - 1, b[1] - 1) == self.mest_rp:
                b = [random.randint(1, self.rasmer[0]), random.randint(1, self.rasmer[1])]
            self.pole[b[0] - 1][b[1] - 1] = 50
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(self.rasmer[0]):
            for j in range(self.rasmer[1]):
                if self.pole[i][j] != 50:
                    for dy, dx in offsets:
                        ny, nx = i + dy, j + dx
                        if ny in range(self.rasmer[0]) and nx in range(self.rasmer[1]):
                            if self.pole[ny][nx] == 50:
                                self.pole[i][j] += 1
                string = str(self.pole[i][j])
                self.tocki[i][j].setText(string)
        self.peremennya[2] = False

    def postroika_button(self):
        vis = 40
        for i in range(self.rasmer[0]):
            tochki_1 = []
            vis += 40
            dlin = 11
            for j in range(self.rasmer[1]):
                b = QPushButton("0", self)
                b.setGeometry(dlin, vis, 40, 40)
                b.setStyleSheet("color:transparent;")
                tochki_1.append(b)
                dlin += 39
                if j == self.rasmer[1] - 1 and i == self.rasmer[0] - 1:
                    self.lcdNumber_2.move(dlin - 100, 20)
                    self.pushButton_3.move(int((dlin + 10) / 2) - 20, vis + 40)
                    self.pushButton_3.setStyleSheet("background-image : url(lopata.jpg);")
                    self.pushButton_2.setStyleSheet("background-image : url(dobp_smile_min.jpg);")
                    self.pushButton_2.move(int((dlin + 10) / 2) - 20, 20)
                    self.setGeometry(300, 100, dlin + 10, vis + 40 + 70)
            self.tocki.append(tochki_1)

    def game_over(self):
        self.pushButton_2.setStyleSheet("background-image : url(gryst_smile.jpg);")
        self.peremennya[1] = False
        for j in self.tocki:
            for i in j:
                i.setEnabled(False)
                if i.text() == "50" or i.text() == " ":
                    i.setText("")
                    i.setStyleSheet("background-image : url(bomba.png);")
                else:
                    i.setStyleSheet("color:notransparent;")
        self.timer.stop()

    def restart_game(self):
        count = 0
        if self.peremennya[1]:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Вопрос")
            if self.win == 1:
                dlg.setText("Вы победили! Можете начать заново!?")
            else:
                dlg.setText("Можете начать заново!?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()
            if button == QMessageBox.Yes:
                count = 1
        else:
            count = 1
        if count == 1:
            self.timer.stop()
            self.peremennya = [True for i in range(len(self.peremennya))]
            for j in self.tocki:
                for i in j:
                    i.setEnabled(True)
                    i.setText("0")
                    i.setStyleSheet("background-image : no;")
                    i.setStyleSheet("color:transparent;")
            self.pushButton_3.setStyleSheet("background-image : url(lopata.jpg);")
            self.pushButton_2.setStyleSheet("background-image : url(dobp_smile_min.jpg);")
            self.pole = []
            self.timer.setInterval(1000)  # 1 sec
            self.time = 0
            self.vsego_min = self.rasmer[2]
            self.lcdNumber.display(str(self.vsego_min))
            self.win = 0

    def smena(self):
        if self.peremennya[0]:
            self.pushButton_3.setStyleSheet("background-image : url(flag.jpg);")
            self.peremennya[0] = False
        else:
            self.peremennya[0] = True
            self.pushButton_3.setStyleSheet("background-image : url(lopata.jpg);")

    def return_move(self):
        self.w = MainWindow()
        self.w.show()
        self.close()


class Setting_zone(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('setting_zone_map.ui', self)
        with open('settings.txt', 'rt', encoding="utf8") as f:
            string = f.read().split("\n")[0].split(";")
            self.number = int(string[0])
            self.setting_map_game = [int(string[1]), int(string[2]), int(string[3])]
            self.text = [string[4], "Поле:" + string[1] + "x" + string[2], "Мин:" + string[3]]
            self.tip_game.buttons()[int(string[0])].setChecked(True)
        self.label_2.setText("\n".join(self.text))
        self.setWindowTitle("Настройки")
        self.pushButton.clicked.connect(self.return_move)
        self.pushButton_2.clicked.connect(self.save_setting)
        self.pushButton_3.clicked.connect(self.rule)
        [i.clicked.connect(self.for_text_label2) for i in self.tip_game.buttons()]

    def rule(self):
        self.d = Rule_game()
        self.d.show()

    def for_text_label2(self):
        string = self.tip_game.checkedButton().text()
        string = " ".join(string.split())
        if string == "Настраиваемый":
            pole2, ok_pressed = QInputDialog.getInt(
                self, "Настраиваемый", "По высоте?",
                8, 8, 16, 1)
            pole1, ok_pressed = QInputDialog.getInt(
                self, "Настраиваемый", "По длине?",
                8, 8, 30, 1)
            mina, ok_pressed = QInputDialog.getInt(
                self, "Настраиваемый", "Сколько мин?",
                10, 1, int((60 * pole1 * pole2) / 100), 1)
            self.number = 3
        else:
            if string == "Новичок":
                pole1, pole2, mina, self.number = 8, 8, 10, 0
            elif string == "Любитель":
                pole1, pole2, mina, self.number = 16, 16, 40, 1
            elif string == "Профессионал":
                pole1, pole2, mina, self.number = 30, 16, 99, 2
        self.setting_map_game = [pole1, pole2, mina]
        self.text = [string, "Поле:" + str(pole1) + "x" + str(pole2), "Мин:" + str(mina)]
        self.label_2.setText("\n".join(self.text))

    def save_setting(self):
        f = open('settings.txt', 'w', encoding="utf8")
        string = [str(self.number)]
        [string.append(i) for i in list(map(str, self.setting_map_game))]
        string.append(self.text[0])
        print(";".join(string), file=f)
        f.close()

    def return_move(self):
        self.w = MainWindow()
        self.w.show()
        self.close()


class Rule_game(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('rule_game.ui', self)
        self.setWindowTitle("Правила игры")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())