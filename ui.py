import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QTextEdit, \
    QPushButton, QGridLayout, QFrame, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QPoint
from data.star import satellite, fromRVtoTLE
from astropy.time import Time
from astropy import units as u
import numpy as np
from models.Satellite import Satellite
from calculation.checkSats import selection


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Satellite search')
        self.setGeometry(100, 100, 1024, 768)  # Увеличен размер окна

        self.setWindowFlags(Qt.FramelessWindowHint)  # Убирает стандартные рамки окна
        self.setAttribute(Qt.WA_TranslucentBackground)  # Прозрачный фон для скругленных углов

        self.tabs = QTabWidget()
        self.tab_search = QWidget()
        self.tab_modify = QWidget()
        self.tab_collisions = QWidget()

        self.tabs.addTab(self.tab_search, "Поиск")
        self.tabs.addTab(self.tab_modify, "Изменение")
        self.tabs.addTab(self.tab_collisions, "Столкновения")

        self.create_search_tab()
        self.create_modify_tab()
        self.create_collisions_tab()

        vbox = QVBoxLayout()
        vbox.addWidget(self.tabs)

        # Скругление самого окна
        container = QVBoxLayout()
        container.addLayout(vbox)
        container.setContentsMargins(20, 20, 20, 20)
        rounded_frame = QFrame()
        rounded_frame.setLayout(container)
        rounded_frame.setStyleSheet("QFrame { background-color: #A5A4E7; border-radius: 20px; }")

        # Добавление кнопок управления окном в титульную строку
        self.title_bar = QHBoxLayout()
        self.title_bar.setContentsMargins(10, 10, 10, 10)
        self.title_bar.addWidget(QLabel('Satellite Search'))
        self.title_bar.addStretch(1)

        self.minimize_button = QPushButton("-")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.maximize_button = QPushButton("▢")
        self.maximize_button.clicked.connect(self.toggleMaximize)
        self.close_button = QPushButton("X")
        self.close_button.clicked.connect(self.close)

        for button in [self.minimize_button, self.maximize_button, self.close_button]:
            button.setFixedSize(30, 30)
            button.setStyleSheet(
                "QPushButton { background-color: #080940; color: #6C8ABB; border: none; } QPushButton:hover { background-color: #6C8ABB; color: #080940; }")

        self.title_bar.addWidget(self.minimize_button)
        self.title_bar.addWidget(self.maximize_button)
        self.title_bar.addWidget(self.close_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.title_bar)
        main_layout.addWidget(rounded_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.drag_position = QPoint()
        self.apply_styles()

    def mousePressEvent(self, event):
        self.drag_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_position)
            self.drag_position = event.globalPos()
            event.accept()

    def create_search_tab(self):
        layout = QVBoxLayout()

        self.search_id_input = QLineEdit()
        self.search_button = QPushButton('Найти')
        self.search_button.clicked.connect(self.getSat)
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)
        self.search_results.setStyleSheet("QTextEdit { background-color: #FFFFFF; }")  # Поле для вывода результатов

        layout.addWidget(QLabel('ID:'))
        layout.addWidget(self.search_id_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.search_results)

        self.tab_search.setLayout(layout)

    def getSat(self):
        id = self.search_id_input.text()
        flag = 0
        if id.isdigit() and len(id) == 5:
            for sat in satellite:
                if sat.get_id() == int(id):
                    self.search_results.append('-----------------')
                    self.search_results.append(sat.to_string())
                    self.search_results.append('-----------------')
                    flag = 1
                    break
            if flag == 0:
                self.search_results.append('-----------------')
                self.search_results.append(f"Спутник ({id}) не найден")
                self.search_results.append('-----------------')
        else:
            self.search_results.append('-----------------')
            self.search_results.append(f"ID некорректен ({id})")
            self.search_results.append('-----------------')

    def create_modify_tab(self):
        layout = QVBoxLayout()

        # Проверка
        check_layout = QVBoxLayout()
        self.check_id_input = QLineEdit()
        check_button = QPushButton('Проверить')
        check_button.clicked.connect(self.checkSat)

        check_layout.addWidget(QLabel('ID:'))
        check_layout.addWidget(self.check_id_input)
        check_layout.addWidget(check_button)

        # Добавление спутников
        add_layout = QVBoxLayout()

        add_button = QPushButton('Добавить')
        add_button.clicked.connect(self.createSat)
        self.line1inputs = QLineEdit()
        self.line2inputs = QLineEdit()

        add_layout.addWidget(QLabel(f'1line'))
        add_layout.addWidget(self.line1inputs)
        add_layout.addWidget(QLabel('2line'))
        add_layout.addWidget(self.line2inputs)
        add_layout.addWidget(add_button)

        # Удаление
        remove_layout = QVBoxLayout()
        self.remove_id_input = QLineEdit()
        remove_button = QPushButton('Удалить')
        remove_button.clicked.connect(self.remove)
        self.remove_results = QTextEdit()
        self.remove_results.setReadOnly(True)
        self.remove_results.setStyleSheet("QTextEdit { background-color: #FFFFFF; }")  # Поле для вывода результатов

        remove_layout.addWidget(QLabel('ID:'))
        remove_layout.addWidget(self.remove_id_input)
        remove_layout.addWidget(remove_button)
        remove_layout.addWidget(self.remove_results)

        check_frame = QFrame()
        check_frame.setFrameShape(QFrame.HLine)
        check_frame.setFrameShadow(QFrame.Sunken)

        add_frame = QFrame()
        add_frame.setFrameShape(QFrame.HLine)
        add_frame.setFrameShadow(QFrame.Sunken)

        layout.addLayout(check_layout)
        layout.addWidget(check_frame)
        layout.addLayout(add_layout)
        layout.addWidget(add_frame)
        layout.addLayout(remove_layout)

        self.tab_modify.setLayout(layout)

    def check_id(self, id):
        if str(id).isdigit() and len(str(id)) == 5:
            for sat in satellite:
                if sat.get_id() == int(id):
                    return 1
            return 2
        else:
            return 0

    def checkSat(self):
        id = self.check_id_input.text()
        n = self.check_id(id)
        if n == 1:
            self.remove_results.append('-----------------')
            self.remove_results.append(id + " " + "Уже существует")
            self.remove_results.append('-----------------')

        if n == 2:
            self.remove_results.append('-----------------')
            self.remove_results.append(f"Id ({id}) cвободно")
            self.remove_results.append('-----------------')
        if n == 0:
            self.remove_results.append('-----------------')
            self.remove_results.append(f"ID некорректен ({id})")
            self.remove_results.append('-----------------')

    def is_numeric(self, s):
        s = s.replace('.', '', 1)
        s = s.replace('-', '', 1)
        return s.isdigit()

    def createSat(self):
        line1 = self.line1inputs.text().strip()
        line2 = self.line2inputs.text().strip()

        try:
            sat = Satellite(line1, line2)
            id = sat.get_id()
            if self.check_id(id) == 2:
                satellite.append(sat)
                self.remove_results.append('-----------------')
                self.remove_results.append(f'Спутник {id} добавлен в коллекцию')
                self.remove_results.append('-----------------')
            else:
                self.remove_results.append('-----------------')
                self.remove_results.append(f'Спутник {id} уже существует')
                self.remove_results.append('-----------------')
        except Exception as e:
            print(e)
            self.remove_results.append('Некорректные TLE данные')

    def remove(self):
        id = self.remove_id_input.text()
        if str(id).isdigit() and len(str(id)) == 5:
            for sat in satellite:
                if sat.get_id() == int(id):
                    satellite.remove(sat)
                    self.remove_results.append('-----------------')
                    self.remove_results.append(f'Спутник {id} удален')
                    self.remove_results.append('-----------------')
                    break
            else:
                self.remove_results.append('-----------------')
                self.remove_results.append(f'Спутник {id} не найден')
                self.remove_results.append('-----------------')
        else:
            self.remove_results.append('-----------------')
            self.remove_results.append(f'Некорректный ид')
            self.remove_results.append('-----------------')

    def create_collisions_tab(self):
        layout = QVBoxLayout()

        self.collision_id_input = QLineEdit()
        self.time_interval_input = QLineEdit()
        self.start_button = QPushButton('Старт')
        self.collision_results = QTextEdit()
        self.collision_results.setReadOnly(True)  # Поле для вывода результатов
        self.collision_results.setStyleSheet("QTextEdit { background-color: #FFFFFF; }")  # Установка белого цвета фона

        layout.addWidget(QLabel('ID:'))
        layout.addWidget(self.collision_id_input)
        layout.addWidget(QLabel('Временной промежуток:'))
        layout.addWidget(self.time_interval_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.collision_results)

        self.start_button.clicked.connect(self.collision)

        self.tab_collisions.setLayout(layout)

    def collision(self):
        id = self.collision_id_input.text()
        p = self.time_interval_input.text()
        n = self.check_id(id)
        if n == 1:
            for sat in satellite:
                if sat.get_id() == int(id):
                    if p == "":
                        n = selection(sat, satellite)
                        if not n:
                            self.collision_results.append('-----------------')
                            self.collision_results.append(
                                f"Опасных сближений спутника {id} не обнаружено на промежутке времени 3600сек")
                            self.collision_results.append('-----------------')
                        else:
                            for k in n:
                                self.collision_results.append('-----------------')
                                self.collision_results.append(
                                    f"Обнаружено сближение спутника {id} со спутником {k[1]} на расстояние {k[0]}км в течении 3600сек")
                                self.collision_results.append('-----------------')
                    elif p.isdigit():
                        n = selection(sat, satellite, p=int(p))
                        if not n:
                            self.collision_results.append('-----------------')
                            self.collision_results.append(
                                f"Опасных сближений спутника {id} не обнаружено на промежутке времени {p}сек ")
                            self.collision_results.append('-----------------')
                        else:
                            for k in n:
                                self.collision_results.append('-----------------')
                                self.collision_results.append(
                                    f"Обнаружено сближение спутника {id} со спутником {k[1]} на расстояние {k[0]}км в течении {p}сек")
                                self.collision_results.append('-----------------')
        else:
            self.collision_results.append('-----------------')
            self.collision_results.append(f"ID некорректен ({id})")
            self.collision_results.append('-----------------')

    def apply_styles(self):
        # Define the colors
        background_color = QColor(165, 164, 231)
        button_color = QColor(8, 9, 64)
        text_color = QColor(108, 138, 187)

        # Set the palette
        palette = self.palette()
        palette.setColor(QPalette.Window, Qt.transparent)  # Прозрачный фон окна для скругленных углов
        palette.setColor(QPalette.Button, button_color)
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        self.setPalette(palette)

        # Apply rounded corners and other styles
        self.setStyleSheet("""
            QWidget {
                font-size: 18px;
                font-family: "PixelFont", Arial;  /* Использовать пиксельный шрифт */
            }
            QLineEdit, QTextEdit, QDateTimeEdit {
                border: 5px solid #6969BD;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;  /* Увеличен размер текста */
                font-family: Arial;
            }
            QTextEdit {
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #080940;
                color: #6C8ABB;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 18px;  /* Увеличен размер текста */
                font-family: "PixelFont", Arial;
            }
            QPushButton:hover { background-color: #9DABDD; color: #080940;  border: 2px solid #080940;}
            QTabWidget::pane {
                border: 5px solid #6969BD;
                border-radius: 10px;
                border-top-left-radius: 0px;
            }
            QTabBar::tab {
                background: #A5A4E7;
                border: 5px solid #6969BD;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: none;
                padding: 10px;
                font-size: 18px;  /* Увеличен размер текста */
                font-family: "PixelFont", Arial;
            }
            QTabBar::tab:selected {
                background: #080940;
                color: #6C8ABB;
            }
        """)

    def toggleMaximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
