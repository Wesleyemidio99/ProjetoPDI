from tkinter import Tk, filedialog, messagebox
from models.model import Model
from views.view import View
from models.edge_model import EdgeDetector
from models.threshold_model import ThresholdModel
from models.color_model import ColorModel
from models.histogram_model import HistogramModel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk
import cv2


class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.title("PDI Studio - Sistema Interativo de Processamento de Imagens")
        self.root.geometry("1600x900")

        # Model
        self.model = Model()

        # View
        self.view = View(self.root, controller=self)

    # ========== Métodos principais ==========
    def run(self):
        self.root.mainloop()

    def open_image(self):
        path = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[("Arquivos de imagem", "*.png;*.jpg;*.jpeg;*.bmp")]
        )
        if path:
            image = self.model.load_image(path)
            self.view.display_original(image)
            self.view.display_processed(image)
            self.view.log_action(f"Imagem carregada: {path}")

    def save_image(self):
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")]
        )
        if path:
            self.model.save_image(path)
            self.view.log_action(f"Imagem salva em: {path}")

    def apply_gray(self):
        result = self.model.convert_to_gray()
        self.view.display_image(result)
        self.view.log_action("Conversão para tons de cinza aplicada.")

    def apply_equalization(self):
        result = self.model.equalize_histogram()
        self.view.display_image(result)
        self.view.log_action("Equalização de histograma aplicada.")

    def apply_sobel(self):
        result = EdgeDetector.sobel(self.model.current)
        self.view.update_image(result)
        if self.model.current is None:
            messagebox.showerror("Erro", "Nenhuma imagem carregada!")
            return

        result = EdgeDetector.sobel(self.model.current)
        self.view.log_action("Filtro Sobel aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_laplacian(self):
        result = EdgeDetector.laplacian(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Laplaciano aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_canny(self):
        result = EdgeDetector.canny(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Canny aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_sobel_x(self):
        result = EdgeDetector.sobel_x(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel X aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_sobel_y(self):
        result = EdgeDetector.sobel_y(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel Y aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_sobel_xy(self):
        result = EdgeDetector.sobel_xy(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel XY aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def apply_sobel_magnitude(self):
        result = EdgeDetector.sobel_magnitude(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel Magnitude aplicado.")
        self.show_histogram()                       # atualiza o histograma

    def reset_image(self):
        """Restaura a imagem original e reseta sliders."""
        if self.model.original is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada para restaurar.")
            return

        # Restaura imagem original
        self.model.image = self.model.original.copy()
        self.view.image_panel.update_image(self.model.image)

        # Reseta sliders
        self.view.control_panel.brightness_slider.set(0)
        self.view.control_panel.contrast_slider.set(0)
        self.view.control_panel.tones_slider.set(4)

        self.view.log_action("Imagem restaurada e sliders resetados.")


    # ========== Limiarização ==========
    def apply_threshold_global(self):
        result = ThresholdModel.global_threshold(self.model.image, 127)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização global aplicada (valor 127).")
            self.show_histogram()                       # atualiza o histograma

    def apply_threshold_otsu(self):
        result = ThresholdModel.otsu_threshold(self.model.image)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização Otsu aplicada.")
            self.show_histogram()                       # atualiza o histograma

    def apply_threshold_adaptive(self):
        result = ThresholdModel.adaptive_threshold(self.model.image)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização adaptativa aplicada.")
            self.show_histogram()                       # atualiza o histograma

    # ========== Conversão de Cores ==========
    def apply_hsv(self):
        result = ColorModel.to_hsv(self.model.image)
        if result is not None:
            self.view.display_processed(cv2.cvtColor(result, cv2.COLOR_HSV2BGR))
            self.model.image = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
            self.view.log_action("Conversão para HSV aplicada.")

    def apply_lab(self):
        result = ColorModel.to_lab(self.model.image)
        if result is not None:
            self.view.display_processed(cv2.cvtColor(result, cv2.COLOR_LAB2BGR))
            self.model.image = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
            self.view.log_action("Conversão para LAB aplicada.")

    def apply_ycrcb(self):
        result = ColorModel.to_ycrcb(self.model.image)
        if result is not None:
            self.view.display_processed(cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR))
            self.model.image = cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR)
            self.view.log_action("Conversão para YCrCb aplicada.")

    def apply_cmyk(self):
        result = ColorModel.to_cmyk(self.model.image)
        if result is not None:
            # Mostra só C, M, Y (ignora o canal K para visualização)
            cmy = cv2.merge([result[..., 0], result[..., 1], result[..., 2]])
            self.view.display_processed(cmy)
            self.model.image = cmy
            self.view.log_action("Conversão para CMYK aplicada (simulada).")

    def apply_rgba(self):
        result = ColorModel.to_rgba(self.model.image)
        if result is not None:
            self.view.display_processed(cv2.cvtColor(result, cv2.COLOR_BGRA2BGR))
            self.model.image = cv2.cvtColor(result, cv2.COLOR_BGRA2BGR)
            self.view.log_action("Conversão para RGBA aplicada.")

    def handle_pixel_click(self, x, y, panel_type):
        """Busca e exibe os valores RGB e HSV do pixel clicado."""
        if panel_type == "original":
            image = self.model.original
        else:
            image = self.model.image

        values = self.model.get_pixel_values_from(image, x, y)
        if values:
            text = (
                f"[{panel_type.upper()}] Pixel (x={values['coord'][0]}, y={values['coord'][1]})\n"
                f"RGB = {values['rgb']} | HSV = {values['hsv']}"
            )
            self.view.show_pixel_info(text)

    # ========== Histograma ==========
    def show_histogram(self):
        """Abre uma janela para exibir o histograma da imagem atual."""
        if self.model.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return

        # Cria uma nova janela para o gráfico
        hist_window = tk.Toplevel(self.root)
        hist_window.title("Histograma da Imagem")
        hist_window.geometry("600x400")

        HistogramModel.show_histogram(self.model.image, hist_window)
        self.view.log_action("Histograma exibido.")

    def apply_equalization(self):
        """Aplica equalização de histograma na imagem atual."""
        # Pega a imagem atual do ImagePanel
        img = self.view.image_panel.current_image

        if img is None:
            print("Nenhuma imagem carregada")
            return

        # Se a imagem for colorida, converte para cinza
        if len(img.shape) == 3 and img.shape[2] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        # Aplica equalização
        equalized = cv2.equalizeHist(gray)

        # Atualiza a imagem processada no painel
        self.view.image_panel.update_image(equalized)

    def apply_multilevel_threshold(self, levels=4):
        img = self.view.image_panel.current_image
        if img is None:
            return
        result = ThresholdModel.multilevel_threshold(img, levels)
        self.view.image_panel.update_image(result)

        # Adicionar canvas no ImagePanel
        if hasattr(self, 'hist_canvas'):
            self.hist_canvas.get_tk_widget().destroy()  # remove canvas antigo

        self.hist_canvas = FigureCanvasTkAgg(fig, master=self.view.image_panel.frame)
        self.hist_canvas.get_tk_widget().grid(row=2, column=1, pady=10)  # abaixo do painel processado
        self.hist_canvas.draw()

    def update_brightness_contrast(self, brightness, contrast):
        """
        Ajusta brilho e contraste da imagem atual.
        brightness: -100 a 100
        contrast: -100 a 100
        """
        # Pega a imagem original (não alterada)
        img = self.model.image  # ou self.model.current / self.model.original dependendo de como você guarda
        if img is None:
            return

        # Calcula alpha e beta
        alpha = 1.0 + (contrast / 100.0)
        beta = brightness

        # Aplica brilho/contraste na imagem original
        adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        # Atualiza a imagem processada no painel
        self.view.image_panel.update_image(adjusted)