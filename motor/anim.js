
const E=id=>document.getElementById(id);
const cl=(v,a,b)=>Math.max(a,Math.min(b,v));
const oc=p=>1-Math.pow(1-p,3);                 // easeOutCubic
const oe=p=>p>=1?1:1-Math.pow(2,-9*p);         // easeOutExpo, aterriza suave
const ob=p=>{const c=1.9;return 1+ (c+1)*Math.pow(p-1,3)+c*Math.pow(p-1,2);}; // overshoot
function ph(t,st,du){return cl((t-st)/du,0,1);}
// entrada: fade + desplazamiento
function ent(id,t,st,du,dy,ease){const p=ph(t,st,du);const e=(ease||oc)(p);const el=E(id);if(!el)return;
 el.style.opacity=p<=0?0:e; el.style.transform=`translateY(${(1-e)*(dy===undefined?26:dy)}px)`;}
// numero que cuenta y desacelera
function cnt(id,t,st,du,from,to,dec,suf,pre){const p=ph(t,st,du);const e=oe(p);
 const val=from+(to-from)*e; const el=E(id); if(!el)return;
 el.textContent=(pre||'')+val.toFixed(dec).replace('.',',')+(suf||'');}
// golpe de escala al aterrizar
function pop(id,t,st,du){const p=ph(t,st,du);const el=E(id);if(!el)return;
 el.style.opacity=p<=0?0:1; el.style.transform=`scale(${p<=0?0.6:ob(p)})`;}
function bar(id,t,st,du,w){const p=ph(t,st,du);const el=E(id);if(!el)return;
 el.style.width=(oc(p)*w)+'%';}
function wipe(id,t,st,du,w){const p=ph(t,st,du);const el=E(id);if(!el)return;
 el.style.width=(oc(p)*w)+'px';}
function words(id,t,st,step,du){const el=E(id);if(!el)return;
 const ws=el.querySelectorAll('span');
 ws.forEach((s,i)=>{const p=ph(t,st+i*step,du);s.style.opacity=p;s.style.transform=`translateY(${(1-oc(p))*14}px)`;});}
