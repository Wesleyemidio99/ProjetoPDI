import tkinter as tk
from tkinter import scrolledtext

class ControlPanel:
    def __init__(self, root):
        self.frame = tk.Frame(root, bg="#333", width=250)
        self.frame.pack_propagate(False)

        # ===== Seção de ajuste de brilho e contraste =====
        tk.Label(self.frame, text="Ajuste de Brilho e Contraste", fg="white", bg="#333", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        # Slider de brilho
        tk.Label(self.frame, text="Brilho", fg="white", bg="#333").pack()
        self.brightness_slider = tk.Scale(
            self.frame, from_=-100, to=100, orient="horizontal",
            length=200, bg="#333", fg="white", highlightthickness=0,
            command=self.on_brightness_change
        )
        self.brightness_slider.pack(pady=(0, 10))

        # Slider de contraste
        tk.Label(self.frame, text="Contraste", fg="white", bg="#333").pack()
        self.contrast_slider = tk.Scale(
            self.frame, from_=-100, to=100, orient="horizontal",
            length=200, bg="#333", fg="white", highlightthickness=0,
            command=self.on_contrast_change
        )
        self.contrast_slider.pack(pady=(0, 10))

        # Botão de reset (opcional)
        self.reset_btn = tk.Button(
            self.frame, text="Resetar Ajustes",
            command=self.reset_adjustments, bg="#555", fg="white", width=20
        )
        self.reset_btn.pack(pady=(5, 15))

        # ===== Seção de log =====
        tk.Label(self.frame, text="Histórico de Ações", fg="white", bg="#333", font=("Arial", 10, "bold")).pack(pady=(5, 0))
        self.log_area = scrolledtext.ScrolledText(self.frame, width=35, height=25, bg="#111", fg="white")
        self.log_area.pack(padx=5, pady=5)

        # Controle interno
        self.controller = None
        self.current_brightness = 0
        self.current_contrast = 0

        # ===== Seção de Limiarização Multiníveis =====
        tk.Label(self.frame, text="Limiarização Multiníveis", fg="white", bg="#333", font=("Arial", 10, "bold")).pack(pady=(10, 5))

        self.tones_slider = tk.Scale(
            self.frame,
            from_=2,
            to=16,
            resolution=2,
            orient="horizontal",
            length=200,
            bg="#333",
            fg="white",
            highlightthickness=0,
            command=self.on_tone_change
        )
        self.tones_slider.set(4)  # valor inicial
        self.tones_slider.pack(pady=(0, 10))

    # ===== Métodos de integração =====
    def set_controller(self, controller):
        """Define o controller, chamado pela View."""
        self.controller = controller

    def on_brightness_change(self, value):
        """Envia novo valor de brilho ao controller."""
        self.current_brightness = int(value)
        if self.controller:
            self.controller.update_brightness_contrast(self.current_brightness, self.current_contrast)

    def on_contrast_change(self, value):
        """Envia novo valor de contraste ao controller."""
        self.current_contrast = int(value)
        if self.controller:
            self.controller.update_brightness_contrast(self.current_brightness, self.current_contrast)

    def reset_adjustments(self):
        """Reseta sliders e imagem para o estado original."""
        self.brightness_slider.set(0)
        self.contrast_slider.set(0)
        if self.controller:
            self.controller.reset_image()
        self.add_log("Ajustes de brilho e contraste resetados.")

    def add_log(self, text):
        """Adiciona mensagem no histórico."""
        self.log_area.insert(tk.END, f"> {text}\n")
        self.log_area.see(tk.END)

    def on_tone_change(self, value):
        """Envia o valor selecionado pelo slider ao Controller."""
        levels = int(value)
        if self.controller:
            self.controller.apply_multilevel_threshold(levels)
            self.add_log(f"Limiarização multinível aplicada com {levels} tons.")

