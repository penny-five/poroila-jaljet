#!/usr/bin/env python3
"""Recover four *documented* school subpage links from Wayback CDX.

Public history only; records exact archived URLs, timestamps and short contextual
metadata, no bypass, no wholesale republishing of pupil-identifying page texts.
"""
import json,datetime,os,re,time,urllib.request,urllib.parse,urllib.error
from html.parser import HTMLParser
PAGES=[("Hyrsylän koulu","121"),("Hyrsylän Vanhemmat","160"),("Kouluelämää","176"),("Japanilainen viikko Hyrsylän koulussa","219")]
BASE="http://www.nummi-pusula.fi:80/koulut/default.asp?"
HEADERS={"User-Agent":"PoroilaHistoricalArchiveResearch/1.0 (rate limited public archive review)","Accept":"application/json,text/html;q=0.8"}
class Parser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.skip=0;self.words=[];self.title="";self.intitle=False;self.links=[];self.active=None
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if tag in ("script","style","svg","noscript"):self.skip+=1
  if self.skip:return
  if tag=="title":self.intitle=True
  if tag=="a":self.active={"href":d.get("href",""),"text":""}
  if tag in ("p","li","div","br","tr","td","h1","h2","h3"):self.words.append(" ")
 def handle_endtag(self,tag):
  if tag in ("script","style","svg","noscript"):self.skip=max(0,self.skip-1);return
  if self.skip:return
  if tag=="title":self.intitle=False
  if tag=="a" and self.active:self.links.append(self.active);self.active=None
  if tag in ("p","li","h1","h2","h3"):self.words.append(" ")
 def handle_data(self,t):
  if self.skip:return
  if self.intitle:self.title+=t
  if self.active:self.active["text"]+=t
  self.words.append(t)
def fetch(u,accept_size=100000):
 req=urllib.request.Request(u,headers=HEADERS)
 try:
  with urllib.request.urlopen(req,timeout=25) as r:
   b=r.read(accept_size)
   return {"status":r.status,"data":b,"effective_url":r.url,"ctype":r.headers.get("Content-Type","")}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:190]}
def process(label,alasivu):
 url=BASE+urllib.parse.urlencode({"sivu":121,"alasivu":alasivu,"kieli":246})
 q="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode({"url":url,"output":"json","fl":"timestamp,original,statuscode,mimetype","filter":"statuscode:200","from":"2000","to":"2015","limit":"50"})
 record={"label":label,"source_url":url}
 r=fetch(q,220000);record["cdx_status"]=r.get("status",r.get("error"))
 if "data" not in r:return record
 try:
  arr=json.loads(r["data"]);record["captures"]=[dict(zip(arr[0],item)) for item in arr[1:]] if arr else []
 except Exception as e:
  record["parse_error"]=str(e)[:150];return record
 for c in record["captures"][:1]:
  u=f'https://web.archive.org/web/{c["timestamp"]}id_/{c["original"]}'
  page=fetch(u,350000)
  record["capture_url"]=u
  record["capture_status"]=page.get("status",page.get("error"))
  if "data" in page:
   h=page["data"].decode("windows-1252",errors="replace")
   p=Parser();p.feed(h);s=" ".join("".join(p.words).split())
   record["title"]=" ".join(p.title.split())
   record["html_bytes"]=len(page["data"])
   record["content_chars"]=len(s)
   record["hyrsylan_mentions"]=len(re.findall("hyrsyl",s,re.I))
   record["poroila_mentions"]=len(re.findall("poroila",s,re.I))
   record["relevant_links"]=[a for a in p.links if "hyrs" in (a["href"]+" "+a["text"]).lower()][:20]
   # Short text extract for reporting, no bulk republication of the page body.
   record["public_context"]=s[:500]
 return record
def main():
 os.makedirs("reports",exist_ok=True);out={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":[]}
 for label,num in PAGES:
  r=process(label,num);out["results"].append(r)
  print(label,"CDX",r.get("cdx_status"),"captures",len(r.get("captures",[])),"replay",r.get("capture_status"),"title",r.get("title","")[:120],"mention Poroila",r.get("poroila_mentions",0),flush=True)
  for c in r.get("captures",[])[:6]:print(" capture:",f'https://web.archive.org/web/{c["timestamp"]}/{c["original"]}',flush=True)
  time.sleep(3)
 with open("reports/hyrsylan-pages.json","w",encoding="utf-8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
