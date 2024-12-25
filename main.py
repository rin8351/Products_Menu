import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGroupBox, QCheckBox, QPushButton, QCalendarWidget, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QLabel)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QIcon, QPalette

class FoodTrackingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.consumption = {}
        self.last_consumed = {}
        self.load_food_items()
        self.load_consumption()
        self.initUI()
        self.setWindowIcon(QIcon('icon.png'))
        self.apply_custom_style()

    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Top section
        top_layout = QHBoxLayout()
        
        # Food category checkboxes
        self.protein_group = self.create_checkbox_group("Белки", "protein.txt")
        self.fat_group = self.create_checkbox_group("Жиры", "fat.txt")
        self.veget_group = self.create_checkbox_group("Овощи", "veget.txt")
        self.cereals_group = self.create_checkbox_group("Крупы", "cereals.txt")
        self.carbs_group = self.create_checkbox_group("Фрукты", "fruits.txt")
        
        top_layout.addWidget(self.protein_group)
        top_layout.addWidget(self.fat_group)
        top_layout.addWidget(self.veget_group)
        top_layout.addWidget(self.cereals_group)
        top_layout.addWidget(self.carbs_group)
        
        # Date selection and Add button
        date_layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setMinimumDate(QDate.currentDate().addDays(-365))  # Ограничиваем выбор дат одним годом назад
        self.calendar.setMaximumDate(QDate.currentDate())  # Ограничиваем выбор дат сегодняшним днем
        self.calendar.setFixedSize(350, 250)  # Устанавливаем фиксированный размер календаря
        date_layout.addWidget(self.calendar)
        
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_selected_items)
        date_layout.addWidget(self.add_button)
        
        top_layout.addLayout(date_layout)
        
        main_layout.addLayout(top_layout)
        
        # Bottom section
        bottom_layout = QHBoxLayout()
        
        # Table for selected items
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Дата", "Прием", "Продукты"])
        
        # Устанавливаем фиксированную ширину для столбцов "Дата" и "Прием"
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.table.setColumnWidth(0, 100)  # Устанавливаем фиксированную ширину для столбца "Дата"
        self.table.setColumnWidth(1, 50)  # Устанавливаем фиксированную ширину для столбца "Прием"
        
        self.table.setWordWrap(True)  # Включаем перенос текста
        self.table.verticalHeader().setDefaultSectionSize(60)  # Увеличиваем высоту строк
        bottom_layout.addWidget(self.table)
        
        # List of least consumed items
        self.least_consumed_list = QTableWidget()
        self.least_consumed_list.setColumnCount(2)
        self.least_consumed_list.setHorizontalHeaderLabels(["Продукт", "Последнее употребление"])
        self.least_consumed_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        bottom_layout.addWidget(self.least_consumed_list)
        
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Трекер питания')
        self.setGeometry(100, 100, 1300, 900)

        self.update_table()
        self.update_least_consumed_list()

    def create_checkbox_group(self, title, filename):
        group_box = QGroupBox(title)
        layout = QVBoxLayout()
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                checkbox = QCheckBox(line.strip())
                layout.addWidget(checkbox)
        
        group_box.setLayout(layout)
        return group_box

    def load_food_items(self):
        files = ["protein.txt", "fat.txt", "veget.txt", "cereals.txt", "fruits.txt"]
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip() not in self.last_consumed:
                        self.last_consumed[line.strip()] = None

    def apply_custom_style(self):
        # Основной стиль приложения
        self.setStyleSheet("""
            QWidget {
                background-color: #F0F4F0;
                color: #2C3E50;
                font-family: Arial, sans-serif;
            }
            QGroupBox {
                background-color: #E8F5E9;
                border: 2px solid #81C784;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 15px;
                margin: 5px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTableWidget {
                gridline-color: #81C784;
                selection-background-color: #C8E6C9;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: 1px solid #81C784;
            }
        # Добавляем стили для календаря
            QCalendarWidget QToolButton {
                height: 20px;
                width: 80px;
                color: white;
                font-size: 10px;
                icon-size: 16px, 16px;
                background-color: #4CAF50;
            }
            QCalendarWidget QMenu {
                width: 100px;
                left: 20px;
                color: white;
                font-size: 10px;
                background-color: #4CAF50;
            }
            QCalendarWidget QSpinBox {
                width: 100px;
                font-size: 10px;
                color: white;
                background-color: #4CAF50;
                selection-background-color: #45a049;
                selection-color: white;
            }
            QCalendarWidget QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; width: 16px; }
            QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right; width: 16px;}
            QCalendarWidget QSpinBox::up-arrow { width: 10px; height: 10px; }
            QCalendarWidget QSpinBox::down-arrow { width: 10px; height: 10px; }
            
            /* Форматирование дней недели */
            QCalendarWidget QWidget { alternate-background-color: #E8F5E9; }
            
            /* Форматирование дней */
            QCalendarWidget QAbstractItemView:enabled 
            {
                font-size: 10px;  
                color: #2C3E50;  
                background-color: white;  
                selection-background-color: #4CAF50; 
                selection-color: white; 
            }
            
            /* Форматирование сегодняшней даты */
            QCalendarWidget QAbstractItemView:disabled 
            { 
                color: #76D7C4;
            }
        """)

        # Настройка цветов для календаря
        calendar_palette = self.calendar.palette()
        calendar_palette.setColor(QPalette.Highlight, QColor("#4CAF50"))
        calendar_palette.setColor(QPalette.HighlightedText, Qt.white)
        self.calendar.setPalette(calendar_palette)

    def get_color_for_days(self, days):
        if days > 0:  # Будущая дата
            return QColor(200, 200, 200)  # Серый цвет
        
        days = abs(days)
        if days > 24:
            return QColor(255, 0, 0) 
        elif days > 22:
            return QColor(255, 28, 0)
        elif days > 22:
            return QColor(255, 57, 0)
        elif days > 20:
            return QColor(255, 85, 0)
        elif days > 18:
            return QColor(255, 113, 0)
        elif days > 16:
            return QColor(255, 142, 0)
        elif days > 14:
            return QColor(255, 170, 0)
        elif days > 12:
            return QColor(255, 198, 0)
        elif days > 10:
            return QColor(255, 226, 0)
        elif days > 8:
            return QColor(255, 255, 0)
        elif days > 6:
            return QColor(182, 255, 0)
        elif days > 4:
            return QColor(145, 255, 0)
        elif days > 2:
            return QColor(72, 255, 0)
        else:
            return QColor(0, 255, 0)  # Зеленый
        
    def load_consumption(self):
        try:
            with open('consumption.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.consumption = data['consumption']
                self.last_consumed = data['last_consumed']
        except FileNotFoundError:
            print("Файл consumption.json не найден. Создаем новые словари.")

    def save_consumption(self):
        with open('consumption.json', 'w', encoding='utf-8') as f:
            json.dump({
                'consumption': self.consumption,
                'last_consumed': self.last_consumed
            }, f, ensure_ascii=False, indent=4)

    def add_selected_items(self):
        selected_date = self.calendar.selectedDate().toString(Qt.ISODate)
        selected_items = []
        
        for group in [self.protein_group, self.fat_group, self.veget_group, self.cereals_group, self.carbs_group]:
            for i in range(group.layout().count()):
                checkbox = group.layout().itemAt(i).widget()
                if checkbox.isChecked():
                    selected_items.append(checkbox.text())
                    self.update_last_consumed(checkbox.text(), selected_date)
                    checkbox.setChecked(False)
        
        if selected_items:
            if selected_date not in self.consumption:
                self.consumption[selected_date] = {}
            
            new_meal_number = str(len(self.consumption[selected_date]) + 1)
            self.consumption[selected_date][new_meal_number] = selected_items
            
            self.update_table()
            self.update_least_consumed_list()
            self.save_consumption()

    def update_last_consumed(self, item, new_date):
        if item not in self.last_consumed or self.last_consumed[item] is None:
            self.last_consumed[item] = new_date
        else:
            current_date = QDate.fromString(self.last_consumed[item], Qt.ISODate)
            new_qdate = QDate.fromString(new_date, Qt.ISODate)
            if new_qdate > current_date:
                self.last_consumed[item] = new_date

    def update_table(self):
        self.table.setRowCount(0)
        for date in sorted(self.consumption.keys(), reverse=True):
            for meal_number, items in self.consumption[date].items():
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(date))
                self.table.setItem(row_position, 1, QTableWidgetItem(meal_number))
                
                products_item = QTableWidgetItem(", ".join(items))
                products_item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
                self.table.setItem(row_position, 2, products_item)

    def update_least_consumed_list(self):
        current_date = QDate.currentDate()
        
        # Создаем список кортежей (продукт, дата, дней_с_последнего_употребления)
        sorted_items = []
        for item, date in self.last_consumed.items():
            if date is None:
                days_since = float('inf')  # Бесконечность для неупотребляемых продуктов
            else:
                days_since = current_date.daysTo(QDate.fromString(date, Qt.ISODate))
            sorted_items.append((item, date, days_since))
        
        # Сортируем список: сначала неупотребляемые, затем от самых давних к недавним
        sorted_items.sort(key=lambda x: (-x[2] if x[1] is None else x[2]))
        
        self.least_consumed_list.setRowCount(0)
        
        for i, (item, date, days_since) in enumerate(sorted_items):
            self.least_consumed_list.insertRow(i)
            self.least_consumed_list.setItem(i, 0, QTableWidgetItem(item))
            self.least_consumed_list.setItem(i, 1, QTableWidgetItem(str(date) if date else "Не употреблялось"))
            
            # Color coding
            if date is None:
                color = QColor(255, 0, 0)  # Red for never consumed
            else:
                color = self.get_color_for_days(days_since)
            
            self.least_consumed_list.item(i, 0).setBackground(color)
            self.least_consumed_list.item(i, 1).setBackground(color)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FoodTrackingApp()
    ex.show()
    sys.exit(app.exec_())