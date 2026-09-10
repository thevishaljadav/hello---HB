package com.hellobaroda.navratri;

import android.app.*;
import android.os.*;
import android.content.*;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.*;
import android.view.inputmethod.InputMethodManager;
import android.widget.*;
import org.json.*;
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class MainActivity extends Activity {
    final int MAROON=Color.rgb(128,0,40), DEEP=Color.rgb(55,0,20), GOLD=Color.rgb(255,198,38), CREAM=Color.rgb(255,249,236), PINK=Color.rgb(175,0,52), WHITE=Color.WHITE, MUTED=Color.rgb(104,82,86);
    SupabaseApi api=new SupabaseApi(); ExecutorService io=Executors.newSingleThreadExecutor(); LinearLayout root,content; int day=1; String mode="queen",saveName="",saveBio=""; Uri selected; ImageView selectedPreview;
    int dp(float v){return (int)(v*getResources().getDisplayMetrics().density+0.5f);}
    TextView text(String s,float size,int color,boolean bold){TextView t=new TextView(this);t.setText(s);t.setTextSize(size);t.setTextColor(color);t.setPadding(dp(4),dp(5),dp(4),dp(5));if(bold)t.setTypeface(null,1);return t;}
    GradientDrawable bg(int color,float radius){GradientDrawable g=new GradientDrawable();g.setColor(color);g.setCornerRadius(dp(radius));return g;}
    Button button(String s){Button b=new Button(this);b.setText(s);b.setTextSize(14);b.setTextColor(WHITE);b.setAllCaps(false);b.setMinHeight(dp(48));b.setPadding(dp(16),dp(8),dp(16),dp(8));b.setBackground(bg(PINK,18));return b;}
    Button outline(String s){Button b=button(s);b.setTextColor(PINK);b.setBackground(bg(CREAM,18));b.setPadding(dp(12),dp(7),dp(12),dp(7));return b;}
    EditText field(String hint){EditText e=new EditText(this);e.setHint(hint);e.setTextSize(16);e.setSingleLine(true);e.setPadding(dp(14),0,dp(14),0);e.setBackground(bg(WHITE,14));return e;}
    LinearLayout row(){LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.HORIZONTAL);l.setGravity(Gravity.CENTER_VERTICAL);return l;}
    void addSpace(int h){Space s=new Space(this);content.addView(s,new LinearLayout.LayoutParams(1,dp(h)));}

    @Override public void onCreate(Bundle b){super.onCreate(b);getWindow().setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);showWelcome();}

    void shell(String heading,boolean bottom){
        root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(CREAM);
        LinearLayout top=row();top.setPadding(dp(8),dp(4),dp(8),dp(4));top.setBackgroundColor(DEEP);
        if(!heading.equals("Home")){Button back=new Button(this);back.setText("‹");back.setTextSize(30);back.setTextColor(WHITE);back.setBackgroundColor(Color.TRANSPARENT);back.setContentDescription("Back");back.setOnClickListener(v->home());top.addView(back,new LinearLayout.LayoutParams(dp(52),dp(60)));}
        TextView h=text(heading,20,WHITE,true);h.setGravity(Gravity.CENTER);top.addView(h,new LinearLayout.LayoutParams(0,dp(60),1));
        if(heading.equals("Home")){Button bell=new Button(this);bell.setText("🔔");bell.setTextSize(19);bell.setTextColor(WHITE);bell.setBackgroundColor(Color.TRANSPARENT);top.addView(bell,new LinearLayout.LayoutParams(dp(52),dp(60)));}
        root.addView(top);
        ScrollView sv=new ScrollView(this);sv.setFillViewport(true);content=new LinearLayout(this);content.setOrientation(LinearLayout.VERTICAL);content.setPadding(dp(14),dp(14),dp(14),dp(bottom?88:24));sv.addView(content);root.addView(sv,new LinearLayout.LayoutParams(-1,0,1));
        if(bottom)nav();setContentView(root);
    }

    void nav(){LinearLayout n=new LinearLayout(this);n.setOrientation(LinearLayout.HORIZONTAL);n.setGravity(Gravity.CENTER);n.setBackgroundColor(WHITE);String[] labels={"⌂\nHome","⌖\nGrounds","＋\nCreate","●\nChat","♙\nProfile"};for(int i=0;i<labels.length;i++){Button b=new Button(this);b.setText(labels[i]);b.setTextSize(10);b.setTextColor(DEEP);b.setAllCaps(false);b.setBackgroundColor(WHITE);final int x=i;if(x==0)b.setOnClickListener(v->home());if(x==1)b.setOnClickListener(v->grounds());if(x==2)b.setOnClickListener(v->create());if(x==3)b.setOnClickListener(v->community());if(x==4)b.setOnClickListener(v->profile());n.addView(b,new LinearLayout.LayoutParams(0,dp(64),1));}root.addView(n,new LinearLayout.LayoutParams(-1,dp(64)));}

    void showWelcome(){
        shell("",false);content.setPadding(dp(20),dp(18),dp(20),dp(18));
        LinearLayout brand=new LinearLayout(this);brand.setOrientation(LinearLayout.VERTICAL);brand.setGravity(Gravity.CENTER_HORIZONTAL);brand.setPadding(dp(12),dp(18),dp(12),dp(12));brand.setBackground(bg(MAROON,30));
        TextView logo=text("👑  Hello! Baroda  👸",30,GOLD,true);logo.setGravity(Gravity.CENTER);brand.addView(logo);TextView sub=text("NAVRATRI • PEOPLE • PLACES • CULTURE",12,WHITE,true);sub.setGravity(Gravity.CENTER);brand.addView(sub);brand.addView(text("Garba Connect • Celebrate Baroda",18,WHITE,true));content.addView(brand,new LinearLayout.LayoutParams(-1,dp(205)));
        addSpace(22);TextView welcome=text("Same City\nDifferent Vibes\nOne Navratri",26,DEEP,true);welcome.setGravity(Gravity.CENTER);content.addView(welcome);addSpace(18);
        Button start=button("Get Started  →");content.addView(start,new LinearLayout.LayoutParams(-1,dp(56)));start.setOnClickListener(v->modeChoice());addSpace(10);
        Button have=outline("I Already Have an Account");content.addView(have,new LinearLayout.LayoutParams(-1,dp(52)));have.setOnClickListener(v->showLogin());
    }

    void modeChoice(){
        shell("Choose Your Mode",false);TextView s=text("Play your Navratri. Your way.",14,MUTED,false);s.setGravity(Gravity.CENTER);content.addView(s);addSpace(10);
        LinearLayout q=modeCard("👸","QUEEN MODE","Grace • Garba • Community",PINK);content.addView(q,new LinearLayout.LayoutParams(-1,dp(205)));q.setOnClickListener(v->{mode="queen";showLogin();});addSpace(14);
        LinearLayout k=modeCard("👑","KING MODE","Energy • Garba • Brotherhood",Color.rgb(244,171,0));content.addView(k,new LinearLayout.LayoutParams(-1,dp(205)));k.setOnClickListener(v->{mode="king";showLogin();});addSpace(18);
        TextView quote=text("“Same City • Different Vibes • One Navratri • Hello! Baroda”",15,PINK,true);quote.setGravity(Gravity.CENTER);content.addView(quote);
    }
    LinearLayout modeCard(String icon,String name,String desc,int color){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setGravity(Gravity.CENTER);c.setPadding(dp(12),dp(10),dp(12),dp(10));c.setBackground(bg(color,28));TextView i=text(icon,66,WHITE,true);i.setGravity(Gravity.CENTER);c.addView(i);TextView n=text(name,20,WHITE,true);n.setGravity(Gravity.CENTER);c.addView(n);TextView d=text(desc,12,WHITE,false);d.setGravity(Gravity.CENTER);c.addView(d);return c;}

    void showLogin(){
        shell("",false);content.setPadding(dp(20),dp(10),dp(20),dp(20));
        TextView logo=text("👑 Hello! Baroda 👸",28,PINK,true);logo.setGravity(Gravity.CENTER);content.addView(logo);TextView sub=text("Vadodara • Navratri Community",16,DEEP,true);sub.setGravity(Gravity.CENTER);content.addView(sub);TextView line=text("Real online community • people • places • Garba",13,MUTED,false);line.setGravity(Gravity.CENTER);content.addView(line);addSpace(14);
        EditText email=field("Email address");content.addView(email,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(9);
        EditText pass=field("Password");pass.setInputType(129);content.addView(pass,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(9);
        EditText name=field("Your name (for new account)");content.addView(name,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(15);
        Button login=button("Login");content.addView(login,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(9);
        Button signup=outline("Create Account");content.addView(signup,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(15);
        TextView modeText=text(mode.equals("king")?"👑 KING MODE":"👸 QUEEN MODE",14,PINK,true);modeText.setGravity(Gravity.CENTER);content.addView(modeText);addSpace(8);
        Button change=outline("Change Mode");content.addView(change,new LinearLayout.LayoutParams(-1,dp(48)));change.setOnClickListener(v->modeChoice());
        login.setOnClickListener(v->auth(false,email.getText().toString(),pass.getText().toString(),name.getText().toString()));signup.setOnClickListener(v->auth(true,email.getText().toString(),pass.getText().toString(),name.getText().toString()));
    }

    void auth(boolean signup,String e,String p,String n){if(e.trim().isEmpty()||p.length()<6){toast("Enter a valid email and password (6+ characters)");return;}busy(true);io.execute(()->{boolean ok=signup?api.signUp(e.trim(),p,n.trim().isEmpty()?"Garba Friend":n.trim()):api.login(e.trim(),p);if(ok){JSONObject prof=api.loadProfile();saveName=prof.optString("full_name",n);saveBio=prof.optString("bio","");mode=prof.optString("mode",mode);day=prof.optInt("navratri_day",1);}runOnUiThread(()->{busy(false);if(ok)home();else toast(api.error);});});}
    void busy(boolean x){if(x)Toast.makeText(this,"Connecting to Hello! Baroda online…",Toast.LENGTH_SHORT).show();}

    void home(){
        shell("Home",true);
        LinearLayout hero=new LinearLayout(this);hero.setOrientation(LinearLayout.VERTICAL);hero.setPadding(dp(18),dp(16),dp(18),dp(16));hero.setBackground(bg(DEEP,24));
        TextView hi=text("Hello, "+(saveName.isEmpty()?"Garba Friend":saveName)+" 👋",14,GOLD,true);hero.addView(hi);TextView h=text("Day "+day+" • "+(mode.equals("king")?"KING MODE 👑":"QUEEN MODE 👸"),25,WHITE,true);hero.addView(h);hero.addView(text("Garba connect • celebrate Baroda",13,WHITE,false));content.addView(hero,new LinearLayout.LayoutParams(-1,dp(132)));
        addSpace(14);TextView dayTitle=text("Navratri Days",18,DEEP,true);content.addView(dayTitle);HorizontalScrollView hsv=new HorizontalScrollView(this);LinearLayout days=row();for(int i=1;i<=12;i++){Button d=button("Day "+i);d.setTextSize(11);d.setTextColor(i==day?DEEP:WHITE);d.setBackground(bg(i==day?GOLD:PINK,15));final int x=i;d.setOnClickListener(v->{day=x;saveProfile();home();});days.addView(d,new LinearLayout.LayoutParams(dp(72),dp(48)));Space sp=new Space(this);days.addView(sp,new LinearLayout.LayoutParams(dp(6),1));}hsv.addView(days);content.addView(hsv,new LinearLayout.LayoutParams(-1,dp(58)));
        addSpace(10);TextView explore=text("Explore",18,DEEP,true);content.addView(explore);
        LinearLayout actions=row();String[] a={"📍\nGrounds","🔥\nTrending","📅\nEvents","👥\nCommunity"};for(int i=0;i<a.length;i++){Button b=button(a[i]);b.setTextSize(12);b.setTextColor(i==2?DEEP:WHITE);b.setBackground(bg(i==2?GOLD:(i==1?PINK:MAROON),18));final int x=i;if(x==0)b.setOnClickListener(v->grounds());if(x==1)b.setOnClickListener(v->trending());if(x==3)b.setOnClickListener(v->community());actions.addView(b,new LinearLayout.LayoutParams(0,dp(70),1));if(i<3){Space sp=new Space(this);actions.addView(sp,new LinearLayout.LayoutParams(dp(6),1));}}content.addView(actions);
        addSpace(16);rowTitle("Popular Garba Grounds","See all",()->grounds());loadGroundPreview();addSpace(16);rowTitle("Community moments","View trending",()->trending());loadPosts(false);
    }
    void rowTitle(String a,String b,View.OnClickListener l){LinearLayout r=row();TextView t=text(a,18,DEEP,true);r.addView(t,new LinearLayout.LayoutParams(0,dp(42),1));Button more=outline(b);more.setTextSize(11);more.setOnClickListener(l);r.addView(more,new LinearLayout.LayoutParams(dp(95),dp(42)));content.addView(r);}

    void loadGroundPreview(){io.execute(()->{JSONArray a=api.venues();runOnUiThread(()->{if(a.length()==0){content.addView(card("📍  Garba grounds will appear here","Add verified/community-submitted venues from the Grounds screen."));return;}LinearLayout r=row();int n=Math.min(3,a.length());for(int i=0;i<n;i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;LinearLayout c=miniCard("📍",o.optString("name","Garba Ground"),o.optString("area","Vadodara"));r.addView(c,new LinearLayout.LayoutParams(0,dp(120),1));if(i<n-1){Space sp=new Space(this);r.addView(sp,new LinearLayout.LayoutParams(dp(7),1));}}content.addView(r);});});}
    LinearLayout miniCard(String icon,String name,String sub){LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(8),dp(8),dp(8),dp(8));c.setBackground(bg(WHITE,16));TextView i=text(icon,26,PINK,true);i.setGravity(Gravity.CENTER);c.addView(i);TextView n=text(name,13,DEEP,true);n.setMaxLines(2);c.addView(n);TextView s=text(sub,11,MUTED,false);c.addView(s);return c;}
    TextView card(String title,String sub){TextView t=text(title+"\n"+sub,14,DEEP,false);t.setPadding(dp(16),dp(14),dp(16),dp(14));t.setBackground(bg(WHITE,16));return t;}

    void grounds(){
        shell("Garba Grounds",true);TextView intro=text("📍 Vadodara Garba Grounds",22,DEEP,true);content.addView(intro);content.addView(text("Community-submitted directory. Verify details before visiting.",12,MUTED,false));addSpace(8);
        EditText search=field("🔎 Search grounds in Vadodara…");content.addView(search,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(9);LinearLayout filters=row();String[] f={"All","Popular","Nearby","A to Z"};for(String x:f){Button b=outline(x);b.setTextSize(11);filters.addView(b,new LinearLayout.LayoutParams(0,dp(44),1));}content.addView(filters);addSpace(8);
        io.execute(()->{JSONArray a=api.venues();runOnUiThread(()->renderGrounds(a,search));});
        Button add=button("＋ Add Ground");content.addView(add,new LinearLayout.LayoutParams(-1,dp(52)));add.setOnClickListener(v->addGround());
    }
    void renderGrounds(JSONArray a,EditText search){LinearLayout list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);content.addView(list,content.indexOfChild(search)+3,new LinearLayout.LayoutParams(-1,-2));Runnable render=()->{list.removeAllViews();String q=search.getText().toString().toLowerCase(Locale.ROOT).replace("🔎","").trim();int shown=0;for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;String name=o.optString("name","Venue"),area=o.optString("area","");if(!q.isEmpty()&&!name.toLowerCase(Locale.ROOT).contains(q)&&!area.toLowerCase(Locale.ROOT).contains(q))continue;shown++;LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(14),dp(12),dp(14),dp(12));c.setBackground(bg(WHITE,18));TextView n=text("📍 "+name,17,PINK,true);c.addView(n);c.addView(text(area+"\n"+o.optString("address","")+"\n"+(o.optBoolean("verified",false)?"✓ Verified":"Community submitted"),12,DEEP,false));list.addView(c,new LinearLayout.LayoutParams(-1,dp(112)));Space sp=new Space(this);list.addView(sp,new LinearLayout.LayoutParams(1,dp(8)));}if(shown==0)list.addView(card("No matching grounds","Try another venue or area, or add a ground."));};render.run();search.addTextChangedListener(new TextWatcher(){public void beforeTextChanged(CharSequence s,int st,int c,int a){}public void onTextChanged(CharSequence s,int st,int before,int count){render.run();}public void afterTextChanged(Editable e){}});}
    void addGround(){if(!api.isLoggedIn()){toast("Please login first");return;}LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);EditText n=field("Ground / venue name"),a=field("Address"),ar=field("Area in Vadodara"),de=field("Description");box.addView(n);addSpaceTo(box,7);box.addView(a);addSpaceTo(box,7);box.addView(ar);addSpaceTo(box,7);box.addView(de);new AlertDialog.Builder(this).setTitle("Add Garba Ground").setView(box).setNegativeButton("Cancel",null).setPositiveButton("Submit",(q,w)->io.execute(()->{boolean ok=api.addVenue(n.getText().toString().trim(),a.getText().toString().trim(),ar.getText().toString().trim(),de.getText().toString().trim());runOnUiThread(()->{toast(ok?"Ground added online":"Could not add ground: "+api.error);if(ok)grounds();});})).show();}
    void addSpaceTo(LinearLayout l,int h){Space s=new Space(this);l.addView(s,new LinearLayout.LayoutParams(1,dp(h)));}

    void create(){
        shell("Create Post",true);content.addView(text("Share your Navratri moment",23,DEEP,true));content.addView(text("Photos are uploaded to the online Hello! Baroda community.",13,MUTED,false));addSpace(10);
        LinearLayout photo=new LinearLayout(this);photo.setOrientation(LinearLayout.VERTICAL);photo.setGravity(Gravity.CENTER);photo.setPadding(dp(10),dp(10),dp(10),dp(10));photo.setBackground(bg(WHITE,20));selectedPreview=new ImageView(this);selectedPreview.setImageResource(android.R.drawable.ic_menu_camera);selectedPreview.setScaleType(ImageView.ScaleType.CENTER_INSIDE);photo.addView(selectedPreview,new LinearLayout.LayoutParams(-1,dp(180)));Button pick=outline("＋ Add Photo");photo.addView(pick,new LinearLayout.LayoutParams(-1,dp(48)));content.addView(photo);pick.setOnClickListener(v->{Intent i=new Intent(Intent.ACTION_OPEN_DOCUMENT);i.setType("image/*");i.addCategory(Intent.CATEGORY_OPENABLE);startActivityForResult(i,7);});addSpace(10);
        EditText cap=field("Write a caption…");cap.setSingleLine(false);cap.setMinLines(3);cap.setGravity(Gravity.TOP);content.addView(cap,new LinearLayout.LayoutParams(-1,dp(105)));addSpace(9);content.addView(text("Post as",13,MUTED,true));TextView modeTag=text(mode.equals("king")?"👑 KING MODE":"👸 QUEEN MODE",13,PINK,true);modeTag.setPadding(dp(14),dp(10),dp(14),dp(10));modeTag.setBackground(bg(WHITE,16));content.addView(modeTag);addSpace(12);
        Button post=button("Publish Online  ✦");content.addView(post,new LinearLayout.LayoutParams(-1,dp(54)));post.setOnClickListener(v->publish(cap.getText().toString().trim()));
    }
    void publish(String caption){if(caption.isEmpty()){toast("Write a caption first");return;}if(!api.isLoggedIn()){toast("Please login first");return;}busy(true);io.execute(()->{String path="";boolean ok=true;try{if(selected!=null){InputStream in=getContentResolver().openInputStream(selected);ByteArrayOutputStream out=new ByteArrayOutputStream();byte[] buf=new byte[8192];int n;while((n=in.read(buf))!=-1)out.write(buf,0,n);in.close();path=api.userId()+"/"+System.currentTimeMillis()+".jpg";ok=api.uploadImage(out.toByteArray(),"post_media",path);} }catch(Exception e){ok=false;api.error=e.getMessage();}if(ok)ok=api.addPost(caption,day,path);final boolean result=ok;runOnUiThread(()->{busy(false);toast(result?"Posted online 🎉":"Publish failed: "+api.error);if(result)home();});});}
    @Override protected void onActivityResult(int r,int c,Intent d){super.onActivityResult(r,c,d);if(r==7&&c==RESULT_OK&&d!=null){selected=d.getData();if(selectedPreview!=null)selectedPreview.setImageURI(selected);toast("Photo selected");}}

    void trending(){shell("🔥 Trending",true);content.addView(text("Trending Garba content",22,DEEP,true));content.addView(text("Discover moments shared by the Vadodara community.",13,MUTED,false));addSpace(10);loadPosts(true);}
    void loadPosts(boolean onlyTrending){io.execute(()->{JSONArray a=api.posts();runOnUiThread(()->{int limit=onlyTrending?20:8;for(int i=0;i<a.length()&&i<limit;i++){JSONObject o=a.optJSONObject(i);if(o==null)continue;addPostCard(o);}if(a.length()==0)content.addView(card("No posts yet","Be the first to share a Garba moment."));});});}
    void addPostCard(JSONObject o){String id=o.optString("id",""),cap=o.optString("caption","Garba moment"),media=o.optString("media_path","");int pd=o.optInt("navratri_day",0);LinearLayout c=new LinearLayout(this);c.setOrientation(LinearLayout.VERTICAL);c.setPadding(dp(12),dp(12),dp(12),dp(10));c.setBackground(bg(WHITE,20));TextView head=text((mode.equals("king")?"👑":"👸")+"  Community post  •  Day "+(pd>0?pd:"—"),13,PINK,true);c.addView(head);if(!media.isEmpty()){ImageView im=new ImageView(this);im.setScaleType(ImageView.ScaleType.CENTER_CROP);c.addView(im,new LinearLayout.LayoutParams(-1,dp(190)));loadImage(api.publicUrl("post_media",media),im);}TextView body=text(cap,16,DEEP,true);c.addView(body);LinearLayout acts=row();Button like=outline("♡ Like");Button comment=outline("💬 Comment");acts.addView(like,new LinearLayout.LayoutParams(0,dp(46),1));acts.addView(comment,new LinearLayout.LayoutParams(0,dp(46),1));like.setOnClickListener(v->io.execute(()->{boolean ok=api.like(id);runOnUiThread(()->toast(ok?"Like updated":"Like failed"));}));comment.setOnClickListener(v->commentsDialog(id));c.addView(acts);content.addView(c,new LinearLayout.LayoutParams(-1,-2));addSpace(10);}
    void loadImage(String url,ImageView target){io.execute(()->{try{HttpURLConnection c=(HttpURLConnection)new URL(url).openConnection();c.setConnectTimeout(10000);c.setReadTimeout(15000);InputStream in=c.getInputStream();final android.graphics.Bitmap b=android.graphics.BitmapFactory.decodeStream(in);in.close();runOnUiThread(()->{if(b!=null)target.setImageBitmap(b);});}catch(Exception ignored){}});}
    void commentsDialog(String postId){io.execute(()->{JSONArray a=api.comments(postId);runOnUiThread(()->{LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null)box.addView(text("• "+o.optString("body"),14,DEEP,false));}EditText e=field("Add a comment…");box.addView(e);new AlertDialog.Builder(this).setTitle("Comments").setView(box).setNegativeButton("Close",null).setPositiveButton("Post",(d,w)->io.execute(()->{boolean ok=api.addComment(postId,e.getText().toString().trim());runOnUiThread(()->toast(ok?"Comment added":"Comment failed"));})).show();});});}

    void days(){shell("Navratri Days",true);content.addView(text("Celebrate all 12 days",22,DEEP,true));content.addView(text("Choose a day to personalize your feed.",13,MUTED,false));addSpace(10);String[] names={"Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi"};for(int i=1;i<=12;i++){Button b=button("Day "+i+"  •  "+names[i-1]);if(i==day)b.setTextColor(DEEP);b.setBackground(bg(i==day?GOLD:PINK,16));content.addView(b,new LinearLayout.LayoutParams(-1,dp(52)));addSpace(7);final int x=i;b.setOnClickListener(v->{day=x;saveProfile();home();});}}

    void community(){shell("Community",true);content.addView(text("👥 Vadodara Garba Community",22,DEEP,true));content.addView(text("Share plans, Garba moments and helpful local information.",13,MUTED,false));addSpace(8);io.execute(()->{String cid=api.communityId();if(cid.isEmpty()){runOnUiThread(()->content.addView(card("Community is not available yet","The online community needs to be created in Supabase before chat can start.")));return;}api.joinCommunity(cid);JSONArray a=api.messages(cid);runOnUiThread(()->{for(int i=0;i<a.length();i++){JSONObject o=a.optJSONObject(i);if(o!=null){TextView m=text("• "+o.optString("body"),14,DEEP,false);m.setPadding(dp(14),dp(10),dp(14),dp(10));m.setBackground(bg(WHITE,14));content.addView(m);addSpace(6);}}EditText m=field("Message…");content.addView(m,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(8);Button send=button("Send Message");content.addView(send);send.setOnClickListener(v->{String body=m.getText().toString().trim();if(body.isEmpty())return;io.execute(()->{boolean ok=api.sendMessage(cid,body);runOnUiThread(()->{toast(ok?"Message sent online":"Send failed: "+api.error);if(ok)community();});});});});});}

    void profile(){shell("My Profile",true);LinearLayout avatar=new LinearLayout(this);avatar.setOrientation(LinearLayout.VERTICAL);avatar.setGravity(Gravity.CENTER);avatar.setPadding(dp(12),dp(14),dp(12),dp(14));avatar.setBackground(bg(DEEP,24));TextView av=text(mode.equals("king")?"👑":"👸",48,GOLD,true);av.setGravity(Gravity.CENTER);avatar.addView(av);TextView n0=text(saveName.isEmpty()?"Garba Friend":saveName,22,WHITE,true);n0.setGravity(Gravity.CENTER);avatar.addView(n0);TextView md=text("Garba • Culture • Vadodara",12,WHITE,false);md.setGravity(Gravity.CENTER);avatar.addView(md);content.addView(avatar,new LinearLayout.LayoutParams(-1,dp(145)));addSpace(12);
        LinearLayout modes=row();Button king=button("👑 King Mode"),queen=outline("♕ Queen Mode");modes.addView(king,new LinearLayout.LayoutParams(0,dp(48),1));modes.addView(queen,new LinearLayout.LayoutParams(0,dp(48),1));content.addView(modes);king.setOnClickListener(v->{mode="king";saveProfile();profile();});queen.setOnClickListener(v->{mode="queen";saveProfile();profile();});addSpace(12);
        EditText name=field("Your name");name.setText(saveName);content.addView(name,new LinearLayout.LayoutParams(-1,dp(54)));addSpace(8);EditText bio=field("Bio");bio.setText(saveBio);bio.setSingleLine(false);bio.setMinLines(2);content.addView(bio,new LinearLayout.LayoutParams(-1,dp(82)));addSpace(10);Button save=button("Save Profile Online");content.addView(save);save.setOnClickListener(v->{saveName=name.getText().toString().trim();saveBio=bio.getText().toString().trim();saveProfile();toast("Profile saved online");});addSpace(10);Button logout=outline("Log Out");content.addView(logout);logout.setOnClickListener(v->{api.logout();saveName="";saveBio="";showWelcome();});}
    void saveProfile(){if(!api.isLoggedIn())return;io.execute(()->api.saveProfile(saveName,mode,day,saveBio));}

    void toast(String s){Toast.makeText(this,s==null?"Something went wrong":s,Toast.LENGTH_LONG).show();}
    @Override protected void onDestroy(){io.shutdownNow();super.onDestroy();}
}
