import tkinter as tk
from PIL import Image, ImageTk
import cv2

class ImagePanel:
    def __init__(self, root):
        # Frame principal (área central da janela)
        self.frame = tk.Frame(root, bg="#2b2b2b")
        self.frame.pack(fill="both", expand=True)

        # Títulos
        self.label_original = tk.Label(self.frame, text="Imagem Original", bg="#2b2b2b", fg="white")
        self.label_original.grid(row=0, column=0, padx=10, pady=5)

        self.label_processed = tk.Label(self.frame, text="Imagem Processada", bg="#2b2b2b", fg="white")
        self.label_processed.grid(row=0, column=1, padx=10, pady=5)

        # Dois painéis de imagem lado a lado
        self.original_panel = tk.Label(self.frame, bg="gray")
        self.original_panel.grid(row=1, column=0, padx=10, pady=10)

        self.processed_panel = tk.Label(self.frame, bg="gray")
        self.processed_panel.grid(row=1, column=1, padx=10, pady=10)

        # Guarda as referências das imagens
        self.original_imgtk = None
        self.processed_imgtk = None

    def show_original(self, image):
        """Exibe imagem original (OpenCV -> Tkinter)."""
        self.original_imgtk = self._convert_image(image)
        if self.original_imgtk:
            self.original_panel.config(image=self.original_imgtk)
            self.original_panel.image = self.original_imgtk

    def show_processed(self, image):
        """Exibe imagem processada (OpenCV -> Tkinter)."""
        self.processed_imgtk = self._convert_image(image)
        if self.processed_imgtk:
            self.processed_panel.config(image=self.processed_imgtk)
            self.processed_panel.image = self.processed_imgtk

    def _convert_image(self, img):
        """Aceita tanto imagem OpenCV (NumPy) quanto PhotoImage."""
        from PIL import Image, ImageTk
        import cv2

        if img is None:
            return None

        # Se já for PhotoImage, retorna direto
        if isinstance(img, ImageTk.PhotoImage):
            return img

        # Se for array NumPy, converte normalmente
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img_pil = Image.fromarray(img)
        return ImageTk.PhotoImage(img_pil)
