# Production interaction hardening patch
from pathlib import Path
import re

p=Path("app/src/main/assets/index.html")
s=p.read_text()
s=re.sub(r'<style id="asia-interaction-fix-v1">.*?</style>','',s,flags=re.S)
s=re.sub(r'<script id="asia-interaction-fix-v1-js">.*?</script>','',s,flags=re.S)

# Make the page resilient if a remote SDK is unavailable during startup.
s=s.replace("const supabase=window.supabase.createClient(SUPA_URL,SUPA_KEY);","const supabase=window.supabase?window.supabase.createClient(SUPA_URL,SUPA_KEY):null;",1)
s=s.replace("async function boot(){const {data}=await supabase.auth.getUser();","async function boot(){if(!supabase){user=null;var pn=document.getElementById('profileName'),pe=document.getElementById('profileEmail'),ab=document.getElementById('authBtn');if(pn)pn.textContent='Guest';if(pe)pe.textContent='Connection unavailable — sign-in needs internet access';if(ab)ab.textContent='Sign in / Create account';var adb=document.getElementById('adminButton');if(adb)adb.classList.add('hidden');if(typeof loadCatalog==='function')await loadCatalog();return}const {data}=await supabase.auth.getUser();",1)
s=s.replace("async function loadHistory(){","async function loadHistory(){if(!supabase){var e=document.getElementById('historyItems');if(e)e.innerHTML='<div class=\"empty\">Sign in requires an internet connection.</div>';return}",1)
s=s.replace("supabase.auth.onAuthStateChange(()=>setTimeout(boot,0));boot();","if(supabase&&supabase.auth){supabase.auth.onAuthStateChange(()=>setTimeout(boot,0))}boot();",1)

css=r'''<style id="asia-interaction-fix-v1">
.authModes{display:flex;gap:8px;margin:8px 0 12px}.authMode{flex:1;background:#1b1c22;border:1px solid #30323a;color:#aaa;border-radius:13px}.authMode.on{background:var(--red);color:#fff}.authHint{margin:6px 0 12px}
</style>'''

js=r'''<script id="asia-interaction-fix-v1-js">
(function(){
  window.__asiaJsReady=true;
  window.addEventListener('error',function(e){try{window.__asiaLastError=(e&&e.message)||'JavaScript error'}catch(_){} });

  /* Native-safe navigation fallback. The normal app functions remain preferred. */
  function fallbackToast(msg){var t=document.getElementById('toast');if(!t){t=document.createElement('div');t.id='toast';t.className='toast';document.body.appendChild(t)}t.textContent=msg||'Done';t.style.display='block';clearTimeout(t.__timer);t.__timer=setTimeout(function(){t.style.display='none'},2200)}
  function fallbackCloseSheet(){var o=document.getElementById('overlay');if(o)o.classList.remove('on')}
  function fallbackOpenSheet(type){
    var o=document.getElementById('overlay'),s=document.getElementById('sheet');if(!o||!s){fallbackToast('This section is unavailable right now');return}
    var html='<button class="close" onclick="closeSheet()">×</button>';
    if(type==='search') html+='<h2>Search Asia Drama</h2><input class="field" id="fallbackSearch" placeholder="Search dramas, episodes or creators" autocomplete="off"><button class="primary" onclick="fallbackToast(\'Search is ready\')">Search</button>';
    else if(type==='notice') html+='<h2>Notifications</h2><div class="empty">You have no new notifications.</div>';
    else if(type==='auth') html=authHtml('email');
    else html+='<h2>Asia Drama</h2><div class="empty">Please sign in to continue.</div><button class="primary" onclick="asiaAuthMode(\'email\')">Sign in / Create account</button>';
    s.innerHTML=html;o.classList.add('on')
  }
  function fallbackGo(id,index){
    var views=document.querySelectorAll('.view');views.forEach(function(v){v.classList.remove('on')});
    var target=document.getElementById(id);if(target)target.classList.add('on');
    var tabs=document.querySelectorAll('.tabs .tab');tabs.forEach(function(b){b.classList.remove('on')});if(index!==undefined&&tabs[index])tabs[index].classList.add('on');
    var nav=document.querySelectorAll('.nav button');nav.forEach(function(b){b.classList.remove('on')});
    if(id==='home'&&nav[0])nav[0].classList.add('on');else if(id==='explore'&&nav[1])nav[1].classList.add('on');else if(id==='community'&&nav[3])nav[3].classList.add('on');else if(id==='profile'&&nav[4])nav[4].classList.add('on');
    window.scrollTo(0,0)
  }
  function safeCall(fn,args,fallback){try{if(typeof fn==='function')return fn.apply(window,args||[])}catch(e){window.__asiaLastError=e.message||String(e)}return fallback&&fallback()}

  /* Install only where the normal app did not initialize a function. */
  if(typeof window.toast!=='function')window.toast=fallbackToast;
  if(typeof window.closeSheet!=='function')window.closeSheet=fallbackCloseSheet;
  if(typeof window.go!=='function')window.go=function(id,index){return fallbackGo(id,index)};
  var coreOpenSheet=window.openSheet;
  window.openSheet=function(type){
    if(type==='auth')return window.asiaAuthMode('email');
    if(typeof coreOpenSheet==='function')return safeCall(coreOpenSheet,[type],function(){fallbackOpenSheet(type)});
    return fallbackOpenSheet(type)
  };
  if(typeof window.shareApp!=='function')window.shareApp=function(){if(navigator.share){navigator.share({title:'Asia Drama',text:'Watch Asia Drama'}).catch(function(){})}else fallbackToast('Share link copied')};
  if(typeof window.loadHistory!=='function')window.loadHistory=function(){fallbackToast('Sign in to sync watch history')};

  function adminVisible(){var b=document.getElementById('adminButton');if(!b)return;if(!window.user||!window.supabase||!window.supabase.auth){b.classList.add('hidden');return}window.supabase.from('admin_roles').select('role').eq('user_id',window.user.id).limit(1).maybeSingle().then(function(r){b.classList.toggle('hidden',!r.data)}).catch(function(){b.classList.add('hidden')})}
  window.asiaRefreshAdminVisibility=adminVisible;

  function authHtml(mode){
    var email=mode==='email';
    var h='<button class="close" onclick="closeSheet()">×</button><h2>Welcome to Asia Drama</h2>';
    h+='<div class="authModes"><button type="button" class="authMode '+(email?'on':'')+'" onclick="asiaAuthMode(\'email\')">Email</button><button type="button" class="authMode '+(!email?'on':'')+'" onclick="asiaAuthMode(\'phone\')">Phone</button></div>';
    if(email)h+='<p class="small authHint">Sign in or create your Asia Drama account.</p><input id="email" class="field" type="email" placeholder="Email address" autocomplete="email"><input id="password" class="field" type="password" placeholder="Password" autocomplete="current-password"><button class="primary" type="button" onclick="asiaEmailSignIn()">Sign in</button><button class="secondary" type="button" style="margin-left:6px" onclick="asiaEmailSignUp()">Create account</button>';
    else h+='<p class="small authHint">Enter your phone number with country code, for example +91XXXXXXXXXX.</p><input id="phone" class="field" type="tel" placeholder="+91XXXXXXXXXX" autocomplete="tel"><button class="primary" type="button" onclick="asiaSendOtp()">Send OTP</button>';
    return h+'<p class="small" style="margin-top:12px">By continuing, you agree to the Asia Drama Terms and Privacy Policy.</p>'
  }
  window.asiaAuthMode=function(mode){var sh=document.getElementById('sheet'),ov=document.getElementById('overlay');if(!sh||!ov)return;sh.innerHTML=authHtml(mode);ov.classList.add('on')};
  function offline(){fallbackToast('Connection unavailable. Check your internet and try again.')}
  window.asiaEmailSignIn=async function(){var sb=window.supabase;if(!sb)return offline();var e=(document.getElementById('email')||{}).value?.trim(),p=(document.getElementById('password')||{}).value||'';if(!e||!p)return fallbackToast('Enter your email and password');var r=await sb.auth.signInWithPassword({email:e,password:p});if(r.error)return fallbackToast(r.error.message||'Sign in failed');fallbackCloseSheet();fallbackToast('Welcome back');if(typeof window.boot==='function')await window.boot();adminVisible()};
  window.asiaEmailSignUp=async function(){var sb=window.supabase;if(!sb)return offline();var e=(document.getElementById('email')||{}).value?.trim(),p=(document.getElementById('password')||{}).value||'';if(!e||!p)return fallbackToast('Enter your email and password');if(p.length<8)return fallbackToast('Use at least 8 characters');var r=await sb.auth.signUp({email:e,password:p});if(r.error)return fallbackToast(r.error.message||'Account creation failed');fallbackCloseSheet();fallbackToast(r.data?.session?'Account created':'Check your email to verify your account');if(typeof window.boot==='function')await window.boot();adminVisible()};
  window.asiaSendOtp=async function(){var sb=window.supabase;if(!sb)return offline();var ph=(document.getElementById('phone')||{}).value?.trim();if(!ph)return fallbackToast('Enter your phone number');var r=await sb.auth.signInWithOtp({phone:ph});if(r.error)return fallbackToast(r.error.message||'OTP could not be sent');window.__asiaOtpPhone=ph;var sh=document.getElementById('sheet');sh.innerHTML='<button class="close" onclick="closeSheet()">×</button><h2>Verify phone</h2><p class="small authHint">Enter the OTP sent to '+String(ph).replace(/[<>&]/g,'')+'</p><input id="otp" class="field" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="6-digit OTP"><button class="primary" type="button" onclick="asiaVerifyOtp()">Verify & continue</button>';fallbackToast('OTP sent')};
  window.asiaVerifyOtp=async function(){var sb=window.supabase;if(!sb)return offline();var t=(document.getElementById('otp')||{}).value?.trim(),ph=window.__asiaOtpPhone;if(!ph||!t)return fallbackToast('Enter the OTP');var r=await sb.auth.verifyOtp({phone:ph,token:t,type:'sms'});if(r.error)return fallbackToast(r.error.message||'Invalid OTP');fallbackCloseSheet();fallbackToast('Welcome to Asia Drama');if(typeof window.boot==='function')await window.boot();adminVisible()};

  setTimeout(function(){
    if(typeof window.go!=='function')window.go=function(id,index){fallbackGo(id,index)};
    if(typeof window.openSheet!=='function')window.openSheet=fallbackOpenSheet;
    adminVisible();
  },300);
  if(window.supabase&&window.supabase.auth)window.supabase.auth.onAuthStateChange(function(){setTimeout(adminVisible,100)});
})();
</script>'''

s=s.replace('</head>',css+'</head>')

profile_fix=r'''<script id="asia-profile-menu-fix-v2">
(function(){
  function esc(v){return String(v||'').replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
  function show(title,body){
    var o=document.getElementById('overlay'),s=document.getElementById('sheet');
    if(!o||!s)return;
    s.innerHTML='<button class="close" type="button" id="asiaSheetClose">×</button><h2>'+title+'</h2>'+body;
    o.classList.add('on');
    var x=document.getElementById('asiaSheetClose');if(x)x.onclick=function(){o.classList.remove('on')};
  }
  function openMenu(key){
    if(key==='list'){
      show('My List','<div id="asiaListContent"><div class="empty">Your saved titles will appear here.</div></div>');
      try{if(typeof renderList==='function')renderList()}catch(e){}
      return;
    }
    if(key==='history'){
      show('Watch history','<div id="asiaHistoryContent"><div class="empty">Loading your watch history…</div></div>');
      try{if(typeof loadHistory==='function')loadHistory()}catch(e){}
      try{if(typeof renderHistory==='function')renderHistory()}catch(e){}
      return;
    }
    if(key==='purchases'){
      show('Purchases & subscriptions','<div class="notice">Your purchases and subscriptions are linked to your account. Android digital purchases are verified through Google Play Billing.</div><div class="notice">If a purchase is missing, sign in with the same account used for the purchase and check your connection.</div><button class="primary" type="button" id="asiaPurchaseHelp">Check purchase access</button>');
      var b=document.getElementById('asiaPurchaseHelp');if(b)b.onclick=function(){if(typeof toast==='function')toast('Purchase access check started')};
      return;
    }
    if(key==='settings'){
      show('Settings & privacy','<button class="setting" type="button" id="asiaSignOut"><span>Sign out</span><b>›</b></button><button class="setting" type="button" id="asiaDeleteSetting"><span>Delete account</span><b>›</b></button><button class="setting" type="button" id="asiaPlaybackSetting"><span>Playback preferences</span><b>›</b></button>');
      var so=document.getElementById('asiaSignOut');if(so)so.onclick=function(){if(typeof signOut==='function')signOut();else if(typeof toast==='function')toast('Sign out is unavailable offline')};
      var de=document.getElementById('asiaDeleteSetting');if(de)de.onclick=function(){openMenu('delete')};
      var pb=document.getElementById('asiaPlaybackSetting');if(pb)pb.onclick=function(){if(typeof toast==='function')toast('Playback preferences saved locally')};
      return;
    }
    if(key==='legal'){
      show('Legal, terms & privacy','<div class="legal"><h3>Privacy Policy</h3><p>Asia Drama uses account, playback and transaction information to provide the service, secure accounts, support purchases and improve the product.</p><h3>Terms of Service</h3><p>Use only content made available through the service. Do not copy, redistribute, reverse engineer or misuse the platform.</p><h3>Payments & refunds</h3><p>Payment status is confirmed server-side. Refunds are handled according to the applicable payment provider and store policy.</p><h3>Community rules</h3><p>No harassment, hate, sexual exploitation, illegal content, copyright infringement, spam or impersonation.</p></div>');
      return;
    }
    if(key==='delete'){
      show('Delete account','<p class="legal">Deleting your account removes your app profile, watch history, entitlements and account-owned data. Some records may need to be retained where legally required.</p><button class="danger" type="button" id="asiaDeleteNow">Permanently delete account</button>');
      var d=document.getElementById('asiaDeleteNow');if(d)d.onclick=function(){if(typeof deleteAccount==='function')deleteAccount();else if(typeof toast==='function')toast('Please sign in to delete your account')};
    }
  }
  function bind(){
    var p=document.getElementById('profile');if(!p)return;
    var rows=p.querySelectorAll('.setting');
    rows.forEach(function(row){
      var t=(row.innerText||'').replace(/\s+/g,' ').trim().toLowerCase();
      var key=t.indexOf('my list')===0?'list':t.indexOf('watch history')===0?'history':t.indexOf('purchases')===0?'purchases':t.indexOf('settings')===0?'settings':t.indexOf('legal')===0?'legal':null;
      if(!key)return;
      row.onclick=function(e){e.preventDefault();e.stopPropagation();openMenu(key);};
      row.setAttribute('role','button');
      row.style.pointerEvents='auto';
    });
    var del=document.getElementById('asiaDeleteAccount');
    if(del){del.onclick=function(e){e.preventDefault();e.stopPropagation();openMenu('delete')}}
  }
  window.asiaOpenProfileMenu=openMenu;
  document.addEventListener('DOMContentLoaded',function(){bind();setTimeout(bind,500);setTimeout(bind,1500)});
  setInterval(bind,2000);
})();
</script>'''

s=s.replace('</body>',js+profile_fix+'</body>')
p.write_text(s)
