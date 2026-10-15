#!/usr/bin/env python3
"""Secondary web archive probe at Arquivo.pt public metadata APIs.

Read-only, rate limited; no challenge circumvention, identities or page bodies.
A lack of results is not evidence that the original pages never existed.
"""
import datetime,json,os,time,urllib.parse,urllib.request,urllib.error
TERMS=[
 ("Poroilan Saunalahti",{"versionHistory":"www.saunalahti.fi/poroila/"}),
 ("Poroilan DNA Internet",{"versionHistory":"kotisivu.dnainternet.net/poroila/"}),
 ("Nummi-Pusulan koulut",{"versionHistory":"www.nummi-pusula.fi/koulut/"}),
 ("Hyrsylän koulun vanhat sivut",{"q":'"Hyrsylän koulu"'}),
 ("Poroila julkisissa arkistoissa",{"q":'"Olli Poroila"'})
]
HEAD={"Accept":"application/json","User-Agent":"HyrsylanSchoolDigitalHistory/1.0 (noncommercial, public metadata, low requests)"}
def get(params):
 url="https://arquivo.pt/textsearch?"+urllib.parse.urlencode({**params,"maxItems":12,"prettyPrint":"false"})
 req=urllib.request.Request(url,headers=HEAD)
 try:
  with urllib.request.urlopen(req,timeout=20) as r:
   raw=r.read(250000);data=json.loads(raw)
   found=data.get("response_items",[])
   return {"http":r.status,"estimated_matches":data.get("estimated_nr_results"),"hits":[{k:x.get(k) for k in ("title","originalURL","linkToArchive","tstamp","crawlDate")} for x in found]}
 except Exception as e:return {"error":type(e).__name__+": "+str(e)[:160],"hits":[]}
def main():
 os.makedirs("reports",exist_ok=True);out={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"queries":[]}
 for i,(label,params) in enumerate(TERMS):
  x=get(params);out["queries"].append({"label":label,"params":params,**x})
  print(f'[{i+1}/{len(TERMS)}] {label}: {x.get("http",x.get("error"))}; hits {len(x["hits"])}',flush=True)
  for item in x["hits"][:7]:print(" CAPTURE",item.get("originalURL"),item.get("linkToArchive"),flush=True)
  time.sleep(3)
 with open("reports/arquivo-secondary-archive.json","w",encoding="utf8") as f:json.dump(out,f,ensure_ascii=False,indent=2)
 print("Archive index research completed; empty results do not imply absence.",flush=True)
if __name__=="__main__":main()
