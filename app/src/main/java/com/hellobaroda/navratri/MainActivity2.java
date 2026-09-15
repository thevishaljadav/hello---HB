package com.hellobaroda.navratri;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import com.android.billingclient.api.AcknowledgePurchaseParams;
import com.android.billingclient.api.BillingClient;
import com.android.billingclient.api.BillingClientStateListener;
import com.android.billingclient.api.BillingFlowParams;
import com.android.billingclient.api.BillingResult;
import com.android.billingclient.api.ProductDetails;
import com.android.billingclient.api.Purchase;
import com.android.billingclient.api.PurchasesUpdatedListener;
import com.android.billingclient.api.QueryProductDetailsParams;
import com.android.billingclient.api.QueryPurchasesParams;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class MainActivity2 extends Activity {
    private WebView web;
    private BillingClient billingClient;
    private final Map<String, Purchase> pendingPurchases = new HashMap<>();

    private final PurchasesUpdatedListener purchasesUpdatedListener = (billingResult, purchases) -> {
        if (billingResult.getResponseCode() == BillingClient.BillingResponseCode.OK && purchases != null) {
            for (Purchase purchase : purchases) {
                for (String productId : purchase.getProducts()) {
                    pendingPurchases.put(purchase.getPurchaseToken(), purchase);
                    runJs("window.onPlayPurchase && window.onPlayPurchase(" + js(productId) + "," + js(purchase.getPurchaseToken()) + ")");
                }
            }
        } else if (billingResult.getResponseCode() != BillingClient.BillingResponseCode.USER_CANCELED) {
            runJs("window.onPlayPurchaseError && window.onPlayPurchaseError(" + js(billingResult.getDebugMessage()) + ")");
        }
    };

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        web = new WebView(this);
        web.setBackgroundColor(0xFF08090C);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(false);
        s.setMediaPlaybackRequiresUserGesture(false);
        web.setWebViewClient(new WebViewClient());
        web.addJavascriptInterface(new NativeBridge(), "Android");
        setContentView(web);
        web.loadUrl("file:///android_asset/index.html");
        setupBilling();
    }

    private void setupBilling() {
        billingClient = BillingClient.newBuilder(this).setListener(purchasesUpdatedListener).enablePendingPurchases().build();
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
                    runJs("window.onExistingPlayPurchase && window.onExistingPlayPurchase(" + js(productId) + "," + js(purchase.getPurchaseToken()) + ")");
                }
            }
        });
    }

    private void buy(String productId) {
        if (billingClient == null || !billingClient.isReady()) { Toast.makeText(this, "Google Play is connecting. Try again.", Toast.LENGTH_SHORT).show(); return; }
        QueryProductDetailsParams params = QueryProductDetailsParams.newBuilder().setProductList(Arrays.asList(QueryProductDetailsParams.Product.newBuilder().setProductId(productId).setProductType(BillingClient.ProductType.INAPP).build())).build();
        billingClient.queryProductDetailsAsync(params, (result, details) -> {
            if (result.getResponseCode() != BillingClient.BillingResponseCode.OK || details.getProductDetailsList().isEmpty()) { runJs("window.onPlayPurchaseError && window.onPlayPurchaseError('Product is not available on Google Play yet.')"); return; }
            ProductDetails pd = details.getProductDetailsList().get(0);
            BillingFlowParams flow = BillingFlowParams.newBuilder().setProductDetailsParamsList(Arrays.asList(BillingFlowParams.ProductDetailsParams.newBuilder().setProductDetails(pd).build())).build();
            billingClient.launchBillingFlow(this, flow);
        });
    }

    private void acknowledge(String token) {
        Purchase purchase = pendingPurchases.get(token); if (purchase == null || purchase.isAcknowledged()) return;
        billingClient.acknowledgePurchase(AcknowledgePurchaseParams.newBuilder().setPurchaseToken(token).build(), result -> { if (result.getResponseCode() == BillingClient.BillingResponseCode.OK) pendingPurchases.remove(token); });
    }

    private void runJs(String code) { runOnUiThread(() -> { if (web != null) web.evaluateJavascript(code, null); }); }
    private static String js(String value) { if (value == null) return "null"; return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r") + "\""; }

    public class NativeBridge {
        @JavascriptInterface public void buy(String productId) { runOnUiThread(() -> MainActivity2.this.buy(productId)); }
        @JavascriptInterface public void acknowledge(String token) { runOnUiThread(() -> MainActivity2.this.acknowledge(token)); }
    }

    @Override public void onBackPressed() {
        if (web == null) { super.onBackPressed(); return; }
        web.evaluateJavascript("window.handleAndroidBack ? window.handleAndroidBack() : false", value -> {
            if ("true".equals(value)) return;
            if (web.canGoBack()) web.goBack(); else MainActivity2.super.onBackPressed();
        });
    }

    @Override protected void onDestroy() { if (billingClient != null) billingClient.endConnection(); if (web != null) web.destroy(); super.onDestroy(); }
}
