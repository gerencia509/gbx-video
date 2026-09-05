#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Captura cuadro a cuadro y ensambla. uso: python3 motor/producir.py <carpeta_salida> <perfil.json>"""
import json,os,sys,subprocess
from playwright.sync_api import sync_playwright

D=sys.argv[1]; P=json.load(open(sys.argv[2]))
plan=json.load(open(f'{D}/plan.json')); FPS=P['fps']; HOLD=plan['hold']
W,H=P['ancho'],P['alto']; C=P['codec']

def sh(c): subprocess.run(c,shell=True,check=True)

# 1 · captura
with sync_playwright() as pw:
    b=pw.chromium.launch(args=['--force-color-profile=srgb','--font-render-hinting=none'])
    pg=b.new_page(viewport={'width':W,'height':H},device_scale_factor=1)
    for x in plan['paginas']:
        n=x['n']; fr=int(x['dur']*FPS); od=f'{D}/f{n}'; os.makedirs(od,exist_ok=True)
        pg.goto('file://'+os.path.abspath(f'{D}/s{n}.html')); pg.wait_for_timeout(1500)
        for f in range(fr):
            pg.evaluate(f"render({f/FPS})")
            pg.screenshot(path=f'{od}/f{f:04d}.jpg',type='jpeg',quality=93)
        print(f'  escena {n} ({x["bloque"]}): {fr} cuadros',flush=True)
    b.close()

# 2 · una escena por clip, con pausa de lectura al final
for x in plan['paginas']:
    n=x['n']
    sh(f'ffmpeg -y -v error -framerate {FPS} -i {D}/f{n}/f%04d.jpg '
       f'-vf "tpad=stop_mode=clone:stop_duration={HOLD}" -c:v {C["v"]} -preset ultrafast -crf 18 '
       f'-pix_fmt {C["pix"]} -r {FPS} {D}/c{n}.mp4')

# 3 · ensamblado encadenado con las transiciones del guion
cur=f'{D}/c1.mp4'; acc=plan['paginas'][0]['dur']+HOLD
for i,x in enumerate(plan['paginas'][1:],1):
    kind,dur=plan['transiciones'][i-1].split(':'); dur=float(dur)
    off=acc-dur; nxt=f'{D}/j{i}.mp4'
    sh(f'ffmpeg -y -v error -i {cur} -i {D}/c{x["n"]}.mp4 -filter_complex '
       f'"[0][1]xfade=transition={kind}:duration={dur}:offset={off:.2f},format={C["pix"]}[v]" '
       f'-map "[v]" -c:v {C["v"]} -preset ultrafast -crf 19 -r {FPS} {nxt}')
    acc = acc + x['dur'] + HOLD - dur; cur=nxt

# 4 · master
extra = '-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -map 1:a -shortest -c:a aac -b:a 96k' if P.get('audio_silencioso') else ''
fs = '-movflags +faststart' if C.get('faststart') else ''
out=f'{D}/GBX_video.mp4'
sh(f'ffmpeg -y -v error -i {cur} {extra} -map 0:v -c:v {C["v"]} -preset medium -crf {C["crf"]} '
   f'-pix_fmt {C["pix"]} -r {FPS} -profile:v {C["perfil"]} -level {C["nivel"]} {fs} {out}')

d=subprocess.run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {out}',
                 shell=True,capture_output=True,text=True).stdout.strip()
print(f'LISTO {out}  {float(d):.1f}s')
if P.get('duracion_max_s') and float(d)>P['duracion_max_s']:
    print(f'!! EXCEDE el tope de {P["duracion_max_s"]}s de {P["nombre"]}')
