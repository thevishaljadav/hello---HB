from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'

# --- Android release configuration ---
build = APP / 'build.gradle'
s = build.read_text()
s = s.replace("versionCode 5", "versionCode 6")
s = s.replace("versionName '2.2'", "versionName '2.3'")
s = s.replace("minifyEnabled false\n            shrinkResources false", "minifyEnabled true\n            shrinkResources true")
if "proguard-rules.pro" not in s:
    s = s.replace("minifyEnabled true\n            shrinkResources true", "minifyEnabled true\n            shrinkResources true\n            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'")
build.write_text(s)

proguard = APP / 'proguard-rules.pro'
proguard.write_text(r'''# Asia Drama release rules.
-keepclassmembers class com.hellobaroda.navratri.MainActivity2$NativeBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class com.hellobaroda.navratri.MainActivity2$NativeBridge { *; }
-keep class com.hellobaroda.navratri.PatchActivity { *; }
-keepattributes *Annotation*,InnerClasses,EnclosingMethod,SourceFile,LineNumberTable
-keep class androidx.media3.** { *; }
''')

# --- Pin web SDKs and remove unused alternative-payment web SDK from the Play build ---
html = APP / 'src/main/assets/index.html'
h = html.read_text()
h = h.replace('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2', 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.116.0')
h = h.replace('<script src="https://checkout.razorpay.com/v1/checkout.js"></script>', '')
html.write_text(h)

# --- Harden WebView ---
java = APP / 'src/main/java/com/hellobaroda/navratri/MainActivity2.java'
j = java.read_text()
old = '''        s.setSupportMultipleWindows(false);\n        web.addJavascriptInterface(new NativeBridge(), "Android");'''
new = '''        s.setSupportMultipleWindows(false);\n        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {\n            s.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);\n        }\n        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.JELLY_BEAN) {\n            s.setAllowFileAccessFromFileURLs(false);\n            s.setAllowUniversalAccessFromFileURLs(false);\n        }\n        if ((getApplicationInfo().flags & android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0) {\n            WebView.setWebContentsDebuggingEnabled(true);\n        }\n        web.addJavascriptInterface(new NativeBridge(), "Android");'''
if old in j:
    j = j.replace(old, new, 1)

old_client = '''        web.setWebViewClient(new WebViewClient() {\n            @Override public void onPageFinished(WebView view, String url) {\n                super.onPageFinished(view, url);\n                injectPurchaseBridge();\n            }\n        });'''
new_client = '''        web.setWebViewClient(new WebViewClient() {\n            @Override public boolean shouldOverrideUrlLoading(WebView view, String url) {\n                if (url == null || url.startsWith("file:///android_asset/")) return false;\n                try { startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url))); } catch (Exception ignored) { }\n                return true;\n            }\n            @Override public void onReceivedSslError(WebView view, android.webkit.SslErrorHandler handler, android.net.http.SslError error) { handler.cancel(); }\n            @Override public void onPageFinished(WebView view, String url) {\n                super.onPageFinished(view, url);\n                injectPurchaseBridge();\n            }\n        });'''
if old_client in j:
    j = j.replace(old_client, new_client, 1)
if 'import android.content.Intent;' not in j:
    j = j.replace('import android.app.PictureInPictureParams;\n', 'import android.app.PictureInPictureParams;\nimport android.content.Intent;\n')
java.write_text(j)

# --- Add in-app account deletion / privacy surface ---
marker = '</body>'
legal = r'''<style id="asia-production-legal-v1">#asiaLegalCard{margin:16px 15px 96px;padding:16px;border:1px solid var(--line);border-radius:18px;background:var(--panel);color:#d7d7dc;line-height:1.55}#asiaLegalCard h3{margin:0 0 8px;color:#fff}#asiaLegalCard p{margin:6px 0}.asiaLegalActions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}.asiaLegalActions button{min-height:44px;border-radius:12px;padding:0 14px;background:#282a31}.asiaLegalActions button.danger{background:#6f1523}</style><script id="asia-production-legal-v1">(function(){
function ensureLegal(){try{if(document.getElementById('asiaLegalCard'))return;var nav=[...document.querySelectorAll('.nav button')];var active=nav.find(function(b){return /profile|account/i.test((b.innerText||'')+' '+(b.getAttribute('aria-label')||''))&&b.classList.contains('on');});if(!active)return;var host=document.querySelector('.view.on')||document.querySelector('.profile');if(!host)return;var card=document.createElement('section');card.id='asiaLegalCard';card.innerHTML='<h3>Privacy & Account</h3><p>Asia Drama uses your account information, viewing activity and purchase records to provide sign-in, playback, access control and support. Payment credentials are handled by the payment provider.</p><p>We use secure connections for account and playback services. You can request deletion of your Asia Drama account and associated app data from this screen.</p><div class="asiaLegalActions"><button type="button" id="asiaDeleteAccount" class="danger">Delete my account</button></div>';host.appendChild(card);card.querySelector('#asiaDeleteAccount').onclick=deleteAccount;}catch(e){}}
async function deleteAccount(){try{if(!confirm('Delete your Asia Drama account and associated app data? This action cannot be undone.'))return;var sess=await window.supabase.auth.getSession();var token=sess&&sess.data&&sess.data.session&&sess.data.access_token;if(!token){window.toast&&window.toast('Please sign in again.');return;}var r=await fetch('https://wevutronudkcqbzmverf.supabase.co/functions/v1/delete-account',{method:'POST',headers:{Authorization:'Bearer '+token}});var j=await r.json().catch(function(){return{};});if(!r.ok||!j.deleted)throw new Error(j.error||'Account deletion failed.');await window.supabase.auth.signOut();window.toast&&window.toast('Account deleted.');setTimeout(function(){location.reload();},500);}catch(e){window.toast&&window.toast(e.message||'Account deletion failed.');}}
var last='';setInterval(function(){var key=(document.querySelector('.view.on')||{}).id||'';if(key!==last){last=key;ensureLegal();}},800);document.addEventListener('DOMContentLoaded',ensureLegal);window.__asiaEnsureLegal=ensureLegal;})();</script>'''
if 'asia-production-legal-v1' not in h:
    h = h.replace(marker, legal + marker, 1)
html.write_text(h)

print('Production hardening patch applied.')
