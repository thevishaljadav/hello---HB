(function(){
  function apply(){
    var tabs=document.querySelector('.tabs'); if(!tabs)return;
    var micro=Array.from(tabs.querySelectorAll('.tab')).find(function(x){return x.textContent.trim().toLowerCase()==='micro drama'});
    var shorts=Array.from(tabs.querySelectorAll('.tab')).find(function(x){return x.textContent.trim().toLowerCase()==='shorts'});
    if(!micro||!shorts)return;
    micro.onclick=function(){
      shorts.click();
      setTimeout(function(){
        tabs.querySelectorAll('.tab').forEach(function(x){x.classList.toggle('on',x===micro)});
        micro.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
      },100);
    };
  }
  apply();
  setTimeout(apply,500);
})();
