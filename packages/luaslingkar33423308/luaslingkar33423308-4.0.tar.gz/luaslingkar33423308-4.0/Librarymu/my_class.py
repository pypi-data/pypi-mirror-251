class Segitiga:
    def __init__(self, sisi_a, sisi_b, sisi_c):
        self.sisi_a = sisi_a
        self.sisi_b = sisi_b
        self.sisi_c = sisi_c

    def hitung_keliling(self):
        keliling = self.sisi_a + self.sisi_b + self.sisi_c
        return keliling

    def hitung_luas(self):
        s = (self.sisi_a + self.sisi_b + self.sisi_c) / 2
        luas = (s * (s - self.sisi_a) * (s - self.sisi_b) * (s - self.sisi_c)) ** 0.5
        return luas
