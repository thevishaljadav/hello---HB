from pathlib import Path

p = Path('app/src/main/java/com/hellobaroda/navratri/MainActivity2.java')
s = p.read_text()

old = '''                + "if(window.playEpisode&&!window.__playWrapped){window.__playWrapped=true;const original=window.playEpisode;window.playEpisode=function(id,title,url,paid){if(paid){if(!window.Android){window.toast&&window.toast('Google Play is unavailable');return;}const ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===id);Android.buy(ep?.play_product_id||id);return;}if(url&&window.Android){Android.playVideo(title||'Asia Drama',url,0);return;}return original.apply(this,arguments);};}"\n'''

new = '''                + "window.__asiaSecurePlaybackBridge=async function(id,title,paid){try{if(paid){if(!window.Android){window.toast&&window.toast('Google Play is unavailable');return;}const ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===id);Android.buy(ep?.play_product_id||id);return;}const s=await window.supabase.auth.getSession();const a=s.data.session?.access_token;if(!a)throw new Error('Please sign in to watch.');const r=await fetch('" + API_BASE + "/playback-url?episode_id='+encodeURIComponent(id),{headers:{Authorization:'Bearer '+a},cache:'no-store'});const j=await r.json();if(!r.ok)throw new Error(j.error||'Playback unavailable');if(window.Android)Android.playVideo(j.title||title||'Asia Drama',j.url,0);}catch(e){window.toast&&window.toast(e.message||'Playback unavailable');}};"\n"
                + "if(window.playEpisode&&!window.__playWrapped){window.__playWrapped=true;window.playEpisode=function(id,title,url,paid){return window.__asiaSecurePlaybackBridge(id,title,!!paid);};}"\n'''

if old in s:
    s = s.replace(old, new, 1)
elif 'window.__asiaSecurePlaybackBridge=' not in s:
    raise SystemExit('secure playback bridge target not found')

# Remove the accidental standalone quote left by older generated versions.
s = s.replace('                + "\\"\n', '')

p.write_text(s)
