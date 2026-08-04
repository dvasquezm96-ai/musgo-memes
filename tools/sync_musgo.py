from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import re

BASE = 'https://chicxmusgo.neocities.org/'


def bajar(url: str) -> bytes:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 MUSGO-GitHub-copy'})
    with urlopen(req, timeout=40) as respuesta:
        return respuesta.read()


html = bajar(BASE).decode('utf-8', errors='replace')

# Copiar automáticamente las imágenes locales usadas por la página.
recursos = set(re.findall(
    r'''(?:src|href)=["']([^"']+\.(?:png|jpe?g|webp|gif|avif))(?:\?[^"']*)?["']''',
    html,
    flags=re.I,
))
for recurso in recursos:
    if recurso.startswith(('data:', 'http://', 'https://', '//')):
        continue
    url = urljoin(BASE, recurso)
    nombre = Path(urlparse(url).path).name
    if not nombre:
        continue
    try:
        Path(nombre).write_bytes(bajar(url))
        html = html.replace(recurso, nombre)
    except Exception as error:
        print('No se pudo copiar', url, error)

# Mantener MEMES como módulo vivo leído desde musgo-memes/main.
API_MEMES = 'https://api.github.com/repos/dvasquezm96-ai/musgo-memes/contents/memes?ref=main'
if API_MEMES not in html:
    seccion = '''<section class="memes-home-wrap"><section class="memes-panel" id="memes">
<div class="memes-panel-head"><h2 class="memes-panel-title">MEMES</h2><span class="meme-count-lite" id="meme-count-lite">cargando...</span></div>
<div class="memes-minis" id="memes-minis"><span class="meme-count-lite">buscando memes...</span></div>
<details class="memes-foldout" id="memes-completo"><summary class="memes-summary">ver todos los memes ↓</summary>
<div class="memes-full"><div class="memes-oldschool-top"><span class="blinkish">memes</span><span class="memes-oldschool-note">archivo viejo escuela</span></div>
<div id="memes-lista"></div>
<div class="memes-oldschool-bottom"><a href="#memes">volver arriba ↑</a></div></div></details>
</section></section>'''
    html, cambios = re.subn(
        r'<section class="memes-home-wrap">.*?</section></section><main class="container sustrato-wrap"',
        seccion + '<main class="container sustrato-wrap"',
        html,
        count=1,
        flags=re.S,
    )
    if cambios != 1:
        raise RuntimeError('No se encontró la sección MEMES para volverla dinámica')

    js = r'''
async function cargarMemesDesdeGitHub() {
  const minis=document.getElementById('memes-minis');
  const lista=document.getElementById('memes-lista');
  const contador=document.getElementById('meme-count-lite');
  if(!minis||!lista||!contador)return;
  const extensiones=/\.(png|jpe?g|webp|gif|avif)$/i;
  const respaldo=[
    {name:'musgo-meme-sapo-charango.webp',download_url:'musgo-meme-sapo-charango.webp'},
    {name:'musgo-meme-hormigas.webp',download_url:'musgo-meme-hormigas.webp'}
  ];
  function mini(item){
    const a=document.createElement('a');a.className='mini-meme';a.href='#memes-completo';a.title=item.name;
    const img=document.createElement('img');img.src=item.download_url;img.alt=item.name;img.loading='lazy';a.appendChild(img);return a;
  }
  function ficha(item,n){
    const art=document.createElement('article');art.className='meme-card-full';
    const seq=document.createElement('div');seq.className='meme-seq';seq.textContent=String(n).padStart(2,'0');
    const a=document.createElement('a');a.className='meme-full-image-link';a.href=item.download_url;a.target='_blank';a.rel='noopener';
    const img=document.createElement('img');img.src=item.download_url;img.alt=item.name;img.loading='lazy';a.appendChild(img);
    const meta=document.createElement('div');meta.className='meme-full-meta';
    const nombre=document.createElement('span');nombre.className='meme-date';nombre.textContent=item.name;
    const abrir=document.createElement('a');abrir.href=item.download_url;abrir.target='_blank';abrir.rel='noopener';abrir.textContent='abrir imagen ↗';
    meta.append(nombre,abrir);art.append(seq,a,meta);return art;
  }
  try{
    const r=await fetch(''' + repr(API_MEMES) + r''',{cache:'no-store'});
    const data=r.ok?await r.json():[];
    const subidos=Array.isArray(data)?data.filter(x=>x.type==='file'&&extensiones.test(x.name)).sort((a,b)=>b.name.localeCompare(a.name)):[];
    const nombres=new Set(subidos.map(x=>x.name));
    const items=[...subidos,...respaldo.filter(x=>!nombres.has(x.name))];
    minis.innerHTML='';lista.innerHTML='';contador.textContent=`${String(items.length).padStart(2,'0')} piezas`;
    items.slice(0,6).forEach(x=>minis.appendChild(mini(x)));
    items.forEach((x,i)=>lista.appendChild(ficha(x,i+1)));
  }catch(error){
    minis.innerHTML='';lista.innerHTML='';contador.textContent='02 piezas';
    respaldo.forEach(x=>minis.appendChild(mini(x)));respaldo.forEach((x,i)=>lista.appendChild(ficha(x,i+1)));
  }
}
cargarMemesDesdeGitHub();
'''
    if '</script>\n</body>' in html:
        html = html.replace('</script>\n</body>', js + '\n</script>\n</body>', 1)
    else:
        html = html.replace('</body>', '<script>' + js + '</script>\n</body>', 1)

Path('index.html').write_text(html, encoding='utf-8')
Path('.nojekyll').write_text('', encoding='utf-8')
Path('README-MUSGO-DRAFT.md').write_text(
    '# MUSGO — borrador completo\n\n'
    'Copia del sitio de Neocities preparada para GitHub. '
    'MEMES se carga automáticamente desde la rama main y la carpeta memes/. '
    'La rama main y la galería publicada no se modifican.\n',
    encoding='utf-8',
)
print('MUSGO preparado:', len(html), 'caracteres;', len(recursos), 'recursos detectados')
