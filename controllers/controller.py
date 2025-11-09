from tkinter import Tk, filedialog, messagebox
from models.model import Model
from views.view import View
from models.edge_model import EdgeDetector
from models.threshold_model import ThresholdModel
from models.color_model import ColorModel
from models.histogram_model import HistogramModel

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

    def apply_laplacian(self):
        result = EdgeDetector.laplacian(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Laplaciano aplicado.")

    def apply_canny(self):
        result = EdgeDetector.canny(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Canny aplicado.")

    def apply_sobel_x(self):
        result = EdgeDetector.sobel_x(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel X aplicado.")

    def apply_sobel_y(self):
        result = EdgeDetector.sobel_y(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel Y aplicado.")

    def apply_sobel_xy(self):
        result = EdgeDetector.sobel_xy(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel XY aplicado.")

    def apply_sobel_magnitude(self):
        result = EdgeDetector.sobel_magnitude(self.model.current)
        self.view.update_image(result)
        self.view.log_action("Filtro Sobel Magnitude aplicado.")

    def reset_image(self):
        """Restaura a imagem processada ao estado original."""
        restored = self.model.reset_image()
        if restored is not None:
            self.view.display_processed(restored)
            self.view.log_action("Imagem restaurada ao estado original.")
        else:
            from tkinter import messagebox
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada para restaurar.")


    # ========== Limiarização ==========
    def apply_threshold_global(self):
        result = ThresholdModel.global_threshold(self.model.image, 127)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização global aplicada (valor 127).")

    def apply_threshold_otsu(self):
        result = ThresholdModel.otsu_threshold(self.model.image)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização Otsu aplicada.")

    def apply_threshold_adaptive(self):
        result = ThresholdModel.adaptive_threshold(self.model.image)
        if result is not None:
            self.view.display_processed(result)
            self.model.image = result
            self.view.log_action("Limiarização adaptativa aplicada.")

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