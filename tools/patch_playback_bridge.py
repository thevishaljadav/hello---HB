from pathlib import Path

p = Path('app/src/main/java/com/hellobaroda/navratri/MainActivity2.java')
s = p.read_text(encoding='utf-8')
old = '''+ "window.onPlayPurchaseVerified=function(id){const c=typeof catalog!=='undefined'?catalog:[];const e=c.flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(x=>x.id===id);if(e&&e.video_url&&window.Android){Android.playVideo(e.title||'Asia Drama',e.video_url,0);}};"'''
new = '''+ "window.onPlayPurchaseVerified=async function(id){try{const s=await window.supabase.auth.getSession();const a=s.data.session?.access_token;if(!a)throw new Error('Please sign in again.');const r=await fetch('" + API_BASE + "/playback-url?episode_id='+encodeURIComponent(id),{headers:{Authorization:'Bearer '+a}});const j=await r.json();if(!r.ok)throw new Error(j.error||'Playback unavailable');if(window.Android)Android.playVideo(j.title||'Asia Drama',j.url,0);}catch(e){window.toast&&window.toast(e.message||'Playback unavailable');}};"'''
if old not in s:
    raise SystemExit('purchase verification bridge target not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('secure Play purchase playback bridge patched')
