from pathlib import Path
import html

ROOT = Path(".")
INDEX = ROOT / "index.html"
SOURCE = ROOT / "content/entradas/2026-08-03-el-barco-sobre-los-duraznos.txt"
POST = ROOT / "posts/el-barco-sobre-los-duraznos.html"

title = "el barco sobre los duraznos"
date = "03/08/26"
asset = "assets/el-barco-sobre-los-duraznos.webp"

text = SOURCE.read_text(encoding="utf-8").strip()
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

def p_html(p: str) -> str:
    return f"<p>{html.escape(p)}</p>"

intro = "\n".join(p_html(p) for p in paragraphs[:3])
body = "\n".join(p_html(p) for p in paragraphs[3:])

page = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="El barco sobre los duraznos — cuento en MUSGO.">
<title>el barco sobre los duraznos · MUSGO</title>
<style>
:root{{--fondo:#050505;--texto:#e9e9e4;--rosa:#ff66cc;--verde:#6b9c33;--borde:#303030;}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{
  background:
    radial-gradient(circle at 12% 8%,rgba(255,102,204,.04),transparent 26rem),
    radial-gradient(circle at 88% 90%,rgba(107,156,51,.05),transparent 30rem),
    #000;
  color:var(--texto);
  font-family:"Courier New",monospace;
  padding:18px;
  line-height:1.65;
}}
main{{max-width:980px;margin:auto;border:1px solid var(--borde);background:var(--fondo);padding:18px}}
nav{{margin-bottom:14px;font-size:.72rem;letter-spacing:.09em}}
nav a{{color:var(--rosa);text-decoration:none}}
.meta{{color:#777;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase}}
h1{{font-weight:400;font-size:clamp(1.25rem,4vw,2.25rem);letter-spacing:.08em;margin:6px 0 15px}}
.apertura{{
  display:grid;
  grid-template-columns:minmax(250px,.85fr) minmax(0,1.15fr);
  gap:16px;
  align-items:start;
  margin-bottom:22px;
}}
.apertura img{{width:100%;height:100%;max-height:430px;object-fit:cover;border:1px solid var(--verde);display:block}}
.apertura-texto{{font-family:Georgia,"Times New Roman",serif;font-size:1.02rem;line-height:1.72}}
.apertura-texto p+p{{margin-top:1em}}
.cuerpo{{width:min(100%,720px);margin:auto;font-family:Georgia,"Times New Roman",serif;font-size:1.03rem;line-height:1.78}}
.cuerpo p{{margin-bottom:1.18em}}
.cuerpo p:first-child::first-letter{{color:var(--rosa);font-size:2.6em;float:left;line-height:.82;padding-right:.08em}}
footer{{max-width:980px;margin:12px auto 0;color:#555;font-size:.65rem;letter-spacing:.08em}}
@media(max-width:680px){{
  body{{padding:8px}}
  main{{padding:10px}}
  .apertura{{grid-template-columns:44% minmax(0,1fr);gap:9px}}
  .apertura img{{min-height:240px}}
  .apertura-texto{{font-size:.78rem;line-height:1.5}}
  .cuerpo{{font-size:.94rem;line-height:1.72}}
}}
</style>
</head>
<body>
<main>
<nav><a href="../index.html#entradas">← volver a MUSGO</a></nav>
<div class="meta">{date} · cuento</div>
<h1>{title}</h1>
<section class="apertura">
<img src="../{asset}" alt="Barco aéreo suspendido sobre huertos de duraznos">
<div class="apertura-texto">{intro}</div>
</section>
<article class="cuerpo">{body}</article>
</main>
<footer>MUSGO / archivo vivo</footer>
</body>
</html>
'''
POST.parent.mkdir(parents=True, exist_ok=True)
POST.write_text(page, encoding="utf-8")

index = INDEX.read_text(encoding="utf-8")

css = r'''
/* entrada modular · el barco sobre los duraznos */
.entrada-flujo {
  width: min(100%, 920px);
  margin: 0 auto 14px;
  border: 1px solid #3b3b37;
  background: linear-gradient(135deg, rgba(107,156,51,.08), transparent 45%), #040404;
}
.entrada-flujo > a {
  display: grid;
  grid-template-columns: minmax(250px,.82fr) minmax(0,1.18fr);
  min-height: 220px;
  color: inherit;
  text-decoration: none;
}
.entrada-flujo-imagen {
  width: 100%;
  height: 100%;
  min-height: 220px;
  object-fit: cover;
  display: block;
  border-right: 1px solid #343430;
  filter: saturate(.84) contrast(1.04);
}
.entrada-flujo-copy {
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-width: 0;
}
.entrada-flujo-meta {
  color: var(--verde);
  font-size: .64rem;
  letter-spacing: .11em;
  text-transform: uppercase;
}
.entrada-flujo h3 {
  color: #f1f1ed;
  font-size: clamp(1rem,2.4vw,1.35rem);
  font-weight: normal;
  letter-spacing: .06em;
  margin: 5px 0 10px;
}
.entrada-flujo p {
  color: #b8b8b2;
  font-family: Georgia, "Times New Roman", serif;
  font-size: .88rem;
  line-height: 1.55;
}
.entrada-flujo-abrir {
  color: var(--rosa);
  margin-top: 12px;
  font-size: .66rem;
  letter-spacing: .08em;
}
.entrada-flujo:hover {
  border-color: var(--verde);
}
.entrada-flujo:hover .entrada-flujo-imagen {
  filter: saturate(1) contrast(1.02);
}
@media (max-width: 600px) {
  .entrada-flujo > a {
    grid-template-columns: 43% minmax(0,1fr);
    min-height: 168px;
  }
  .entrada-flujo-imagen {
    min-height: 168px;
  }
  .entrada-flujo-copy {
    padding: 9px;
  }
  .entrada-flujo-meta {
    font-size: .54rem;
  }
  .entrada-flujo h3 {
    font-size: .82rem;
    margin: 4px 0 7px;
  }
  .entrada-flujo p {
    font-size: .67rem;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .entrada-flujo-abrir {
    margin-top: 7px;
    font-size: .56rem;
  }
}
'''

if "/* entrada modular · el barco sobre los duraznos */" not in index:
    index = index.replace("</style>", css + "\n</style>", 1)

card = f'''<article class="entrada-flujo" id="el-barco-sobre-los-duraznos">
<a href="posts/el-barco-sobre-los-duraznos.html">
<img class="entrada-flujo-imagen" src="{asset}" alt="Barco aéreo suspendido sobre huertos de duraznos" loading="lazy">
<div class="entrada-flujo-copy">
<div class="entrada-flujo-meta">{date} · cuento</div>
<h3>{title}</h3>
<p>El barco llevaba cuatro días suspendido sobre los duraznos. Al cuarto día buscaron a Bruna.</p>
<span class="entrada-flujo-abrir">leer completo ↗</span>
</div>
</a>
</article>'''

marker = '<section class="entradas-wrap" id="post-hoy-v05"><h2 class="entradas-title">ENTRADAS</h2>'
if 'id="el-barco-sobre-los-duraznos"' not in index:
    if marker not in index:
        raise RuntimeError("No se encontró el inicio de ENTRADAS")
    index = index.replace(marker, marker + card, 1)

archive_marker = '<ul class="archive-list">'
archive_item = f'''<li class="archive-item">
<span class="archive-date">{date}</span>
<a href="posts/el-barco-sobre-los-duraznos.html">➔ {title}</a>
</li>'''
if 'href="posts/el-barco-sobre-los-duraznos.html">➔' not in index:
    index = index.replace(archive_marker, archive_marker + "\n" + archive_item, 1)

index = index.replace(
    '<strong>última mutación:</strong> 03/08/26  ·  memes se ganó su propio espacio',
    '<strong>última mutación:</strong> 03/08/26  ·  entró un barco sobre los duraznos',
    1,
)

INDEX.write_text(index, encoding="utf-8")
print("Entrada creada:", POST, "párrafos:", len(paragraphs))
