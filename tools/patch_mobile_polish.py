from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text()
marker = 'asia-mobile-polish-v1'
if marker in s:
    raise SystemExit(0)

css = r'''<style id="asia-mobile-polish-v1">
/* Mobile polish: larger, clearer controls and a real profile surface. */
.top{min-height:70px;padding:11px 14px}
.brand img{width:46px;height:46px;border-radius:13px;flex:0 0 46px}
.brand b{font-size:23px}.brand span{font-size:21px}
.actions{gap:8px}.actions .icon{width:52px;height:52px;min-width:52px;border-radius:50%;display:grid;place-items:center;padding:0;background:#17181e;border:1px solid #24262d;font-size:0}
.actions .icon svg{width:23px;height:23px;stroke:currentColor;stroke-width:2.2;fill:none}
.actions .icon.profileTrigger{overflow:hidden;padding:3px}
.actions .icon.profileTrigger img{width:100%;height:100%;border-radius:50%;object-fit:cover}
.tabs{top:70px;min-height:66px;padding:9px 13px;gap:9px}
.tabs .tab{min-height:48px;padding:0 18px;border-radius:24px;font-size:16px}
.nav{height:82px;padding:4px 5px calc(4px + env(safe-area-inset-bottom));box-sizing:border-box}
.nav button{min-height:62px;font-size:11px;font-weight:700;gap:4px}
.nav .navIcon{width:27px;height:27px;display:grid;place-items:center}
.nav .navIcon svg{width:25px;height:25px;stroke:currentColor;stroke-width:2;fill:none}
.nav button.on .navIcon svg{stroke-width:2.4}
.nav .plus{width:60px;height:60px;min-width:60px;font-size:30px;margin:0 4px;box-shadow:0 8px 24px rgba(255,41,66,.22)}
.profileHero{display:flex;align-items:center;gap:14px;margin:10px 15px 14px;padding:18px;background:linear-gradient(145deg,#191a20,#111217);border:1px solid var(--line);border-radius:20px}
.profileAvatar{width:76px;height:76px;min-width:76px;border-radius:50%;object-fit:cover;background:#272932;border:2px solid #3b3d46}
.profileIdentity{min-width:0;flex:1}.profileIdentity h2{margin:0 0 4px;font-size:21px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.profileIdentity p{margin:0;color:var(--muted);font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.profileActions{display:flex;gap:8px;margin-top:11px;flex-wrap:wrap}.profileActions button{min-height:44px}
.avatarFile{display:none}.profileEdit{margin:0 15px 12px;padding:14px;background:#121318;border:1px solid var(--line);border-radius:17px}.profileEdit[hidden]{display:none}.profileEdit .field{margin:5px 0}.profileEditRow{display:flex;gap:8px;flex-wrap:wrap}.profileEditRow button{flex:1;min-width:120px}
@media(max-width:420px){.actions .icon{width:48px;height:48px;min-width:48px}.brand img{width:44px;height:44px;flex-basis:44px}.brand b{font-size:21px}.brand span{font-size:19px}.tabs .tab{padding:0 16px}.nav button{font-size:10px}.nav .navIcon{width:25px;height:25px}}
</style>'''

js = r'''<script id="asia-mobile-polish-v1-js">
(function(){
  var icons={
    search:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"></circle><path d="m16 16 4 4"></path></svg>',
    bell:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 9a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"></path><path d="M10 21h4"></path></svg>',
    user:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"></circle><path d="M5 20c.8-4 3-6 7-6s6.2 2 7 6"></path></svg>',
    home:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3.5 10 8.5-7 8.5 7v10a1 1 0 0 1-1 1h-15a1 1 0 0 1-1-1z"></path><path d="M9 21v-6h6v6"></path></svg>',
    explore:'<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="2"></rect><path d="M8 8h8M8 12h8M8 16h5"></path></svg>',
    community:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 10a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM16 11a2.5 2.5 0 1 0 0-5"></path><path d="M2.8 20c.5-4 2.3-6 5.2-6s4.7 2 5.2 6M14 14c3.8-.2 5.8 1.8 6.3 6"></path></svg>',
    profile:'<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="3.5"></circle><path d="M5 20c.8-4 3-6 7-6s6.2 2 7 6"></path></svg>'
  };
  function setHeaderIcons(){
    var a=document.querySelectorAll('.actions .icon');
    if(a[0])a[0].innerHTML=icons.search;
    if(a[1])a[1].innerHTML=icons.bell;
    if(a[2]){a[2].classList.add('profileTrigger');a[2].innerHTML=icons.profile}
    try{
      if(typeof supabase==='undefined')return;
      supabase.auth.getUser().then(function(r){
        var u=r&&r.data&&r.data.user;if(!u)return;
        var url=(u.user_metadata&&u.user_metadata.avatar_url)||'';
        if(url&&a[2])a[2].innerHTML='<img src="'+String(url).replace(/"/g,'&quot;')+'" alt="Profile photo">';
      }).catch(function(){});
    }catch(e){}
  }
  function setNavIcons(){
    var nav=document.querySelectorAll('.nav button');
    var map=[icons.home,icons.explore,null,icons.community,icons.profile];
    nav.forEach(function(b,i){
      if(i===2)return;
      var label=(b.textContent||'').trim().replace(/^\s+|\s+$/g,'');
      var text=label||(['Home','Explore','','Community','Profile'][i]);
      b.innerHTML='<span class="navIcon">'+(map[i]||icons.user)+'</span><span class="navLabel">'+text+'</span>';
    });
  }
  function profileImage(u){
    return (u&&u.user_metadata&&u.user_metadata.avatar_url)||'';
  }
  function ensureProfileSurface(){
    var p=document.getElementById('profile');if(!p)return;
    var old=p.querySelector('#asiaProfileHero');
    if(old)return;
    var wrap=document.createElement('div');wrap.innerHTML='<section class="profileHero" id="asiaProfileHero"><img class="profileAvatar" id="asiaProfileAvatar" src="" alt="Profile photo"><div class="profileIdentity"><h2 id="asiaProfileName">Welcome to Asia Drama</h2><p id="asiaProfileEmail">Sign in to create your profile</p><div class="profileActions"><button class="secondary" id="asiaChangePhoto">Change photo</button><button class="secondary" id="asiaEditProfile">Edit profile</button></div></div><input class="avatarFile" id="asiaAvatarFile" type="file" accept="image/png,image/jpeg,image/webp"></section><section class="profileEdit" id="asiaProfileEdit" hidden><input class="field" id="asiaDisplayName" maxlength="60" placeholder="Display name"><div class="profileEditRow"><button class="primary" id="asiaSaveProfile">Save profile</button><button class="secondary" id="asiaCancelProfile">Cancel</button></div></section>';
    p.prepend(wrap.firstElementChild);
    p.insertBefore(wrap.lastElementChild,p.children[1]||null);
    bindProfile();loadProfile();
  }
  function bindProfile(){
    var change=document.getElementById('asiaChangePhoto'),file=document.getElementById('asiaAvatarFile'),edit=document.getElementById('asiaEditProfile'),box=document.getElementById('asiaProfileEdit'),cancel=document.getElementById('asiaCancelProfile'),save=document.getElementById('asiaSaveProfile');
    if(change&&file)change.onclick=function(){file.click()};
    if(edit&&box)edit.onclick=function(){box.hidden=false};
    if(cancel&&box)cancel.onclick=function(){box.hidden=true};
    if(file)file.onchange=function(){if(file.files&&file.files[0])uploadAvatar(file.files[0])};
    if(save)save.onclick=saveProfile;
  }
  function loadProfile(){
    try{
      if(typeof supabase==='undefined')return;
      supabase.auth.getUser().then(function(r){
        var u=r&&r.data&&r.data.user;if(!u)return;
        var m=u.user_metadata||{},name=m.display_name||m.full_name||u.email&&u.email.split('@')[0]||'Asia Drama User',url=profileImage(u);
        var n=document.getElementById('asiaProfileName'),e=document.getElementById('asiaProfileEmail'),a=document.getElementById('asiaProfileAvatar'),d=document.getElementById('asiaDisplayName');
        if(n)n.textContent=name;if(e)e.textContent=u.email||'Signed in';if(d)d.value=name;
        if(a){a.src=url||'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Crect width=%22100%22 height=%22100%22 fill=%22%23202229%22/%3E%3Ccircle cx=%2250%22 cy=%2238%22 r=%2218%22 fill=%22%23aaa%22/%3E%3Cpath d=%22M20 88c4-22 18-32 30-32s26 10 30 32%22 fill=%22%23aaa%22/%3E%3C/svg%3E';}
      }).catch(function(){});
    }catch(e){}
  }
  function saveProfile(){
    var input=document.getElementById('asiaDisplayName'),box=document.getElementById('asiaProfileEdit');if(!input)return;
    try{if(typeof supabase==='undefined')return toast('Sign in to edit your profile');supabase.auth.updateUser({data:{display_name:input.value.trim()||'Asia Drama User'}}).then(function(r){if(r.error)throw r.error;toast('Profile updated');if(box)box.hidden=true;loadProfile();setHeaderIcons()}).catch(function(){toast('Could not update profile')})}catch(e){toast('Could not update profile')}
  }
  function uploadAvatar(file){
    try{if(typeof supabase==='undefined')return toast('Sign in to add a profile photo');if(file.size>5*1024*1024)return toast('Photo must be under 5 MB');supabase.auth.getUser().then(function(r){var u=r&&r.data&&r.data.user;if(!u)throw new Error('auth');var ext=(file.name.split('.').pop()||'jpg').toLowerCase().replace(/[^a-z0-9]/g,'');var path='avatars/'+u.id+'.'+(ext||'jpg');return supabase.storage.from('asia-posters').upload(path,file,{upsert:true,contentType:file.type||'image/jpeg'}).then(function(x){if(x.error)throw x.error;var g=supabase.storage.from('asia-posters').getPublicUrl(path);var url=g&&g.data&&g.data.publicUrl;if(!url)throw new Error('url');return supabase.auth.updateUser({data:{avatar_url:url}})}).then(function(x){if(x.error)throw x.error;toast('Profile photo updated');loadProfile();setHeaderIcons()}).catch(function(){toast('Could not upload photo')})}).catch(function(){toast('Could not update photo')})}catch(e){toast('Could not update photo')}
  }
  function boot(){setHeaderIcons();setNavIcons();ensureProfileSurface();setTimeout(ensureProfileSurface,700)}
  document.addEventListener('DOMContentLoaded',boot);
  var oldGo=window.go;window.go=function(){var args=arguments;var r=oldGo&&oldGo.apply(window,args);setTimeout(function(){setHeaderIcons();setNavIcons();ensureProfileSurface()},80);return r};
})();
</script>'''

s=s.replace('</head>',css+'</head>')
s=s.replace('</body>',js+'</body>')
html.write_text(s)
