from pathlib import Path
import json,re

index=Path('index.html')
s=index.read_text(encoding='utf-8')

css='''/* FLUJO FLEXIBLE — publicaciones chicas, medianas y grandes */
.flujo-wrap{max-width:760px;margin:20px auto 22px;padding:10px;border:2px solid var(--musgo-verde,#6b9c33);background:linear-gradient(145deg,rgba(107,156,51,.08),transparent 38%),#050505;box-shadow:7px 7px 0 var(--musgo-verde-sombra,#243712);scroll-margin-top:10px}
.flujo-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-bottom:9px}.flujo-head h2{color:var(--musgo-verde,#6b9c33);font-size:.78rem;font-weight:normal;letter-spacing:.2em}.flujo-head span{color:#686868;font-size:.58rem;letter-spacing:.08em}
.flujo-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;align-items:stretch}
.flujo-item{position:relative;min-width:0;overflow:hidden;border:1px solid #343434;background:#090909}.flujo-item[data-size="small"]{grid-column:span 1;aspect-ratio:1/1}.flujo-item[data-size="medium"]{grid-column:1/-1;aspect-ratio:2/1;min-height:170px}.flujo-item[data-size="large"]{grid-column:1/-1;aspect-ratio:4/3;min-height:290px}
.flujo-item>a{display:block;width:100%;height:100%;color:inherit;text-decoration:none}.flujo-item img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .18s ease,filter .18s ease;filter:saturate(.82) contrast(1.04)}.flujo-item:hover img{transform:scale(1.018);filter:saturate(1) contrast(1.02)}
.flujo-copy{position:absolute;inset:auto 0 0;padding:34px 9px 8px;background:linear-gradient(transparent,rgba(0,0,0,.94));pointer-events:none}.flujo-meta{color:var(--musgo-verde,#6b9c33);font-size:.57rem;letter-spacing:.09em;text-transform:uppercase}.flujo-title{color:#f0f0eb;font-size:clamp(.7rem,2.8vw,1.1rem);line-height:1.18;font-weight:normal;margin-top:3px}.flujo-excerpt{color:#b6b6b0;font-family:Georgia,"Times New Roman",serif;font-size:.72rem;line-height:1.35;margin-top:5px;max-width:38rem}.flujo-item[data-size="small"] .flujo-excerpt{display:none}.flujo-item[data-size="small"] .flujo-title{font-size:.66rem}
@media(max-width:760px){.flujo-wrap{margin-top:16px;padding:7px;box-shadow:5px 5px 0 var(--musgo-verde-sombra,#243712)}.flujo-head span{display:none}.flujo-grid{gap:5px}.flujo-copy{padding:24px 7px 6px}.flujo-item[data-size="medium"]{min-height:145px}.flujo-item[data-size="large"]{min-height:250px}.flujo-item[data-size="large"] .flujo-title{font-size:.9rem}.flujo-excerpt{font-size:.65rem;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}}
'''

start=s.index('/* FLUJO TETRIS — contenido separado del código principal */')
end=s.index('\n</style>',start)
s=s[:start]+css+s[end:]
s=s.replace('1 · 2 · 4 · 8 cuerpos','chica · mediana · grande')
s=s.replace('las entradas aprendieron a encajar','las entradas encontraron su ritmo')

old_start=s.index("<script>\n(() => {\n  const grid = document.getElementById('flujo-grid');")
old_end=s.index('</script>',old_start)+len('</script>')
old=s[old_start:old_end]
m=re.search(r'const fallback = (\[.*?\]);\n',old,re.S)
if not m: raise RuntimeError('No se encontró fallback')
fallback=m.group(1)
fallback=re.sub(r'"size"\s*:\s*(4|8)', '"size":"large"', fallback)
fallback=re.sub(r'"size"\s*:\s*2', '"size":"medium"', fallback)
fallback=re.sub(r'"size"\s*:\s*1', '"size":"small"', fallback)

js=f'''<script>
(() => {{
  const grid=document.getElementById('flujo-grid');
  if(!grid)return;
  const fallback={fallback};
  function tamano(v){{v=String(v??'').toLowerCase();if(['1','small','chica','chico'].includes(v))return'small';if(['2','medium','mediana','mediano'].includes(v))return'medium';if(['4','8','large','grande'].includes(v))return'large';return'small'}}
  function tarjeta(item){{const art=document.createElement('article');art.className='flujo-item';art.dataset.size=tamano(item.size);art.id=`flujo-${{item.id}}`;const a=document.createElement('a');a.href=item.href||'#';const img=document.createElement('img');img.src=item.image;img.alt=item.title||'';img.loading='lazy';const copy=document.createElement('div');copy.className='flujo-copy';const meta=document.createElement('div');meta.className='flujo-meta';meta.textContent=[item.date,item.kind].filter(Boolean).join(' · ');const h=document.createElement('h3');h.className='flujo-title';h.textContent=item.title||'sin título';copy.append(meta,h);if(item.excerpt){{const p=document.createElement('p');p.className='flujo-excerpt';p.textContent=item.excerpt;copy.appendChild(p)}}a.append(img,copy);art.appendChild(a);return art}}
  function pintar(items){{grid.innerHTML='';[...items].sort((a,b)=>(b.order||0)-(a.order||0)).forEach(x=>grid.appendChild(tarjeta(x)))}}
  fetch('feed/items.json',{{cache:'no-store'}}).then(r=>r.ok?r.json():Promise.reject()).then(pintar).catch(()=>pintar(fallback));
}})();
</script>'''
s=s[:old_start]+js+s[old_end:]
index.write_text(s,encoding='utf-8')

items=json.loads(Path('feed/items.json').read_text(encoding='utf-8'))
for item in items:
    n=str(item.get('size','')).lower()
    item['size']='large' if n in {'4','8','large','grande'} else 'medium' if n in {'2','medium','mediana','mediano'} else 'small'
Path('feed/items.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('grilla flexible lista')
