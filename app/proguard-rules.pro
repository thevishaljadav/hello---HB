# Asia Drama release rules.
# WebView JavaScript bridge methods are invoked by name from JS.
-keepclassmembers class com.hellobaroda.navratri.MainActivity2$NativeBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class com.hellobaroda.navratri.MainActivity2$NativeBridge { *; }
-keep class com.hellobaroda.navratri.PatchActivity { *; }

# Keep Android components discoverable from the manifest and preserve line information for crash reports.
-keepattributes *Annotation*,InnerClasses,EnclosingMethod,SourceFile,LineNumberTable

# Media3 uses consumer rules for its public APIs; do not strip the native player activity path.
-keep class androidx.media3.** { *; }
