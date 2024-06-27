import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QSpacerItem, QSizePolicy, QGridLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QTimer
from datafetching import fetch_data


class ParameterShowing(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)  # Assuming you want columns for 'Hava Hızı', 'Yer Hızı', 'Enlem', 'Boylam'
        self.table.setHorizontalHeaderLabels([ 'Enlem', 'Boylam','İrtifa])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.update_table()
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Setup timer to refresh data every 1000 ms (1 second)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start(1000)

    def update_table(self):
        data = fetch_data()  # This function needs to return a list of lists
        if data is not None:
            self.load_data(data)

    def load_data(self, data):
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                cell = QTableWidgetItem(str(item))
                self.table.setItem(row_idx, col_idx, cell)


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drone Command Center')
        self.setGeometry(100, 100, 1400, 800)
        widget = QWidget(self)
        self.setCentralWidget(widget)
        
        layout = QHBoxLayout()
        self.paramDisplay = ParameterShowing()  # Create instance of ParameterShowing
        layout.addWidget(self.paramDisplay)
        widget.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainUI()
    ex.show()
    sys.exit(app.exec_())
