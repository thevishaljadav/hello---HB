package com.hellobaroda.navratri;

import android.app.Activity;
import android.app.PictureInPictureParams;
import android.content.pm.ActivityInfo;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.util.Rational;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.OptIn;
import androidx.media3.common.AudioAttributes;
import androidx.media3.common.C;
import androidx.media3.common.MediaItem;
import androidx.media3.common.PlaybackException;
import androidx.media3.common.Player;
import androidx.media3.common.util.UnstableApi;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.ui.PlayerView;

import com.android.billingclient.api.AcknowledgePurchaseParams;
import com.android.billingclient.api.BillingClient;
import com.android.billingclient.api.BillingClientStateListener;
import com.android.billingclient.api.BillingFlowParams;
import com.android.billingclient.api.BillingResult;
import com.android.billingclient.api.PendingPurchasesParams;
import com.android.billingclient.api.ProductDetails;
import com.android.billingclient.api.Purchase;
import com.android.billingclient.api.PurchasesUpdatedListener;
import com.android.billingclient.api.QueryProductDetailsParams;
import com.android.billingclient.api.QueryPurchasesParams;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

@OptIn(markerClass = UnstableApi.class)
public class MainActivity2 extends Activity {
    private static final String API_BASE = "https://wevutronudkcqbzmverf.supabase.co/functions/v1";
    private FrameLayout root;
    private WebView web;
    private View customView;
    private WebChromeClient.CustomViewCallback customViewCallback;
    private int savedSystemUiVisibility;
    private BillingClient billingClient;
    private final Map<String, Purchase> pendingPurchases = new HashMap<>();

    private ExoPlayer player;
    private PlayerView playerView;
    private FrameLayout nativePlayerOverlay;
    private TextView nativeTitle;
    private String currentMediaUrl;
    private String currentMediaTitle;
    private boolean currentMediaIsVideo;

    private final PurchasesUpdatedListener purchasesUpdatedListener = (billingResult, purchases) -> {
        if (billingResult.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (Purchase purchase : purchases) for (String productId : purchase.getProducts()) {
                pendingPurchases.put(purchase.getPurchaseToken(), purchase);
                runJs("window.onPlayPurchase && window.onPlayPurchase(" + js(productId) + "," + js(purchase.getPurchaseToken()) + ")");
            }
        } else if (billingResult.getResponseCode() != BillingClient.BillingResponseCode.USER_CANCELED) {
            runJs("window.toast && window.toast(" + js(billingResult.getDebugMessage()) + ")");
        }
    };

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        root = new FrameLayout(this);
        root.setBackgroundColor(Color.BLACK);
        web = new WebView(this);
        root.addView(web, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        setContentView(root);
        setupWebView(savedInstanceState);
        setupBilling();
    }

    private void setupWebView(Bundle savedInstanceState) {
        web.setBackgroundColor(0xFF08090C);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(true);
        s.setBuiltInZoomControls(false);
        s.setDisplayZoomControls(false);
        s.setSupportMultipleWindows(false);
        web.addJavascriptInterface(new NativeBridge(), "Android");
        web.setWebChromeClient(new WebChromeClient() {
            @Override public void onShowCustomView(View view, CustomViewCallback callback) {
                if (customView != null) { callback.onCustomViewHidden(); return; }
                customView = view;
                customViewCallback = callback;
                savedSystemUiVisibility = getWindow().getDecorView().getSystemUiVisibility();
                root.addView(customView, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
                web.setVisibility(View.GONE);
                getWindow().setStatusBarColor(Color.TRANSPARENT);
                getWindow().setNavigationBarColor(Color.TRANSPARENT);
                getWindow().getDecorView().setSystemUiVisibility(
                        View.SYSTEM_UI_FLAG_FULLSCREEN |
                        View.SYSTEM_UI_FLAG_HIDE_NAVIGATION |
                        View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY |
                        View.SYSTEM_UI_FLAG_LAYOUT_STABLE |
                        View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN |
                        View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
                setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR);
            }

            @Override public void onHideCustomView() { hideCustomView(); }
        });
        web.setWebViewClient(new WebViewClient() {
            @Override public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                injectPurchaseBridge();
            }
        });
        if (savedInstanceState != null && savedInstanceState.getBundle("web_state") != null) {
            web.restoreState(savedInstanceState.getBundle("web_state"));
        } else {
            web.loadUrl("file:///android_asset/index.html");
        }
    }

    private void hideCustomView() {
        if (customView == null) return;
        root.removeView(customView);
        customView = null;
        if (customViewCallback != null) {
            customViewCallback.onCustomViewHidden();
            customViewCallback = null;
        }
        web.setVisibility(View.VISIBLE);
        getWindow().getDecorView().setSystemUiVisibility(savedSystemUiVisibility);
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED);
    }

    private void injectPurchaseBridge() {
        String js = "(function(){"
                + "window.onPlayPurchase=async function(productId,token){try{const s=await window.supabase.auth.getSession();const a=s.data.session?.access_token;if(!a){window.toast&&window.toast('Please sign in before purchasing.');return;}const r=await fetch('" + API_BASE + "/verify-play-purchase',{method:'POST',headers:{Authorization:'Bearer '+a,'Content-Type':'application/json'},body:JSON.stringify({product_id:productId,purchase_token:token})});const j=await r.json();if(!r.ok||!j.verified){window.toast&&window.toast(j.error||'Purchase could not be verified.');return;}window.toast&&window.toast('Purchase verified. Access unlocked.');window.onPlayPurchaseVerified&&window.onPlayPurchaseVerified(j.episode_id);Android.acknowledge(token);}catch(e){window.toast&&window.toast('Purchase verification failed.');}};"
                + "window.onPlayPurchaseVerified=async function(id){try{const s=await window.supabase.auth.getSession();const a=s.data.session?.access_token;if(!a)throw new Error('Please sign in again.');const r=await fetch('" + API_BASE + "/playback-url?episode_id='+encodeURIComponent(id),{headers:{Authorization:'Bearer '+a}});const j=await r.json();if(!r.ok)throw new Error(j.error||'Playback unavailable');if(window.Android)Android.playVideo(j.title||'Asia Drama',j.url,0);}catch(e){window.toast&&window.toast(e.message||'Playback unavailable');}};"
                + "window.__asiaSecurePlaybackBridge=async function(id,title,paid){try{if(paid){if(!window.Android){window.toast&&window.toast('Google Play is unavailable');return;}const ep=(typeof catalog!=='undefined'?catalog:[]).flatMap(x=>(x.seasons||[]).flatMap(s=>s.episodes||[])).find(e=>e.id===id);Android.buy(ep?.play_product_id||id);return;}const s=await window.supabase.auth.getSession();const a=s.data.session?.access_token;if(!a)throw new Error('Please sign in to watch.');const r=await fetch('" + API_BASE + "/playback-url?episode_id='+encodeURIComponent(id),{headers:{Authorization:'Bearer '+a},cache:'no-store'});const j=await r.json();if(!r.ok)throw new Error(j.error||'Playback unavailable');if(window.Android)Android.playVideo(j.title||title||'Asia Drama',j.url,0);}catch(e){window.toast&&window.toast(e.message||'Playback unavailable');}};"
"
                + "if(window.playEpisode&&!window.__playWrapped){window.__playWrapped=true;window.playEpisode=function(id,title,url,paid){return window.__asiaSecurePlaybackBridge(id,title,!!paid);};}"
                + "window.handleAndroidBack=window.handleAndroidBack||function(){const p=document.getElementById('player'),o=document.getElementById('overlay');if(p?.classList.contains('on')){window.closePlayer();return true;}if(o?.classList.contains('on')){window.closeSheet();return true;}return false;};"
                + "})();";
        web.evaluateJavascript(js, null);
    }

    private void setupNativePlayer() {
        if (player != null) return;
        player = new ExoPlayer.Builder(this).build();
        AudioAttributes audioAttributes = new AudioAttributes.Builder()
                .setUsage(C.USAGE_MEDIA)
                .setContentType(C.AUDIO_CONTENT_TYPE_MOVIE)
                .build();
        player.setAudioAttributes(audioAttributes, true);
        player.setHandleAudioBecomingNoisy(true);
        player.addListener(new Player.Listener() {
            @Override public void onIsPlayingChanged(boolean isPlaying) {
                if (isPlaying) runJs("window.onNativePlaybackStarted&&window.onNativePlaybackStarted()");
            }
            @Override public void onPlayerError(PlaybackException error) {
                runJs("window.toast&&window.toast(" + js("Playback error. Please try again.") + ")");
            }
        });

        nativePlayerOverlay = new FrameLayout(this);
        nativePlayerOverlay.setBackgroundColor(Color.BLACK);
        playerView = new PlayerView(this);
        playerView.setPlayer(player);
        playerView.setUseController(true);
        playerView.setShowBuffering(PlayerView.SHOW_BUFFERING_WHEN_PLAYING);
        playerView.setKeepScreenOn(true);
        nativePlayerOverlay.addView(playerView, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        TextView close = new TextView(this);
        close.setText("×");
        close.setTextColor(Color.WHITE);
        close.setTextSize(34);
        close.setGravity(Gravity.CENTER);
        close.setContentDescription("Close player");
        close.setBackgroundColor(0x66000000);
        close.setPadding(12, 0, 12, 4);
        FrameLayout.LayoutParams cp = new FrameLayout.LayoutParams(64, 64, Gravity.TOP | Gravity.START);
        cp.topMargin = 18;
        cp.leftMargin = 12;
        nativePlayerOverlay.addView(close, cp);
        close.setOnClickListener(v -> stopNativePlayer(true));

        nativeTitle = new TextView(this);
        nativeTitle.setTextColor(Color.WHITE);
        nativeTitle.setTextSize(16);
        nativeTitle.setMaxLines(1);
        nativeTitle.setEllipsize(android.text.TextUtils.TruncateAt.END);
        nativeTitle.setGravity(Gravity.CENTER_VERTICAL);
        nativeTitle.setBackgroundColor(0x66000000);
        nativeTitle.setPadding(18, 0, 18, 0);
        FrameLayout.LayoutParams tp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, 56, Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        tp.topMargin = 22;
        nativePlayerOverlay.addView(nativeTitle, tp);
    }

    private void playNativeMedia(String title, String url, long positionMs, boolean isVideo) {
        if (url == null || url.trim().isEmpty()) { Toast.makeText(this, "Media is unavailable.", Toast.LENGTH_SHORT).show(); return; }
        setupNativePlayer();
        currentMediaUrl = url;
        currentMediaTitle = title;
        currentMediaIsVideo = isVideo;
        nativeTitle.setText(title == null ? "Asia Drama" : title);
        playerView.setUseController(true);
        root.addView(nativePlayerOverlay, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        web.setVisibility(View.GONE);
        MediaItem item = MediaItem.fromUri(Uri.parse(url));
        player.setMediaItem(item);
        player.prepare();
        if (positionMs > 0) player.seekTo(positionMs);
        player.play();
        if (isVideo) configurePip();
    }

    private void stopNativePlayer(boolean returnToWeb) {
        if (player != null) player.stop();
        if (nativePlayerOverlay != null && nativePlayerOverlay.getParent() != null) root.removeView(nativePlayerOverlay);
        if (returnToWeb && web != null) web.setVisibility(View.VISIBLE);
        currentMediaUrl = null;
        currentMediaTitle = null;
    }

    private void configurePip() {
        if (Build.VERSION.SDK_INT >= 26) {
            PictureInPictureParams.Builder builder = new PictureInPictureParams.Builder().setAspectRatio(new Rational(16, 9));
            if (Build.VERSION.SDK_INT >= 31) builder.setAutoEnterEnabled(true);
            setPictureInPictureParams(builder.build());
        }
    }

    @Override protected void onUserLeaveHint() {
        super.onUserLeaveHint();
        if (Build.VERSION.SDK_INT >= 26 && currentMediaIsVideo && player != null && player.isPlaying()) {
            enterPictureInPictureMode(new PictureInPictureParams.Builder().setAspectRatio(new Rational(16, 9)).build());
        }
    }

    @Override public void onPictureInPictureModeChanged(boolean isInPictureInPictureMode, android.content.res.Configuration newConfig) {
        super.onPictureInPictureModeChanged(isInPictureInPictureMode, newConfig);
        if (nativePlayerOverlay != null) nativePlayerOverlay.setSystemUiVisibility(isInPictureInPictureMode ? View.SYSTEM_UI_FLAG_LAYOUT_STABLE : 0);
    }

    private void setupBilling() {
        billingClient = BillingClient.newBuilder(this)
                .setListener(purchasesUpdatedListener)
                .enablePendingPurchases(PendingPurchasesParams.newBuilder().enableOneTimeProducts().build())
                .enableAutoServiceReconnection()
                .build();
        billingClient.startConnection(new BillingClientStateListener() {
            @Override public void onBillingSetupFinished(BillingResult result) { if (result.getResponseCode() == BillingClient.BillingResponseCode.OK) queryExistingPurchases(); }
            @Override public void onBillingServiceDisconnected() { }
        });
    }

    private void queryExistingPurchases() {
        billingClient.queryPurchasesAsync(QueryPurchasesParams.newBuilder().setProductType(BillingClient.ProductType.INAPP).build(), (result, purchases) -> {
            if (result.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
                for (Purchase purchase : purchases) for (String productId : purchase.getProducts()) {
                    pendingPurchases.put(purchase.getPurchaseToken(), purchase);
                    runJs("window.onPlayPurchase && window.onPlayPurchase(" + js(productId) + "," + js(purchase.getPurchaseToken()) + ")");
                }
            }
        });
    }

    private void buy(String productId) {
        if (productId == null || productId.trim().isEmpty()) { runJs("window.toast&&window.toast('This episode is not configured for Google Play yet.')"); return; }
        if (billingClient == null || !billingClient.isReady()) { Toast.makeText(this, "Google Play is connecting. Try again.", Toast.LENGTH_SHORT).show(); return; }
        QueryProductDetailsParams params = QueryProductDetailsParams.newBuilder().setProductList(Arrays.asList(
                QueryProductDetailsParams.Product.newBuilder().setProductId(productId).setProductType(BillingClient.ProductType.INAPP).build())).build();
        billingClient.queryProductDetailsAsync(params, (result, details) -> {
            if (result.getResponseCode() != BillingClient.BillingResponseCode.OK || details.getProductDetailsList().isEmpty()) {
                runJs("window.toast && window.toast('This paid episode is not available on Google Play yet.')");
                return;
            }
            ProductDetails pd = details.getProductDetailsList().get(0);
            BillingFlowParams flow = BillingFlowParams.newBuilder().setProductDetailsParamsList(Arrays.asList(
                    BillingFlowParams.ProductDetailsParams.newBuilder().setProductDetails(pd).build())).build();
            billingClient.launchBillingFlow(this, flow);
        });
    }

    private void acknowledge(String token) {
        Purchase purchase = pendingPurchases.get(token);
        if (purchase == null || purchase.isAcknowledged() || purchase.getPurchaseState() != Purchase.PurchaseState.PURCHASED) return;
        billingClient.acknowledgePurchase(AcknowledgePurchaseParams.newBuilder().setPurchaseToken(token).build(), result -> {
            if (result.getResponseCode() == BillingClient.BillingResponseCode.OK) pendingPurchases.remove(token);
        });
    }

    private void runJs(String code) { runOnUiThread(() -> { if (web != null) web.evaluateJavascript(code, null); }); }
    private static String js(String value) {
        if (value == null) return "null";
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r") + "\"";
    }

    public class NativeBridge {
        @JavascriptInterface public void buy(String productId) { runOnUiThread(() -> MainActivity2.this.buy(productId)); }
        @JavascriptInterface public void acknowledge(String token) { runOnUiThread(() -> MainActivity2.this.acknowledge(token)); }
        @JavascriptInterface public void playVideo(String title, String url, long positionMs) { runOnUiThread(() -> playNativeMedia(title, url, positionMs, true)); }
        @JavascriptInterface public void playAudio(String title, String url, long positionMs) { runOnUiThread(() -> playNativeMedia(title, url, positionMs, false)); }
        @JavascriptInterface public void stopPlayback() { runOnUiThread(() -> stopNativePlayer(true)); }
    }

    @Override protected void onSaveInstanceState(Bundle outState) {
        Bundle webState = new Bundle();
        web.saveState(webState);
        outState.putBundle("web_state", webState);
        if (player != null) {
            outState.putString("media_url", currentMediaUrl);
            outState.putString("media_title", currentMediaTitle);
            outState.putLong("media_position", player.getCurrentPosition());
            outState.putBoolean("media_video", currentMediaIsVideo);
        }
        super.onSaveInstanceState(outState);
    }

    @Override protected void onRestoreInstanceState(Bundle state) {
        super.onRestoreInstanceState(state);
        String url = state.getString("media_url");
        if (url != null) playNativeMedia(state.getString("media_title", "Asia Drama"), url, state.getLong("media_position", 0), state.getBoolean("media_video", true));
    }

    @Override public void onBackPressed() {
        if (customView != null) { hideCustomView(); return; }
        if (nativePlayerOverlay != null && nativePlayerOverlay.getParent() != null) { stopNativePlayer(true); return; }
        if (web == null) { super.onBackPressed(); return; }
        web.evaluateJavascript("window.handleAndroidBack ? window.handleAndroidBack() : false", value -> {
            if ("true".equals(value)) return;
            if (web.canGoBack()) web.goBack(); else MainActivity2.super.onBackPressed();
        });
    }

    @Override protected void onDestroy() {
        if (customView != null) hideCustomView();
        if (player != null) { player.release(); player = null; }
        if (billingClient != null) billingClient.endConnection();
        if (web != null) { web.stopLoading(); web.loadUrl("about:blank"); web.clearHistory(); web.removeAllViews(); web.destroy(); }
        super.onDestroy();
    }
}
