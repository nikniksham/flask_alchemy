import os
import sys
import zipfile
from datetime import datetime
from os.path import expanduser

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


def make_reserve_arc(source, dest):
    os.chdir(dest)
    with zipfile.ZipFile(f'{str(datetime.now()).split(".")[0].replace(":", "-")}.zip',
                         "w",
                         zipfile.ZIP_DEFLATED,
                         allowZip64=True) as zf:
        for root, _, filenames in os.walk(source):
            for name in filenames:
                name = os.path.join(root, name)
                name = os.path.normpath(name)
                zf.write(name, name[len(source):])
        print("Успешная архивация")


class Arhivator(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('arhivator.ui', self)
        self.dir_from = ''
        self.dir_where = ''
        self.from_button.clicked.connect(self.choice_dir_1)
        self.where_button.clicked.connect(self.choice_dir_2)
        self.z_button.clicked.connect(self.z_dir)

    def choice_dir_1(self):
        self.dir_from = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))

    def choice_dir_2(self):
        self.dir_where = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))

    def z_dir(self):
        return make_reserve_arc(self.dir_from, self.dir_where)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ar = Arhivator()
    ar.show()
    sys.exit(app.exec_())
