# -*- coding: utf-8 -*-
"""Catalogo de bloques de placa. Cada bloque devuelve (html, timeline).
Para agregar un tipo de placa nuevo, se agrega una funcion aca. El chasis no se toca."""

def _sp(txt, cls=""):
    """palabra por palabra; {{...}} marca enfasis; <br> queda fuera de la animacion"""
    t = txt.replace("<br>", " <br> ").replace("{{", " \u27ea ").replace("}}", " \u27eb ")
    out=[]; hi=False
    for tok in t.split(" "):
        if not tok: continue
        if tok=="\u27ea": hi=True; continue
        if tok=="\u27eb": hi=False; continue
        if tok=="<br>": out.append("<br>"); continue
        c=f' class="{cls}"' if (hi and cls) else (' class="hi"' if hi else '')
        out.append(f"<span{c}>{tok}</span>")
    return " ".join(out)

def hook(e):
    tit="".join(f'<div id="t{i+1}">{l}</div>' for i,l in enumerate(e["titulo"]))
    body=f"""<div class="mid">
 <div class="eb" id="eb">{e['eyebrow']}</div>
 <h1>{tit}<div id="tr" class="az">{e['remate']}</div></h1>
 <div class="wr" id="wr"></div>
 <div class="sb" id="sb">{e['bajada']}</div></div>"""
    tl=" ent('eb',t,0.25,0.50,-18);\n"
    for i in range(len(e["titulo"])):
        tl+=f" ent('t{i+1}',t,{0.60+i*0.40:.2f},0.55,34);\n"
    tl+=f" pop('tr',t,{0.60+len(e['titulo'])*0.40+0.25:.2f},0.85);\n wipe('wr',t,3.10,0.55,107);\n ent('sb',t,3.55,0.65,22);\n"
    return body,tl

def dato(e):
    rr=' rr' if e.get("acento")=="rojo" else ''
    caja=""
    if e.get("contraste"):
        c=e["contraste"]
        caja=(f'<div><span class="qcmp{rr}" id="qcmp"><span class="lbl">{c["label"]}</span>'
              f'<span class="val" id="cmpv">0</span></span></div>')
    body=f"""<div class="dato">
 <div><span class="qtag{rr}" id="tag">{e['tag']}</span></div>
 <div><span class="cifra{rr}" id="cif">0</span></div>
 <div class="qrule" id="qr"></div>
 <div class="qlab" id="qlab">{e['etiqueta']}</div>
 <div class="qsub" id="qsub">{e['contexto']}</div>
 {caja}</div>"""
    tl=(f" ent('tag',t,0.15,0.45,-16);\n pop('cif',t,0.35,0.70);\n"
        f" cnt('cif',t,0.35,1.30,{e['cifra_a']},{e['cifra_b']},0,'{e['sufijo']}');\n"
        f" wipe('qr',t,1.50,0.55,150);\n ent('qlab',t,1.70,0.60,26);\n ent('qsub',t,2.10,0.60,20);\n")
    if e.get("contraste"):
        c=e["contraste"]
        tl+=f" pop('qcmp',t,2.95,0.60); cnt('cmpv',t,3.05,0.85,0,{c['valor']},0,'{c['sufijo']}');\n"
    return body,tl

def _fila(p,lab,a,b,cls,bar,tasa_lbl="Tasa anual"):
    col='bcn' if cls=='cn' else 'bus'
    return f"""<div class="row{' last' if p=='us' else ''}" id="{p}row">
 <div class="rt"><div><div class="pais {cls}" id="{p}lab">{lab}</div>
 <div class="rec"><span id="{p}a">{a}</span><span id="{p}ar" style="opacity:.55">→</span><span id="{p}b">0%</span></div></div>
 <div><div class="tl" id="{p}tl">{tasa_lbl}</div><div class="tasa {'v' if cls=='cn' else 'r'}" id="{p}ta">0,0%</div></div></div>
 <div class="bar"><div class="bf {col}" id="{p}bar"></div></div></div>"""

def comparativa(e):
    A,B=e["a"],e["b"]
    tit="".join(f'<div id="t{i+1}">{l}</div>' for i,l in enumerate(e["titulo"]))
    body=f"""<div class="eb" id="eb">{e['eyebrow']}</div>
<h1>{tit}<div id="tr" class="az">{e['remate']}</div></h1>
<div class="wr" id="wr"></div>
<div class="sb" id="sb">{e['fuente']}</div>
<div class="body">
{_fila('cn',A['label'],f"{A['de']}%",f"{A['a']}%",'cn',A['barra'])}
{_fila('us',B['label'],f"{B['de']}%",f"{B['a']}%",'us',B['barra'])}
<div class="lec" id="lecbox"><div class="tx" id="lec">{_sp(e['lectura'])}</div></div></div>"""
    tl=f"""
 ent('eb',t,0.20,0.45,-18);
 ent('t1',t,0.42,0.50,32); ent('t2',t,0.68,0.50,32); ent('tr',t,0.94,0.50,32);
 wipe('wr',t,1.40,0.55,107); ent('sb',t,1.60,0.50,16);
 ent('cnrow',t,2.15,0.50,28); ent('cnlab',t,2.25,0.45,14);
 pop('cna',t,2.45,0.50); ent('cnar',t,2.75,0.40,0);
 pop('cnb',t,2.95,0.55); cnt('cnb',t,2.95,1.25,{A['de']},{A['a']},0,'%');
 bar('cnbar',t,3.05,1.25,{A['barra']});
 ent('cntl',t,3.00,0.45,10); pop('cnta',t,3.35,0.50); cnt('cnta',t,3.35,1.20,0,{A['tasa']},1,'%','+');
 ent('usrow',t,4.35,0.50,28); ent('uslab',t,4.45,0.45,14);
 pop('usa',t,4.65,0.50); ent('usar',t,4.95,0.40,0);
 pop('usb',t,5.15,0.55); cnt('usb',t,5.15,1.25,{B['de']},{B['a']},0,'%');
 bar('usbar',t,5.25,1.25,{B['barra']});
 ent('ustl',t,5.20,0.45,10); pop('usta',t,5.55,0.50); cnt('usta',t,5.55,1.20,0,{B['tasa']},1,'%');
 ent('lecbox',t,6.85,0.60,26); words('lec',t,7.15,0.085,0.48);
"""
    return body,tl

def empate(e):
    A,B=e["a"],e["b"]
    tit="".join(f'<div id="t{i+1}">{l}</div>' for i,l in enumerate(e["titulo"]))
    def f(p,d,cls,col):
        return f"""<div class="row{' last' if p=='us' else ''}" id="{p}row"><div class="rt">
 <div><div class="pais {cls}" id="{p}lab">{d['label']}</div><div class="rec"><span id="{p}a">{d['valor']}</span></div></div>
 <div><div class="tl" id="{p}tl">Crecimiento</div><div class="tasa" id="{p}ta">0,0%</div></div></div>
 <div class="bar"><div class="bf {col}" id="{p}bar"></div></div></div>"""
    body=f"""<div class="eb" id="eb">{e['eyebrow']}</div>
<h1>{tit}<div id="tr" class="az">{e['remate']}</div></h1>
<div class="wr" id="wr"></div>
<div class="sb" id="sb">{e['fuente']}</div>
<div class="body">{f('cn',A,'cn','bcn')}{f('us',B,'us','bgr')}
<div class="lec" id="lecbox"><div class="tx" id="lec">{_sp(e['lectura'])}</div></div></div>"""
    tl=f"""
 ent('eb',t,0.20,0.45,-18);
 ent('t1',t,0.42,0.50,32); ent('t2',t,0.68,0.50,32); pop('tr',t,1.10,0.80);
 wipe('wr',t,1.85,0.55,107); ent('sb',t,2.05,0.50,16);
 ent('cnrow',t,2.55,0.50,28); ent('cnlab',t,2.65,0.45,14);
 pop('cna',t,2.85,0.55); bar('cnbar',t,3.00,1.20,{A['barra']});
 ent('cntl',t,3.00,0.45,10); pop('cnta',t,3.25,0.50); cnt('cnta',t,3.25,1.20,0,{A['tasa']},1,'%','+');
 ent('usrow',t,4.20,0.50,28); ent('uslab',t,4.30,0.45,14);
 pop('usa',t,4.50,0.55); bar('usbar',t,4.65,1.20,{B['barra']});
 ent('ustl',t,4.65,0.45,10); pop('usta',t,4.90,0.50); cnt('usta',t,4.90,1.20,0,{B['tasa']},1,'%','+');
 ent('lecbox',t,6.15,0.60,26); words('lec',t,6.45,0.085,0.48);
"""
    return body,tl

def conclusion(e):
    ps="".join(f'<div class="cl" id="cl{i+1}" style="margin-top:{34 if i==0 else 26}px">{_sp(p)}</div>'
               for i,p in enumerate(e["parrafos"]))
    r1=" ".join(f"<span>{w}</span>" for w in e["remate"][0].split(" "))
    r2=" ".join(f"<span>{w}</span>" for w in e["remate"][1].split(" "))
    body=f"""<div class="conc"><div class="eb" id="eb">{e['eyebrow']}</div>
 {ps}<div class="crule" id="cr"></div>
 <div class="crem" id="r1">{r1}</div>
 <div class="crem az2" id="r2">{r2}</div></div>"""
    tl=" ent('eb',t,0.25,0.50,-18);\n"
    for i in range(len(e["parrafos"])):
        tl+=f" words('cl{i+1}',t,{0.75+i*1.40:.2f},0.073,0.45);\n"
    tl+=" wipe('cr',t,4.45,0.60,190);\n words('r1',t,4.95,0.110,0.55);\n words('r2',t,6.55,0.115,0.60);\n"
    return body,tl

def cierre(e):
    body=f"""<style>.top{{opacity:0}}</style>
<div class="fin"><img class="lgb" id="lgb" src="{{LOGO}}">
 <div class="frule" id="fr"></div>
 <div class="url" id="url">{e['url']}</div>
 <div class="tag" id="tg">{e['bajada']}</div></div>"""
    tl=""" pop('lgb',t,0.35,0.85);
 if(E('lg')) E('lg').style.opacity=0; if(E('pg')) E('pg').style.opacity=0;
 wipe('fr',t,1.35,0.60,220); ent('url',t,1.75,0.65,24); ent('tg',t,2.35,0.60,18);
"""
    return body,tl

CATALOGO={"hook":hook,"dato":dato,"comparativa":comparativa,"empate":empate,
          "conclusion":conclusion,"cierre":cierre}
