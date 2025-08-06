import sys
import hashlib
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QComboBox, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


class HashCracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-hash Algorithm Decryptor")
        self.setWindowIcon(QIcon("iconfile27.ico"))
        self.setGeometry(100, 100, 500, 250)

        layout = QVBoxLayout()

        self.hash_label = QLabel("Enter hash value:")
        self.hash_input = QLineEdit()

        self.algo_label = QLabel("Select hash algorithm:")
        self.algo_select = QComboBox()
        self.algo_select.addItems(["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"])

        self.wordlist_button = QPushButton("Choose Wordlist (.txt)")
        self.wordlist_button.clicked.connect(self.load_wordlist)
        self.wordlist_path = ""

        self.crack_button = QPushButton("Crack Hash")
        self.crack_button.clicked.connect(self.crack_hash)

        layout.addWidget(self.hash_label)
        layout.addWidget(self.hash_input)
        layout.addWidget(self.algo_label)
        layout.addWidget(self.algo_select)
        layout.addWidget(self.wordlist_button)
        layout.addWidget(self.crack_button)

        self.setLayout(layout)

    def load_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Wordlist", "", "Text Files (*.txt)")
        if file_path:
            self.wordlist_path = file_path
            self.wordlist_button.setText(f"📁 Wordlist loaded")

    def crack_hash(self):
        target_hash = self.hash_input.text().strip()
        algorithm = self.algo_select.currentText().lower()

        if not target_hash:
            QMessageBox.warning(self, "Error", "⚠️ Please enter a hash value.")
            return
        if not self.wordlist_path:
            QMessageBox.warning(self, "Error", "⚠️ Please load a wordlist.")
            return

        try:
            with open(self.wordlist_path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    word = line.strip()
                    hashed_word = hashlib.new(algorithm, word.encode()).hexdigest()

                    if hashed_word == target_hash:
                        QMessageBox.information(self, "Success", f"✅ Password found: {word}")
                        return

            QMessageBox.information(self, "Result", "❌ Password not found in wordlist.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HashCracker()
    window.show()
    sys.exit(app.exec())
