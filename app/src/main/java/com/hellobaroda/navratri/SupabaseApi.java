package com.hellobaroda.navratri;

import org.json.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class SupabaseApi {
  public static final String BASE="https://wevutronudkcqbzmverf.supabase.co";
  public static final String KEY="sb_publishable_St3gO8iFD5Y5DyepQuzS_w_tAbcvTD1";
  private String token="";
  private String userId="";
  public String error="";
  public boolean isLoggedIn(){return token.length()>0&&userId.length()>0;}
  public String userId(){return userId;}
  private String request(String method,String path,String body,String auth) throws Exception{
    HttpURLConnection c=(HttpURLConnection)new URL(BASE+path).openConnection();
    c.setRequestMethod(method); c.setConnectTimeout(12000); c.setReadTimeout(15000);
    c.setRequestProperty("apikey",KEY); c.setRequestProperty("Accept","application/json");
    if(auth!=null&&!auth.isEmpty()) c.setRequestProperty("Authorization","Bearer "+auth);
    if(body!=null){c.setDoOutput(true);c.setRequestProperty("Content-Type","application/json");c.getOutputStream().write(body.getBytes(StandardCharsets.UTF_8));}
    int code=c.getResponseCode(); InputStream in=code>=200&&code<300?c.getInputStream():c.getErrorStream(); String out=read(in);
    if(code<200||code>=300) throw new Exception(out); return out;
  }
  private String read(InputStream in)throws Exception{if(in==null)return "";BufferedReader r=new BufferedReader(new InputStreamReader(in,StandardCharsets.UTF_8));StringBuilder b=new StringBuilder();String s;while((s=r.readLine())!=null)b.append(s);return b.toString();}
  private JSONObject obj(String s){try{return new JSONObject(s);}catch(Exception e){return new JSONObject();}}
  public synchronized boolean signUp(String email,String password,String name){
    try{String r=request("POST","/auth/v1/signup",new JSONObject().put("email",email).put("password",password).put("data",new JSONObject().put("full_name",name)).toString(),"");
      JSONObject o=obj(r); JSONObject u=o.optJSONObject("user");
      if(o.optString("access_token").length()>0&&u!=null){token=o.optString("access_token");userId=u.optString("id");ensureProfile(name);error="";return true;}
      error="Account created. Check your email to confirm, then log in."; return false;
    }catch(Exception e){error=e.getMessage();return false;}
  }
  public synchronized boolean login(String email,String password){try{String r=request("POST","/auth/v1/token?grant_type=password",new JSONObject().put("email",email).put("password",password).toString(),"");JSONObject o=obj(r);token=o.optString("access_token");JSONObject u=o.optJSONObject("user");userId=u==null?"":u.optString("id");if(token.length()>0&&userId.length()>0){loadProfile();return true;}error="Login failed.";return false;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized void logout(){token="";userId="";}
  public synchronized JSONObject ensureProfile(String name){try{return new JSONObject(request("POST","/rest/v1/profiles?on_conflict=id",new JSONObject().put("id",userId).put("full_name",name).toString(),token));}catch(Exception e){return new JSONObject();}}
  public synchronized JSONObject loadProfile(){try{JSONArray a=new JSONArray(request("GET","/rest/v1/profiles?id=eq."+URLEncoder.encode(userId,"UTF-8")+"&select=*",null,token));return a.length()>0?a.getJSONObject(0):new JSONObject();}catch(Exception e){return new JSONObject();}}
  public synchronized boolean saveProfile(String name,String mode,int day,String bio){try{request("POST","/rest/v1/profiles?on_conflict=id",new JSONObject().put("id",userId).put("full_name",name).put("mode",mode).put("navratri_day",day).put("bio",bio).put("updated_at",new java.util.Date().toInstant().toString()).toString(),token);return true;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized JSONArray venues(){try{return new JSONArray(request("GET","/rest/v1/venues?select=*&order=created_at.desc",null,token));}catch(Exception e){error=e.getMessage();return new JSONArray();}}
  public synchronized boolean addVenue(String name,String address,String area,String desc){try{request("POST","/rest/v1/venues",new JSONObject().put("name",name).put("address",address).put("area",area).put("description",desc).put("created_by",userId).toString(),token);return true;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized JSONArray posts(){try{return new JSONArray(request("GET","/rest/v1/posts?select=*&order=created_at.desc&limit=50",null,token));}catch(Exception e){error=e.getMessage();return new JSONArray();}}
  public synchronized boolean addPost(String caption,int day){return addPost(caption,day,"");}
  public synchronized boolean addPost(String caption,int day,String mediaPath){try{JSONObject o=new JSONObject().put("user_id",userId).put("caption",caption).put("navratri_day",day);if(mediaPath!=null&&!mediaPath.isEmpty())o.put("media_path",mediaPath).put("media_type","image");request("POST","/rest/v1/posts",o.toString(),token);return true;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized boolean like(String postId){try{request("POST","/rest/v1/likes",new JSONObject().put("post_id",postId).put("user_id",userId).toString(),token);return true;}catch(Exception e){try{request("DELETE","/rest/v1/likes?post_id=eq."+URLEncoder.encode(postId,"UTF-8")+"&user_id=eq."+URLEncoder.encode(userId,"UTF-8"),null,token);return true;}catch(Exception x){error=x.getMessage();return false;}}}
  public synchronized JSONArray comments(String postId){try{return new JSONArray(request("GET","/rest/v1/comments?post_id=eq."+URLEncoder.encode(postId,"UTF-8")+"&order=created_at.asc",null,token));}catch(Exception e){return new JSONArray();}}
  public synchronized boolean addComment(String postId,String body){try{request("POST","/rest/v1/comments",new JSONObject().put("post_id",postId).put("user_id",userId).put("body",body).toString(),token);return true;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized String communityId(){try{JSONArray a=new JSONArray(request("GET","/rest/v1/conversations?name=eq.Vadodara%20Garba%20Community&select=id",null,token));if(a.length()>0)return a.getJSONObject(0).optString("id");}catch(Exception ignored){}return "";}
  public synchronized boolean joinCommunity(String cid){try{request("POST","/rest/v1/conversation_members",new JSONObject().put("conversation_id",cid).put("user_id",userId).toString(),token);return true;}catch(Exception e){return false;}}
  public synchronized JSONArray messages(String cid){try{return new JSONArray(request("GET","/rest/v1/messages?conversation_id=eq."+URLEncoder.encode(cid,"UTF-8")+"&order=created_at.asc&limit=100",null,token));}catch(Exception e){return new JSONArray();}}
  public synchronized boolean sendMessage(String cid,String body){try{request("POST","/rest/v1/messages",new JSONObject().put("conversation_id",cid).put("user_id",userId).put("body",body).toString(),token);return true;}catch(Exception e){error=e.getMessage();return false;}}
  public synchronized boolean uploadImage(byte[] bytes,String bucket,String path){try{HttpURLConnection c=(HttpURLConnection)new URL(BASE+"/storage/v1/object/"+bucket+"/"+URLEncoder.encode(path,"UTF-8")).openConnection();c.setRequestMethod("POST");c.setDoOutput(true);c.setConnectTimeout(15000);c.setReadTimeout(30000);c.setRequestProperty("apikey",KEY);c.setRequestProperty("Authorization","Bearer "+token);c.setRequestProperty("Content-Type","image/jpeg");c.setRequestProperty("x-upsert","true");c.getOutputStream().write(bytes);int code=c.getResponseCode();if(code<200||code>=300)throw new Exception(read(c.getErrorStream()));return true;}catch(Exception e){error=e.getMessage();return false;}}
  public String publicUrl(String bucket,String path){return BASE+"/storage/v1/object/public/"+bucket+"/"+path;}
}
