from pathlib import Path
import re

p = Path('app/src/main/assets/index.html')
s = p.read_text()
s = re.sub(r'<script id="asia-final-navigation-v1">.*?</script>', '', s, flags=re.S)

js = r'''<script id="asia-final-navigation-v1">
(function(){
  function fallbackGo(id,index){
    var views=document.querySelectorAll('.view');
    views.forEach(function(v){v.classList.remove('on')});
    var target=document.getElementById(id);
    if(target) target.classList.add('on');
    var tabs=document.querySelectorAll('.tabs .tab');
    tabs.forEach(function(b){b.classList.remove('on')});
    if(index!==undefined&&tabs[index]) tabs[index].classList.add('on');
    var nav=document.querySelectorAll('.nav button');
    nav.forEach(function(b){b.classList.remove('on')});
    if(id==='home'&&nav[0])nav[0].classList.add('on');
    else if(id==='explore'&&nav[1])nav[1].classList.add('on');
    else if(id==='community'&&nav[3])nav[3].classList.add('on');
    else if(id==='profile'&&nav[4])nav[4].classList.add('on');
    window.scrollTo(0,0);
  }
  var coreGo=window.go;
  window.go=function(id,index,btn){
    try{
      if(typeof coreGo==='function'){
        coreGo.apply(window,arguments);
        var t=document.getElementById(id);
        if(t&&t.classList.contains('on'))return;
      }
    }catch(e){window.__asiaLastError=e.message||String(e)}
    fallbackGo(id,index);
  };
  var coreOpen=window.openSheet;
  window.openSheet=function(type){
    try{if(typeof coreOpen==='function')return coreOpen.apply(window,arguments)}catch(e){window.__asiaLastError=e.message||String(e)}
    if(typeof window.fallbackOpenSheet==='function')return window.fallbackOpenSheet(type);
    var o=document.getElementById('overlay'),sh=document.getElementById('sheet');
    if(o&&sh){sh.innerHTML='<button class="close" onclick="closeSheet()">×</button><h2>Asia Drama</h2><div class="empty">This section is temporarily unavailable. Please try again.</div>';o.classList.add('on')}
  };
})();
</script>'''

s = s.replace('</body>', js + '</body>')
p.write_text(s)
