#!/usr/bin/env python3
"""Check a small selection of public Common Crawl indexes for Hyrsylä school URLs.

Queries public indexes, reports URLs and HTTP metadata only. Does not retrieve
page bodies or personal information about pupils. Respectful: 1 req/3 seconds.
"""
import urllib.request,urllib.parse,urllib.error,json,time,datetime,os
HEAD={"User-Agent":"HyrsylanHistoricalArchiveResearch/1.0 (public CDX metadata, low request rate)","Accept":"application/json"}
INDEXES=["CC-MAIN-2013-20","CC-MAIN-2014-10","CC-MAIN-2015-18","CC-MAIN-2015-40"]
TARGETS=[
("Nummi-Pusulan koulusivut","www.nummi-pusula.fi/koulut/*"),
("Hyrsylä koulusivut (vanha parametri)","www.nummi-pusula.fi/koulut/default.asp?sivu=121*"),
("Poroilan Saunalahti","www.saunalahti.fi/poroila/*"),
("Poroilan DNA Internet","kotisivu.dnainternet.net/poroila/*")]
def fetch(url):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=22) as r:
   body=r.read(350000).decode("utf8",errors="replace")
   if not body.strip():return {"http":r.status,"records":[]}
   records=[json.loads(line) for line in body.splitlines() if line.strip()]
   return {"http":r.status,"records":[{k:x.get(k) for k in ("url","timestamp","status","mime","filename","offset","length") if k in x} for x in records]}
 except urllib.error.HTTPError as e:return {"http":e.code,"records":[]}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:120],"records":[]}
def main():
 os.makedirs("reports",exist_ok=True)
 out={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"method":"Common Crawl index only; not extracted document bodies","checks":[]}
 for index in INDEXES:
  for label,target in TARGETS:
   q=urllib.parse.urlencode({"url":target,"output":"json","filter":"status:200","collapse":"urlkey"})
   endpoint=f"https://index.commoncrawl.org/{index}-index?"+q
   d=fetch(endpoint)
   out["checks"].append({"index":index,"target":target,"label":label,**d})
   print(index,label,d.get("http",d.get("error")),"records",len(d["records"]),flush=True)
   for x in d["records"][:8]:print(" HIT",x.get("timestamp"),x.get("url"),flush=True)
   time.sleep(3)
 with open("reports/commoncrawl-legacy-pages.json","w",encoding="utf8") as f:
  json.dump(out,f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
