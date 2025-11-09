import tkinter as tk

class MenuBar:
    def __init__(self, root, controller):
        self.controller = controller
        self.menubar = tk.Menu(root)

        # Menu Arquivo
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Abrir", command=controller.open_image)
        file_menu.add_command(label="Salvar como...", command=controller.save_image)
        file_menu.add_separator()

        # NOVO: botão de reset
        file_menu.add_command(label="Resetar imagem", command=controller.reset_image)
        file_menu.add_separator()

        file_menu.add_command(label="Sair", command=root.quit)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Filtros
        filter_menu = tk.Menu(self.menubar, tearoff=0)
        filter_menu.add_command(label="Converter para tons de cinza", command=controller.apply_gray)
        filter_menu.add_command(label="Equalizar histograma", command=controller.apply_equalization)
        self.menubar.add_cascade(label="Filtros", menu=filter_menu)
        edge_menu = tk.Menu(filter_menu, tearoff=0)
        edge_menu.add_command(label="Sobel X", command=self.controller.apply_sobel_x)
        edge_menu.add_command(label="Sobel Y", command=self.controller.apply_sobel_y)
        edge_menu.add_command(label="Sobel XY", command=self.controller.apply_sobel_xy)
        edge_menu.add_command(label="Sobel Magnitude", command=self.controller.apply_sobel_magnitude)
        edge_menu.add_separator()
        edge_menu.add_command(label="Sobel", command=self.controller.apply_sobel)
        edge_menu.add_command(label="Laplaciano", command=self.controller.apply_laplacian)
        edge_menu.add_command(label="Canny", command=self.controller.apply_canny)
        filter_menu.add_cascade(label="Detecção de Bordas", menu=edge_menu)

        # Menu de Limiarização
        threshold_menu = tk.Menu(filter_menu, tearoff=0)
        threshold_menu.add_command(label="Limiarização Global", command=self.controller.apply_threshold_global)
        threshold_menu.add_command(label="Limiarização Otsu", command=self.controller.apply_threshold_otsu)
        threshold_menu.add_command(label="Limiarização Adaptativa", command=self.controller.apply_threshold_adaptive)
        filter_menu.add_cascade(label="Limiarização", menu=threshold_menu)

        # Submenu de Conversão de Cores
        color_menu = tk.Menu(filter_menu, tearoff=0)
        color_menu.add_command(label="Converter para HSV", command=self.controller.apply_hsv)
        color_menu.add_command(label="Converter para LAB", command=self.controller.apply_lab)
        color_menu.add_command(label="Converter para YCrCb", command=self.controller.apply_ycrcb)
        color_menu.add_command(label="Converter para CMYK (simulado)", command=self.controller.apply_cmyk)
        filter_menu.add_cascade(label="Conversão de Cores", menu=color_menu)
