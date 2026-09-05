#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GBX · motor de video estandarizado.
   uso:  python3 render.py guiones/xxx.json --perfil historia|reel|x [--hold 1.2]
   El chasis de marca no se modifica desde aca. Solo cambia el guion."""
import json, os, sys, base64, subprocess, shutil, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motor'))
from bloques import CATALOGO

R = os.path.dirname(os.path.abspath(__file__))
def b64(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()

def chasis(perfil):
    css = open(f'{R}/motor/chasis.css').read()
    m = perfil['margen_contenido']
    # el chasis trae los margenes por defecto; el perfil los sobreescribe
    import re
    css = re.sub(r"(\.w\{position:absolute;left:)[\d.]+px;right:[\d.]+px;top:[\d.]+px;bottom:[\d.]+px;",
                 rf"\g<1>{m['lados']}px;right:{m['lados']}px;top:{m['arriba']}px;bottom:{m['abajo']}px;", css)
    return css

def seleccionar(escenas, perfil, transiciones):
    """recorta por prioridad hasta entrar en el tope de duracion de la plataforma"""
    tope = perfil.get('duracion_max_s')
    if not tope: return escenas, transiciones, None
    for pmax in (3,2,1):
        sel=[e for e in escenas if e.get('prioridad',1)<=pmax]
        if not any(e['bloque']=='cierre' for e in sel):
            sel += [e for e in escenas if e['bloque']=='cierre']
        tr = transiciones[:max(len(sel)-1,0)]
        dur = sum(e['dur'] for e in sel) - sum(float(t.split(':')[1]) for t in tr)
        if dur <= tope:
            recorte = None if pmax==3 else f"prioridad<={pmax}: {len(escenas)-len(sel)} escenas fuera"
            return sel, tr, recorte
    return sel, tr, "no entra ni con prioridad 1"

def construir(guion, perfil, salida, hold=1.2):
    os.makedirs(salida, exist_ok=True)
    css = chasis(perfil); js = open(f'{R}/motor/anim.js').read()
    LOGO = b64(f'{R}/marca/logo_blanco.png'); XAZ = b64(f'{R}/marca/isotipo_x_azul.png')
    esc, tr, recorte = seleccionar(guion['escenas'], perfil, guion['transiciones'])
    tot = len(esc); paginas=[]
    for i,e in enumerate(esc,1):
        body, tl = CATALOGO[e['bloque']](e)
        body = body.replace('{LOGO}', LOGO)
        doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="dots"></div><div class="veil"></div>
<img class="xbig" src="{XAZ}"><div class="xscrim"></div>
<div class="w"><div class="top"><img class="lg" id="lg" src="{LOGO}"><div class="pg" id="pg">{i} / {tot}</div></div>
{body}</div>
<script>{js}
function render(t){{ ent('lg',t,0.05,0.5,-14); ent('pg',t,0.15,0.5,-10);
{tl}
}} render(0);</script></body></html>"""
        open(f'{salida}/s{i}.html','w').write(doc)
        paginas.append({'n':i,'dur':e['dur'],'bloque':e['bloque']})
    json.dump({'paginas':paginas,'transiciones':tr,'recorte':recorte,'hold':hold},
              open(f'{salida}/plan.json','w'), ensure_ascii=False, indent=1)
    return paginas, tr, recorte

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('guion'); ap.add_argument('--perfil',default='historia')
    ap.add_argument('--hold',type=float,default=1.2)
    ap.add_argument('--solo-plan',action='store_true')
    a=ap.parse_args()
    g=json.load(open(a.guion)); p=json.load(open(f'{R}/perfiles/{a.perfil}.json'))
    nom=os.path.splitext(os.path.basename(a.guion))[0]
    out=f'{R}/salida/{nom}__{a.perfil}'
    pgs,tr,rec=construir(g,p,out,a.hold)
    dur=sum(x['dur'] for x in pgs)+len(pgs)*a.hold-sum(float(t.split(':')[1]) for t in tr)
    print(f"perfil: {p['nombre']}  {p['ancho']}x{p['alto']}")
    print(f"escenas: {len(pgs)}  ->  {[x['bloque'] for x in pgs]}")
    print(f"duracion estimada: {dur:.1f}s / tope {p.get('duracion_max_s')}s")
    if rec: print(f"AVISO recorte: {rec}")
    print(f"html en: {out}")
