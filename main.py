import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextBrowser, QTableWidget, QTableWidgetItem

class CurrencyConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Currency Converter")
        self.setGeometry(100, 100, 800, 400) 

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)

        left_panel = QWidget(self)
        right_panel = QWidget(self)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        left_layout = QVBoxLayout(left_panel)
        self.currency_table = QTableWidget()
        self.currency_table.setColumnCount(2)
        self.currency_table.setHorizontalHeaderLabels(["Currency", "Exchange Rate"])
        left_layout.addWidget(self.currency_table)

        self.load_currencies()
        self.update_currency_table()

        right_layout = QVBoxLayout(right_panel)

        self.currency_combo_from = QComboBox()
        self.currency_combo_to = QComboBox()

        right_layout.addWidget(self.currency_combo_from)
        right_layout.addWidget(self.currency_combo_to)

        self.amount_line_edit = QLineEdit()
        right_layout.addWidget(self.amount_line_edit)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert)
        right_layout.addWidget(self.convert_button)

        self.result_label = QLabel()
        right_layout.addWidget(self.result_label)

        self.update_currency_combos()

    def load_currencies(self):
        response = requests.get("https://www.cbr-xml-daily.ru/latest.js")
        data = response.json()
        self.base_currency = data["base"]
        self.rates = data["rates"]
        self.rates["RUB"] = 1.0  # Добавляем RUB с курсом 1.0

    def update_currency_table(self):
        self.currency_table.setRowCount(0)
        for currency, rate in self.rates.items():
            row_position = self.currency_table.rowCount()
            self.currency_table.insertRow(row_position)
            self.currency_table.setItem(row_position, 0, QTableWidgetItem(currency))
            self.currency_table.setItem(row_position, 1, QTableWidgetItem(str(rate)))

    def update_currency_combos(self):
        self.currency_combo_from.addItems(self.rates.keys())
        self.currency_combo_to.addItems(self.rates.keys())
        self.currency_combo_from.setCurrentText("RUB")
        self.currency_combo_to.setCurrentText("USD")

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
