# Asia Drama release rules.
-keepclassmembers class com.hellobaroda.navratri.MainActivity2$NativeBridge {
    @android.webkit.JavascriptInterface <methods>;
}
-keep class com.hellobaroda.navratri.MainActivity2$NativeBridge { *; }
-keep class com.hellobaroda.navratri.PatchActivity { *; }
-keepattributes *Annotation*,InnerClasses,EnclosingMethod,SourceFile,LineNumberTable
-keep class androidx.media3.** { *; }
