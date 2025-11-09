import cv2

class ThresholdModel:
    """Responsável por aplicar limiarizações na imagem."""

    @staticmethod
    def global_threshold(image, thresh_value=127):
        """Aplica limiarização global simples."""
        if image is None:
            return None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def otsu_threshold(image):
        """Aplica limiarização automática de Otsu."""
        if image is None:
            return None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_val, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"Limiar calculado por Otsu: {thresh_val:.2f}")
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def adaptive_threshold(image):
        """Aplica limiarização adaptativa (local)."""
        if image is None:
            return None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)