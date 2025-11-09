import tkinter as tk
from views.menu_bar import MenuBar
from views.image_panel import ImagePanel
from views.control_panel import ControlPanel
from PIL import Image, ImageTk
import cv2


class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # ===== Menu superior =====
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # ===== Painéis principais =====
        self.image_panel = ImagePanel(self.root)
        self.control_panel = ControlPanel(self.root)

        # Layout: painel de controle à direita, imagens à esquerda
        self.control_panel.frame.pack(side="right", fill="y")
        self.image_panel.frame.pack(side="left", fill="both", expand=True)

    # ===== Exibição de imagens =====
    def display_original(self, image):
        """Mostra a imagem original no painel esquerdo."""
        self.image_panel.show_original(image)

    def display_processed(self, image):
        """Mostra a imagem processada no painel direito."""
        self.image_panel.show_processed(image)

    def display_image(self, image):
        """Compatibilidade com filtros antigos (mostra como processada)."""
        self.display_processed(image)

    def update_image(self, image):
        """Atualiza o painel processado (mantendo suporte a filtros)."""
        self.display_processed(image)

    # ===== Log de ações =====
    def log_action(self, text):
        self.control_panel.add_log(text)