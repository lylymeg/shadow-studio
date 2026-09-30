import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QPushButton, QColorDialog, QFrame, QTextEdit,
    QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor


class CSSShadowStudio(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Studio CSS Box-Shadow 🎨")
        self.setFixedSize(850, 580)
        self.setStyleSheet("background-color: #1E222B;")

        # Valeurs par défaut du Box-Shadow
        self.offset_x = 10
        self.offset_y = 10
        self.blur_radius = 20
        self.spread_radius = 5
        self.shadow_color = QColor(0, 0, 0, 100)  # RGBA avec alpha à ~40%
        self.box_color = QColor("#61AFEF")
        self.bg_color = QColor("#282C34")

        self.init_ui()
        self.update_preview()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ================= PANNEAU DE CONTRÔLE (GAUCHE) =================
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)

        title = QLabel("⚙️ Réglages Box-Shadow")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: #ECEFF4;")
        controls_layout.addWidget(title)

        # Sliders
        self.slider_x, self.lbl_x = self.create_slider_row("Décalage X (px):", -50, 50, self.offset_x, controls_layout)
        self.slider_y, self.lbl_y = self.create_slider_row("Décalage Y (px):", -50, 50, self.offset_y, controls_layout)
        self.slider_blur, self.lbl_blur = self.create_slider_row("Flou / Blur (px):", 0, 100, self.blur_radius, controls_layout)
        self.slider_spread, self.lbl_spread = self.create_slider_row("Diffusion / Spread (px):", -20, 50, self.spread_radius, controls_layout)
        self.slider_opacity, self.lbl_opacity = self.create_slider_row("Opacité Ombre (%):", 0, 100, int(self.shadow_color.alpha() / 255 * 100), controls_layout)

        # Connection des sliders
        self.slider_x.valueChanged.connect(self.update_values)
        self.slider_y.valueChanged.connect(self.update_values)
        self.slider_blur.valueChanged.connect(self.update_values)
        self.slider_spread.valueChanged.connect(self.update_values)
        self.slider_opacity.valueChanged.connect(self.update_values)

        # Sélecteurs de Couleurs
        colors_layout = QHBoxLayout()

        btn_shadow_color = QPushButton("Couleur Ombre")
        btn_shadow_color.setCursor(Qt.PointingHandCursor)
        btn_shadow_color.setStyleSheet(self.get_btn_style("#98C379", "#1E222B"))
        btn_shadow_color.clicked.connect(self.choose_shadow_color)

        btn_box_color = QPushButton("Couleur Bloc")
        btn_box_color.setCursor(Qt.PointingHandCursor)
        btn_box_color.setStyleSheet(self.get_btn_style("#61AFEF", "#1E222B"))
        btn_box_color.clicked.connect(self.choose_box_color)

        colors_layout.addWidget(btn_shadow_color)
        colors_layout.addWidget(btn_box_color)
        controls_layout.addLayout(colors_layout)

        # Zone d'affichage du code CSS
        lbl_css_title = QLabel("💻 Code CSS généré :")
        lbl_css_title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        lbl_css_title.setStyleSheet("color: #ABB2BF;")
        controls_layout.addWidget(lbl_css_title)

        self.txt_css_output = QTextEdit()
        self.txt_css_output.setReadOnly(True)
        self.txt_css_output.setFont(QFont("Consolas", 10))
        self.txt_css_output.setFixedHeight(80)
        self.txt_css_output.setStyleSheet("""
            QTextEdit {
                background-color: #21252B;
                color: #98C379;
                border: 1px solid #3E4451;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        controls_layout.addWidget(self.txt_css_output)

        # Bouton Copier CSS
        btn_copy = QPushButton("📋 Copier le Code CSS")
        btn_copy.setFont(QFont("Segoe UI", 10, QFont.Bold))
        btn_copy.setCursor(Qt.PointingHandCursor)
        btn_copy.setStyleSheet(self.get_btn_style("#E5C07B", "#1E222B"))
        btn_copy.clicked.connect(self.copy_css_code)
        controls_layout.addWidget(btn_copy)

        main_layout.addLayout(controls_layout, stretch=1)

        # ================= ZONE D'APERÇU (DROITE) =================
        self.preview_container = QFrame()
        self.preview_container.setStyleSheet(f"background-color: {self.bg_color.name()}; border-radius: 12px;")
        preview_layout = QVBoxLayout(self.preview_container)

        self.preview_box = QFrame()
        self.preview_box.setFixedSize(200, 200)
        preview_layout.addWidget(self.preview_box, alignment=Qt.AlignCenter)

        main_layout.addWidget(self.preview_container, stretch=1)

    def create_slider_row(self, text, min_val, max_val, default_val, parent_layout):
        layout = QVBoxLayout()
        header_layout = QHBoxLayout()

        lbl_title = QLabel(text)
        lbl_title.setStyleSheet("color: #ABB2BF;")
        lbl_val = QLabel(str(default_val))
        lbl_val.setStyleSheet("color: #61AFEF; font-weight: bold;")

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_val, alignment=Qt.AlignRight)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: #3E4451;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #61AFEF;
                width: 16px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #61AFEF;
                border-radius: 3px;
            }
        """)

        layout.addLayout(header_layout)
        layout.addWidget(slider)
        parent_layout.addLayout(layout)

        return slider, lbl_val

    def choose_shadow_color(self):
        color = QColorDialog.getColor(self.shadow_color, self, "Choisir la couleur de l'ombre")
        if color.isValid():
            # Conserver la transparence actuelle du slider
            alpha = self.shadow_color.alpha()
            self.shadow_color = color
            self.shadow_color.setAlpha(alpha)
            self.update_preview()

    def choose_box_color(self):
        color = QColorDialog.getColor(self.box_color, self, "Choisir la couleur du bloc")
        if color.isValid():
            self.box_color = color
            self.update_preview()

    def update_values(self):
        self.offset_x = self.slider_x.value()
        self.offset_y = self.slider_y.value()
        self.blur_radius = self.slider_blur.value()
        self.spread_radius = self.slider_spread.value()

        # Conversion pourcentage slider -> 0..255 alpha
        opacity_pct = self.slider_opacity.value()
        self.shadow_color.setAlpha(int(opacity_pct / 100 * 255))

        self.lbl_x.setText(f"{self.offset_x}px")
        self.lbl_y.setText(f"{self.offset_y}px")
        self.lbl_blur.setText(f"{self.blur_radius}px")
        self.lbl_spread.setText(f"{self.spread_radius}px")
        self.lbl_opacity.setText(f"{opacity_pct}%")

        self.update_preview()

    def update_preview(self):
        rgba_str = f"rgba({self.shadow_color.red()}, {self.shadow_color.green()}, {self.shadow_color.blue()}, {round(self.shadow_color.alpha() / 255, 2)})"
        css_shadow = f"{self.offset_x}px {self.offset_y}px {self.blur_radius}px {self.spread_radius}px {rgba_str}"

        # Application du style CSS au composant d'aperçu
        self.preview_box.setStyleSheet(f"""
            QFrame {{
                background-color: {self.box_color.name()};
                border-radius: 16px;
                box-shadow: {css_shadow};
            }}
        """)

        # Mise à jour du texte CSS
        formatted_css = f"box-shadow: {css_shadow};\n-webkit-box-shadow: {css_shadow};"
        self.txt_css_output.setText(formatted_css)

    def copy_css_code(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.txt_css_output.toPlainText())
        QMessageBox.information(self, "Copié !", "Code CSS copié dans le presse-papier avec succès !")

    def get_btn_style(self, bg_color, text_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CSSShadowStudio()
    window.show()
    sys.exit(app.exec_())