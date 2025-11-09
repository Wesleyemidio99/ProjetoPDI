import cv2
import numpy as np

class EdgeDetector:
    @staticmethod
    def sobel(img):
        if img is None:
            raise ValueError("Nenhuma imagem carregada para aplicar Sobel.")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude(grad_x, grad_y)
        sobel = np.uint8(np.clip(sobel, 0, 255))
        return sobel


    @staticmethod
    def laplacian(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap = np.uint8(np.clip(np.absolute(lap), 0, 255))
        return lap

    @staticmethod
    def canny(img, low=100, high=200):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low, high)
        return edges
