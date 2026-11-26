import os
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Profundidad de la piscina: 1 m en x = 0 y 2 m en x = 10
x, y = sp.symbols('x y')
f = 1 + sp.Rational(1, 10) * x

# Orden dy dx: primero se integra en y y luego en x
v1 = sp.integrate(sp.integrate(f, (y, 0, 5)), (x, 0, 10))

# Orden dx dy: primero se integra en x y luego en y
v2 = sp.integrate(sp.integrate(f, (x, 0, 10)), (y, 0, 5))

print("Orden dy dx:", v1, "m3")
print("Orden dx dy:", v2, "m3")
print("Largo x ancho x profundidad promedio:", 10 * 5 * 1.5, "m3")

# Grafica del fondo de la piscina en 3D
X, Y = np.meshgrid(np.linspace(0, 10, 40), np.linspace(0, 5, 20))
Z = -(1 + 0.1 * X)

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="Blues_r")
ax.plot_surface(X, Y, 0 * X, color="#38bdf8", alpha=0.15)
ax.set_xlabel("x: largo (m)")
ax.set_ylabel("y: ancho (m)")
ax.set_zlabel("profundidad (m)")
ax.view_init(elev=22, azim=-60)

# Guardar la imagen junto a este archivo (si no se puede, el programa sigue)
try:
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, "figura1.png")
    plt.savefig(ruta, dpi=200, bbox_inches="tight")
    print("Imagen guardada en:", ruta)
except OSError as error:
    print("No se pudo guardar la imagen:", error)
    print("Use el boton del disquete de la ventana para guardarla.")

plt.show()