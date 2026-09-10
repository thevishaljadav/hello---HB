package com.hellobaroda.navratri;

import android.content.Context;
import android.content.SharedPreferences;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public class SupabaseClient {
  private static final String URL = "https://wevutronudkcqbzmverf.supabase.co";
  private static final String KEY = "sb_publishable_St3gO8iFD5Y5DyepQuzS_w_tAbcvTD1";
  private final SharedPreferences sp;
  public SupabaseClient(Context c){sp=c.getSharedPreferences("hb_online",0);}
  public String token(){return sp.getString("token","");}
  public boolean loggedIn(){return !token().isEmpty();}
  private String request(String method,String path,String body,String auth) throws Exception{
    HttpURLConnection c=(HttpURLConnection)new URL(URL+path).openConnection();
    c.setRequestMethod(method); c.setRequestProperty("apikey",KEY); c.setRequestProperty("Content-Type","application/json"); c.setRequestProperty("Accept","application/json");
    if(auth!=null&&!auth.isEmpty())c.setRequestProperty("Authorization","Bearer "+auth);
    if(body!=null){c.setDoOutput(true);try(OutputStream o=c.getOutputStream()){o.write(body.getBytes(StandardCharsets.UTF_8));}}
    InputStream in=c.getResponseCode()<400?c.getInputStream():c.getErrorStream();
    ByteArrayOutputStream b=new ByteArrayOutputStream();byte[] x=new byte[4096];int n;while((n=in.read(x))!=-1)b.write(x,0,n);String out=b.toString("UTF-8");
    if(c.getResponseCode()>=400)throw new IOException(out);return out;
  }
  public String signUp(String email,String password,String name) throws Exception{
    JSONObject o=new JSONObject();o.put("email",email);o.put("password",password);JSONObject d=new JSONObject();d.put("full_name",name);o.put("data",d);
    return request("POST","/auth/v1/signup",o.toString(),"");
  }
  public String signIn(String email,String password) throws Exception{
    JSONObject o=new JSONObject();o.put("email",email);o.put("password",password);
    String r=request("POST","/auth/v1/token?grant_type=password",o.toString(),"");JSONObject j=new JSONObject(r);String t=j.optString("access_token","");
    if(t.isEmpty())throw new IOException("Login did not return a session");sp.edit().putString("token",t).putString("email",email).apply();return r;
  }
  public void signOut(){sp.edit().clear().apply();}
  public JSONArray venues() throws Exception{return new JSONArray(request("GET","/rest/v1/venues?select=*&order=created_at.desc",null,token()));}
  public JSONArray posts() throws Exception{return new JSONArray(request("GET","/rest/v1/posts?select=*&order=created_at.desc&limit=30",null,token()));}
  public void addVenue(String name,String address,String area) throws Exception{
    JSONObject o=new JSONObject();o.put("name",name);o.put("address",address);o.put("area",area);o.put("submitted_by",userId());
    request("POST","/rest/v1/venues",o.toString(),token());
  }
  public String createPost(String caption,int day,String mode) throws Exception{
    JSONObject o=new JSONObject();o.put("caption",caption);o.put("navratri_day",day);o.put("mode",mode);o.put("author_id",userId());
    return request("POST","/rest/v1/posts",o.toString(),token());
  }
  public String userId() throws Exception{return new JSONObject(request("GET","/auth/v1/user",null,token())).getString("id");}
  public void updateProfile(String fullName,String username,String mode) throws Exception{
    String id=userId();JSONObject o=new JSONObject();o.put("full_name",fullName);o.put("username",username);o.put("mode",mode);
    request("PATCH","/rest/v1/profiles?id=eq."+URLEncoder.encode(id,"UTF-8"),o.toString(),token());
  }
}
