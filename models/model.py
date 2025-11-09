import cv2
import numpy as np
from PIL import Image, ImageTk

class Model:
    def __init__(self):
        self.image = None       # Imagem atual (processada)
        self.original = None    # Imagem original
        self.current = None     # Cópia para operações temporárias

    def load_image(self, path):
        """Carrega imagem com suporte a caminhos com acento."""
        try:
            data = np.fromfile(path, dtype=np.uint8)
            self.image = cv2.imdecode(data, cv2.IMREAD_COLOR)

            if self.image is None:
                raise ValueError(f"Não foi possível carregar a imagem: {path}")

            # Guarda cópias
            self.original = self.image.copy()
            self.current = self.image.copy()

            return self.image  # Retorna imagem em formato OpenCV (array NumPy)

        except Exception as e:
            raise ValueError(f"Erro ao carregar a imagem: {e}")

    def save_image(self, path):
        """Salva a imagem atual."""
        if self.image is not None:
            cv2.imwrite(path, self.image)

    def reset_image(self):
        """Restaura a imagem processada ao estado original."""
        if self.original is not None:
            self.image = self.original.copy()
            return self.image  # Retorna imagem OpenCV (não PhotoImage)
        return None

    # ========== Operações de PDI ==========
    def convert_to_gray(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        return self.image

    def equalize_histogram(self):
        if self.image is None:
            return None
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        self.image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        return self.image

    # ========== Conversão auxiliar (opcional) ==========
    def to_tk_image(self, cv_image):
        """Converte imagem OpenCV -> Tkinter PhotoImage."""
        rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        return ImageTk.PhotoImage(img)