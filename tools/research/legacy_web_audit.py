#!/usr/bin/env python3
"""Hyrsylän koulun and Poroila's historical websites: link-level audit.

Uses public Internet Archive replay and CDX endpoints only. No bot challenge bypass.
Extracts *navigation structure and capture metadata*, not school children's work,
names or personal data. Avoids turning unsourced links into factual claims.
"""
from __future__ import annotations
import datetime,json,os,re,time,urllib.parse,urllib.request,urllib.error
from html.parser import HTMLParser

CAPTURES=[
 ("Hyrsylän koulun kunnallinen sivukartta 2011","20111129034532","http://www.nummi-pusula.fi:80/koulut/sivukartta.asp?kieli=246"),
 ("Olli Poroilan etusivu 2001","20010622055404","http://www.saunalahti.fi:80/poroila/"),
 ("Olli Poroilan etusivu 2013","20130629214829","http://kotisivu.dnainternet.net:80/poroila/"),
]
TEST_PATHS=[
 ("Poroilan vanha perusteet-sivu", "http://www.saunalahti.fi/poroila/olli-perustiedot.htm"),
 ("Poroilan vanha uudistettu-sivu", "http://www.saunalahti.fi/poroila/uudistettu.htm"),
 ("Hyrsylän koulun oma sivu", "http://www.nummi-pusula.fi/koulut/default.asp?sivu=121&alasivu=121&kieli=246"),
 ("Hyrsylän kouluelämää", "http://www.nummi-pusula.fi/koulut/default.asp?sivu=121&alasivu=176&kieli=246"),
 ("Japanilainen viikko", "http://www.nummi-pusula.fi/koulut/default.asp?sivu=121&alasivu=219&kieli=246"),
 ("Hyrsylän oppilaskunta", "http://www.nummi-pusula.fi/koulut/default.asp?sivu=121&alasivu=144&kieli=246"),
 ("Vanha Peda.net -oppimisympäristö", "http://www.peda.net/veraja/nummi-pusula/koulujalukio"),
]
HEAD={"User-Agent":"HyrsylanKouluHistoricalResearch/1.0 (public archive, low rate)","Accept":"application/json,text/html;q=0.9"}
class Links(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.skip=0;self.links=[];self.anchor=None;self.title="";self.in_title=False
 def handle_starttag(self,tag,attrs):
  if tag in ("script","style","noscript","svg"):self.skip+=1
  if self.skip:return
  attrs=dict(attrs)
  if tag=="title":self.in_title=True
  if tag=="a":self.anchor={"href":attrs.get("href",""),"label":""}
 def handle_endtag(self,tag):
  if tag in ("script","style","noscript","svg"):self.skip=max(self.skip-1,0);return
  if self.skip:return
  if tag=="title":self.in_title=False
  if tag=="a" and self.anchor is not None:
   self.links.append({k:" ".join(v.split()) for k,v in self.anchor.items()})
   self.anchor=None
 def handle_data(self,data):
  if self.skip:return
  if self.in_title:self.title+=data
  if self.anchor is not None:self.anchor["label"]+=data
def fetch(url,byteslimit=900000):
 req=urllib.request.Request(url,headers=HEAD)
 try:
  with urllib.request.urlopen(req,timeout=25) as r:
   return {"http_status":r.status,"effective_url":r.url,"body":r.read(byteslimit),"content_type":r.headers.get("Content-Type","")}
 except urllib.error.HTTPError as e:return {"http_status":e.code,"error":"HTTP "+str(e.code)}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:160]}
def replay(label,ts,original):
 u=f"https://web.archive.org/web/{ts}id_/{original}"
 r=fetch(u)
 d={"label":label,"archive_url":u,**{k:v for k,v in r.items() if k!="body"}}
 if "body" in r:
  raw=r["body"]
  # HTML was generally authored in Western European encodings.
  text=raw.decode("windows-1252",errors="replace")
  p=Links();p.feed(text)
  d["page_title"]=" ".join(p.title.split())
  d["link_count"]=len(p.links)
  if "sivukartta" in original:
   # Only retain the navigational entries starting at Hyrsylän koulu until Ikkalan koulu.
   first=next((i for i,e in enumerate(p.links) if e["label"].lower()=="hyrsylän koulu"),-1)
   end=next((i for i in range(first+1,len(p.links)) if p.links[i]["label"].lower()=="ikkalan koulu"),-1) if first>=0 else -1
   d["hyrsylan_section_nav"]=p.links[first:end] if first>=0 and end>first else []
  elif "2001" in label:
   d["historical_links"]=[e for e in p.links if e["href"]][:30]
  else:
   d["historical_links"]=[e for e in p.links if any(w in (e["label"]+" "+e["href"]).lower() for w in ("sisään","tuntemuksiani","archive","saunalahti"))][:10]
 return d
def cdx(label,original):
 q={"url":original,"output":"json","fl":"timestamp,original,statuscode,mimetype","filter":"statuscode:200","limit":"20","from":"1996","to":"2016"}
 endpoint="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(q)
 r=fetch(endpoint,180000)
 d={"label":label,"original":original,**{k:v for k,v in r.items() if k!="body"}}
 if "body" in r:
  try:
   a=json.loads(r["body"])
   d["captures"]=[dict(zip(a[0],v)) for v in a[1:]] if a else []
  except Exception as e:d["parse_error"]=str(e)[:100]
 return d
def main():
 os.makedirs("reports",exist_ok=True)
 report={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"navigation":[],"targets":[]}
 for label,ts,url in CAPTURES:
  d=replay(label,ts,url);report["navigation"].append(d)
  print("REPLAY",label,"status",d.get("http_status",d.get("error")),"title",d.get("page_title",""),"links",d.get("link_count",0),flush=True)
  if d.get("hyrsylan_section_nav"):
   print("HYRSYLÄ SCHOOL HISTORICAL MENU:",flush=True)
   for a in d["hyrsylan_section_nav"]:print(" MENU",repr(a["label"]),a["href"],flush=True)
  if d.get("historical_links"):print(" LINKS",json.dumps(d["historical_links"],ensure_ascii=False)[:1100],flush=True)
  time.sleep(2)
 for label,url in TEST_PATHS:
  d=cdx(label,url);report["targets"].append(d)
  print("CDX",label,"status",d.get("http_status",d.get("error")),"captures",len(d.get("captures",[])),flush=True)
  for row in d.get("captures",[])[:6]:print(" CAPTURE",row["timestamp"],row["original"],flush=True)
  time.sleep(3)
 with open("reports/legacy-web-audit.json","w",encoding="utf-8") as f:json.dump(report,f,ensure_ascii=False,indent=2)
 print("Complete source navigation and public capture metadata saved in Actions artifact.",flush=True)
if __name__=="__main__":main()
