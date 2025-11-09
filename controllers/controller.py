from tkinter import Tk, filedialog, messagebox
from models.model import Model
from views.view import View
from models.edge_model import EdgeDetector


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
        result = self.model.threshold_global(127)
        if result is not None:
            self.view.display_processed(result)
            self.view.log_action("Limiarização global aplicada (valor 127).")

    def apply_threshold_otsu(self):
        result = self.model.threshold_otsu()
        if result is not None:
            self.view.display_processed(result)
            self.view.log_action("Limiarização Otsu aplicada.")

    def apply_threshold_adaptive(self):
        result = self.model.threshold_adaptive()
        if result is not None:
            self.view.display_processed(result)
            self.view.log_action("Limiarização adaptativa aplicada.")