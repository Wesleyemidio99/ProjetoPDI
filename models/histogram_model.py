import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HistogramModel:
    """Responsável por calcular e exibir histogramas de imagens."""

    @staticmethod
    def calculate_histogram(image):
        """Calcula o histograma da imagem em tons de cinza ou por canal de cor."""
        if image is None:
            return None

        # Se for imagem colorida, calcula histograma de cada canal
        if len(image.shape) == 3:
            chans = cv2.split(image)
            colors = ('b', 'g', 'r')
            hist_data = []
            for chan, color in zip(chans, colors):
                hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
                hist_data.append((hist, color))
            return hist_data

        # Caso seja imagem em tons de cinza
        else:
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            return [(hist, 'gray')]

    @staticmethod
    def show_histogram(image, parent):
        """Gera e exibe o histograma dentro de uma janela ou frame Tkinter."""
        hist_data = HistogramModel.calculate_histogram(image)
        if hist_data is None:
            return

        # Cria figura matplotlib
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_title("Histograma da Imagem")
        ax.set_xlabel("Intensidade")
        ax.set_ylabel("Número de Pixels")

        for hist, color in hist_data:
            ax.plot(hist, color=color)
            ax.set_xlim([0, 256])

        # Renderiza dentro do Tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
