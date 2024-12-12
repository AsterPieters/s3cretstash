#s3cretstash.py

from modules.authentication import authenticate
from modules.user import User
from modules.secrets import add_secret, get_secrets

import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QCheckBox, QGroupBox, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMainWindow, QFrame
from PyQt5 import QtCore


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title and geo
        self.setWindowTitle("S3cretstash")
        self.setGeometry(100, 100, 800, 600)

        # Run the login screen
        self.login_screen()
 
    def login_screen(self):
        # Create the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the layout
        self.login_layout = QVBoxLayout()

        # Add stretch to push field down
        self.login_layout.addStretch()

        s3cretstash = QLabel("S3cretstash Login", self)
        self.login_layout.addWidget(s3cretstash)
        self.login_layout.setAlignment(s3cretstash, QtCore.Qt.AlignCenter)

        # Master secret field
        self.master_secret_field = QLineEdit(self)
        self.master_secret_field.setEchoMode(QLineEdit.Password)
        self.master_secret_field.setPlaceholderText("Enter Master Secret")
        self.master_secret_field.setFixedSize(200, 30)
        self.login_layout.addWidget(self.master_secret_field)
        self.login_layout.setAlignment(self.master_secret_field, QtCore.Qt.AlignCenter)

        # Login button
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(partial(self.login, self.login_layout))
        login_button.setFixedSize(200, 30)
        self.login_layout.addWidget(login_button)
        self.login_layout.setAlignment(login_button, QtCore.Qt.AlignCenter)

        # Add stretch to push button up
        self.login_layout.addStretch()

        # Set the layout on the central widget
        self.central_widget.setLayout(self.login_layout)


    def login(self, layout):
        # Try to authenticate 
        if authenticate(self.master_secret_field.text()):
            
            # Create the user
            self.user = User(self.master_secret_field.text())
            
            # Start the main screen
            self.main_screen()

        else:    
            self.show_error_message("Master secret is not correct.", layout)

    def show_error_message(self, message, layout):
        # Make sure the label exitst
        if not hasattr(self, 'error_label'):
            self.error_label = None

        if self.error_label:
            layout.removeWidget(self.error_label)
            self.error_label.deleteLater()

        # Create and add a new error label
        self.error_label = QLabel(message, self)
        layout.addWidget(self.error_label)
        layout.update()

    def main_screen(self):
        # Create the central widget
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)

        # Create the top layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Create the add secret button
        add_secret_button = QPushButton('+', self)
        add_secret_button.clicked.connect(self.add_secret_screen)
        add_secret_button.setFixedSize(30, 30)
        top_layout.addWidget(add_secret_button, alignment=QtCore.Qt.AlignRight)

        # Add the top layout to the main layout 
        self.main_layout.addLayout(top_layout)

        # Show secrets
        self.show_secrets()

        # Set the layout on the central widget
        self.central_widget.setLayout(self.main_layout)

        # Refresh the window
        self.main_layout.update()

    def show_secrets(self):
        # Get the secrets
        self.secrets = get_secrets()

        # Create a groupbox for each secret
        for secret_name in self.secrets:
            
            # Secret box
            secret_box = QGroupBox("", self)
            secret_box.setFixedSize(400, 100)
            secret_box.setStyleSheet("QGroupBox { font-weight: bold; margin: 1px; padding: 1px; }")

            # Secret name
            secret_name_label = QLabel(secret_name)
            secret_box_layout = QVBoxLayout()
            secret_box_layout.addWidget(secret_name_label)
            
            # Secret line
            secret_line = QFrame(self)
            secret_line.setFrameShape(QFrame.HLine)
            secret_line.setFrameShadow(QFrame.Sunken)
            secret_box_layout.addWidget(secret_line)

            # Secret value
            secret_value = QLabel("*******")
            secret_box_layout.addWidget(secret_value)

            # Secret checkbox
            secret_checkbox = QCheckBox("Reveal", self)
            secret_checkbox.setAcceptDrops(True)
            secret_box_layout.addWidget(secret_checkbox)


            secret_box.setLayout(secret_box_layout)
            
            self.main_layout.addWidget(secret_box)

        self.main_layout.addStretch()

        self.central_widget.setLayout(self.main_layout)

    def add_secret_screen(self):
        # Create the central widget
        self.central_widget = QWidget()
        self.add_secret_layout = QVBoxLayout()
        self.setCentralWidget(self.central_widget)
        
        # Secret name field
        self.secret_name_field = QLineEdit(self)
        self.secret_name_field.setEchoMode(QLineEdit.Normal)
        self.secret_name_field.setPlaceholderText("Secret name")
        self.add_secret_layout.addWidget(self.secret_name_field)
        
        # Secret field
        self.secret_field = QLineEdit(self)
        self.secret_field.setEchoMode(QLineEdit.Password)
        self.secret_field.setPlaceholderText("Secret")
        self.add_secret_layout.addWidget(self.secret_field)

        # Add secret button
        add_secret_button = QPushButton('Add secret', self)
        add_secret_button.clicked.connect(self.add_secret)
        self.add_secret_layout.addWidget(add_secret_button)

        # Set the layout on the central widget
        self.central_widget.setLayout(self.add_secret_layout)

        # Refresh the window
        self.add_secret_layout.update()

    def add_secret(self):
        add_secret(self.secret_name_field.text(), self.secret_field.text(), self.user)
        self.main_screen()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = UI()

    ui.show()
    sys.exit(app.exec_())

