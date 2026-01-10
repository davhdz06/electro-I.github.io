---
layout: single
title: "No existen los monopolos magnéticos"
categories: [electromagnetismo, campo-magnético]
toc: true
use_math: true
---

Una de las diferencias fundamentales entre el **campo eléctrico** y el **campo magnético** es la **ausencia experimental de monopolos magnéticos**.

Mientras que las cargas eléctricas positivas y negativas existen de manera aislada, **no se ha observado ningún objeto que actúe como fuente o sumidero aislado de campo magnético**.

---

## 1. Enunciado físico

El hecho experimental se resume en la ecuación de Maxwell:

\\[
\nabla \cdot \mathbf{B} = 0.
\\]

Esta ecuación indica que el campo magnético **no tiene fuentes ni sumideros** y es válida incluso cuando tenemos campos magnéticos que cambianc on el tiempo. Recordemos que para el campo eléctrico se cumple: 

\\[
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}.
\\]

---

## 2. Líneas de campo magnético

Las líneas de campo magnético presentan dos propiedades esenciales:

- Siempre forman **curvas cerradas**,
- Nunca comienzan ni terminan en un punto del espacio.

Esto contrasta con las líneas del campo eléctrico, que **sí** comienzan y terminan en cargas.

---

## 3. Modelo físico: un bucle de corriente pequeño

Para ilustrar este fenómeno, vamos a considerar un **bucle circular de corriente muy pequeño**, que puede aproximarse como un **dipolo magnético** (porque no existen los monopolos magnéticos).


La siguiente figura muestra:

- A la izquierda: **líneas de campo tridimensionales** del bucle,
- A la derecha: una **sección del plano \\(XZ\\)**,
- La magnitud del campo representada en **escala logarítmica**.

<figure>
  <img src="{{ '/assets/sims/no-monopolos/no-monopolos.png' | relative_url }}"
       alt="Campo magnético de un bucle: líneas cerradas y divergencia nula"
       style="max-width:100%; border-radius:12px;">
  <figcaption>
    Las líneas de campo magnético se cierran sobre sí mismas, reflejando que
    \( \nabla\cdot\mathbf B = 0 \). No existen fuentes puntuales del campo.
  </figcaption>
</figure>

---

## Código de la simulación

📥 Descargar el código completo:  
[no_monopolos.py]({{ '/downloads/no_monopolos.py' | relative_url }})

