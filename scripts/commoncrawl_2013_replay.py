#!/usr/bin/env python3
"""Read one previously indexed 2013 Common Crawl capture, no crawling.

Archive metadata and WARC record belong to Common Crawl's public CC-MAIN-2013-20
collection. Extract only title, school URL paths, and short Hyrsylä-name context.
Do not store or publish student-identifying prose or full page HTML.
"""
import gzip,io,json,re,os,datetime,urllib.request,urllib.parse,urllib.error
from html.parser import HTMLParser
HDR={"User-Agent":"HyrsylanKouluHistoricalResearch/1.0 (public indexed WARC, low volume)"}
class Scrape(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.skip=0;self.title="";self.in_title=False;self.links=[];self.a=None;self.text=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ("style","script","noscript","svg"):self.skip+=1
  if self.skip:return
  if t=="title":self.in_title=True
  if t=="a":self.a={"href":a.get("href",""),"text":""}
  if t in ("p","div","h1","h2","br","li","td","tr"):self.text.append(" ")
 def handle_endtag(self,t):
  if t in ("style","script","noscript","svg"):self.skip=max(0,self.skip-1);return
  if self.skip:return
  if t=="title":self.in_title=False
  if t=="a" and self.a:self.links.append(self.a);self.a=None
  if t in ("p","div","h1","h2","li","td","tr"):self.text.append(" ")
 def handle_data(self,t):
  if self.skip:return
  if self.in_title:self.title+=t
  if self.a:self.a["text"]+=t
  self.text.append(t)
def download(u,headers={}):
 req=urllib.request.Request(u,headers={**HDR,**headers})
 with urllib.request.urlopen(req,timeout=35) as response:
  return response.status,response.read(750000),response.headers.get("Content-Type","")
def main():
 out={"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_index":"CC-MAIN-2013-20"}
 q=urllib.parse.urlencode({"url":"www.nummi-pusula.fi/koulut/*","output":"json","filter":"status:200","collapse":"urlkey"})
 url="https://index.commoncrawl.org/CC-MAIN-2013-20-index?"+q
 try:
  http,body,ctype=download(url)
  entries=[json.loads(s) for s in body.decode("utf8").splitlines() if s.strip()]
  target=next((x for x in entries if "koulut/default.asp" in x.get("url","")),None)
  if not target:raise RuntimeError("2013 archive index returned no school homepage entry")
  out["capture_metadata"]={k:target.get(k) for k in ("url","timestamp","status","mime","filename","offset","length")}
  print("INDEX",out["capture_metadata"],flush=True)
  start=int(target["offset"]);length=int(target["length"])
  if length>700000:raise RuntimeError("WARC record too long; not retrieved")
  warc_url="https://data.commoncrawl.org/"+target["filename"]
  status,data,ctype=download(warc_url,{"Range":f"bytes={start}-{start+length-1}"})
  out["warc_http_status"]=status;out["warc_download_size"]=len(data)
  if status!=206:raise RuntimeError(f"Expected HTTP 206 byte range, received {status}")
  unpacked=gzip.decompress(data)
  # WARC headers, HTTP response headers and HTML body each have a separator.
  parts=unpacked.split(b"\r\n\r\n",2)
  if len(parts)<3:parts=unpacked.split(b"\n\n",2)
  if len(parts)<3:raise RuntimeError("Unexpected WARC record envelope")
  doc=parts[2]
  html=doc.decode("windows-1252",errors="replace")
  p=Scrape();p.feed(html)
  text=" ".join("".join(p.text).split())
  out["page_title"]=" ".join(p.title.split())
  out["html_bytes"]=len(doc);out["link_count"]=len(p.links)
  out["hyrsylan_mentions"]=len(list(re.finditer("hyrsyl",text,re.I)))
  out["hyrsylan_context"]=[text[max(0,m.start()-90):m.start()+140] for m in list(re.finditer("hyrsyl",text,re.I))[:8]]
  out["school_related_links"]=[{"href":a["href"],"label":" ".join(a["text"].split())[:90]} for a in p.links if ("hyrs" in (a["href"]+a["text"]).lower() or "/koulut/" in a["href"].lower())][:45]
  out["contains_personal_data_review_required"]=True
  print("REPLAY",json.dumps({k:v for k,v in out.items() if k not in ("school_related_links","hyrsylan_context")},ensure_ascii=False),flush=True)
  print("HYRSYLÄ CONTEXT:",json.dumps(out["hyrsylan_context"],ensure_ascii=False),flush=True)
  print("SCHOOL LINKS:",json.dumps(out["school_related_links"],ensure_ascii=False)[:4800],flush=True)
 except Exception as e:
  out["error"]=type(e).__name__+": "+str(e)[:280]
  print("ERROR:",out["error"],flush=True)
 os.makedirs("reports",exist_ok=True)
 with open("reports/commoncrawl-2013-school-replay.json","w",encoding="utf8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
