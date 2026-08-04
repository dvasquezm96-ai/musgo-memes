from pathlib import Path
import json
import html

ROOT = Path('.')
INDEX = ROOT / 'index.html'
SOURCE = ROOT / 'content/entradas/2026-08-03-el-barco-sobre-los-duraznos.txt'
POST = ROOT / 'posts/el-barco-sobre-los-duraznos.html'
FEED = ROOT / 'feed/items.json'

items = [
    {
        'id': 'el-barco-sobre-los-duraznos',
        'order': 100,
        'date': '03/08/26',
        'kind': 'cuento',
        'size': 4,
        'title': 'El barco sobre los duraznos',
        'excerpt': 'El barco llevaba cuatro días suspendido sobre los duraznos. Al cuarto día buscaron a Bruna.',
        'image': 'assets/el-barco-sobre-los-duraznos.webp',
        'href': 'posts/el-barco-sobre-los-duraznos.html',
    },
    {
        'id': 'resistiendo-invierno',
        'order': 90,
        'date': '02/08/26',
        'kind': 'huerta',
        'size': 2,
        'title': 'Resistiendo el invierno',
        'excerpt': 'Lo que alguna vez fue la huerta del verano.',
        'image': 'musgo-huerta-camino.webp',
        'href': '#resistiendo-el-invierno',
    },
    {
        'id': 'demasiado-cerca',
        'order': 80,
        'date': '29/07/26',
        'kind': 'detalle',
        'size': 1,
        'title': 'Demasiado cerca',
        'image': 'musgo-microscopio.webp',
        'href': '#demasiado-cerca',
    },
    {
        'id': 'lata-vieja',
        'order': 70,
        'date': 'resto',
        'kind': 'imagen',
        'size': 1,
        'title': 'Hacer luz con una lata vieja',
        'image': 'musgo-lamparas-metal.webp',
        'href': '#sustrato',
    },
]

FEED.parent.mkdir(parents=True, exist_ok=True)
FEED.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')

paragraphs = [p.strip() for p in SOURCE.read_text(encoding='utf-8').split('\n\n') if p.strip()]
body = '\n'.join(f'<p>{html.escape(p)}</p>' for p in paragraphs)
POST.parent.mkdir(parents=True, exist_ok=True)
POST.write_text(f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>El barco sobre los duraznos · MUSGO</title>
<style>
:root{{--rosa:#ff66cc;--verde:#6b9c33;--texto:#e9e9e4}}
*{{box-sizing:border-box}}body{{margin:0;background:#000;color:var(--texto);font-family:"Courier New",monospace;padding:12px;line-height:1.65}}
main{{max-width:820px;margin:auto;background:#050505;border:1px solid #333;padding:clamp(12px,4vw,28px)}}
a{{color:var(--rosa)}}.meta{{font-size:.68rem;color:var(--verde);letter-spacing:.12em;text-transform:uppercase}}
h1{{font-weight:400;letter-spacing:.06em;font-size:clamp(1.35rem,6vw,2.5rem);line-height:1.15;margin:.35em 0 .7em}}
.hero{{width:100%;display:block;border:1px solid var(--verde);margin-bottom:1.4rem}}
.cuento{{max-width:680px;margin:auto;font-family:Georgia,"Times New Roman",serif;font-size:clamp(1rem,2.5vw,1.12rem);line-height:1.78}}
.cuento p{{margin:0 0 1.15em}}nav{{font-size:.72rem;margin-bottom:1rem}}
</style></head><body><main><nav><a href="../index.html#entradas">← volver a MUSGO</a></nav><div class="meta">03/08/26 · cuento</div><h1>El barco sobre los duraznos</h1><img class="hero" src="../assets/el-barco-sobre-los-duraznos.webp" alt="Barco aéreo suspendido sobre huertos de duraznos"><article class="cuento">{body}</article></main></body></html>''', encoding='utf-8')

css = r'''

/* FLUJO TETRIS — contenido separado del código principal */
.flujo-wrap {
  max-width: 760px;
  margin: 20px auto 22px;
  padding: 10px;
  border: 2px solid var(--musgo-verde, #6b9c33);
  background: linear-gradient(145deg, rgba(107,156,51,.08), transparent 38%), #050505;
  box-shadow: 7px 7px 0 var(--musgo-verde-sombra, #243712);
  scroll-margin-top: 10px;
}
.flujo-head { display:flex; justify-content:space-between; align-items:baseline; gap:12px; margin-bottom:9px; }
.flujo-head h2 { color:var(--musgo-verde,#6b9c33); font-size:.78rem; font-weight:normal; letter-spacing:.2em; }
.flujo-head span { color:#686868; font-size:.58rem; letter-spacing:.08em; }
.flujo-grid {
  --flujo-gap: 7px;
  --flujo-cell: 180px;
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  grid-auto-rows:var(--flujo-cell);
  grid-auto-flow:dense;
  gap:var(--flujo-gap);
}
.flujo-item { position:relative; min-width:0; min-height:0; overflow:hidden; border:1px solid #343434; background:#090909; }
.flujo-item[data-size="1"] { grid-column:span 1; grid-row:span 1; }
.flujo-item[data-size="2"] { grid-column:span 2; grid-row:span 1; }
.flujo-item[data-size="2"][data-shape="vertical"] { grid-column:span 1; grid-row:span 2; }
.flujo-item[data-size="4"] { grid-column:span 2; grid-row:span 2; }
.flujo-item[data-size="8"] { grid-column:span 2; grid-row:span 4; }
.flujo-item > a { display:block; width:100%; height:100%; color:inherit; text-decoration:none; }
.flujo-item img { width:100%; height:100%; object-fit:cover; display:block; transition:transform .18s ease,filter .18s ease; filter:saturate(.82) contrast(1.04); }
.flujo-item:hover img { transform:scale(1.018); filter:saturate(1) contrast(1.02); }
.flujo-copy { position:absolute; inset:auto 0 0; padding:34px 9px 8px; background:linear-gradient(transparent,rgba(0,0,0,.94)); pointer-events:none; }
.flujo-meta { color:var(--musgo-verde,#6b9c33); font-size:.57rem; letter-spacing:.09em; text-transform:uppercase; }
.flujo-title { color:#f0f0eb; font-size:clamp(.7rem,2.8vw,1.1rem); line-height:1.18; font-weight:normal; margin-top:3px; }
.flujo-excerpt { color:#b6b6b0; font-family:Georgia,"Times New Roman",serif; font-size:.72rem; line-height:1.35; margin-top:5px; max-width:38rem; }
.flujo-item[data-size="1"] .flujo-excerpt { display:none; }
.flujo-item[data-size="1"] .flujo-title { font-size:.66rem; }
.flujo-filler {
  display:grid; place-items:center; border:1px dashed #344626;
  background:linear-gradient(45deg,transparent 46%,rgba(107,156,51,.16) 47% 53%,transparent 54%),radial-gradient(circle at 30% 30%,rgba(255,102,204,.12),transparent 45%),#060606;
  color:#567b2d; font-size:clamp(1rem,8vw,2.1rem); letter-spacing:.15em;
}
.flujo-filler small { font-size:.5rem; color:#526246; writing-mode:vertical-rl; }
@media(max-width:760px){
  .flujo-wrap{margin-top:16px;padding:7px;box-shadow:5px 5px 0 var(--musgo-verde-sombra,#243712)}
  .flujo-head span{display:none}
  .flujo-grid{--flujo-gap:5px}
  .flujo-copy{padding:27px 7px 6px}
  .flujo-excerpt{font-size:.65rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
}
'''

section = '''<section class="flujo-wrap" id="entradas">
<div class="flujo-head"><h2>ENTRADAS</h2><span>1 · 2 · 4 · 8 cuerpos</span></div>
<div class="flujo-grid" id="flujo-grid" aria-live="polite"></div>
</section>'''

fallback = json.dumps(items, ensure_ascii=False)
js = r'''
<script>
(() => {
  const grid = document.getElementById('flujo-grid');
  if (!grid) return;
  const fallback = __FALLBACK__;
  const marks = ['✦','MUSGO','⌁','⋮'];
  function ajustar(){ const gap=parseFloat(getComputedStyle(grid).gap)||0; grid.style.setProperty('--flujo-cell',`${(grid.clientWidth-gap)/2}px`); }
  new ResizeObserver(ajustar).observe(grid); ajustar();
  function tarjeta(item){
    const art=document.createElement('article'); art.className='flujo-item';
    art.dataset.size=String([1,2,4,8].includes(Number(item.size))?Number(item.size):1);
    if(item.shape)art.dataset.shape=item.shape; art.id=`flujo-${item.id}`;
    const a=document.createElement('a');a.href=item.href||'#';
    const img=document.createElement('img');img.src=item.image;img.alt=item.title||'';img.loading='lazy';
    const copy=document.createElement('div');copy.className='flujo-copy';
    const meta=document.createElement('div');meta.className='flujo-meta';meta.textContent=[item.date,item.kind].filter(Boolean).join(' · ');
    const h=document.createElement('h3');h.className='flujo-title';h.textContent=item.title||'sin título';copy.append(meta,h);
    if(item.excerpt){const p=document.createElement('p');p.className='flujo-excerpt';p.textContent=item.excerpt;copy.appendChild(p)}
    a.append(img,copy);art.appendChild(a);return art;
  }
  function relleno(n){const art=document.createElement('div');art.className='flujo-item flujo-filler';art.dataset.size='1';art.setAttribute('aria-hidden','true');const mark=document.createElement(n%2?'small':'span');mark.textContent=marks[n%marks.length];art.appendChild(mark);return art}
  function pintar(data){grid.innerHTML='';const list=[...data].sort((a,b)=>(b.order||0)-(a.order||0));list.forEach(x=>grid.appendChild(tarjeta(x)));const bodies=list.reduce((n,x)=>n+([1,2,4,8].includes(Number(x.size))?Number(x.size):1),0);const missing=(8-(bodies%8))%8;for(let i=0;i<missing;i++)grid.appendChild(relleno(i));requestAnimationFrame(ajustar)}
  fetch('feed/items.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject()).then(pintar).catch(()=>pintar(fallback));
})();
</script>
'''.replace('__FALLBACK__', fallback)

index = INDEX.read_text(encoding='utf-8')
if '/* FLUJO TETRIS' not in index:
    index = index.replace('</style>', css + '\n</style>', 1)
anchor = '<div id="entradas" style="position:relative; top:-6px; height:0; overflow:hidden;"></div>'
if 'id="flujo-grid"' not in index:
    if anchor not in index:
        raise RuntimeError('No se encontró el ancla de entradas')
    index = index.replace(anchor, section, 1)
if 'fetch(\'feed/items.json\'' not in index:
    index = index.replace('</body>', js + '\n</body>', 1)
index = index.replace(
    '<strong>última mutación:</strong> 03/08/26  ·  memes se ganó su propio espacio',
    '<strong>última mutación:</strong> 03/08/26  ·  las entradas aprendieron a encajar',
    1,
)
INDEX.write_text(index, encoding='utf-8')
print('Tetris aplicado:', len(items), 'piezas;', sum(x['size'] for x in items), 'cuerpos')
