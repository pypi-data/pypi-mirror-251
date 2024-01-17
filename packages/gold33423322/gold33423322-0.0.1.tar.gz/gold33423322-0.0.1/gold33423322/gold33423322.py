import math

class GoldenRatio:
    def __init__(self):
        pass

    def hitung_golden_ratio(self):
        golden_ratio = (1 + math.sqrt(5)) / 2
        return golden_ratio

    def tampilkan_hasil(self):
        hasil_golden_ratio = self.hitung_golden_ratio()

        print(f"Nilai Golden Ratio: {hasil_golden_ratio}")

if __name__ == "__main__":
    calculator = GoldenRatio()

    calculator.tampilkan_hasil()

