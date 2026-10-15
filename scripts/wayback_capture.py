#!/usr/bin/env python3
"""Read two known, publicly indexed historical Wayback captures.

Read-only Wayback replay. Does not evade bot challenges or restrictions.
Use public indexed captures only. Keep full extraction in workflow artifact,
not publicly printed to GitHub logs; avoid republishing personal data.
"""
from html.parser import HTMLParser
from urllib import request, error
import json, os, re, hashlib, datetime, time

CAPTURES=[
 ("etusivu", "20130629214829", "http://kotisivu.dnainternet.net:80/poroila/"),
 ("tuntemuksiani", "20130701074848", "http://kotisivu.dnainternet.net:80/poroila/tuntemuksiani.htm"),
]
HDR={"User-Agent":"PoroilaHistoricalArchiveResearch/1.0 (read-only, public capture; rate-limited)",
     "Accept":"text/html,application/xhtml+xml;q=0.9,*/*;q=0.6"}
class Extractor(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True)
  self.skip=0;self.parts=[];self.headings=[];self.links=[];self.title="";self.activeheading="";self.active_title=False;self.active_anchor=None
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag in ("script","style","noscript","svg","iframe"):self.skip+=1
  if self.skip:return
  if tag=="title":self.active_title=True
  if tag in ("h1","h2","h3","h4"):self.activeheading=tag
  if tag=="a":self.active_anchor={"href":attrs.get("href",""),"text":""}
  if tag in ("p","div","li","br","tr","h1","h2","h3","td"):self.parts.append("\n")
 def handle_endtag(self,tag):
  if tag in ("script","style","noscript","svg","iframe"):
   self.skip=max(0,self.skip-1);return
  if self.skip:return
  if tag=="title":self.active_title=False
  if tag in ("h1","h2","h3","h4"):self.activeheading=""
  if tag=="a" and self.active_anchor:
   self.links.append(self.active_anchor)
   self.active_anchor=None
  if tag in ("p","li","h1","h2","h3"):self.parts.append("\n")
 def handle_data(self,data):
  if self.skip:return
  text=data.strip()
  if not text:return
  if self.active_title:self.title+=" "+text
  elif self.activeheading:self.headings.append({"level":self.activeheading,"text":text})
  if self.active_anchor:self.active_anchor["text"]+=" "+text
  self.parts.append(data+" ")

def get(url):
 try:
  req=request.Request(url,headers=HDR)
  with request.urlopen(req,timeout=30) as res:
   body=res.read(850_000)
   ctype=res.headers.get("Content-Type","")
   charset=res.headers.get_content_charset()
   if not charset:
    match=re.search(rb'<meta[^>]*charset\s*=\s*["\']?([\w-]+)',body,re.I)
    charset=match.group(1).decode("ascii","ignore") if match else "windows-1252"
   for coding in [charset,"utf-8","windows-1252"]:
    try:html=body.decode(coding);break
    except (UnicodeError, LookupError):continue
   return {"status":res.status, "content_type":ctype,"charset":charset,
           "effective_url":res.url,"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"html":html}
 except error.HTTPError as e:return {"status":e.code,"error":"HTTP "+str(e.code),"retry_after":e.headers.get("Retry-After")}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:280]}
def main():
 os.makedirs("reports",exist_ok=True)
 doc={"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"records":[]}
 for i,(label,ts,original) in enumerate(CAPTURES):
  item={"label":label,"timestamp":ts,"original":original}
  for suffix in ("id_/",""):
   url="https://web.archive.org/web/"+ts+suffix+original
   r=get(url)
   item["tried_url"]=url
   item["response"]={k:v for k,v in r.items() if k!="html"}
   if "html" in r:
    e=Extractor()
    e.feed(r["html"])
    text="\n".join(" ".join(line.split()) for line in "".join(e.parts).split("\n"))
    text="\n".join(line for line in text.split("\n") if line).strip()
    item["title"]=e.title.strip()
    item["headings"]=e.headings[:30]
    item["links"]=e.links[:200]
    item["text"]=text[:55000]
    item["truncated"]=len(text)>55000
    print("FOUND",label,"HTTP",r["status"],"bytes",r["bytes"],"title",item["title"][:140], "headings",len(e.headings),"links",len(e.links),flush=True)
    print("TOP HEADINGS",json.dumps(item["headings"][:8],ensure_ascii=False),flush=True)
    break
   else:
    print("ATTEMPT",label,r,flush=True)
   time.sleep(3)
  doc["records"].append(item)
  time.sleep(3)
 with open("reports/wayback-capture-text.json","w",encoding="utf-8") as f:json.dump(doc,f,ensure_ascii=False,indent=2)
 print("Capture text stored in downloadable workflow artifact (not printed in job logs).",flush=True)
if __name__=="__main__":main()
