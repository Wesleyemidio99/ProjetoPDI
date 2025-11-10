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

        # ===== Painel de Controle (criado após menu, antes das imagens) =====
        self.control_panel = ControlPanel(self.root)
        self.control_panel.set_controller(controller)

        # ===== Painel de Imagens =====
        # ⚠️ Verifique se ImagePanel aceita 2 parâmetros. Se não aceitar controller, use apenas (self.root)
        self.image_panel = ImagePanel(self.root, self.controller)

        # ===== Eventos de clique =====
        self.image_panel.original_panel.bind("<Button-1>", lambda e: self.on_click(e, "original"))
        self.image_panel.processed_panel.bind("<Button-1>", lambda e: self.on_click(e, "processed"))

        # ===== Layout =====
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
        """Atualiza o painel processado."""
        self.display_processed(image)

    # ===== Log de ações =====
    def log_action(self, text):
        self.control_panel.add_log(text)

    # ===== Clique nas imagens =====
    def on_click(self, event, panel_type):
        """Detecta clique do usuário e informa ao Controller as coordenadas do pixel."""
        if self.controller.model.image is None:
            return

        if panel_type == "original":
            img = self.controller.model.original
            panel = self.image_panel.original_panel
        else:
            img = self.controller.model.image
            panel = self.image_panel.processed_panel

        if img is None:
            return

        # Dimensões reais x exibidas
        h, w = img.shape[:2]
        panel_w = panel.winfo_width()
        panel_h = panel.winfo_height()

        # Coordenadas proporcionais
        x = int(event.x * w / panel_w)
        y = int(event.y * h / panel_h)

        # Envia para o controller
        self.controller.handle_pixel_click(x, y, panel_type)

    def show_pixel_info(self, text):
        """Mostra informações do pixel clicado no painel de log."""
        self.control_panel.add_log(text)
