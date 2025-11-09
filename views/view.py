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

        # Menu superior
        self.menu = MenuBar(self.root, controller)
        self.root.config(menu=self.menu.menubar)

        # Painéis
        self.image_panel = ImagePanel(self.root)
        self.control_panel = ControlPanel(self.root)

        # Prioriza empacotar o painel de controle primeiro para reservar espaço do log
        self.control_panel.frame.pack(side="right", fill="y")
        self.image_panel.frame.pack(side="left", fill="both", expand=True)

    def display_image(self, image):
        self.image_panel.show_image(image)

    def log_action(self, text):
        self.control_panel.add_log(text)

    def update_image(self, result):
        # Converte o resultado (matriz do OpenCV) em imagem Tkinter
        from PIL import Image, ImageTk
        import cv2

        if result is None:
            return

        # Se for imagem 2D (tons de cinza), converte para RGB
        if len(result.shape) == 2:
            image_rgb = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
        else:
            image_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        # Converte para imagem compatível com Tkinter
        image_pil = Image.fromarray(image_rgb)
        img_tk = ImageTk.PhotoImage(image_pil)

        # Atualiza o painel de imagem
        self.image_panel.show_image(img_tk)

    def display_processed(self, img):
        """Exibe uma imagem processada (OpenCV) no Tkinter"""
        # Converte de BGR (OpenCV) para RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)

        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk  # mantém referência
