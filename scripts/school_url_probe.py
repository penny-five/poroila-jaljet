#!/usr/bin/env python3
"""Find possible historical municipal school-site paths from public CDX index.

Queries known municipal www.nummi-pusula.fi/koulut URL; capture metadata only.
No guessing that returned sites belong to Hyrsylä without source links.
"""
import json,time,urllib.parse,urllib.request,urllib.error,os,datetime
TARGETS=[
 {"label":"www.nummi-pusula.fi/koulut/ (prefix)","url":"http://www.nummi-pusula.fi/koulut/","matchType":"prefix"},
 {"label":"www.nummi-pusula.fi/koulut (prefix)","url":"http://www.nummi-pusula.fi/koulut","matchType":"prefix"},
 {"label":"www.nummi-pusula.fi/koulut/ (exact)","url":"http://www.nummi-pusula.fi/koulut/","matchType":"exact"},
 {"label":"nummi-pusula.fi/koulut/ (prefix)","url":"http://nummi-pusula.fi/koulut/","matchType":"prefix"}
]
def go(t):
 args={"url":t["url"],"output":"json","matchType":t["matchType"],"fl":"timestamp,original,statuscode,mimetype","collapse":"urlkey","from":"1999","to":"2015","limit":"250","filter":"mimetype:text/html"}
 url="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(args)
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"PoroilaHistoricalArchiveResearch/1.0 (read-only public index)","Accept":"application/json"})
  with urllib.request.urlopen(req,timeout=35) as res:
   raw=res.read(450000)
   arr=json.loads(raw)
   return {"status":res.status,"records":[dict(zip(arr[0],row)) for row in arr[1:]] if arr else []}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:200],"records":[]}
def main():
 report={"checked_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"targets":[]}
 os.makedirs("reports",exist_ok=True)
 for i,t in enumerate(TARGETS):
  r=go(t);report["targets"].append({**t,**r})
  print(f'[{i+1}/{len(TARGETS)}] {t["label"]}: {len(r["records"])} records, {r.get("status",r.get("error"))}',flush=True)
  for entry in r["records"]:
   original=entry.get("original","")
   if "hyrs" in original.lower(): print("POTENTIAL HYRSYLÄ PATH:",original,"capture",entry.get("timestamp"),flush=True)
  if i==0:
   print("First 30 unique paths:",flush=True)
   for entry in r["records"][:30]: print(entry.get("original",""),flush=True)
  time.sleep(2)
 with open("reports/school-url-probe.json","w",encoding="utf-8") as f: json.dump(report,f,ensure_ascii=False,indent=2)
 print("Complete URL index saved as Actions artifact school-url-cdx-index.")
if __name__=="__main__":main()
