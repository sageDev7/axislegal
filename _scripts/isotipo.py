"""Isotipo compacto de Axis Legal: la A del logo con la pluma más chica.
No toca logo.png; genera isotipo.png (A verde) e isotipo-claro.png (A marfil) en la carpeta del proyecto."""
import sys
import numpy as np
from PIL import Image
D = r"C:\Users\axeli\Desktop\laburo\Desarrollo Web\bocetos-estudios\Axis Legal"
S = float(sys.argv[1]) if len(sys.argv) > 1 else 0.6

im = np.array(Image.open(D + r"\logo.png").convert("RGBA")).astype(float)
R, G, B, A = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
H, W = A.shape
yy, xx = np.mgrid[0:H, 0:W]
pure = (G > R + 18) & (G > B + 10)                  # verde del logo (excluye la sombra oliva de la pluma)
amask = (A > 30) & pure & (xx < 275) & (yy < 262)

# --- reconstruir la pierna derecha de la A (tapada por la pluma)
# bordes visibles: por fila, el tramo verde más a la derecha antes de x=275
def right_run(y):
    xs = np.where(amask[y, :275])[0]
    if len(xs) == 0:
        return None
    # último tramo continuo
    runs = np.split(xs, np.where(np.diff(xs) > 1)[0] + 1)
    r = runs[-1]
    return r[0], r[-1]
rows = [y for y in range(40, 118)]
L, Rr = [], []
for y in rows:
    rr = right_run(y)
    if rr and rr[1] - rr[0] > 6:
        L.append((y, rr[0])); Rr.append((y, rr[1]))
L, Rr = np.array(L), np.array(Rr)
kl = np.polyfit(L[:, 0], L[:, 1], 1); kr = np.polyfit(Rr[:, 0], Rr[:, 1], 1)
print("borde izq pierna", kl, "borde der", kr)
fill = np.zeros_like(amask)
for y in range(45, 238):
    x0, x1 = np.polyval(kl, y), np.polyval(kr, y)
    fill[y, int(np.floor(x0)):int(np.ceil(x1)) + 1] = True

alpha_A = np.where(amask, A, 0)
alpha_A = np.maximum(alpha_A, np.where(fill, 255, 0))
# cerrar las motas que dejó el borde de la pluma vieja (dilatar y erosionar el alfa)
from PIL import ImageFilter
al = Image.fromarray(alpha_A.clip(0, 255).astype(np.uint8))
al = al.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.MinFilter(9))
alpha_A = np.maximum(alpha_A, np.array(al).astype(float))
# quedarse solo con la A (la pieza conectada que nace en el vértice); descarta motas sueltas
from PIL import ImageDraw
bw = Image.fromarray(np.where(alpha_A > 60, 255, 0).astype(np.uint8)).copy()  # copia: fromarray es de solo lectura y floodfill no se aplicaría
top = np.argwhere(np.array(bw)[:, :275] > 0)[0]          # vértice superior de la A
seed = (int(top[1]), int(top[0]))
ImageDraw.floodfill(bw, seed, 128)
keep = Image.fromarray(np.where(np.array(bw) == 128, 255, 0).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
alpha_A = np.where(np.array(keep) > 0, alpha_A, 0)

# --- pluma: todo lo no verde a la derecha de la A
fmask = (A > 10) & ~pure & (R >= G - 5) & ((R > 150) | (R > B + 40)) & (xx >= 150) & (yy < 274) & ~((xx >= 262) & (yy >= 228))
feather = np.zeros((H, W, 4), np.uint8)
feather[fmask] = im[fmask].astype(np.uint8)
fe = Image.fromarray(feather)
ys, xs = np.where(fmask)
tip = (xs.min(), ys.max())                           # punta inferior izquierda
fb = fe.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
fw, fh = fb.size
fs = fb.resize((max(1, round(fw * S)), max(1, round(fh * S))), Image.LANCZOS)

def build(color, name):
    a_img = np.zeros((H, W, 4), np.uint8)
    a_img[..., 0], a_img[..., 1], a_img[..., 2] = color
    a_img[..., 3] = alpha_A.clip(0, 255).astype(np.uint8)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(Image.fromarray(a_img))
    # la pluma entra por la misma punta, más corta
    canvas.alpha_composite(fs, (tip[0], tip[1] - fs.size[1] + 1))
    bb = canvas.getbbox()
    canvas = canvas.crop(bb)
    canvas.save(D + "\\" + name)
    print(name, canvas.size)

build((0x2D, 0x4C, 0x2D), "isotipo.png")
build((0xF2, 0xED, 0xE0), "isotipo-claro.png")
