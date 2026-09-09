package com.hellobaroda.navratri;

import android.app.*;import android.os.*;import android.graphics.*;import android.view.*;import android.content.*;import android.widget.*;import java.util.*;

public class MainActivity extends Activity {
  NavView v;
  @Override public void onCreate(Bundle b){super.onCreate(b);v=new NavView(this);setContentView(v);}
  void inputDialog(String title,String hint){EditText e=new EditText(this);e.setHint(hint);new AlertDialog.Builder(this).setTitle(title).setView(e).setNegativeButton("Cancel",null).setPositiveButton("Save",(d,w)->Toast.makeText(this,"Saved locally",Toast.LENGTH_SHORT).show()).show();}
  class NavView extends View{
    Paint p=new Paint(3);int screen=0;boolean king=false;int day=3;float dx,dy;
    String[] tabs={"⌂","⌖","⊕","◯","♙"};String[] names={"Home","Grounds","Create","Chat","Profile"};
    int maroon=Color.rgb(88,0,29),deep=Color.rgb(55,0,20),gold=Color.rgb(255,198,38),cream=Color.rgb(255,249,235),pink=Color.rgb(125,0,39),muted=Color.rgb(105,82,91);
    NavView(Context c){super(c);setBackgroundColor(cream);}
    void bg(Canvas c,float w,float h){p.setShader(new LinearGradient(0,0,0,360,deep,Color.rgb(145,0,42),Shader.TileMode.CLAMP));c.drawRect(0,0,w,360,p);p.setShader(null);}
    void rr(Canvas c,float l,float t,float r,float b,int col,float rad){p.setColor(col);c.drawRoundRect(l,t,r,b,rad,rad,p);}
    void text(Canvas c,String s,float x,float y,float z,int col,boolean bold){p.setColor(col);p.setTextSize(z);p.setTypeface(Typeface.create("sans",bold?1:0));c.drawText(s,x,y,p);}
    void center(Canvas c,String s,float x,float y,float z,int col,boolean bold){p.setTextSize(z);p.setTypeface(Typeface.create("sans",bold?1:0));p.setColor(col);c.drawText(s,x-p.measureText(s)/2,y,p);}
    @Override protected void onDraw(Canvas c){super.onDraw(c);float w=getWidth(),h=getHeight();if(screen==0){bg(c,w,h);home(c,w,h);}else{c.drawColor(cream);header(c,screen==1?"Garba Grounds":screen==2?"Create":screen==3?"Community":"My Profile");if(screen==1)grounds(c,w,h);if(screen==2)create(c,w,h);if(screen==3)chat(c,w,h);if(screen==4)profile(c,w,h);}bottom(c,w,h);}
    void header(Canvas c,String title){text(c,"‹",18,47,38,Color.WHITE,false);text(c,title,57,43,21,Color.WHITE,true);text(c,"⋮",getWidth()-35,44,26,Color.WHITE,true);}
    void home(Canvas c,float w,float h){
      text(c,"Hello Baroda",18,35,20,Color.WHITE,true);text(c,"Vadodara  •  Navratri",18,57,10,0xFFFFE5B4,false);text(c,"♧",w-34,45,18,Color.WHITE,true);
      center(c,king?"KING MODE":"QUEEN MODE",w/2,95,14,Color.WHITE,true);center(c,king?"Energy • Garba • Brotherhood":"Grace • Garba • Community",w/2,115,10,0xFFFFD777,false);
      // Hero panel
      rr(c,14,135,w-14,318,0xFFFFE9C7,22);center(c,"NAVRATRI",w/2,160,11,pink,true);center(c,"Day "+day,w/2,205,34,pink,true);center(c,"Garba  •  People  •  Places  •  Culture",w/2,227,10,muted,false);
      rr(c,27,245,w-27,285,pink,20);center(c,"Explore today's Garba  →",w/2,270,12,Color.WHITE,true);
      // visual festival tile
      rr(c,14,330,w-14,462,Color.BLACK,18);p.setShader(new RadialGradient(w/2,382,170,0xFF7A0040,0xFF18000B,Shader.TileMode.CLAMP));c.drawRect(14,330,w-14,462,p);p.setShader(null);
      center(c,"✦  GARBA NIGHT  ✦",w/2,370,13,0xFFFFD56A,true);center(c,king?"Energy • Dance • Brotherhood":"Grace • Dance • Celebration",w/2,395,17,Color.WHITE,true);center(c,"Vadodara",w/2,420,11,0xFFFFE8BD,false);
      // quick actions
      quick(c,14,478,(w-42)/4,548,"⌖","Grounds");quick(c,24+(w-42)/4,478,2*(w-42)/4+24,548,"♨","Trending");quick(c,34+2*(w-42)/4,478,3*(w-42)/4+34,548,"★","Events");quick(c,44+3*(w-42)/4,478,w-14,548,"♣","Community");
      text(c,"Popular Garba Grounds",16,580,16,deep,true);text(c,"See All  ›",w-72,580,11,pink,true);
      smallGround(c,16,595,(w-46)/3,680,"UNITED WAY");smallGround(c,24+(w-46)/3,595,2*(w-46)/3+24,680,"LAXMI VILAS");smallGround(c,32+2*(w-46)/3,595,w-16,680,"ALEMBIC");
    }
    void quick(Canvas c,float l,float t,float r,float b,String icon,String label){rr(c,l,t,r,b,Color.WHITE,18);center(c,icon,(l+r)/2,t+30,20,pink,true);center(c,label,(l+r)/2,t+53,9,deep,true);}
    void smallGround(Canvas c,float l,float t,float r,float b,String name){rr(c,l,t,r,b,Color.WHITE,14);rr(c,l+4,t+4,r-4,t+40,maroon,10);center(c,"✦",(l+r)/2,t+29,18,gold,true);center(c,name,(l+r)/2,t+56,8,deep,true);center(c,"Popular",(l+r)/2,t+69,7,muted,false);}
    void grounds(Canvas c,float w,float h){rr(c,16,65,w-16,108,Color.WHITE,22);text(c,"⌕  Search grounds in Vadodara...",30,92,12,muted,false);String[] f={"All","Popular","Nearby","A to Z"};float x=18;for(String s:f){float rw=62;rr(c,x,122,x+rw,154,s.equals("All")?gold:Color.WHITE,17);center(c,s,x+rw/2,143,10,deep,true);x+=rw+7;}text(c,"Vadodara Garba directory",18,184,17,deep,true);text(c,"Verified information can be added by the community.",18,204,10,muted,false);String[] n={"United Way Garba","Laxmi Vilas Ground","Alembic Ground","Nyay Mandir Ground","Gotri Garba Ground"};int y=220;for(String s:n){rr(c,16,y,w-16,y+82,Color.WHITE,16);rr(c,25,y+10,112,y+70,maroon,12);center(c,"✦",68,y+47,24,gold,true);text(c,s,124,y+30,13,deep,true);text(c,"Vadodara  •  Garba",124,y+49,9,muted,false);rr(c,124,y+58,196,y+75,0xFFFFE8B0,9);center(c,"View details",160,y+70,8,pink,true);text(c,"♡",w-40,y+35,20,pink,false);y+=92;}}
    void create(Canvas c,float w,float h){text(c,"Share your Navratri moment",18,92,20,deep,true);text(c,"Photos, videos and Garba memories",18,115,11,muted,false);rr(c,16,140,w-16,280,Color.WHITE,20);center(c,"＋",w/2,205,44,pink,true);center(c,"Add photo / video",w/2,232,13,pink,true);rr(c,16,300,w-16,350,pink,20);center(c,"Create Post",w/2,331,13,Color.WHITE,true);}
    void chat(Canvas c,float w,float h){String[] rows={"Vadodara Garba Lovers","United Way Group","King Mode Crew","Queen Mode Circle","Photography Hub"};int y=72;for(String s:rows){rr(c,16,y,w-16,y+62,Color.WHITE,15);rr(c,26,y+10,70,y+54,maroon,22);center(c,"✦",48,y+39,16,gold,true);text(c,s,82,y+27,13,deep,true);text(c,"Community conversation",82,y+45,9,muted,false);y+=72;}rr(c,16,h-140,w-16,h-88,pink,20);center(c,"＋  New conversation",w/2,h-107,13,Color.WHITE,true);}
    void profile(Canvas c,float w,float h){center(c,king?"♛":"♕",w/2,105,54,gold,true);center(c,"Guest",w/2,142,20,deep,true);center(c,"Garba  |  Culture  |  Vadodara",w/2,162,10,muted,false);rr(c,16,184,w-16,234,Color.WHITE,18);center(c,"Login / Create account",w/2,215,12,pink,true);String[] rows={"♡  My Bookmarks","▣  My Posts","★  My Events","♧  Invite Friends","⚙  Settings","?  Help & Support"};int y=270;for(String s:rows){text(c,s,28,y,13,deep,true);text(c,"›",w-35,y,18,muted,false);y+=48;}}
    void bottom(Canvas c,float w,float h){float top=h-68;rr(c,0,top,w,h,Color.WHITE,0);for(int i=0;i<5;i++){float x=w*(i+.5f)/5;int col=screen==i?pink:muted;center(c,tabs[i],x,top+27,17,col,true);center(c,names[i],x,top+47,7,col,screen==i);}}
    @Override public boolean onTouchEvent(MotionEvent e){if(e.getAction()==0){dx=e.getX();dy=e.getY();return true;}if(e.getAction()==1){float x=e.getX(),y=e.getY(),w=getWidth(),h=getHeight();if(y>h-82){screen=Math.min(4,(int)(x/(w/5)));invalidate();return true;}if(screen==0&&y>470&&y<560){if(x<w/2)screen=1;else screen=1;invalidate();return true;}if(screen==0&&y>175&&y<300){day++;if(day>12)day=1;invalidate();return true;}if(screen==0&&y>545&&y<625){king=x<w/2;invalidate();return true;}if(screen==1&&y>h-180){inputDialog("Add Ground","Ground name / verified details");return true;}if(screen==4&&y>175&&y<245){inputDialog("Login / Create account","Email or phone");return true;}return true;}return true;}
  }
}"}