package com.hellobaroda.navratri;

import android.app.*;import android.os.*;import android.graphics.*;import android.graphics.drawable.*;import android.view.*;import android.view.inputmethod.InputMethodManager;import android.content.*;import android.widget.*;import java.util.*;

public class MainActivity extends Activity {
  NavView v;
  @Override public void onCreate(Bundle b){super.onCreate(b); v=new NavView(this); setContentView(v);}
  void inputDialog(String title,String hint){ final EditText e=new EditText(this); e.setHint(hint); new AlertDialog.Builder(this).setTitle(title).setView(e).setNegativeButton("Cancel",null).setPositiveButton("Save",(d,w)->{Toast.makeText(this,"Saved locally for this prototype",Toast.LENGTH_SHORT).show();}).show(); }

  class NavView extends View {
    Paint p=new Paint(3); int screen=0; boolean king=false; int day=1; float downX,downY;
    String[] tabs={"Home","Grounds","Create","Chat","Profile"};
    NavView(Context c){super(c); p.setTypeface(Typeface.create("sans",0)); setBackgroundColor(Color.rgb(255,247,231));}
    void rect(Canvas c,float l,float t,float r,float b,int color,float rad){p.setColor(color);c.drawRoundRect(l,t,r,b,rad,rad,p);}
    void txt(Canvas c,String s,float x,float y,float size,int color,boolean bold){p.setColor(color);p.setTextSize(size);p.setTypeface(Typeface.create("sans",bold?1:0));c.drawText(s,x,y,p);}
    void center(Canvas c,String s,float x,float y,float size,int color,boolean bold){p.setTextSize(size);p.setTypeface(Typeface.create("sans",bold?1:0));p.setColor(color);c.drawText(s,x-p.measureText(s)/2,y,p);}
    @Override protected void onDraw(Canvas c){super.onDraw(c); float w=getWidth(),h=getHeight();
      p.setShader(new LinearGradient(0,0,w,420,Color.rgb(70,0,25),Color.rgb(135,0,31),Shader.TileMode.CLAMP)); c.drawRect(0,0,w,420,p); p.setShader(null);
      if(screen==0) home(c,w,h); else if(screen==1) grounds(c,w,h); else if(screen==2) create(c,w,h); else if(screen==3) chat(c,w,h); else profile(c,w,h); bottom(c,w,h);
    }
    void header(Canvas c,String title){txt(c,"‹",20,48,36,Color.WHITE,false);txt(c,title,58,45,22,Color.WHITE,true);}
    void home(Canvas c,float w,float h){
      txt(c,"Hello Baroda",20,42,25,Color.WHITE,true);txt(c,"Vadodara • Navratri",20,68,14,0xFFFFE6B5,false);txt(c,"◉",w-48,48,22,Color.WHITE,false);
      center(c,king?"KING MODE":"QUEEN MODE",w/2,120,17,Color.WHITE,true); center(c,king?"Energy • Garba • Brotherhood":"Grace • Garba • Community",w/2,145,13,0xFFFFD979,false);
      rect(c,18,170,w-18,355,0xFFF8E7C9,24); center(c,"NAVRATRI",w/2,204,15,0xFF85001F,true); center(c,"Day "+day, w/2,250,42,0xFF85001F,true); center(c,"Garba • People • Places • Culture",w/2,280,14,0xFF5A2535,false);
      rect(c,32,302,w-32,340,0xFF85001F,18);center(c,"Explore today's Garba",w/2,327,14,Color.WHITE,true);
      txt(c,"Popular this season",20,390,19,0xFF210812,true);
      card(c,20,412,w/2-10,535,"Garba Grounds","Discover verified venue information",0xFF85001F);
      card(c,w/2+5,412,w-20,535,"Trending","Photos and community posts",0xFFB47A00);
      txt(c,"Choose your mode",20,570,18,0xFF210812,true);
      rect(c,20,590,w/2-8,638,king?0xFFFFC928:0xFFFFFFFF,18); center(c,"KING MODE",(20+w/2-8)/2,620,13,0xFF3A0014,true);
      rect(c,w/2+8,590,w-20,638,!king?0xFFFFC928:0xFFFFFFFF,18); center(c,"QUEEN MODE",(w/2+8+w-20)/2,620,13,0xFF3A0014,true);
    }
    void card(Canvas c,float l,float t,float r,float b,String a,String btxt,int accent){rect(c,l,t,r,b,Color.WHITE,18);p.setColor(accent);c.drawRect(l,t,l+7,b,p);txt(c,a,l+18,t+35,16,0xFF210812,true);txt(c,btxt,l+18,t+60,11,0xFF6B5360,false);txt(c,"Open ›",l+18,b-18,12,accent,true);}
    void grounds(Canvas c,float w,float h){header(c,"Garba Grounds"); rect(c,18,75,w-18,120,Color.WHITE,22);txt(c,"⌕  Search grounds in Vadodara...",34,103,14,0xFF806A72,false);txt(c,"Verified ground directory",20,153,18,0xFF210812,true);txt(c,"Add venue information as it is verified.",20,178,12,0xFF806A72,false);
      empty(c,205,"No ground data added yet","Use Add Ground to build your Vadodara directory."); rect(c,20,h-160,w-20,h-105,0xFF85001F,22);center(c,"+  Add Ground",w/2,h-125,15,Color.WHITE,true);
    }
    void empty(Canvas c,float y,String a,String b){rect(c,20,y,getWidth()-20,y+150,Color.WHITE,20);center(c,"◎",getWidth()/2,y+52,34,0xFFB47A00,true);center(c,a,getWidth()/2,y+84,15,0xFF210812,true);center(c,b,getWidth()/2,y+108,11,0xFF806A72,false);}
    void create(Canvas c,float w,float h){header(c,"Create");txt(c,"Share a Navratri moment",20,100,23,0xFF210812,true);txt(c,"Keep it Garba-related and community-focused.",20,128,13,0xFF806A72,false);rect(c,20,155,w-20,250,Color.WHITE,20);center(c,"＋",w/2,205,40,0xFF85001F,true);center(c,"Add photo / video",w/2,232,14,0xFF85001F,true);rect(c,20,270,w-20,320,0xFF85001F,20);center(c,"Create post",w/2,302,15,Color.WHITE,true);txt(c,"You can connect this screen to your preferred photo storage and backend later.",20,350,w>400?12:11,0xFF806A72,false);}
    void chat(Canvas c,float w,float h){header(c,"Community");String[] rows={"Garba Community","My Ground","King Mode","Queen Mode","Photography Hub"};float y=85;for(String s:rows){rect(c,20,y,w-20,y+58,Color.WHITE,16);txt(c,"●",35,y+36,20,0xFF85001F,true);txt(c,s,65,y+27,15,0xFF210812,true);txt(c,"Tap to open conversation",65,y+45,10,0xFF806A72,false);y+=68;}rect(c,20,h-160,w-20,h-105,0xFF85001F,20);center(c,"+  New conversation",w/2,h-125,15,Color.WHITE,true);}
    void profile(Canvas c,float w,float h){header(c,"My Profile");center(c,king?"♛":"♕",w/2,130,62,0xFFFFC928,true);center(c,"Guest",w/2,170,22,0xFF210812,true);center(c,"Hello Baroda • Navratri",w/2,194,12,0xFF806A72,false);rect(c,20,220,w-20,270,Color.WHITE,18);center(c,"Login / Create account",w/2,252,14,0xFF85001F,true);txt(c,"Your saved grounds, posts and communities will appear here.",20,315,13,0xFF806A72,false);}
    void bottom(Canvas c,float w,float h){float top=h-72;rect(c,0,top,w,h,Color.WHITE,0);for(int i=0;i<5;i++){float x=w*(i+.5f)/5;int col=screen==i?0xFF85001F:0xFF806A72;center(c,tabs[i],x,top+40,10,col,screen==i);}}
    @Override public boolean onTouchEvent(android.view.MotionEvent e){if(e.getAction()==0){downX=e.getX();downY=e.getY();return true;}if(e.getAction()==1){float x=e.getX(),y=e.getY();float h=getHeight(),w=getWidth();
      if(y>h-90){screen=Math.min(4,(int)(x/(w/5)));invalidate();return true;}
      if(screen==0 && y>585){king=x<w/2;invalidate();return true;}
      if(screen==1 && y>h-190){inputDialog("Add Ground","Ground name / verified details");return true;}
      if(screen==4 && y>200&&y<300){inputDialog("Login / Create account","Email or phone");return true;}
      if(screen==0 && y>165&&y<360){day++;if(day>12)day=1;invalidate();return true;}
      return true;}return true;}
  }
}
