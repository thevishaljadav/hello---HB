from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text()

marker = 'asia-visual-hardening-v1'
if marker in s:
    raise SystemExit(0)

css = r'''<style id="asia-visual-hardening-v1">
/* Final mobile/WebView layout hardening: keep sticky UI opaque and prevent page-level horizontal drift. */
html,body{width:100%;max-width:100%;overflow-x:hidden}
body{overscroll-behavior-x:none}
.app{width:100%;max-width:680px;overflow-x:clip}
.top{width:100%;max-width:680px}
.tabs{width:100%;max-width:680px;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;background:#08090c!important;backdrop-filter:blur(18px)}
.tabs .tab{flex:0 0 auto}
.hero{width:auto;max-width:calc(100% - 24px)}
.row{max-width:100%;overflow-x:auto;overflow-y:hidden}
.grid{max-width:100%;min-width:0}
.card,.panel,.post,.profile,.adminBox{min-width:0}
img,video,audio{max-width:100%}
.nav{max-width:680px;overflow:hidden}
@media(max-width:680px){.top,.tabs,.nav{max-width:100vw}.brand{min-width:0}.brand div{white-space:nowrap}.actions{min-width:0}.icon{flex:0 0 48px}}
</style>'''

js = r'''<script id="asia-visual-hardening-v1-js">
(function(){
  function resetTabs(){
    var tabs=document.querySelector('.tabs');
    if(tabs) tabs.scrollTo({left:0,behavior:'auto'});
  }
  window.asiaResetTabs=resetTabs;
  document.addEventListener('DOMContentLoaded',resetTabs);
  document.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.tabs .tab');
    if(b){setTimeout(function(){b.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});},0)}
  },true);
  window.addEventListener('resize',function(){document.documentElement.style.setProperty('--vw',window.innerWidth+'px')},{passive:true});
})();
</script>'''

s = s.replace('</head>', css + '</head>')
s = s.replace('</body>', js + '</body>')
html.write_text(s)
