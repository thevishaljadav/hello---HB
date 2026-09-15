from pathlib import Path

html = Path('app/src/main/assets/index.html')
s = html.read_text()

# Remove an older copy if a previous workflow attempt already inserted it.
import re
s = re.sub(r'<style id="asia-interaction-fix-v1">.*?</style>', '', s, flags=re.S)
s = re.sub(r'<script id="asia-interaction-fix-v1-js">.*?</script>', '', s, flags=re.S)

css = r'''<style id="asia-interaction-fix-v1">
.authModes{display:flex;gap:8px;margin:8px 0 12px}.authMode{flex:1;background:#1b1c22;border:1px solid #30323a;color:#aaa;border-radius:13px}.authMode.on{background:var(--red);color:#fff}.authHint{margin:6px 0 12px}
</style>'''

js = r'''<script id="asia-interaction-fix-v1-js">
(function(){
  /*
   * WebView interaction hardening. The app is a local HTML application inside
   * Android WebView, so keep a delegated touch path in addition to inline click
   * handlers. This makes dynamically-created sheet controls reliable too.
   */
  window.__asiaJsReady=true;
  window.addEventListener('error',function(e){
    try{window.__asiaLastError=(e&&e.message)||'JavaScript error'}catch(_){ }
  });

  var touch={x:0,y:0,time:0,target:null};
  document.addEventListener('touchstart',function(e){
    var t=e.touches&&e.touches[0];
    touch.x=t?t.clientX:0;touch.y=t?t.clientY:0;touch.time=Date.now();
    touch.target=e.target&&e.target.closest?e.target.closest('button,[role="button"],a'):null;
  },{passive:true,capture:true});
  document.addEventListener('touchend',function(e){
    var t=e.changedTouches&&e.changedTouches[0],b=touch.target;
    if(!b||!b.isConnected)return;
    var dx=t?t.clientX-touch.x:0,dy=t?t.clientY-touch.y:0;
    if(Math.abs(dx)>12||Math.abs(dy)>12)return;
    var code=b.getAttribute('onclick');
    if(!code)return;
    e.preventDefault();
    try{b.__asiaTouchHandled=Date.now();(new Function(code)).call(b)}catch(err){try{window.toast&&window.toast(err.message||'Action could not be completed')}catch(_){}}
  },{passive:false,capture:true});
  document.addEventListener('click',function(e){
    var b=e.target&&e.target.closest?e.target.closest('button,[role="button"],a'):null;
    if(!b)return;
    var stamp=b.__asiaTouchHandled||0;
    if(Date.now()-stamp<700){e.preventDefault();e.stopImmediatePropagation();b.__asiaTouchHandled=0;}
  },true);

  function adminVisible(){
    var btn=document.getElementById('adminButton');
    if(!btn)return;
    if(!window.user){btn.classList.add('hidden');return;}
    supabase.from('admin_roles').select('role').eq('user_id',user.id).limit(1).maybeSingle().then(function(r){
      btn.classList.toggle('hidden',!r.data);
    }).catch(function(){btn.classList.add('hidden')});
  }
  window.asiaRefreshAdminVisibility=adminVisible;
  if(window.supabase&&supabase.auth){supabase.auth.onAuthStateChange(function(){setTimeout(adminVisible,80)});setTimeout(adminVisible,300)}

  /* Email + phone authentication in one account sheet. */
  var originalOpenSheet=window.openSheet;
  function authHtml(mode){
    var email=mode==='email', phone=mode==='phone', verify=mode==='verify';
    var h='<button class="close" onclick="closeSheet()">×</button><h2>Welcome to Asia Drama</h2>';
    h+='<div class="authModes"><button type="button" class="authMode '+(email?'on':'')+'" onclick="asiaAuthMode(\'email\')">Email</button><button type="button" class="authMode '+(phone?'on':'')+'" onclick="asiaAuthMode(\'phone\')">Phone</button></div>';
    if(email){
      h+='<p class="small authHint">Sign in or create your Asia Drama account.</p><input id="email" class="field" type="email" placeholder="Email address" autocomplete="email"><input id="password" class="field" type="password" placeholder="Password" autocomplete="current-password"><button class="primary" type="button" onclick="asiaEmailSignIn()">Sign in</button><button class="secondary" type="button" style="margin-left:6px" onclick="asiaEmailSignUp()">Create account</button>';
    }else if(phone){
      h+='<p class="small authHint">Enter your phone number with country code, for example +91XXXXXXXXXX.</p><input id="phone" class="field" type="tel" placeholder="+91XXXXXXXXXX" autocomplete="tel"><button class="primary" type="button" onclick="asiaSendOtp()">Send OTP</button>';
    }else if(verify){
      h+='<p class="small authHint">Enter the OTP sent to your phone.</p><input id="otp" class="field" inputmode="numeric" autocomplete="one-time-code" maxlength="6" placeholder="6-digit OTP"><button class="primary" type="button" onclick="asiaVerifyOtp()">Verify & continue</button>';
    }
    h+='<p class="small" style="margin-top:12px">By continuing, you agree to the Asia Drama Terms and Privacy Policy.</p>';
    return h;
  }
  window.asiaAuthMode=function(mode){
    var s=document.getElementById('sheet');if(!s)return;
    s.innerHTML=authHtml(mode);document.getElementById('overlay').classList.add('on');
  };
  window.asiaEmailSignIn=async function(){
    var email=(document.getElementById('email')||{}).value?.trim(),password=(document.getElementById('password')||{}).value||'';
    if(!email||!password)return toast('Enter your email and password');
    var r=await supabase.auth.signInWithPassword({email,password});
    if(r.error)return toast(r.error.message||'Sign in failed');
    closeSheet();toast('Welcome back');await boot();adminVisible();
  };
  window.asiaEmailSignUp=async function(){
    var email=(document.getElementById('email')||{}).value?.trim(),password=(document.getElementById('password')||{}).value||'';
    if(!email||!password)return toast('Enter your email and password');
    if(password.length<8)return toast('Use at least 8 characters');
    var r=await supabase.auth.signUp({email,password});
    if(r.error)return toast(r.error.message||'Account creation failed');
    closeSheet();toast(r.data?.session?'Account created':'Check your email to verify your account');await boot();adminVisible();
  };
  window.asiaSendOtp=async function(){
    var phone=(document.getElementById('phone')||{}).value?.trim();
    if(!phone)return toast('Enter your phone number');
    var r=await supabase.auth.signInWithOtp({phone});
    if(r.error)return toast(r.error.message||'OTP could not be sent');
    window.__asiaOtpPhone=phone;asiaAuthMode('verify');toast('OTP sent');
  };
  window.asiaVerifyOtp=async function(){
    var token=(document.getElementById('otp')||{}).value?.trim(),phone=window.__asiaOtpPhone;
    if(!phone||!token)return toast('Enter the OTP');
    var r=await supabase.auth.verifyOtp({phone,token,type:'sms'});
    if(r.error)return toast(r.error.message||'Invalid OTP');
    closeSheet();toast('Welcome to Asia Drama');await boot();adminVisible();
  };
  window.openSheet=function(type){
    if(type==='auth')return asiaAuthMode('email');
    return originalOpenSheet.apply(this,arguments);
  };
  setTimeout(adminVisible,500);
})();
</script>'''

if 'asia-interaction-fix-v1' not in s:
    s = s.replace('</head>', css + '</head>')
    s = s.replace('</body>', js + '</body>')

html.write_text(s)
