#!/usr/bin/env python3
"""Targeted public Wayback CDX search for the lost Hyrsylä school pages.

Tries index-normalization variants for archived ASP query-string routes
and early Saunalahti HTML paths. Index metadata only: no pupil content.
No proxies, spoofing or challenge bypass. Rate limited.
"""
from __future__ import annotations
import datetime,json,os,time,urllib.parse,urllib.request,urllib.error
HEAD={"User-Agent":"HyrsylanKouluHistoricalResearch/1.0 (+public archive indexing; respectful cadence)","Accept":"application/json"}
REQUESTS=[
 ("school query prefix ASP","http://www.nummi-pusula.fi/koulut/default.asp?*"),
 ("school ASP prefix","http://www.nummi-pusula.fi/koulut/default.asp"),
 ("school ASP /any","www.nummi-pusula.fi/koulut/default.asp*"),
 ("school Hyrsylä numeric 121 with query","http://www.nummi-pusula.fi/koulut/default.asp?sivu=121*"),
 ("school Hyrsylä parameter alternate","http://www.nummi-pusula.fi/koulut/default.asp?alasivu=176&kieli=246&sivu=121"),
 ("school legacy host mirror","http://nummi-pusula.fi/koulut/default.asp*"),
 ("Saunalahti directory all types","http://www.saunalahti.fi/poroila/*"),
 ("Saunalahti earlier pages link 1","http://www.saunalahti.fi/poroila/uudistettu.htm"),
 ("Saunalahti earlier pages link 2","http://www.saunalahti.fi/poroila/olli-perustiedot.htm"),
 ("Saunalahti domain variant","http://saunalahti.fi/poroila/*"),
]
def fetch(q):
  url="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode(q)
  req=urllib.request.Request(url,headers=HEAD)
  try:
   with urllib.request.urlopen(req,timeout=24) as r:
    data=r.read(430000)
    arr=json.loads(data)
    records=[dict(zip(arr[0],row)) for row in arr[1:]] if arr else []
    return {"http":r.status,"rows":records}
  except Exception as e:return {"error":type(e).__name__+": "+str(e)[:160],"rows":[]}
def main():
 os.makedirs("reports",exist_ok=True)
 report={"at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"queries":[]}
 for n,(label,url) in enumerate(REQUESTS):
  q={"url":url,"output":"json","fl":"timestamp,original,statuscode,mimetype","from":"1998","to":"2016","limit":"110","collapse":"urlkey"}
  if label.startswith("school"):q["filter"]="mimetype:text/html"
  else:q["filter"]="statuscode:200"
  result=fetch(q)
  row={"label":label,"query":url,**result};report["queries"].append(row)
  print(f"[{n+1}/{len(REQUESTS)}] {label}: {result.get('http',result.get('error'))}; {len(result['rows'])} distinct captures",flush=True)
  for r in result["rows"][:28]:
   print("  ENTRY",r.get("timestamp"),r.get("statuscode"),r.get("original")[:190],flush=True)
  time.sleep(2)
 with open("reports/lost-school-web-index.json","w",encoding="utf8") as f:json.dump(report,f,ensure_ascii=False,indent=2)
 print("Artifact contains original URLs and Wayback CDX capture metadata only.",flush=True)
if __name__=="__main__":main()
