from pathlib import Path
import re
p=Path("app/src/main/assets/index.html")
s=p.read_text()
s=re.sub(r'<style id="asia-interaction-fix-v1">.*?</style>','',s,flags=re.S)
s=re.sub(r'<script id="asia-interaction-fix-v1-js">.*?</script>','',s,flags=re.S)
s=s.replace("const supabase=window.supabase.createClient(SUPA_URL,SUPA_KEY);","const supabase=window.supabase?window.supabase.createClient(SUPA_URL,SUPA_KEY):null;",1)
s=s.replace("async function boot(){const {data}=await supabase.auth.getUser();","async function boot(){if(!supabase){user=null;document.getElementById('profileName').textContent='Guest';document.getElementById('profileEmail').textContent='Connection unavailable — sign-in needs internet access';document.getElementById('authBtn').textContent='Sign in / Create account';document.getElementById('adminButton').classList.add('hidden');await loadCatalog();return}const {data}=await supabase.auth.getUser();",1)
s=s.replace("async function loadHistory(){","async function loadHistory(){if(!supabase){const e=document.getElementById('historyItems');if(e)e.innerHTML='<div class=\"empty\">Sign in requires an internet connection.</div>';return}",1)
s=s.replace("supabase.auth.onAuthStateChange(()=>setTimeout(boot,0));boot();","if(supabase&&supabase.auth){supabase.auth.onAuthStateChange(()=>setTimeout(boot,0))}boot();",1)
css=r'''<style id="asia-interaction-fix-v1">
.authModes{display:flex;gap:8px;margin:8px 0 12px}.authMode{flex:1;background:#1b1c22;border:1px solid #30323a;color:#aaa;border-radius:13px}.authMode.on{background:var(--red);color:#fff}.authHint{margin:6px 0 12px}
</style>'''
js=r'''<script id="asia-interaction-fix-v1-js">
(function(){
window.__asiaJsReady=true;
window.addEventListener('error',function(e){try{window.__asiaLastError=(e&&e.message)||'JavaScript error'}catch(_){} });
function adminVisible(){var b=document.getElementById('adminButton');if(!b)return;if(!window.user||!window.supabase||!supabase){b.classList.add('hidden');return}supabase.from('admin_roles').select('role').eq('user_id',user.id).limit(1).maybeSingle().then(function(r){b.classList.toggle('hidden',!r.data)}).catch(function(){b.classList.add('hidden')})}
window.asiaRefreshAdminVisibility=adminVisible;
var originalOpenSheet=window.openSheet;
function authHtml(mode){var email=mode==='email';var h='<button class="close" onclick="closeSheet()">×</button><h2>Welcome to Asia Drama</h2>';h+='<div class="authModes"><button type="button" class="authMode '+(email?'on':'')+'" onclick="asiaAuthMode(\'email\')">Email</button><button type="button" class="authMode '+(!email?'on':'')+'" onclick="asiaAuthMode(\'phone\')">Phone</button></div>';if(email){h+='<p class="small authHint">Sign in or create your Asia Drama account.</p><input id="email" class="field" type="email" placeholder="Email address" autocomplete="email"><input id="password" class="field" type="password" placeholder="Password" autocomplete="current-password"><button class="primary" type="button" onclick="asiaEmailSignIn()">Sign in</button><button class="secondary" type="button" style="margin-left:6px" onclick="asiaEmailSignUp()">Create account</button>'}else{h+='<p class="small authHint">Enter your phone number with country code, for example +91XXXXXXXXXX.</p><input id="phone" class="field" type="tel" placeholder="+91XXXXXXXXXX" autocomplete="tel"><button class="primary" type="button" onclick="asiaSendOtp()">Send OTP</button>'}h+='<p class="small" style="margin-top:12px">By continuing, you agree to the Asia Drama Terms and Privacy Policy.</p>';return h}
window.asiaAuthMode=function(mode){var s=document.getElementById('sheet');if(!s)return;s.innerHTML=authHtml(mode);document.getElementById('overlay').classList.add('on')};
function offline(){toast('Connection unavailable. Check your internet and try again.')}
window.asiaEmailSignIn=async function(){if(!supabase)return offline();var e=(document.getElementById('email')||{}).value?.trim(),p=(document.getElementById('password')||{}).value||'';if(!e||!p)return toast('Enter your email and password');var r=await supabase.auth.signInWithPassword({email:e,password:p});if(r.error)return toast(r.error.message||'Sign in failed');closeSheet();toast('Welcome back');await boot();adminVisible()};
window.asiaEmailSignUp=async function(){if(!supabase)return offline();var e=(document.getElementById('email')||{}).value?.trim(),p=(document.getElementById('password')||{}).value||'';if(!e||!p)return toast('Enter your email and password');if(p.length<8)return toast('Use at least 8 characters');var r=await supabase.auth.signUp({email:e,password:p});if(r.error)return toast(r.error.message||'Account creation failed');closeSheet();toast(r.data?.session?'Account created':'Check your email to verify your account');await boot();adminVisible()};
window.asiaSendOtp=async function(){if(!supabase)return offline();var ph=(document.getElementById('phone')||{}).value?.trim();if(!ph)return toast('Enter your phone number');var r=await supabase.auth.signInWithOtp({phone:ph});if(r.error)return toast(r.error.message||'OTP could not be sent');window.__asiaOtpPhone=ph;var s=document.getElementById('sheet');s.innerHTML='<button class="close" onclick="closeSheet()">×</button><h2>Verify phone</h2><p class="small authHint">Enter the OTP sent to '+safe(ph)+'</p><input id="otp" class="field" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="6-digit OTP"><button class="primary" type="button" onclick="asiaVerifyOtp()">Verify & continue</button>';toast('OTP sent')};
window.asiaVerifyOtp=async function(){if(!supabase)return offline();var t=(document.getElementById('otp')||{}).value?.trim(),ph=window.__asiaOtpPhone;if(!ph||!t)return toast('Enter the OTP');var r=await supabase.auth.verifyOtp({phone:ph,token:t,type:'sms'});if(r.error)return toast(r.error.message||'Invalid OTP');closeSheet();toast('Welcome to Asia Drama');await boot();adminVisible()};
window.openSheet=function(type){if(type==='auth')return asiaAuthMode('email');return originalOpenSheet.apply(this,arguments)};
if(window.supabase&&supabase&&supabase.auth)supabase.auth.onAuthStateChange(function(){setTimeout(adminVisible,100)});
setTimeout(adminVisible,500);
})();
</script>'''
if 'asia-interaction-fix-v1' not in s:
    s=s.replace('</head>',css+'</head>')
    s=s.replace('</body>',js+'</body>')
p.write_text(s)
