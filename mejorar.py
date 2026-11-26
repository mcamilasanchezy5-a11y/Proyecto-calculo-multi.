"""Uso:  python mejorar.py piscina.html
Crea piscina_mejorado.html con gráficas interactivas y diseño nuevo.
No cambia ningún texto, dato ni cálculo del proyecto."""
import sys, os

src = sys.argv[1] if len(sys.argv) > 1 else "index.html"
h = open(src, encoding="utf-8").read()

def rep(a, b):
    global h
    assert a in h, "No encontré este fragmento en tu HTML:\n" + a
    h = h.replace(a, b, 1)

CSS = r'''
/* ===== MEJORAS VISUALES ===== */
body{background:radial-gradient(1100px 600px at 8% -10%,#cffafe 0,transparent 60%),radial-gradient(900px 500px at 100% 8%,#e0e7ff 0,transparent 55%),var(--fondo);background-attachment:fixed}
h1,h2,h3,.num{font-family:"Sora","Segoe UI",system-ui,sans-serif}
#prog{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,#22d3ee,#f59e0b);z-index:50}
.hero{background:radial-gradient(circle at 15% 20%,#155e75,transparent 55%),linear-gradient(135deg,#082f49,#0c4a6e 45%,#0e7490)}
.hero .wrap{position:relative;z-index:2}
.hero h1{text-shadow:0 4px 30px rgba(0,0,0,.25)}
.persona{backdrop-filter:blur(6px);transition:.3s}
.persona:hover{transform:translateY(-3px);background:rgba(255,255,255,.24)}
nav a.on{background:var(--p);color:#fff}
.card{background:rgba(255,255,255,.88);backdrop-filter:blur(6px);transition:transform .3s,box-shadow .3s}
.num{background:linear-gradient(135deg,#0e7490,#22b8cf);box-shadow:0 6px 16px rgba(14,116,144,.35)}
.stat{transition:.3s;box-shadow:0 8px 20px rgba(12,74,110,.25)}
.stat:hover{transform:scale(1.05) rotate(-1deg)}
.rev{opacity:0;transform:translateY(26px);transition:opacity .7s,transform .7s}
.rev.v{opacity:1;transform:none}
.card:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(12,74,110,.18)}
canvas.graf,#cv{touch-action:pan-y;cursor:crosshair}
#cv{cursor:grab}
canvas.graf{box-shadow:inset 0 0 0 1px var(--borde)}
#tip{position:fixed;pointer-events:none;background:#0f172a;color:#fff;padding:8px 12px;border-radius:10px;font-size:13px;line-height:1.5;z-index:60;opacity:0;transition:opacity .15s;box-shadow:0 8px 24px rgba(0,0,0,.3);border-left:3px solid #f59e0b}
.hint{margin-top:8px;font-size:13px;color:var(--p);font-weight:600}
'''

JS = r'''
/* ===== MEJORAS INTERACTIVAS ===== */
const G = {rot: -35, el: .5, rc: -30, ec: .5};
const O = {g1: graf1, g2: graf2, g3: graf3, g4: graf4};
graf1 = function (...a) { G.a1 = a; O.g1(...a); };
graf2 = function (...a) { G.a2 = a; O.g2(...a); };
graf3 = function (...a) { G.a3 = a; O.g3(...a); };
graf4 = function (...a) { G.a4 = a; O.g4(...a); };
const _gr = graficas;
graficas = function (...a) { G.a1 = G.a2 = G.a3 = G.a4 = null; _gr(...a); };

const tip = document.createElement('div'); tip.id = 'tip'; document.body.appendChild(tip);

/* Gira la piscina siguiendo el mouse (suave, con inercia) */
function orbit(cv, kr, ke, r0, r1, e0, e1, draw) {
  let tr = G[kr], te = G[ke], run = false;
  const step = () => {
    G[kr] += (tr - G[kr]) * .15; G[ke] += (te - G[ke]) * .15; draw();
    if (Math.abs(tr - G[kr]) > .05 || Math.abs(te - G[ke]) > .002) requestAnimationFrame(step); else run = false;
  };
  cv.addEventListener('pointermove', e => {
    const r = cv.getBoundingClientRect();
    tr = r0 + (r1 - r0) * (e.clientX - r.left) / r.width;
    te = e0 + (e1 - e0) * (e.clientY - r.top) / r.height;
    if (!run) { run = true; requestAnimationFrame(step); }
  });
}
orbit($('cv'), 'rc', 'ec', -90, 90, .25, .9, () => { $('giro').value = G.rc; dibujar(); });
orbit($('g1'), 'rot', 'el', -125, 55, .2, .9, () => { if (G.a1) O.g1(...G.a1); });

/* Resalta y explica lo que está bajo el mouse */
function hover(id, fn) {
  const cv = $(id), k = 'a' + id[1];
  const redraw = () => { if (G[k]) O[id](...G[k]); };
  cv.addEventListener('pointermove', e => {
    if (!G[k]) return;
    const r = cv.getBoundingClientRect();
    const mx = (e.clientX - r.left) / r.width * 560, my = (e.clientY - r.top) / r.height * 380;
    redraw();
    const t = fn(cv.getContext('2d'), mx, my, G[k]);
    if (t) { tip.innerHTML = t; tip.style.opacity = 1; tip.style.left = (e.clientX + 14) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; }
    else tip.style.opacity = 0;
  });
  cv.addEventListener('pointerleave', () => { redraw(); tip.style.opacity = 0; });
}

hover('g2', (g, mx, my, [f, L, W]) => {
  const x = (mx - 64) / 456 * L; if (x < 0 || x > L) return null;
  const dT = Math.max(f(0, 0), f(L, 0), f(0, W), f(L, W)), st = paso(dT * 1.2), eje = Math.ceil(dT * 1.2 / st) * st;
  const X = 64 + x / L * 456, d = f(x, W / 2), Yd = 44 + d / eje * 266;
  const {a, b, c} = leer(), V = W * (a * x + b * x * x / 2) + c * W * W * x / 2;
  g.save(); g.strokeStyle = '#f59e0b'; g.lineWidth = 1.6; g.setLineDash([4, 3]);
  g.beginPath(); g.moveTo(X, 44); g.lineTo(X, 310); g.stroke(); g.setLineDash([]);
  g.fillStyle = '#f59e0b'; g.strokeStyle = '#fff'; g.lineWidth = 2;
  g.beginPath(); g.arc(X, Yd, 6, 0, 7); g.fill(); g.stroke(); g.restore();
  return `x = <b>${fmt(x)} m</b><br>Profundidad: <b>${fmt(d)} m</b><br>Agua hasta aquí: <b>${fmt(V)} m³</b>`;
});

hover('g3', (g, mx, my, [f, L, W]) => {
  const s = Math.min(410 / L, 262 / W), pw = L * s, ph = W * s, x0 = 50 + (410 - pw) / 2, y0 = 34 + (262 - ph) / 2, n = 5;
  const i = Math.floor((mx - x0) / (pw / n)), k = Math.floor((my - y0) / (ph / n)), j = n - 1 - k;
  if (i < 0 || i >= n || k < 0 || k >= n) return null;
  const cw = pw / n, ch = ph / n;
  g.save(); g.fillStyle = 'rgba(245,158,11,.22)';
  g.fillRect(x0, y0 + k * ch, pw, ch); g.fillRect(x0 + i * cw, y0, cw, ph);
  g.strokeStyle = '#f59e0b'; g.lineWidth = 3; g.strokeRect(x0 + i * cw, y0 + k * ch, cw, ch); g.restore();
  const d = f((i + .5) * L / n, (j + .5) * W / n), v = d * L / n * W / n;
  return `Cuadro fila ${j + 1}, col ${i + 1}<br>Profundidad: <b>${fmt(d)} m</b><br>Volumen: <b>${fmt(v)} m³</b>`;
});

hover('g4', (g, mx, my, [f, L, W, V]) => {
  const ns = [2, 5, 10, 20, 50, 100, 200, 400], slot = 470 / 8, i = Math.floor((mx - 64) / slot);
  if (i < 0 || i >= 8 || my < 40 || my > 310) return null;
  const m = ns[i]; let s = 0;
  for (let j = 0; j < m; j++) for (let q = 0; q < m; q++) s += f(q * L / m, j * W / m);
  s *= (L / m) * (W / m);
  const e = Math.abs(s - V); if (e < 1e-9) return null;
  g.save(); g.fillStyle = 'rgba(245,158,11,.18)'; g.fillRect(64 + i * slot, 46, slot, 262); g.restore();
  return `${m} × ${m} cuadritos<br>Aproximación: <b>${fmt(s, 4)} m³</b><br>Error: <b>${fmt(e / V * 100, 3)} %</b>`;
});

/* Pistas bajo cada gráfica */
const pistas = {cv: 'Mueve el mouse sobre la piscina para girarla.', g1: 'Mueve el mouse: la gráfica gira y se inclina contigo.',
  g2: 'Pasa el mouse: verás la profundidad y el agua acumulada en cada punto.',
  g3: 'Pasa el mouse: se resalta el cuadro, su fila y su columna (Fubini).',
  g4: 'Pasa el mouse sobre cada barra para ver su error.'};
for (const id in pistas) $(id).insertAdjacentHTML('afterend', `<p class="hint">🖱️ ${pistas[id]}</p>`);

/* Aparición al hacer scroll, barra de progreso y menú activo */
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('v'); io.unobserve(e.target); } }), {threshold: .08});
document.querySelectorAll('.card,section .titulo').forEach(e => { e.classList.add('rev'); io.observe(e); });
const secs = [...document.querySelectorAll('main section')], links = [...document.querySelectorAll('nav a')];
addEventListener('scroll', () => {
  const d = document.documentElement;
  $('prog').style.width = (d.scrollTop / (d.scrollHeight - d.clientHeight) * 100) + '%';
  let cur = ''; secs.forEach(s => { if (s.getBoundingClientRect().top < 140) cur = s.id; });
  links.forEach(a => a.classList.toggle('on', a.getAttribute('href') === '#' + cur));
}, {passive: true});
'''

# --- 1. Cambios mínimos en el código existente (para que se pueda girar)
rep("t = -35 * Math.PI / 180", "t = G.rot * Math.PI / 180")
rep("yr * 0.5 - z * 1.3", "yr * G.el - z * 1.3")
rep("const t = $('giro').value * Math.PI / 180;", "const t = G.rc * Math.PI / 180;")
rep("(yr * .5 - z)", "(yr * G.ec - z)")
rep("$('giro').addEventListener('input', dibujar);",
    "$('giro').addEventListener('input', () => { G.rc = +$('giro').value; dibujar(); });")

# --- 2. Estructura nueva
rep("<body>", '<body>\n<div id="prog"></div>')
rep("</style>", CSS + "</style>")
rep("<style>", '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700&display=swap" rel="stylesheet">\n<style>')
rep("['L', 'W', 'a', 'b', 'c', 'precio'].forEach(", JS + "\n['L', 'W', 'a', 'b', 'c', 'precio'].forEach(")

base = os.path.dirname(os.path.abspath(src))
nombre = "piscina_final.html"
destinos = [base, os.path.join(os.path.expanduser("~"), "Desktop"), os.path.expanduser("~")]
for carpeta in destinos:
    try:
        out = os.path.join(carpeta, nombre)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(h)
        print("Listo -> guardado en:", out)
        break
    except OSError as e:
        print("No pude guardar en", carpeta, "->", e)
else:
    print("No se pudo guardar en ninguna carpeta.")