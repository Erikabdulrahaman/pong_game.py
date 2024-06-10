import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
LEBAR_LAYAR = 800
TINGGI_LAYAR = 600

# Warna
PUTIH = (255, 255, 255)
HITAM = (0, 0, 0)
BIRU = (0, 0, 255)  # Warna pemukul 1 (biru)
ORENS = (255, 165, 0)  # Warna pemukul 2 (oranye)

# Pengaturan bola
LEBAR_BOLA = 20
TINGGI_BOLA = 20
KECEPATAN_BOLA_X = 4
KECEPATAN_BOLA_Y = 4

# Pengaturan pemukul
LEBAR_PEMUKUL = 15
TINGGI_PEMUKUL = 100
KECEPATAN_PEMUKUL = 6

# Buat layar
layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption("Permainan Pong")

# Kelas Bola
class Bola:
    def __init__(self):
        self.rect = pygame.Rect(LEBAR_LAYAR // 2 - LEBAR_BOLA // 2, TINGGI_LAYAR // 2 - TINGGI_BOLA // 2, LEBAR_BOLA, TINGGI_BOLA)
        self.kecepatan_x = KECEPATAN_BOLA_X * random.choice((1, -1))
        self.kecepatan_y = KECEPATAN_BOLA_Y * random.choice((1, -1))

    def reset(self):
        self.rect.center = (LEBAR_LAYAR // 2, TINGGI_LAYAR // 2)
        self.kecepatan_x = KECEPATAN_BOLA_X * random.choice((1, -1))
        self.kecepatan_y = KECEPATAN_BOLA_Y * random.choice((1, -1))

    def move(self):
        self.rect.x += self.kecepatan_x
        self.rect.y += self.kecepatan_y

        # Memantul dari dinding atas dan bawah
        if self.rect.top <= 0 or self.rect.bottom >= TINGGI_LAYAR:
            self.kecepatan_y *= -1

    def draw(self, layar):
        pygame.draw.ellipse(layar, PUTIH, self.rect)

# Kelas Pemukul
class Pemukul:
    def __init__(self, x, warna):
        self.rect = pygame.Rect(x, TINGGI_LAYAR // 2 - TINGGI_PEMUKUL // 2, LEBAR_PEMUKUL, TINGGI_PEMUKUL)
        self.kecepatan = 0
        self.warna = warna

    def move(self):
        self.rect.y += self.kecepatan

        # Tetapkan pemukul pada layar
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > TINGGI_LAYAR:
            self.rect.bottom = TINGGI_LAYAR

    def draw(self, layar):
        pygame.draw.rect(layar, self.warna, self.rect)

# Inisialisasi skor
skor_kiri = 0
skor_kanan = 0
font = pygame.font.Font(None, 74)

# Buat bola dan pemukul
bola = Bola()
pemukul_kiri = Pemukul(50, BIRU)
pemukul_kanan = Pemukul(LEBAR_LAYAR - 50 - LEBAR_PEMUKUL, ORENS)

# Loop utama permainan
berjalan = True
jam = pygame.time.Clock()

while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pemukul_kiri.kecepatan = -KECEPATAN_PEMUKUL
            if event.key == pygame.K_s:
                pemukul_kiri.kecepatan = KECEPATAN_PEMUKUL
            if event.key == pygame.K_UP:
                pemukul_kanan.kecepatan = -KECEPATAN_PEMUKUL
            if event.key == pygame.K_DOWN:
                pemukul_kanan.kecepatan = KECEPATAN_PEMUKUL
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                pemukul_kiri.kecepatan = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                pemukul_kanan.kecepatan = 0

    # Gerakkan pemukul
    pemukul_kiri.move()
    pemukul_kanan.move()

    # Gerakkan bola
    bola.move()

    # Tabrakan bola dengan pemukul
    if bola.rect.colliderect(pemukul_kiri.rect) or bola.rect.colliderect(pemukul_kanan.rect):
        bola.kecepatan_x *= -1

    # Periksa jika bola keluar batas dan perbarui skor
    if bola.rect.left <= 0:
        skor_kanan += 1
        bola.reset()
    if bola.rect.right >= LEBAR_LAYAR:
        skor_kiri += 1
        bola.reset()

    # Bersihkan layar
    layar.fill(HITAM)

    # Gambar bola dan pemukul
    bola.draw(layar)
    pemukul_kiri.draw(layar)
    pemukul_kanan.draw(layar)

    # Gambar skor
    skor_kiri_teks = font.render(str(skor_kiri), True, PUTIH)
    layar.blit(skor_kiri_teks, (LEBAR_LAYAR // 4, 20))
    skor_kanan_teks = font.render(str(skor_kanan), True, PUTIH)
    layar.blit(skor_kanan_teks, (LEBAR_LAYAR * 3 // 4, 20))

    # Perbarui layar
    pygame.display.flip()

    # Batasi frame rate
    jam.tick(60)

pygame.quit()
