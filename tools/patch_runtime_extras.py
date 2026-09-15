from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text()

ux = r'''<style id="asia-ux-runtime-v2">
:root{--safe-bottom:env(safe-area-inset-bottom,0px)}
body{padding-bottom:calc(82px + var(--safe-bottom));overflow-x:hidden}
.nav{bottom:0;padding-bottom:var(--safe-bottom);height:calc(76px + var(--safe-bottom))}
.nav button,.icon,.round,.tab,.primary,.secondary,.danger,.link,.setting,.play,.close{touch-action:manipulation;-webkit-tap-highlight-color:transparent;user-select:none}
.nav .plus{flex:0 0 54px;width:54px;height:54px;min-width:54px;min-height:54px;margin:0 2px}
.player{padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)}
.playerTop{top:env(safe-area-inset-top);padding-left:max(12px,env(safe-area-inset-left));padding-right:max(12px,env(safe-area-inset-right))}
.player video{width:100%;height:100%;object-fit:contain;max-width:100vw;max-height:100vh}
#asiaAudio{display:block;width:100%;margin:10px 0;border-radius:14px}
.reels{height:calc(100vh - 142px);min-height:520px;overflow:auto;scroll-snap-type:y mandatory;background:#000}
.reelMedia{height:100%;min-height:520px;position:relative;scroll-snap-align:start;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden}
.reelMedia video{width:100%;height:100%;object-fit:cover;background:#000}
.reelMedia .reelOverlay{position:absolute;left:14px;right:14px;bottom:18px;z-index:3;display:flex;justify-content:space-between;align-items:flex-end;gap:12px;text-shadow:0 2px 8px #000}
.reelMedia .reelActions{display:flex;flex-direction:column;gap:8px;align-items:center}
.reelMedia .reelActions button{width:48px;height:48px;border-radius:50%;background:rgba(10,10,12,.7);color:#fff}
.media-empty{margin:15px;padding:24px;border:1px dashed #3a3c45;border-radius:17px;text-align:center;color:#a5a7b0}
@media(min-width:700px){.app{max-width:900px}.nav{width:min(900px,100%)}.sheet{max-width:900px}.grid{grid-template-columns:repeat(4,minmax(0,1fr))}.row .card{flex-basis:190px}}
@media(max-width:360px){.nav button{font-size:9px}.hero{min-height:460px}.hero h1{font-size:29px}}
</style>'''

list_runtime = r'''<script id="asia-list-runtime-v2">
(function(){
 function read(){try{return JSON.parse(localStorage.getItem('asiaDramaList')||'[]')}catch(e){return []}}
 function write(v){localStorage.setItem('asiaDramaList',JSON.stringify(v))}
 window.toggleList=function(id,title){var a=read(),i=a.findIndex(function(x){return x.id===id});if(i>=0){a.splice(i,1);toast('Removed from My List')}else{a.push({id:id,title:title});toast('Added to My List')}write(a);if(window.renderList)renderList()}
 window.renderList=function(){var e=document.getElementById('listItems');if(!e)return;var a=read();e.innerHTML=a.length?a.map(function(x){return '<div class="notice"><b>'+safe(x.title)+'</b><button class="secondary" type="button" style="float:right" onclick="toggleList(\''+x.id+'\',\''+safe(x.title).replace(/'/g,'&#39;')+'\')">Remove</button></div>'}).join(''):'<div class="empty">Your list is empty.</div>'}
})();
</script>'''

community_runtime = r'''<script id="asia-community-runtime-v2">
(function(){
 window.loadCommunity=async function(){var box=document.getElementById('communityList');if(!box)return;var r=await supabase.from('posts').select('id,caption,created_at,user_id').order('created_at',{ascending:false}).limit(30);if(r.error){box.innerHTML='<div class="empty">Community is temporarily unavailable.</div>';return}box.innerHTML=(r.data||[]).map(function(p){return '<article class="post"><b>Community member</b><p>'+safe(p.caption||'')+'</p><div class="small">'+new Date(p.created_at).toLocaleString()+'</div></article>'}).join('')||'<div class="empty">No community posts yet.</div>'}
 window.createPost=async function(){if(!user)return openSheet('auth');var el=document.getElementById('postText'),text=(el?.value||'').trim();if(!text)return toast('Write something first');if(text.length>1000)return toast('Keep your post under 1000 characters');var r=await supabase.from('posts').insert({user_id:user.id,caption:text,media_type:'text'}).select('id').single();if(r.error)return toast(r.error.message||'Post could not be published');closeSheet();toast('Post published');loadCommunity()}
 loadCommunity();
})();
</script>'''

media_runtime = r'''<script id="asia-media-catalog-runtime-v2">
(function(){
 function episodes(){return (typeof catalog!=='undefined'?catalog:[]).flatMap(function(x){return (x.seasons||[]).flatMap(function(s){return s.episodes||[]})})}
 function renderMusic(){var host=document.getElementById('music');if(!host)return;var list=host.querySelector('#asiaMusicList');if(!list)return;var rows=episodes().filter(function(e){return e.content_type==='music'&&e.video_url});if(!rows.length){list.innerHTML='<div class="media-empty">No published music yet.</div>';return}list.innerHTML=rows.map(function(e){return '<div class="notice music"><img src="'+safe(e.thumbnail_url||demo[0].poster_url)+'" alt=""><div><b>'+safe(e.title)+'</b><div class="small">'+Math.round((e.duration_seconds||0)/60)+' min</div></div><button class="play" type="button" onclick="playMusic(\''+e.id+'\')">▶</button></div>'}).join('')}
 window.playMusic=function(id){var e=episodes().find(function(x){return x.id===id});var a=document.getElementById('asiaAudio');if(!e||!a)return;document.getElementById('asiaAudioTitle').textContent=e.title||'Asia Drama Music';a.src=e.video_url;a.load();a.play().catch(function(){toast('Tap play to start audio')})}
 function renderShorts(){var box=document.querySelector('#shorts .reels');if(!box)return;var rows=episodes().filter(function(e){return (e.content_type==='short'||e.content_type==='shorts')&&e.video_url});if(!rows.length)return;box.innerHTML=rows.map(function(e){return '<article class="reelMedia"><video src="'+safe(e.video_url)+'" poster="'+safe(e.thumbnail_url||'')+'" playsinline muted loop preload="metadata"></video><div class="reelOverlay"><div><span class="pill">SHORT</span><h2 style="margin:8px 0 3px">'+safe(e.title)+'</h2><div class="small">Tap to play • Sound starts muted</div></div><div class="reelActions"><button type="button" aria-label="Like" onclick="toast(\'Liked\')">♥</button><button type="button" aria-label="Sound" onclick="toggleShortSound(this)">🔇</button><button type="button" aria-label="Share" onclick="shareApp()">⌁</button></div></div></article>'}).join('');var vids=Array.from(box.querySelectorAll('video'));var io=new IntersectionObserver(function(entries){entries.forEach(function(x){var v=x.target;if(x.isIntersecting){v.play().catch(function(){})}else{v.pause()}})},{threshold:.7});vids.forEach(function(v){io.observe(v);v.addEventListener('click',function(){if(v.paused)v.play().catch(function(){});else v.pause()})})}
 window.toggleShortSound=function(btn){var v=btn.closest('.reelMedia').querySelector('video');v.muted=!v.muted;btn.textContent=v.muted?'🔇':'🔊';if(v.paused)v.play().catch(function(){})}
 function renderAll(){if(typeof catalog==='undefined'||!catalog.length)return;renderMusic();renderShorts()}
 var tries=0;var timer=setInterval(function(){tries++;renderAll();if(tries>20||((typeof catalog!=='undefined')&&catalog.length))clearInterval(timer)},500);renderAll();
})();
</script>'''

admin_runtime = r'''<script id="asia-admin-runtime-v2">
(function(){
 window.loadAdmin=async function(){if(!user)return openSheet('auth');var role=await supabase.from('admin_roles').select('role').eq('user_id',user.id).limit(1).maybeSingle();if(!role.data)return toast('Admin access required');var root=document.getElementById('adminSeries');if(!root)return;var sr=(await supabase.from('series').select('id,title,status,language').order('created_at',{ascending:false})).data||[];var ss=(await supabase.from('seasons').select('id,series_id,season_number,title').order('season_number')).data||[];root.innerHTML='<div class="panel"><b>Content manager</b><p class="small">Create metadata and publish only licensed HTTPS media.</p></div><div class="panel"><h3>Add series</h3><input id="admTitle" class="field" placeholder="Series title"><input id="admPoster" class="field" placeholder="Poster HTTPS URL"><input id="admLang" class="field" placeholder="Language"><textarea id="admDesc" class="field area" placeholder="Description"></textarea><button class="primary" type="button" onclick="adminAddSeries()">Create series</button></div><div class="panel"><h3>Add season</h3><select id="admSeries" class="field">'+sr.map(function(x){return '<option value="'+x.id+'">'+safe(x.title)+'</option>'}).join('')+'</select><input id="admSeasonNo" class="field" type="number" min="1" value="1"><button class="primary" type="button" onclick="adminAddSeason()">Create season</button></div><div class="panel"><h3>Add media</h3><select id="admSeason" class="field">'+ss.map(function(x){var a=sr.find(function(z){return z.id===x.series_id});return '<option value="'+x.id+'">'+safe(a?.title||'Series')+' • S'+x.season_number+'</option>'}).join('')+'</select><input id="admEpNo" class="field" type="number" min="1" value="1"><input id="admEpTitle" class="field" placeholder="Title"><input id="admMediaUrl" class="field" placeholder="Video/audio HTTPS URL"><input id="admThumb" class="field" placeholder="Thumbnail HTTPS URL"><select id="admType" class="field"><option value="episode">Episode</option><option value="short">Short</option><option value="music">Music</option></select><select id="admAccess" class="field"><option value="free">Free</option><option value="pay_per_episode">Pay per episode</option><option value="subscription_only">Subscription only</option><option value="coming_soon">Coming soon</option></select><input id="admPrice" class="field" type="number" min="0" placeholder="Price in paise"><input id="admPlayProduct" class="field" placeholder="Google Play product ID"><select id="admStatus" class="field"><option value="draft">Draft</option><option value="published">Published</option></select><button class="primary" type="button" onclick="adminAddMedia()">Create media</button></div><div class="panel"><b>Catalogue</b>'+sr.map(function(x){return '<div class="notice"><b>'+safe(x.title)+'</b><div class="small">'+safe(x.status)+' • '+safe(x.language||'')+'</div></div>'}).join('')+'</div>'}
 window.adminAddSeries=async function(){var r=await supabase.from('series').insert({title:document.getElementById('admTitle').value.trim(),poster_url:document.getElementById('admPoster').value.trim()||null,language:document.getElementById('admLang').value.trim()||null,description:document.getElementById('admDesc').value.trim()||null,status:'draft',created_by:user.id}).select('id').single();if(r.error)return toast(r.error.message);toast('Series created as draft');loadAdmin()}
 window.adminAddSeason=async function(){var r=await supabase.from('seasons').insert({series_id:document.getElementById('admSeries').value,season_number:Number(document.getElementById('admSeasonNo').value)}).select('id').single();if(r.error)return toast(r.error.message);toast('Season created');loadAdmin()}
 window.adminAddMedia=async function(){var r=await supabase.from('episodes').insert({season_id:document.getElementById('admSeason').value,episode_number:Number(document.getElementById('admEpNo').value),title:document.getElementById('admEpTitle').value.trim(),video_url:document.getElementById('admMediaUrl').value.trim()||null,thumbnail_url:document.getElementById('admThumb').value.trim()||null,content_type:document.getElementById('admType').value,access_type:document.getElementById('admAccess').value,price_paise:Number(document.getElementById('admPrice').value)||null,play_product_id:document.getElementById('admPlayProduct').value.trim()||null,status:document.getElementById('admStatus').value}).select('id').single();if(r.error)return toast(r.error.message);toast('Media created');loadAdmin()}
})();
</script>'''

# Add an actual audio element to the Music screen without disturbing the existing layout.
audio_markup = '<div class="panel"><b id="asiaAudioTitle">Asia Drama Music</b><audio id="asiaAudio" controls preload="metadata" playsinline></audio><div id="asiaMusicList"></div></div>'
if 'id="asiaAudio"' not in s:
    s = s.replace('<div class="empty">Music catalog is managed by authorized content staff.</div></main>', audio_markup + '</main>')

# Each patch is independently idempotent so a previous partial build can never suppress later fixes.
for marker, payload in [
    ('asia-ux-runtime-v2', ux),
    ('asia-list-runtime-v2', list_runtime),
    ('asia-community-runtime-v2', community_runtime),
    ('asia-media-catalog-runtime-v2', media_runtime),
    ('asia-admin-runtime-v2', admin_runtime),
]:
    if marker not in s:
        s = s.replace('</body>', payload + '</body>')

html.write_text(s)
