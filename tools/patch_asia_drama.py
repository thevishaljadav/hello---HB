from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "app/src/main/assets/index.html"
JAVA = ROOT / "app/src/main/java/com/hellobaroda/navratri/MainActivity.java"
BRIDGE = ROOT / "app/src/main/java/com/hellobaroda/navratri/MainActivity2.java"

# Preserve the existing legacy Java compile fix.
if JAVA.exists():
    text = JAVA.read_text()
    text = text.replace(
        'rowTitle("Popular Garba Grounds","See all",()->grounds())',
        'rowTitle("Popular Garba Grounds","See all",v->grounds())',
    )
    text = text.replace(
        'rowTitle("Community moments","View trending",()->trending())',
        'rowTitle("Community moments","View trending",v->trending())',
    )
    JAVA.write_text(text)

# Keep the Android purchase bridge compatible with the current catalog declaration.
if BRIDGE.exists():
    text = BRIDGE.read_text()
    text = text.replace(
        "const ep=window.catalog?.flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===id);",
        "const ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===id);",
    )
    BRIDGE.write_text(text)

s = HTML.read_text()

# Clean historical duplicate patches so the source remains deterministic across builds.
razor = '<script src="https://checkout.razorpay.com/v1/checkout.js"></script>'
s = s.replace(razor, '')
supa = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
s = s.replace(supa, supa + razor, 1)
s = re.sub(r'\s*<style id="asia-interaction-fix">.*?</script>', '', s, flags=re.S)
s = re.sub(r'\s*<style id="asia-runtime-hardening">.*?</script>', '', s, flags=re.S)

# Fix the old web checkout typo left by the first prototype.
s = s.replace('await sb.auth.getSession()', 'await supabase.auth.getSession()')

playback = r'''<script id="asia-media-runtime">
async function startRazorpay(episodeId,title){
  try{
    const session=await supabase.auth.getSession();
    const token=session.data.session?.access_token;
    if(!token)return openSheet('auth');
    const r=await fetch(SUPA_URL+'/functions/v1/create-razorpay-order',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token,'apikey':SUPA_KEY},body:JSON.stringify({episode_id:episodeId})});
    const order=await r.json();
    if(!r.ok)throw new Error(order.error||'Unable to create payment order');
    if(!window.Razorpay)throw new Error('Payment checkout is unavailable');
    const options={key:order.key_id,amount:order.amount,currency:order.currency,name:'Asia Drama',description:title||'Premium episode',order_id:order.order_id,theme:{color:'#ff2942'},handler:async function(response){
      const vr=await fetch(SUPA_URL+'/functions/v1/verify-razorpay-payment',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token,'apikey':SUPA_KEY},body:JSON.stringify({...response,episode_id:episodeId})});
      const result=await vr.json();
      if(!vr.ok||!result.verified)throw new Error(result.error||'Payment verification failed');
      toast('Payment successful — episode unlocked');
      const ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===episodeId);
      if(ep?.video_url)playEpisode(episodeId,ep.title,ep.video_url,false);else toast('Payment verified. Video will be available when published.');
    },modal:{ondismiss:function(){toast('Payment cancelled')}}};
    new Razorpay(options).open();
  }catch(e){toast(e.message||'Payment could not be started')}
}

function mediaMessage(message){
  var old=document.getElementById('mediaStatus');
  if(!old){old=document.createElement('div');old.id='mediaStatus';old.className='status';var p=document.getElementById('player');if(p)p.appendChild(old)}
  old.textContent=message;old.style.display=message?'block':'none';
}

async function playEpisode(id,title,url,paid){
  if(paid){if(!user)return openSheet('auth');return startRazorpay(id,title)}
  if(!url){toast('This episode has no published video yet');return}
  currentEpisodeId=id;lastProgressSent=-1;closeSheet();
  document.getElementById('playerTitle').textContent=title||'Asia Drama';
  var v=document.getElementById('video');
  v.pause();v.removeAttribute('src');v.load();v.src=url;v.preload='metadata';v.controls=true;v.playsInline=true;
  document.getElementById('player').classList.add('on');mediaMessage('Loading video…');
  v.onloadedmetadata=function(){mediaMessage('')};
  v.onplaying=function(){mediaMessage('')};
  v.onwaiting=function(){mediaMessage('Buffering…')};
  v.onstalled=function(){mediaMessage('Connection is slow — buffering…')};
  v.onerror=function(){mediaMessage('Video could not be loaded. Check your connection or try again.')};
  v.ontimeupdate=function(){if(user){var p=Math.floor(v.currentTime);if(p>0&&p%10===0&&p!==lastProgressSent){lastProgressSent=p;saveProgress(id,p,false)}}};
  v.onended=function(){saveProgress(id,Math.floor(v.duration||v.currentTime),true);mediaMessage('')};
  v.play().catch(function(){toast('Tap play to start the video')});
}

function resumeEpisode(id){
  var h=history.find(function(x){return x.episode_id===id});
  var ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(function(x){return (x.seasons||[]).flatMap(function(s){return s.episodes||[]})}).find(function(e){return e.id===id});
  if(!ep||!ep.video_url)return toast('This episode is not available to resume yet');
  playEpisode(id,ep.title,ep.video_url,false);
  setTimeout(function(){var v=document.getElementById('video');if(h&&!h.completed&&h.position_seconds>0){var seek=function(){try{v.currentTime=Math.min(h.position_seconds,Math.max(0,(v.duration||h.position_seconds)-1))}catch(e){}};if(v.readyState>=1)seek();else v.addEventListener('loadedmetadata',seek,{once:true})}},100);
}

function closePlayer(){
  var v=document.getElementById('video');
  if(user&&currentEpisodeId&&v.currentTime>0)saveProgress(currentEpisodeId,Math.floor(v.currentTime),false);
  v.pause();v.removeAttribute('src');v.load();document.getElementById('player').classList.remove('on');currentEpisodeId='';lastProgressSent=-1;mediaMessage('');
}

async function loadHistory(){
  if(!user){document.getElementById('continueRow').innerHTML='<div class="empty">Sign in to sync your watch progress.</div>';return}
  const {data,error}=await supabase.from('watch_history').select('episode_id,position_seconds,completed,last_watched_at,episodes(title,thumbnail_url,duration_seconds)').order('last_watched_at',{ascending:false}).limit(12);
  if(error){document.getElementById('continueRow').innerHTML='<div class="empty">Watch history is temporarily unavailable.</div>';return}
  history=data||[];
  document.getElementById('continueRow').innerHTML=history.map(function(h){return '<article class="card" onclick="resumeEpisode(\''+h.episode_id+'\')"><img src="'+safe(h.episodes?.thumbnail_url||demo[0].poster_url)+'" alt="'+safe(h.episodes?.title||'Episode')+'"><div class="info">'+safe(h.episodes?.title||'Episode')+'<small>'+(h.completed?'Completed':'Resume')+' • '+Math.floor((h.position_seconds||0)/60)+' min</small></div></article>'}).join('')||'<div class="empty">Nothing watched yet.</div>';
}
</script>'''

# Replace the entire old checkout/playback block. The old file has stable boundaries around renderHistory().
s = re.sub(
    r'async function startRazorpay\(episodeId,title\).*?function renderHistory\(\)',
    playback + '\nfunction renderHistory()',
    s,
    flags=re.S,
)

runtime = r'''<style id="asia-runtime-hardening">
:root{--safe-bottom:env(safe-area-inset-bottom,0px)}
body{padding-bottom:calc(82px + var(--safe-bottom));overflow-x:hidden}
.nav{bottom:0;padding-bottom:var(--safe-bottom);height:calc(76px + var(--safe-bottom))}
.nav button,.icon,.round,.tab,.primary,.secondary,.danger,.link,.setting,.play,.close{touch-action:manipulation;-webkit-tap-highlight-color:transparent;user-select:none}
.nav .plus{flex:0 0 54px;width:54px;height:54px;min-width:54px;min-height:54px;margin:0 2px;box-shadow:0 6px 20px rgba(255,41,66,.32)}
.player{padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.playerTop{top:env(safe-area-inset-top);height:64px;padding-left:max(12px,env(safe-area-inset-left));padding-right:max(12px,env(safe-area-inset-right))}
.player video{width:100%;height:100%;object-fit:contain;max-width:100vw;max-height:100vh}
#mediaStatus{position:absolute;z-index:4;left:50%;top:50%;transform:translate(-50%,-50%);margin:0 16px;text-align:center;display:none;background:rgba(0,0,0,.78);border:1px solid #34363e;color:#fff;max-width:90%}
@media (min-width:700px){.app{max-width:900px}.nav{width:min(900px,100%)}.sheet{max-width:900px}.grid{grid-template-columns:repeat(4,minmax(0,1fr))}.row .card{flex-basis:190px}.hero{min-height:560px}}
@media (max-width:360px){.brand b{font-size:18px}.actions{gap:2px}.icon{width:44px;height:44px}.hero{min-height:460px}.hero h1{font-size:29px}.grid{gap:8px;padding:0 10px}.card{height:205px}.nav button{font-size:9px}}
</style>
<script id="asia-ux-runtime">
(function(){
  function updateNetwork(){var online=navigator.onLine!==false;document.documentElement.dataset.network=online?'online':'offline';if(!online)toast('You are offline. Some content may be unavailable.')}
  window.addEventListener('online',function(){toast('Back online');updateNetwork()});window.addEventListener('offline',updateNetwork);updateNetwork();
  var v=document.getElementById('video');if(v){v.setAttribute('controls','controls');v.setAttribute('playsinline','');v.preload='metadata'}
  var plus=document.querySelector('.nav .plus');
  if(plus){plus.type='button';plus.setAttribute('aria-label','Quick actions');plus.onclick=function(e){e.preventDefault();e.stopPropagation();openSheet('search')}}
  document.querySelectorAll('.nav button,.actions button,.tab,.primary,.secondary,.danger,.setting,.play,.link,.round,.close').forEach(function(b){b.type='button'})
  document.addEventListener('visibilitychange',function(){var vv=document.getElementById('video');if(document.hidden&&user&&currentEpisodeId&&vv.currentTime)saveProgress(currentEpisodeId,Math.floor(vv.currentTime),false)})
})();
</script>'''

list_patch = r'''<script id="asia-list-runtime">
(function(){
  function getList(){try{return JSON.parse(localStorage.getItem('asiaDramaList')||'[]')}catch(e){return []}}
  function setList(v){localStorage.setItem('asiaDramaList',JSON.stringify(v))}
  window.toggleList=function(id,title){var a=getList();var i=a.findIndex(function(x){return x.id===id});if(i>=0){a.splice(i,1);toast('Removed from My List')}else{a.push({id:id,title:title});toast('Added to My List')}setList(a);renderList()}
  var originalOpenSeries=window.openSeries;
  window.openSeries=function(id){originalOpenSeries(id);var x=(typeof catalog!=='undefined'?catalog:[]).find(function(a){return a.id===id});if(!x)return;var sh=document.getElementById('sheet');if(!sh)return;var btn=document.createElement('button');btn.className='setting';btn.type='button';btn.innerHTML='<span>My List</span><b>＋</b>';btn.onclick=function(){toggleList(x.id,x.title)};var first=sh.querySelector('h2');if(first)first.insertAdjacentElement('afterend',btn)}
  window.renderList=function(){var e=document.getElementById('listItems');if(!e)return;var a=getList();e.innerHTML=a.length?a.map(function(x){return '<div class="notice"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><b>'+safe(x.title)+'</b><button class="secondary" type="button" onclick="toggleList(\''+x.id+'\',\''+safe(x.title).replace(/'/g,'&#39;')+'\')">Remove</button></div></div>'}).join(''):'<div class="empty">Your list is empty.</div>''}
})();
</script>'''

# Fix a defensive quote typo in the raw JS string above.
list_patch = list_patch.replace("</div>''}", "</div>'}")

product_patch = r'''<script id="asia-product-runtime">
(function(){
  window.loadCommunity=async function(){
    var box=document.getElementById('communityList');if(!box)return;
    var r=await supabase.from('posts').select('id,caption,created_at,user_id').order('created_at',{ascending:false}).limit(30);
    if(r.error){box.innerHTML='<div class="empty">Community is temporarily unavailable.</div>';return}
    var rows=r.data||[];box.innerHTML=rows.map(function(p){return '<article class="post"><b>Community member</b><p>'+safe(p.caption||'')+'</p><div class="small">'+new Date(p.created_at).toLocaleString()+'</div></article>'}).join('')||'<div class="empty">No community posts yet.</div>'
  }
  window.createPost=async function(){
    if(!user)return openSheet('auth');
    var el=document.getElementById('postText'),t=(el?.value||'').trim();if(!t)return toast('Write something first');
    if(t.length>1000)return toast('Keep your post under 1000 characters');
    var r=await supabase.from('posts').insert({user_id:user.id,caption:t,media_type:'text'}).select('id').single();
    if(r.error)return toast(r.error.message||'Post could not be published');
    closeSheet();toast('Post published');loadCommunity()
  }
  var baseBoot=window.boot;window.boot=async function(){await baseBoot();await loadCommunity()};loadCommunity()

  window.loadAdmin=async function(){
    if(!user)return openSheet('auth');
    var role=await supabase.from('admin_roles').select('role').eq('user_id',user.id).limit(1).maybeSingle();
    if(!role.data)return toast('Admin access required');
    var sh=document.getElementById('adminSeries');
    var series=(await supabase.from('series').select('id,title,status,language').order('created_at',{ascending:false})).data||[];
    var seasons=(await supabase.from('seasons').select('id,series_id,season_number,title').order('season_number')).data||[];
    var seriesOpts=series.map(function(x){return '<option value="'+x.id+'">'+safe(x.title)+'</option>'}).join('');
    var seasonOpts=seasons.map(function(x){var sn=series.find(function(s){return s.id===x.series_id});return '<option value="'+x.id+'">'+safe(sn?.title||'Series')+' • S'+x.season_number+'</option>'}).join('');
    sh.innerHTML='<div class="panel"><b>Content manager</b><p class="small">Create catalogue metadata and publish only licensed HTTPS media.</p></div>'+
      '<div class="panel"><h3>Add series</h3><input id="admSeriesTitle" class="field" placeholder="Series title"><input id="admSeriesPoster" class="field" placeholder="Poster HTTPS URL"><input id="admSeriesGenre" class="field" placeholder="Genre"><input id="admSeriesLang" class="field" placeholder="Language"><textarea id="admSeriesDesc" class="field area" placeholder="Description"></textarea><button class="primary" onclick="adminAddSeries()">Create series</button></div>'+
      '<div class="panel"><h3>Add season</h3><select id="admSeasonSeries" class="field">'+seriesOpts+'</select><input id="admSeasonNumber" class="field" type="number" min="1" value="1"><input id="admSeasonTitle" class="field" placeholder="Season title"><button class="primary" onclick="adminAddSeason()">Create season</button></div>'+
      '<div class="panel"><h3>Add episode</h3><select id="admEpisodeSeason" class="field">'+seasonOpts+'</select><input id="admEpisodeNumber" class="field" type="number" min="1" value="1"><input id="admEpisodeTitle" class="field" placeholder="Episode title"><input id="admEpisodeVideo" class="field" placeholder="Video HTTPS URL"><input id="admEpisodeThumb" class="field" placeholder="Thumbnail HTTPS URL"><select id="admEpisodeAccess" class="field"><option value="free">Free</option><option value="pay_per_episode">Pay per episode</option><option value="subscription_only">Subscription only</option><option value="coming_soon">Coming soon</option></select><input id="admEpisodePrice" class="field" type="number" min="0" placeholder="Price in paise"><input id="admEpisodePlayProduct" class="field" placeholder="Google Play product ID (optional)"><select id="admEpisodeStatus" class="field"><option value="draft">Draft</option><option value="published">Published</option></select><button class="primary" onclick="adminAddEpisode()">Create episode</button></div>'+
      '<div class="panel"><b>Current catalogue</b>'+series.map(function(x){return '<div class="notice"><b>'+safe(x.title)+'</b><div class="small">'+safe(x.status)+' • '+safe(x.language||'')+'</div></div>'}).join('')+'</div>'
  }
  window.adminAddSeries=async function(){var r=await supabase.from('series').insert({title:document.getElementById('admSeriesTitle').value.trim(),poster_url:document.getElementById('admSeriesPoster').value.trim()||null,genre:document.getElementById('admSeriesGenre').value.trim()||null,language:document.getElementById('admSeriesLang').value.trim()||null,description:document.getElementById('admSeriesDesc').value.trim()||null,status:'draft',created_by:user.id}).select('id').single();if(r.error)return toast(r.error.message);toast('Series created as draft');loadAdmin()}
  window.adminAddSeason=async function(){var r=await supabase.from('seasons').insert({series_id:document.getElementById('admSeasonSeries').value,season_number:Number(document.getElementById('admSeasonNumber').value),title:document.getElementById('admSeasonTitle').value.trim()||null}).select('id').single();if(r.error)return toast(r.error.message);toast('Season created');loadAdmin()}
  window.adminAddEpisode=async function(){var r=await supabase.from('episodes').insert({season_id:document.getElementById('admEpisodeSeason').value,episode_number:Number(document.getElementById('admEpisodeNumber').value),title:document.getElementById('admEpisodeTitle').value.trim(),video_url:document.getElementById('admEpisodeVideo').value.trim()||null,thumbnail_url:document.getElementById('admEpisodeThumb').value.trim()||null,access_type:document.getElementById('admEpisodeAccess').value,price_paise:Number(document.getElementById('admEpisodePrice').value)||null,play_product_id:document.getElementById('admEpisodePlayProduct').value.trim()||null,status:document.getElementById('admEpisodeStatus').value,content_type:'episode'}).select('id').single();if(r.error)return toast(r.error.message);toast('Episode created');loadAdmin()}
})();
</script>'''

# Add the runtime patches once, after the app's original script has defined its globals.
if 'id="asia-media-runtime"' not in s:
    s = s.replace('</body>', playback + runtime + list_patch + product_patch + '</body>')

HTML.write_text(s)
subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True)
