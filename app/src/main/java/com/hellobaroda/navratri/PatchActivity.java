package com.hellobaroda.navratri;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebView;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

public class PatchActivity extends MainActivity2 {
    private final Handler handler = new Handler(Looper.getMainLooper());
    private int attempts = 0;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        schedulePatch();
    }

    private void schedulePatch() {
        handler.postDelayed(this::injectPatch, attempts == 0 ? 1200 : 1000);
    }

    private void injectPatch() {
        attempts++;
        WebView web = findWebView(getWindow().getDecorView());
        if (web == null) {
            if (attempts < 15) schedulePatch();
            return;
        }
        injectAsset(web, "ux-patch.js");
        injectAsset(web, "ux-patch-fix.js");
        if (attempts < 5) schedulePatch();
    }

    private void injectAsset(WebView web, String name) {
        String js = loadAsset(name);
        if (js == null || js.isEmpty()) return;
        String escaped = js.replace("\\", "\\\\").replace("`", "\\`");
        web.evaluateJavascript("(function(){try{var s=document.createElement('script');s.textContent=`" + escaped + "`;document.head.appendChild(s);}catch(e){}})();", null);
    }

    private String loadAsset(String name) {
        try (InputStream in = getAssets().open(name); ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            byte[] buf = new byte[8192]; int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            return out.toString(StandardCharsets.UTF_8.name());
        } catch (Exception e) { return null; }
    }

    private WebView findWebView(View view) {
        if (view instanceof WebView) return (WebView) view;
        if (!(view instanceof ViewGroup)) return null;
        ViewGroup group = (ViewGroup) view;
        for (int i = 0; i < group.getChildCount(); i++) {
            WebView found = findWebView(group.getChildAt(i));
            if (found != null) return found;
        }
        return null;
    }
}
