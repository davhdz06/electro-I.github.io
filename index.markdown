---
layout: single
#title: "Electromagnetismo I"
nav_order: 0
header:
  show_title: false
---

<div style="text-align:center; margin: 2.2rem 0 2rem 0; padding: 0.5rem 0 1.2rem 0;">

  <img
    src="{{ '/assets/img/Logo_FC_Color.png' | relative_url }}"
    alt="Escudo Facultad de Ciencias UNAM"
    style="height:120px; width:auto; max-width:none; display:block; margin:0 auto 1.2rem auto;"
  />
  
  <div style="font-size:2.0rem; font-weight:400; margin:0 0 0.8rem 0;">
  Electromagnetismo I
  </div>

  <p style="margin:0 auto 0.9rem auto; max-width:720px; line-height:1.65;">
    Material oficial del curso: notas, problemas resueltos y simulaciones.
  </p>

  <hr style="margin: 1.6rem 0 1.2rem 0;">

  <h2>Autores</h2>

  <ul style="list-style:none; padding-left:0; margin:0.8rem 0;">
   <li><strong>Mirna Villavicencio Torres y Mauricio García Vergara</strong> — Facultad de Ciencias, UNAM</li>
  </ul>


  <p style="margin:0.2rem 0 0 0;">
    Contacto:
    <a href="mailto:maugv@ciencias.unam.mx">maugv@ciencias.unam.mx</a>
  </p>
  
  

</div>

<hr style="margin: 1.4rem 0 1.2rem 0;">

## Entradas

<ul style="margin-top:1rem; padding-left:1.2rem;">
{% for post in site.posts %}
  <li style="margin:0.55rem 0;">
    <span style="color:#586e75; white-space:nowrap;">{{ post.date | date: "%Y-%m-%d" }}</span>
    <span style="margin:0 0.35rem; color:#999;">—</span>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
{% endfor %}
</ul>

