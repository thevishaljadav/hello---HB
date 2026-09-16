(function(){
  'use strict';
  if (window.__asiaUxV3) return;
  window.__asiaUxV3 = true;

  var RED = '#ff2942';
  var FALLBACK = 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 900"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#32111b"/><stop offset="1" stop-color="#111217"/></linearGradient></defs><rect width="600" height="900" fill="url(#g)"/><text x="50%" y="48%" fill="#ff2942" font-size="34" font-family="Arial" text-anchor="middle" font-weight="700">ASIA DRAMA</text><text x="50%" y="54%" fill="#aaa" font-size="20" font-family="Arial" text-anchor="middle">MEDIA</text></svg>');

  var style=document.createElement('style');
  style.id='asia-ux-v3-css';
  style.textContent=`
    .tabs{gap:10px;padding:9px 14px;scroll-behavior:smooth}
    .tabs .tab{flex:0 0 auto;min-height:50px;padding:0 18px;border-radius:25px;font-size:16px}
    .actions .icon{width:54px;height:54px;min-width:54px;display:grid;place-items:center}
    .actions .icon svg{width:27px!important;height:27px!important;stroke-width:2.4}
    .nav{height:82px;padding-bottom:env(safe-area-inset-bottom);box-sizing:border-box}
    .nav button{min-height:64px;font-size:11px;gap:4px}
    .nav .navIcon svg{width:28px!important;height:28px!important;stroke-width:2.25}
    .nav .plus{width:60px;height:60px;min-width:60px;min-height:60px;font-size:30px;margin:0 3px}
    .microRail{display:flex;gap:10px;overflow-x:auto;padding:0 15px 7px;scroll-snap-type:x proximity;scrollbar-width:none}
    .microRail::-webkit-scrollbar{display:none}
    .microCard{position:relative;flex:0 0 185px;height:255px;border-radius:18px;overflow:hidden;background:#17181e;border:1px solid var(--line);scroll-snap-align:start;cursor:pointer}
    .microCard img{width:100%;height:100%;object-fit:cover;display:block}
    .microCard:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 32%,rgba(0,0,0,.96) 100%)}
    .microInfo{position:absolute;z-index:2;left:11px;right:11px;bottom:11px}
    .microInfo b{display:block;font-size:15px;margin-top:7px}.microInfo small{display:block;color:#bbb;margin-top:4px}
    .assetFallback{background:linear-gradient(145deg,#32111b,#111217)!important}
    .media-empty{margin:15px;padding:24px;border:1px dashed #3a3c45;border-radius:17px;text-align:center;color:#a5a7b0}
    .musicAll{display:grid;gap:8px}.musicAll .notice{margin:0;min-height:72px}
    .roleBadge{display:inline-flex;align-items:center;margin-left:8px;padding:4px 8px;border-radius:999px;background:#25262d;color:#aaa;font-size:10px;font-weight:800}
    .roleBadge.admin{background:#3a1018;color:#ff7084}
    #asiaAdminCMS{padding-bottom:110px}
    @media(max-width:420px){.actions .icon{width:50px;min-width:50px}.actions .icon svg{width:25px!important;height:25px!important}.tabs .tab{padding:0 16px}.microCard{flex-basis:175px}}
  `;
  document.head.appendChild(style);

  function fallbackImage(img){
    if(!img || img.dataset.asiaFallback) return;
    img.dataset.asiaFallback='1';
    img.addEventListener('error',function(){ this.onerror=null; this.src=FALLBACK; this.classList.add('assetFallback'); },{once:true});
  }
  function hardenImages(){document.querySelectorAll('img').forEach(fallbackImage)}

  var icons={
    search:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"></circle><path d="m16 16 4 4"></path></svg>',
    bell:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"></path><path d="M10 21h4"></path></svg>',
    user:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"></circle><path d="M5 20c.8-4 3-6 7-6s6.2 2 7 6"></path></svg>',
    home:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3.5 10 8.5-7 8.5 7v10a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1z"></path><path d="M9 21v-6h6v6"></path></svg>',
    explore:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="2"></rect><path d="M8 8h8M8 12h8M8 16h5"></path></svg>',
    community:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM16 11a2.5 2.5 0 1 0 0-5"></path><path d="M2.8 20c.5-4 2.3-6 5.2-6s4.7 2 5.2 6M14 14c3.8-.2 5.8 1.8 6.3 6"></path></svg>',
    profile:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"></circle><path d="M5 20c.8-4 3-6 7-6s6.2 2 7 6"></path></svg>'
  };

  function refreshHeader(){
    var a=document.querySelectorAll('.actions .icon');
    if(a[0])a[0].innerHTML=icons.search;
    if(a[1])a[1].innerHTML=icons.bell;
    if(a[2]&&!a[2].querySelector('img'))a[2].innerHTML=icons.profile;
  }
  function refreshNav(){
    var n=document.querySelectorAll('.nav button');
    var labels=['Home','Explore','','Community','Profile'], map=[icons.home,icons.explore,null,icons.community,icons.profile];
    n.forEach(function(b,i){
      if(i===2)return;
      b.innerHTML='<span class="navIcon">'+map[i]+'</span><span class="navLabel">'+labels[i]+'</span>';
    });
  }

  function findTab(label){
    return Array.from(document.querySelectorAll('.tabs .tab')).find(function(x){return x.textContent.trim().toLowerCase()===label.toLowerCase()});
  }
  function setTopTab(label){
    document.querySelectorAll('.tabs .tab').forEach(function(x){x.classList.toggle('on',x.textContent.trim().toLowerCase()===label.toLowerCase())});
    var t=findTab(label); if(t)t.scrollIntoView({behavior:'smooth',block:'nearest',inline:'center'});
  }

  function addMicroTab(){
    var tabs=document.querySelector('.tabs'); if(!tabs||findTab('Micro Drama'))return;
    var b=document.createElement('button'); b.className='tab'; b.textContent='Micro Drama'; b.type='button';
    b.onclick=function(){setTopTab('Micro Drama'); var s=findTab('Shorts'); if(s)s.click()};
    var music=findTab('Music'); tabs.insertBefore(b,music||null);
  }

  function addMicroHome(){
    var home=document.getElementById('home'); if(!home||document.getElementById('asiaMicroDramaHome'))return;
    var h=document.createElement('div');h.className='head';h.innerHTML='<h2>Micro Drama</h2><button class="link" type="button">View all ›</button>';
    h.querySelector('button').onclick=function(){var t=findTab('Micro Drama');if(t)t.click()};
    var rail=document.createElement('div');rail.id='asiaMicroDramaHome';rail.className='microRail';
    var data=[
      ['2 Minute Love','Romance','https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=700&q=80'],
      ['City Secret','Drama','https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=700&q=80'],
      ['One More Chance','Family','https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=700&q=80']
    ];
    data.forEach(function(x){var a=document.createElement('article');a.className='microCard';a.innerHTML='<img src="'+x[2]+'" alt="'+x[0]+'"><div class="microInfo"><span class="pill">MICRO DRAMA</span><b>'+x[0]+'</b><small>'+x[1]+' • 9:16</small></div>';a.onclick=function(){var t=findTab('Micro Drama');if(t)t.click()};rail.appendChild(a);});
    var shortsHead=Array.from(home.querySelectorAll('.head')).find(function(x){return x.querySelector('h2')&&x.querySelector('h2').textContent.trim()==='Shorts'});
    if(shortsHead){home.insertBefore(h,shortsHead);home.insertBefore(rail,shortsHead)}else{home.appendChild(h);home.appendChild(rail)}
  }

  function addMusicFallback(){
    var host=document.getElementById('music'); if(!host||host.querySelector('#asiaMusicAll'))return;
    var panel=host.querySelector('.panel:last-child');if(!panel)return;
    var box=document.createElement('div');box.id='asiaMusicAll';box.className='musicAll';
    ['Asia Drama Theme','Raat Ki Baatein','Tera Saath','Dil Se','Apni Gully'].forEach(function(t,i){
      var row=document.createElement('div');row.className='notice music';row.innerHTML='<div class="song-art" style="width:60px;height:60px;border-radius:12px;background:#202129;display:grid;place-items:center;color:'+RED+';font-size:23px">♫</div><div><b>'+t+'</b><div class="small">Asia Drama Originals • Track '+(i+1)+'</div></div><button class="play" type="button">▶</button>';
      row.querySelector('button').onclick=function(){toast(t+' — published audio will play here')};box.appendChild(row);
    });panel.appendChild(box);
  }

  function correctTabClicks(){
    document.querySelectorAll('.tabs .tab').forEach(function(b){
      if(b.dataset.asiaUxBound)return;b.dataset.asiaUxBound='1';
      b.addEventListener('click',function(){setTimeout(function(){setTopTab(b.textContent.trim())},30)},true);
    });
  }

  async function roleUI(){
    try{
      var badge=document.getElementById('asiaRoleBadge');if(!badge){badge=document.createElement('span');badge.id='asiaRoleBadge';badge.className='roleBadge';var brand=document.querySelector('.top .brand');if(brand)brand.appendChild(badge)}
      if(!window.user||!window.supabase){badge.textContent='Guest';badge.className='roleBadge';document.getElementById('adminButton')?.classList.add('hidden');return}
      var r=await window.supabase.from('admin_roles').select('role').eq('user_id',window.user.id).limit(1).maybeSingle();
      var admin=!!r.data;badge.textContent=admin?'ADMIN':'MEMBER';badge.className='roleBadge'+(admin?' admin':'');
      document.getElementById('adminButton')?.classList.toggle('hidden',!admin);
      if(!admin)document.getElementById('asiaAdminCMS')?.classList.remove('on');
    }catch(e){document.getElementById('adminButton')?.classList.add('hidden')}
  }

  var oldGo=window.go;
  window.go=function(id,nav,btn){
    var r=typeof oldGo==='function'?oldGo.apply(window,arguments):undefined;
    setTimeout(function(){
      var map={home:'For You',series:'Series',movies:'Movies',shorts:'Shorts',music:'Music',community:'For You',profile:'For You',admin:'For You'};
      if(map[id])setTopTab(map[id]);
      refreshHeader();refreshNav();correctTabClicks();hardenImages();roleUI();
    },40);return r;
  };

  document.addEventListener('DOMContentLoaded',function(){
    refreshHeader();refreshNav();addMicroTab();addMicroHome();addMusicFallback();correctTabClicks();hardenImages();setTimeout(roleUI,500);
  });
  window.addEventListener('load',function(){addMicroTab();addMicroHome();addMusicFallback();correctTabClicks();hardenImages();roleUI()});
  setInterval(function(){hardenImages();roleUI()},5000);
})();
