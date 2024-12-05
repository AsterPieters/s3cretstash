#s3cretstash.py

from modules.authentication import authenticate

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel

class S3cretstashWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('S3cretstash')
        self.setGeometry(200, 200, 600, 300)

        self.layout = QVBoxLayout()
        self.login_screen()

        self.error_label = None


    def login_screen(self):

        # Master secret field
        self.master_secret_field = QLineEdit(self)
        self.master_secret_field.setEchoMode(QLineEdit.Password)
        self.master_secret_field.setPlaceholderText("Enter Master Secret")
        self.layout.addWidget(self.master_secret_field)

        # Login button
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        # Set the layout
        self.setLayout(self.layout)




    def login(self):
        if authenticate(self.master_secret_field.text()):
            self.main_window()
        else:    
            self.show_error_message("Master secret is not correct.")

    def show_error_message(self, message):
        # If an error label already exists, remove it
        if self.error_label:
            self.layout.removeWidget(self.error_label)
            self.error_label.deleteLater()

        # Create and add a new error label
        self.error_label = QLabel(message, self)
        self.layout.addWidget(self.error_label)

        self.layout.update()

    def main_window(self):

        # Clear existing layout
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Add new widgets (display authenticated data)
        label = QLabel('You are authenticated!', self)
        self.layout.addWidget(label)

        self.layout.update()  # Refresh the layout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = S3cretstashWindow()
    window.show()
    sys.exit(app.exec_())

