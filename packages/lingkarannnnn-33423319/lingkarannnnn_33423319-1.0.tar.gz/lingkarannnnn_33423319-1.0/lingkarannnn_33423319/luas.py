import math

class LuasLingkaran:
    def __init__(self, jari_jari):
        self.jari_jari = jari_jari

    def hitung_luas(self):
        luas = math.pi * (self.jari_jari ** 2)
        return luas
