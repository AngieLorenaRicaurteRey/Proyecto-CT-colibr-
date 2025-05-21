import numpy as np
import matplotlib.pyplot as plt
import tifffile

ruta_original = r"c:\Users\a.ricaurte\Desktop\colibri_0955.tif"
imagen_original = tifffile.imread(ruta_original).astype(np.uint16)
alto, ancho = imagen_original.shape

x0, y0 = 808.5,778.5
factor_expansion = 1.10  
a = 430
b = 390

Y, X = np.ogrid[:alto, :ancho]
mascara_ovalada = ((X - x0) ** 2 / a**2) + ((Y - y0) ** 2 / b**2) <= 1


imagen_mascara = np.copy(imagen_original)
imagen_mascara[~mascara_ovalada] = 0


dentro_ovalo = imagen_mascara[mascara_ovalada]
percentil_bajo, percentil_alto = 2, 98  
limite_bajo, limite_alto = np.percentile(dentro_ovalo, [percentil_bajo, percentil_alto])
imagen_filtrada = np.clip(imagen_mascara, limite_bajo, limite_alto)


imagen_normalizada = (imagen_filtrada - limite_bajo) / (limite_alto - limite_bajo)
imagen_normalizada[~mascara_ovalada] = 0  


mu_air = np.min(imagen_normalizada[~mascara_ovalada]) 
mu_hueso = np.percentile(imagen_normalizada[mascara_ovalada], 98)  

def convertir_a_hounsfield(imagen, mu_air, mu_hueso):
    hu_image = ((imagen - mu_air) / (mu_hueso - mu_air)) * 1000
    hu_image[~mascara_ovalada] = -1000  
    return hu_image.astype(np.int16)

imagen_hu = convertir_a_hounsfield(imagen_normalizada, mu_air, mu_hueso)


hu_min, hu_max = 190, 940  
mascara_tejido = (imagen_hu >= hu_min) & (imagen_hu <= hu_max)
imagen_tejido = np.zeros_like(imagen_hu)
imagen_tejido[mascara_tejido] = imagen_hu[mascara_tejido]

#REVERTIR ESCALA A 16 BITS


imagen_normalizada_revertida = (imagen_tejido - (-1000)) / (1000 - (-1000))
imagen_normalizada_revertida = np.clip(imagen_normalizada_revertida, 0, 1)


imagen_16bits = (imagen_normalizada_revertida * 65535).astype(np.uint16)


ruta_guardado = r"c:\Users\a.ricaurte\Desktop\imagen_procesada.tiff"


resolucion_ppcm = 558 / 2.54  


tifffile.imwrite(ruta_guardado, imagen_16bits, resolution=(resolucion_ppcm, resolucion_ppcm), resolutionunit=3, dtype=np.uint16)


fig, ax = plt.subplots(figsize=(8, 8))
cax = ax.imshow(imagen_tejido, cmap='gray', vmin=-1000, vmax=1500)
fig.colorbar(cax, label="Imagen HU")
ax.set_title("Imagen HU")


def onclick(event):
    if event.inaxes == ax:
        x, y = int(event.xdata), int(event.ydata)
        valor = imagen_tejido[y, x]  

        ax.text(x, y, f"{valor}", color='red', fontsize=10, 
                bbox=dict(facecolor='white', alpha=0.7))
        fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()







