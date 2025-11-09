import cv2

class ColorModel:
    """Responsável por converter entre diferentes espaços de cor."""

    @staticmethod
    def to_hsv(image):
        """Converte a imagem de BGR (padrão OpenCV) para HSV."""
        if image is None:
            return None
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    @staticmethod
    def to_lab(image):
        """Converte a imagem de BGR para CIELAB."""
        if image is None:
            return None
        return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    @staticmethod
    def to_ycrcb(image):
        """Converte a imagem de BGR para YCrCb (usado em vídeo)."""
        if image is None:
            return None
        return cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    @staticmethod
    def to_cmyk(image):
        """Simula conversão para CMYK (não é nativa no OpenCV)."""
        if image is None:
            return None
        bgr = image.astype(float) / 255.0
        k = 1 - bgr.max(axis=2)
        c = (1 - bgr[..., 2] - k) / (1 - k + 1e-8)
        m = (1 - bgr[..., 1] - k) / (1 - k + 1e-8)
        y = (1 - bgr[..., 0] - k) / (1 - k + 1e-8)
        cmyk = (cv2.merge(((c * 255).astype('uint8'),
                           (m * 255).astype('uint8'),
                           (y * 255).astype('uint8'),
                           (k * 255).astype('uint8'))))
        return cmyk
