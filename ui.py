import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QLineEdit, QTextEdit, \
    QPushButton, QGridLayout, QFrame, QDateTimeEdit
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt, QPoint
from data.star import satellite


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
        grid = QGridLayout()

        add_id_input = QLineEdit()
        add_button = QPushButton('Добавить')
        r_inputs = [QLineEdit() for _ in range(3)]
        v_inputs = [QLineEdit() for _ in range(3)]
        time_input = QDateTimeEdit()
        time_input.setDateTime(QDateTime.currentDateTime())
        time_input.setCalendarPopup(True)

        grid.addWidget(QLabel('ID:'), 0, 0)
        grid.addWidget(add_id_input, 0, 1)
        grid.addWidget(add_button, 5, 0)

        for i in range(3):
            grid.addWidget(QLabel(f'R{i + 1}:'), i + 1, 0)
            grid.addWidget(r_inputs[i], i + 1, 1)
            grid.addWidget(QLabel(f'V{i + 1}:'), i + 1, 2)
            grid.addWidget(v_inputs[i], i + 1, 3)

        grid.addWidget(QLabel('Время:'), 4, 0)
        grid.addWidget(time_input, 4, 1)

        add_layout.addLayout(grid)

        # Удаление
        remove_layout = QVBoxLayout()
        remove_id_input = QLineEdit()
        remove_button = QPushButton('Удалить')
        self.remove_results = QTextEdit()
        self.remove_results.setReadOnly(True)
        self.remove_results.setStyleSheet("QTextEdit { background-color: #FFFFFF; }")  # Поле для вывода результатов

        remove_layout.addWidget(QLabel('ID:'))
        remove_layout.addWidget(remove_id_input)
        remove_layout.addWidget(remove_button)
        remove_layout.addWidget(self.remove_results)

        # Add frames to visually separate sections
        check_frame = QFrame()
        check_frame.setFrameShape(QFrame.HLine)
        check_frame.setFrameShadow(QFrame.Sunken)

        add_frame = QFrame()
        add_frame.setFrameShape(QFrame.HLine)
        add_frame.setFrameShadow(QFrame.Sunken)

        # Add sections to the main layout
        layout.addLayout(check_layout)
        layout.addWidget(check_frame)
        layout.addLayout(add_layout)
        layout.addWidget(add_frame)
        layout.addLayout(remove_layout)

        self.tab_modify.setLayout(layout)

    def checkSat(self):
        id = self.check_id_input.text()
        flag = 0
        if id.isdigit() and len(id) == 5:
            for sat in satellite:
                if sat.get_id() == int(id):
                    self.remove_results.append('-----------------')
                    self.remove_results.append(str(sat) + " " + "Уже существует")
                    self.remove_results.append('-----------------')
                    flag = 1
                    break
            if flag == 0:
                self.remove_results.append('-----------------')
                self.remove_results.append(f"Id ({id}) cвободно")
                self.remove_results.append('-----------------')
        else:
            self.remove_results.append('-----------------')
            self.remove_results.append(f"ID некорректен ({id})")
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

        self.tab_collisions.setLayout(layout)

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
