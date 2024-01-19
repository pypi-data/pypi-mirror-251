# File: Library/circle_calculator.py

class LingkaranCalculator:
    def __init__(self, radius):
        self.radius = radius

    def hitung_luas(self):
        luas = 3.141592653589793 * (self.radius ** 2)
        return luas
