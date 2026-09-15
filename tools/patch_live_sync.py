from pathlib import Path
import re

html = Path('app/src/main/assets/index.html')
s = html.read_text()
s = re.sub(r'<script id="asia-live-sync-v1">.*?</script>', '', s, flags=re.S)

css = r'''<style id="asia-live-sync-css-v1">
.asia-live-dot{display:inline-flex;align-items:center;gap:6px;margin-left:8px;font-size:11px;font-weight:800;color:#a5a7b0}.asia-live-dot i{width:7px;height:7px;border-radius:50%;background:#31d17c;display:inline-block;box-shadow:0 0 8px rgba(49,209,124,.5)}.asia-live-dot.offline i{background:#ff8a00;box-shadow:none}.asia-live-dot.syncing i{background:#ff2942;box-shadow:0 0 8px rgba(255,41,66,.5)}
</style>'''

js = r'''<script id="asia-live-sync-v1">
(function(){
  var lastHash='';
  var busy=false;
  var interval=30000;
  function status(mode,label){
    var h=document.querySelector('.top .brand');
    if(!h)return;
    var e=document.getElementById('asiaLiveStatus');
    if(!e){e=document.createElement('span');e.id='asiaLiveStatus';e.className='asia-live-dot';h.appendChild(e)}
    e.className='asia-live-dot '+(mode||'');
    e.innerHTML='<i></i><span>'+String(label||'Live')+'</span>';
  }
  async function sync(force){
    if(busy||!navigator.onLine)return;
    if(typeof loadCatalog!=='function')return;
    busy=true;status('syncing','Syncing');
    try{
      var r=await fetch(API+'/catalog?ts='+Date.now(),{cache:'no-store'});
      if(!r.ok)throw new Error('catalog '+r.status);
      var j=await r.json();
      var next=Array.isArray(j.series)&&j.series.length?j.series:demo;
      var hash=JSON.stringify(next);
      if(force||hash!==lastHash){
        lastHash=hash;
        catalog=next;
        renderCatalog();
        if(typeof renderMusic==='function')renderMusic();
        if(typeof renderShorts==='function')renderShorts();
      }
      status('','Live');
    }catch(e){status('offline','Offline');}
    finally{busy=false}
  }
  window.asiaLiveSync=function(){sync(true)};
  window.addEventListener('online',function(){status('','Live');sync(true)});
  window.addEventListener('offline',function(){status('offline','Offline')});
  document.addEventListener('visibilitychange',function(){if(!document.hidden)sync(true)});
  window.addEventListener('pageshow',function(){sync(true)});
  setTimeout(function(){sync(true)},1200);
  setInterval(function(){if(!document.hidden)sync(false)},interval);
  if(!navigator.onLine)status('offline','Offline');
})();
</script>'''

s = s.replace('</head>', css + '</head>')
s = s.replace('</body>', js + '</body>')
html.write_text(s)
