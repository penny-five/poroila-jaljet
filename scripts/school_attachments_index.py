#!/usr/bin/env python3
"""Search historical municipal education attachments through public Common Crawl metadata.

Only reports URL, timestamp and mime. Does not fetch student-made documents.
No bot circumvention and limited request cadence.
"""
import datetime,json,os,time,urllib.error,urllib.parse,urllib.request
INDEXES=["CC-MAIN-2013-20","CC-MAIN-2014-10","CC-MAIN-2015-18"]
PATTERNS=[
("Curriculum attachment","www.nummi-pusula.fi/koulut/Liitetiedostot/Yhteiset/Perusopetuksen*"),
("2012 welcome guide","www.nummi-pusula.fi/koulut/Liitetiedostot/Yhteiset/tervetuloa_kouluun2012.pdf"),
("2012 school entry form","www.nummi-pusula.fi/koulut/Liitetiedostot/Yhteiset/Kouluunilmoittautumislomake2012.pdf"),
("Any municipal school attachments","www.nummi-pusula.fi/koulut/Liitetiedostot/*")]
def get(url):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"HyrsylanHistoricalArchiveResearch/1.0 (public indexed captures)","Accept":"application/json"}),timeout=20) as r:
   return {"http":r.status,"records":[{k:v.get(k) for k in ("url","status","mime","timestamp","filename","offset","length") if k in v} for v in (json.loads(s) for s in r.read(300000).decode("utf8").splitlines() if s.strip())]}
 except urllib.error.HTTPError as e:return {"http":e.code,"records":[]}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:150],"records":[]}
def main():
 os.makedirs("reports",exist_ok=True)
 out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"results":[]}
 for idx in INDEXES:
  for label,pattern in PATTERNS:
   q=urllib.parse.urlencode({"url":pattern,"output":"json","filter":"status:200","collapse":"urlkey"})
   u=f"https://index.commoncrawl.org/{idx}-index?"+q
   r=get(u);out["results"].append({"index":idx,"label":label,"pattern":pattern,**r})
   print(idx,label,r.get("http",r.get("error")),"records",len(r["records"]),flush=True)
   for row in r["records"][:10]:print(" LINK",row["timestamp"],row["url"],flush=True)
   time.sleep(2)
 with open("reports/school-attachments-index.json","w",encoding="utf8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
if __name__=="__main__":main()
