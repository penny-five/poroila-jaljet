#!/usr/bin/env python3
"""Find archived HTML referenced by Olli Poroila's *actual* 2013 index.

All file names were transcribed from a preserved Wayback capture:
https://web.archive.org/web/20130701074848/http://kotisivu.dnainternet.net:80/poroila/tuntemuksiani.htm

Public metadata, no personal-data collection or bot-challenge bypass.
An empty response or timeout is NOT evidence of absence.
"""
import urllib.request,urllib.parse,urllib.error,json,time,datetime,os
HOST="http://kotisivu.dnainternet.net/poroila/"
PATHS=["tuntemuksiani-06-07.htm","tuntemuksiani-08-09.htm",
       "tuntemuksiani-12.htm","tukikirjeita.htm","hedelmavati.htm",
       "110404.htm","120829.htm","130114.htm","130525.htm",
       "130529.htm","130421.htm","130509.htm",
       "tuntemuksiani.htm"]
HEAD={"User-Agent":"HyrsylanHistoriatutkimus/1.0 (read-only public archive metadata; low rate)",
      "Accept":"application/json,text/plain;q=0.9"}
def req(url,timeout=14):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=timeout) as r:
   return {"status":r.status,"data":r.read(120000).decode("utf-8",errors="replace")}
 except urllib.error.HTTPError as e:return {"status":e.code,"error":f"HTTP {e.code}"}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:140]}
def check(path):
 url=HOST+path
 # A CDX exact hit confirms a real dated archive record, not necessarily content.
 cdx="https://web.archive.org/cdx/search/cdx?"+urllib.parse.urlencode({
    "url":url,"output":"json","fl":"timestamp,original,statuscode,mimetype",
    "limit":"15","from":"2000","to":"2016"})
 a=req(cdx);out={"path":path,"original":url,"cdx_status":a.get("status",a.get("error"))}
 if "data" in a:
  try:
   data=json.loads(a["data"]);out["cdx_captures"]=[dict(zip(data[0],row)) for row in data[1:]] if data else []
  except Exception as e:out["cdx_error"]=str(e)[:120]
 if not out.get("cdx_captures"):
  time.sleep(1)
  nearest="https://archive.org/wayback/available?"+urllib.parse.urlencode({"url":url,"timestamp":"20130701"})
  b=req(nearest,12)
  out["availability_status"]=b.get("status",b.get("error"))
  if "data" in b:
   try:
    j=json.loads(b["data"])
    out["closest"]=j.get("archived_snapshots",{}).get("closest",{})
   except Exception as e:out["availability_error"]=str(e)[:120]
 return out
def main():
 os.makedirs("reports",exist_ok=True)
 out={"checked_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "source":"2013 original HTML page's internal links","results":[]}
 for i,p in enumerate(PATHS):
  v=check(p);out["results"].append(v)
  hits=v.get("cdx_captures",[])
  available=v.get("closest",{})
  print(f'[{i+1}/{len(PATHS)}] {p}: CDX={v["cdx_status"]} captures={len(hits)} '
        f'closest={available.get("timestamp","none")} availability={v.get("availability_status","not needed")}',flush=True)
  for x in hits[:7]:
   print(" VERIFIED INDEX:",f'https://web.archive.org/web/{x["timestamp"]}/{x["original"]}',
         "status",x.get("statuscode"),flush=True)
  time.sleep(2)
 with open("reports/poroila-deep-html-hunt.json","w",encoding="utf8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
 print("Public record search complete. Empty index results may be incomplete.",flush=True)
if __name__=="__main__":main()
