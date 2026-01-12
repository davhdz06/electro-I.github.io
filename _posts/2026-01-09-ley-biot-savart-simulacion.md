---
title: "Visualización 3D de la Ley de Biot–Savart"
categories: [electromagnetismo, campo-magnético]
toc: true
use_math: true
---

## Introducción

La **ley de Biot–Savart** permite calcular el campo magnético generado por una corriente eléctrica estacionaria.

En este post presentamos una **simulación tridimensional en Python** que ilustra el campo magnético producido por un **cable rectilíneo infinito**, así como la dirección del campo en distintos puntos del espacio.

---

## La ley de Biot–Savart

En forma diferencial, la ley se escribe como:

$$
d\vec{B} = \frac{\mu_0}{4\pi} \frac{I \, d\vec{\ell} \times \vec{r}}{r^3}
$$

donde:
- $$I$$ es la corriente,
- $$d\vec{\ell}$$ es el elemento diferencial del conductor,
- $$\vec{r}$$ es el vector que une el elemento de corriente con el punto de observación.

---

## Descripción de la visualización

La simulación modela un **cable recto** alineado con el eje $z$, discretizado en pequeños segmentos de corriente. El campo magnético se calcula como la suma de las contribuciones de cada segmento, de acuerdo con la ley de Biot–Savart.

Se representan:

- El **cable conductor** y la dirección de la corriente.
- El **campo magnético** en puntos distribuidos cilíndricamente alrededor del cable.
- La **orientación local del campo** usando flechas en 3D.

<figure>
  <img src="{{ '/assets/sims/biot-savart/biot-savart.png' | relative_url }}"
       style="max-width:100%; border-radius:12px;">
  <figcaption>
    Las líneas de campo magnético se cierran sobre sí mismas, siguiendo la regla de la mano derecha donde el pulgar indica al dirección de la corriente. 
  </figcaption>
</figure>

---

## Código de la simulación

📥 Descargar el código completo:  
[biot_savart.py]({{ '/downloads/biot_savart.py' | relative_url }})

