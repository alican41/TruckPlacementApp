from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QTextEdit, QMessageBox,
                             QProgressBar, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from core.truck_loader import TruckLoader
import os


class LoaderThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, excel_path):
        super().__init__()
        self.excel_path = excel_path
        self.loader = TruckLoader()

    def run(self):
        try:
            self.progress.emit(20)
            result = self.loader.optimize_loading(self.excel_path)
            self.progress.emit(80)
            self.finished.emit(result)
            self.progress.emit(100)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = None
        self.excel_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TIR Yükleme Optimizasyon Sistemi")
        self.setGeometry(100, 100, 1200, 800)

        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Başlık
        title_label = QLabel("TIR YÜKLEME OPTİMİZASYON SİSTEMİ")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; padding: 20px;")
        main_layout.addWidget(title_label)

        # Dosya seçim grubu
        file_group = QGroupBox("Excel Dosyası Seçimi")
        file_layout = QHBoxLayout()

        self.file_label = QLabel("Dosya seçilmedi")
        self.file_label.setStyleSheet("padding: 5px; background-color: #ecf0f1; border-radius: 3px;")
        file_layout.addWidget(self.file_label)

        self.select_btn = QPushButton("Dosya Seç")
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_btn)

        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)

        # İşlem butonları
        btn_layout = QHBoxLayout()

        self.optimize_btn = QPushButton("Optimizasyonu Başlat")
        self.optimize_btn.setEnabled(False)
        self.optimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 15px 30px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.optimize_btn.clicked.connect(self.start_optimization)
        btn_layout.addWidget(self.optimize_btn)

        self.export_pdf_btn = QPushButton("PDF Dışa Aktar")
        self.export_pdf_btn.setEnabled(False)
        self.export_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 15px 30px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        btn_layout.addWidget(self.export_pdf_btn)

        main_layout.addLayout(btn_layout)

        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # İstatistik paneli
        stats_group = QGroupBox("Yükleme İstatistikleri")
        stats_layout = QGridLayout()

        self.first_section_label = QLabel("İlk 10 Alan: - kg")
        self.first_section_label.setStyleSheet(
            "font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 3px;")
        stats_layout.addWidget(self.first_section_label, 0, 0)

        self.total_weight_label = QLabel("Toplam Ağırlık: - kg")
        self.total_weight_label.setStyleSheet(
            "font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 3px;")
        stats_layout.addWidget(self.total_weight_label, 0, 1)

        stats_group.setLayout(stats_layout)
        main_layout.addWidget(stats_group)

        # Sonuç alanı
        result_group = QGroupBox("Yükleme Planı")
        result_layout = QVBoxLayout()

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New';
                font-size: 11px;
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        result_layout.addWidget(self.result_text)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        # Durum çubuğu
        self.statusBar().showMessage("Hazır")
        self.statusBar().setStyleSheet("background-color: #34495e; color: white; padding: 5px;")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Excel Dosyası Seç",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_path:
            self.excel_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.optimize_btn.setEnabled(True)
            self.statusBar().showMessage(f"Dosya seçildi: {os.path.basename(file_path)}")

    def start_optimization(self):
        if not self.excel_path:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir Excel dosyası seçin!")
            return

        self.optimize_btn.setEnabled(False)
        self.export_pdf_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("Optimizasyon çalışıyor...")

        self.worker_thread = LoaderThread(self.excel_path)
        self.worker_thread.finished.connect(self.on_optimization_finished)
        self.worker_thread.error.connect(self.on_optimization_error)
        self.worker_thread.progress.connect(self.update_progress)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def on_optimization_finished(self, result):
        self.loader = self.worker_thread.loader
        self.result_text.setText(result)

        # İstatistikleri güncelle
        self.first_section_label.setText(f"İlk 10 Alan: {self.loader.ilk10Alan:.1f} kg")
        self.total_weight_label.setText(f"Toplam Ağırlık: {self.loader.toplamAlan:.1f} kg")

        self.optimize_btn.setEnabled(True)
        self.export_pdf_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Optimizasyon tamamlandı!")

        QMessageBox.information(self, "Başarılı", "Yükleme optimizasyonu başarıyla tamamlandı!")

    def on_optimization_error(self, error_msg):
        self.optimize_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Hata oluştu!")
        QMessageBox.critical(self, "Hata", f"Optimizasyon sırasında hata oluştu:\n{error_msg}")

    def export_pdf(self):
        if not self.loader:
            QMessageBox.warning(self, "Uyarı", "Önce optimizasyonu çalıştırın!")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "PDF Kaydet",
            "truck_layout.pdf",
            "PDF Files (*.pdf)"
        )

        if file_path:
            try:
                self.statusBar().showMessage("PDF oluşturuluyor...")
                self.loader.plot_truck_layout(file_path)
                self.statusBar().showMessage(f"PDF başarıyla kaydedildi: {os.path.basename(file_path)}")
                QMessageBox.information(self, "Başarılı", f"PDF dosyası başarıyla kaydedildi:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"PDF oluşturulurken hata oluştu:\n{str(e)}")
                self.statusBar().showMessage("PDF oluşturma hatası!")