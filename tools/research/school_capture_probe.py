#!/usr/bin/env python3
"""Review selected historical municipal school pages in Wayback; metadata only.

No bot protections bypassed; public captures only.
Stores titles, keyword match contexts and matching links for human review.
"""
import json,os,re,time,datetime,urllib.request,urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin
TARGETS=[
("school_index_2008","20081203121419","http://www.nummi-pusula.fi:80/koulut/default.asp?"),
("school_default_2012","20120428202652","http://www.nummi-pusula.fi:80/koulut/default.asp?sivu=126&alasivu=126&kieli=246"),
("school_default_2013","20130511090520","http://www.nummi-pusula.fi:80/koulut/default.asp?sivu=153&alasivu=153&kieli=246"),
("school_default_htm_2012","20120217090852","http://www.nummi-pusula.fi/koulut/Default.htm"),
("school_sitemap_2011","20111129034532","http://www.nummi-pusula.fi:80/koulut/sivukartta.asp?kieli=246"),
("school_events_2011","20111129034607","http://www.nummi-pusula.fi:80/koulut/tapahtumat.asp?tyyppi=vanhat&kieli=246"),
]
class Html(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.skip=0;self.parts=[];self.links=[];self.a=None;self.title="";self.intitle=False
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ("script","style","noscript","svg"):self.skip+=1
  if self.skip:return
  if tag=="title":self.intitle=True
  if tag=="a":self.a={"href":d.get("href",""),"text":""}
  if tag in ("div","p","br","li","td","tr","h1","h2","h3"):self.parts.append(" ")
 def handle_endtag(self,tag):
  if tag in ("script","style","noscript","svg"):self.skip=max(self.skip-1,0);return
  if self.skip:return
  if tag=="title":self.intitle=False
  if tag=="a" and self.a:self.links.append(self.a);self.a=None
  if tag in ("p","li","h1","h2","h3"):self.parts.append(" ")
 def handle_data(self,data):
  if self.skip:return
  if self.intitle:self.title+=data
  if self.a:self.a["text"]+=data
  self.parts.append(data+" ")
def get(ts,orig):
 u=f"https://web.archive.org/web/{ts}id_/{orig}"
 req=urllib.request.Request(u,headers={"User-Agent":"PoroilaHistoricalArchiveResearch/1.0 (public historic records)", "Accept":"text/html"})
 try:
  with urllib.request.urlopen(req,timeout=25) as res:
   data=res.read(450000)
   cset=res.headers.get_content_charset() or "windows-1252"
   try:s=data.decode(cset,errors="replace")
   except LookupError:s=data.decode("windows-1252",errors="replace")
   return {"status":res.status,"bytes":len(data),"effective_url":res.url,"html":s}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:200]}
def main():
 records=[];os.makedirs("reports",exist_ok=True)
 for label,ts,url in TARGETS:
  result={"label":label,"timestamp":ts,"original":url};r=get(ts,url);result.update({k:v for k,v in r.items() if k!="html"})
  if "html" in r:
   p=Html();p.feed(r["html"]);s=" ".join("".join(p.parts).split())
   result["title"]=" ".join(p.title.split())
   result["hyrsylan_match_count"]=len(list(re.finditer("hyrsyl",s,re.I)))
   result["hyrsylan_contexts"]=[s[max(0,m.start()-100):min(len(s),m.end()+180)] for m in list(re.finditer("hyrsyl",s,re.I))[:12]]
   result["school_links"]=[a for a in p.links if any(key in (a["href"]+" "+a["text"]).lower() for key in ("hyrs","koulu","peruskou","school"))][:60]
   result["link_count"]=len(p.links)
   # only limited public text on municipal index pages, never full page text in artifacts
   result["text_preview"]=s[:550] if "hyrsyl" not in s.lower() else ""
  records.append(result)
  print(label,"status",result.get("status",result.get("error")),"title",result.get("title","")[:110],"Hyrsylä matches",result.get("hyrsylan_match_count",0),"links",result.get("link_count",0),flush=True)
  for a in result.get("school_links",[])[:10]:print(" RELATED LINK",a["href"][:180],a["text"][:60],flush=True)
  time.sleep(2)
 with open("reports/school-archive-page-summary.json","w",encoding="utf-8") as f:
  json.dump({"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"pages":records},f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
