#s3cretstash.py

from modules.authentication import authenticate
from modules.user import User
from modules.secrets import add_secret, get_secrets, delete_secret

import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QMenu, QGroupBox, QScrollArea, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMainWindow, QFrame
from PyQt5 import QtCore


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title and geo
        self.setWindowTitle("S3cretstash")
        self.setGeometry(100, 100, 800, 600)
       
        # Set up secrets
        self.secrets = []

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

        # Main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add secret button
        add_secret_button = QPushButton('+', self)
        add_secret_button.clicked.connect(self.add_secret_screen)
        add_secret_button.setFixedSize(30, 30)
        main_layout.addWidget(add_secret_button, alignment=QtCore.Qt.AlignRight)
        
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)

        # Scroll widget
        scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_widget)
        
        # Secrets
        self.show_secrets()

        # Set 
        scroll_widget.setLayout(self.scroll_layout)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        self.setCentralWidget(main_widget)
        # Refresh the window

        main_layout.update()

    def show_secrets(self):
        
        # Only load secrets if not yet loaded
        if not self.secrets:
            self.secrets = get_secrets(self.user.master_secret)

        # Create a groupbox for each secret
        for secret in self.secrets:
            
            # Get the secret data
            secret_name = secret['secret_name']
            secret_description = secret.get('secret_description', "")

            # Secret box
            secret_box = QGroupBox(secret_name, self)
            secret_box.setFixedSize(400, 150)
            secret_box.setStyleSheet("""
                QGroupBox {
                    border: 1px solid #8f8f91;
                    border-radius: 5px;
                    margin-top: 20px; /* Create space for the title inside the box */
                    background-color: #2e2e2e; /* Box background color */
                }
                QGroupBox::title {
                    subcontrol-origin: margin; /* Title relative to content */
                    subcontrol-position: top left; /* Position at top-left inside the box */
                    padding: 5px 10px; /* Add padding to the title */
                    color: white; /* Title text color */
                    font-weight: bold; /* Make the title bold */
                    background-color: #3c3c3c; /* Title background */
                    border-radius: 3px; /* Rounded corners for title */
                }
            """)

            # Set the layouts
            secret_box_layout = QVBoxLayout()

            # Options button
            options_button = QPushButton( "Options", self)
            options_button.setFixedSize(100, 25)
            secret_box_layout.addWidget(options_button, alignment=QtCore.Qt.AlignRight)

            # Only display description if nessicary
            if secret_description:

                # Secret description
                secret_description_label = QLabel(secret_description)
                secret_box_layout.addWidget(secret_description_label)
                
                # Secret description line
                secret_description_line = QFrame(self)
                secret_description_line.setFrameShape(QFrame.HLine)
                secret_description_line.setFrameShadow(QFrame.Sunken)
                secret_box_layout.addWidget(secret_description_line)

            # Secret value
            secret_value = QLabel("*****")
            secret_box_layout.addWidget(secret_value)

            # Delete option
            options_menu = QMenu(self)
            options_menu.addAction("Delete", lambda name=secret_name, box=secret_box: self._delete_secret(name, box))
            options_button.setMenu(options_menu)
            
            # Secret line
            secret_line = QFrame(self)
            secret_line.setFrameShape(QFrame.HLine)
            secret_line.setFrameShadow(QFrame.Sunken)
            secret_box_layout.addWidget(secret_line)

            # Reveal button
            reveal_button = QPushButton("Reveal", self)
            reveal_button.clicked.connect(
                    # This is some fucking magic
                    lambda _, lbl=secret_value, btn=reveal_button, val=secret['secret_value']: self.toggle_secret(lbl, btn, val)
                    )
            reveal_button.setFixedSize(100, 30)
            secret_box_layout.addWidget(reveal_button)

            # Set layout
            secret_box.setLayout(secret_box_layout)
            
            # Add secret box loayout to main layout
            self.scroll_layout.addWidget(secret_box)

        # Push the secret boxes up
        self.scroll_layout.addStretch()
    
    def toggle_secret(self, label, button, value):
        """
        Toggle between revealing and hiding the secret.
        """
        if button.text() == "Reveal":
            # Reveal the secret
            label.setText(value)
            button.setText("Hide")
        else:
            # Hide the secret
            label.setText("******")
            button.setText("Reveal")

    def _delete_secret(self, secret_name, secret_box):
        
        # Delete the secret
        delete_secret(secret_name)

        # Delete the box
        secret_box.setParent(None)


    def add_secret_screen(self):
        # Create the central widget
        main_widget = QWidget()
        add_secret_layout = QVBoxLayout()
        self.setCentralWidget(main_widget)
        
        # Push widgets down
        add_secret_layout.addStretch()

        # Secret name
        secret_name_label = QLabel("Secret name", self)
        self.secret_name_field = QLineEdit(self)
        self.secret_name_field.setEchoMode(QLineEdit.Normal)
        self.secret_name_field.setFixedSize(200, 30)
        self.secret_name_field.setPlaceholderText("e.g. Spotify.com")
        add_secret_layout.addWidget(secret_name_label, alignment=QtCore.Qt.AlignCenter)
        add_secret_layout.addWidget(self.secret_name_field, alignment=QtCore.Qt.AlignCenter)
       
        # Secret description
        secret_description_label = QLabel("Secret description", self)
        self.secret_description_field = QLineEdit(self)
        self.secret_description_field.setEchoMode(QLineEdit.Normal)
        self.secret_description_field.setFixedSize(200, 30)
        self.secret_description_field.setPlaceholderText("e.g. Password for Dad")
        add_secret_layout.addWidget(secret_description_label, alignment=QtCore.Qt.AlignCenter)
        add_secret_layout.addWidget(self.secret_description_field, alignment=QtCore.Qt.AlignCenter)

        # Secret value
        secret_value_label = QLabel("Secret value", self)
        self.secret_value_field = QLineEdit(self)
        self.secret_value_field.setEchoMode(QLineEdit.Password)
        self.secret_value_field.setPlaceholderText("Secret")
        self.secret_value_field.setFixedSize(200, 30)
        add_secret_layout.addWidget(secret_value_label, alignment=QtCore.Qt.AlignCenter)
        add_secret_layout.addWidget(self.secret_value_field, alignment=QtCore.Qt.AlignCenter)

        # Add secret button
        add_secret_button = QPushButton('Add secret', self)
        add_secret_button.clicked.connect(self._add_secret)
        add_secret_button.setFixedSize(200, 30)
        add_secret_layout.addWidget(add_secret_button, alignment=QtCore.Qt.AlignCenter)

        # Cancel button
        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.main_screen)
        cancel_button.setFixedSize(200, 30)
        add_secret_layout.addWidget(cancel_button, alignment=QtCore.Qt.AlignCenter)

        # Push widgets up
        add_secret_layout.addStretch()

        # Set the layout on the central widget
        main_widget.setLayout(add_secret_layout)

        # Refresh the window
        add_secret_layout.update()

    def _add_secret(self):
        add_secret(self.secret_name_field.text(), self.secret_value_field.text(), self.secret_description_field.text(), self.user)
        self.main_screen()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = UI()

    ui.show()
    sys.exit(app.exec_())
