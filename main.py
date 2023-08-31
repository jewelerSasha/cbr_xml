import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Currency Converter")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.currency_combo_from = QComboBox()
        self.currency_combo_to = QComboBox()

        layout.addWidget(self.currency_combo_from)
        layout.addWidget(self.currency_combo_to)

        self.amount_line_edit = QLineEdit()
        layout.addWidget(self.amount_line_edit)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)

        self.central_widget.setLayout(layout)

        self.load_currencies()
        self.update_currency_combos()

    def load_currencies(self):
        response = requests.get("https://www.cbr-xml-daily.ru/latest.js")
        data = response.json()
        self.base_currency = data["base"]
        self.rates = data["rates"]
        self.rates["RUB"] = 1.0  # Добавляем RUB с курсом 1.0

    def update_currency_combos(self):
        self.currency_combo_from.addItems(self.rates.keys())
        self.currency_combo_to.addItems(self.rates.keys())

    def convert(self):
        currency_from = self.currency_combo_from.currentText()
        currency_to = self.currency_combo_to.currentText()
        exchange_rate_from = self.rates[currency_from]
        exchange_rate_to = self.rates[currency_to]
        amount = float(self.amount_line_edit.text())
        converted_amount = (amount / exchange_rate_from) * exchange_rate_to
        self.result_label.setText(f"Converted Amount: {converted_amount:.2f} {currency_to}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter_app = CurrencyConverterApp()
    converter_app.show()
    sys.exit(app.exec_())
