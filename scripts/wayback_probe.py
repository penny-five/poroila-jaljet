#!/usr/bin/env python3
"""Respectful Wayback/CDX metadata probe for Poroila historical URLs.

Public API only. No proxy rotation, browser impersonation or challenge bypass.
Does not publish page bodies, potentially sensitive data or scraped HTML.
"""
from __future__ import annotations
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib import error, parse, request

TARGETS = [
    {"label": "Alkuperäinen Saunalahti-sivusto / alisivut", "url": "http://www.saunalahti.fi/poroila/", "scope": "prefix"},
    {"label": "Alkuperäinen Saunalahti-sivusto / etusivu", "url": "http://www.saunalahti.fi/poroila/", "scope": "exact"},
    {"label": "Saunalahti ilman www-alkua", "url": "http://saunalahti.fi/poroila/", "scope": "prefix"},
    {"label": "DNA Internet / tukikirjeet", "url": "http://kotisivu.dnainternet.net/poroila/tukikirjeita.htm", "scope": "exact"},
    {"label": "DNA Internet / kirjoitussivu", "url": "http://kotisivu.dnainternet.net/poroila/130525.htm", "scope": "exact"},
    {"label": "Poroilan kotisivu / kaikki alisivut", "url": "http://kotisivu.dnainternet.net/poroila/", "scope": "prefix"},
    {"label": "Poroilan kotisivu / täsmäosoite", "url": "http://kotisivu.dnainternet.net/poroila/", "scope": "exact"},
    {"label": "Länsi-Uusimaa 27.9.2005", "url": "https://www.lansi-uusimaa.fi/arkisto/2005/27-09/lehti/1461218.shtml", "scope": "exact"},
    {"label": "Länsi-Uusimaa 27.10.2005", "url": "https://www.lansi-uusimaa.fi/arkisto/2005/27-10/lehti/1486832.shtml", "scope": "exact"},
]
UA = "PoroilaHistoricalArchiveResearch/1.0 (public metadata; rate limited)"
HEADERS = {"User-Agent": UA, "Accept": "application/json,text/plain;q=0.9"}
TIMEOUT = 35

def get_json(url):
    try:
        with request.urlopen(request.Request(url, headers=HEADERS), timeout=TIMEOUT) as res:
            raw = res.read(250_000)
            return {"http_status":res.status,"data":json.loads(raw)}
    except error.HTTPError as ex:
        return {"http_status":ex.code,"error":"HTTP "+str(ex.code),"retry_after":ex.headers.get("Retry-After")}
    except Exception as ex:
        return {"error":type(ex).__name__+": "+str(ex)[:180]}

def cdx(target):
    q = {
        "url":target["url"],
        "output":"json",
        "fl":"timestamp,original,statuscode,mimetype,length,digest",
        "filter":"statuscode:200",
        "from":"1997",
        "to":"2015",
        "limit":"100",
        "collapse":"digest"
    }
    if target["scope"] == "prefix":q["matchType"]="prefix"
    endpoint = "https://web.archive.org/cdx/search/cdx?" + parse.urlencode(q)
    r = get_json(endpoint)
    data=r.pop("data",None)
    if isinstance(data,list) and data and isinstance(data[0],list):
        fields=data[0]
        records=[dict(zip(fields,row)) for row in data[1:]]
        # Only metadata; snapshot URLs are constructed directly from the capture index.
        r["capture_count_returned"]=len(records)
        r["captures"]=[{**{k:v for k,v in item.items() if k!="digest"},
             "snapshot_url":f"https://web.archive.org/web/{item['timestamp']}/{item['original']}"}
             for item in records]
    elif data is not None:
        r["unexpected_response_shape"]=str(data)[:200]
    return r

def available(target):
    q=parse.urlencode({"url":target["url"],"timestamp":"20060411"})
    r=get_json("https://archive.org/wayback/available?"+q)
    v=r.pop("data",None)
    if isinstance(v,dict):
        # Empty snapshots do NOT prove absence; this API can return false negatives.
        r["archived_snapshots"]=v.get("archived_snapshots",{})
        r["note"]="An empty result from availability API is not evidence that no capture exists."
    return r

def main():
    os.makedirs("reports",exist_ok=True)
    out={"checked_at_utc":datetime.now(timezone.utc).isoformat(),
         "method":"Public CDX metadata and optional nearest snapshot lookup; no challenge circumvention.",
         "results":[]}
    for i,t in enumerate(TARGETS):
        item=dict(t)
        print(f"[{i+1}/{len(TARGETS)}] CDX: {t['label']}",flush=True)
        item["cdx"]=cdx(t)
        print("  CDX response:",json.dumps({k:v for k,v in item["cdx"].items() if k!="captures"},ensure_ascii=False)[:700],flush=True)
        if not item["cdx"].get("captures") and t["scope"]=="exact":
            time.sleep(2)
            item["availability"]=available(t)
            print("  Availability:",json.dumps(item["availability"],ensure_ascii=False)[:450],flush=True)
        out["results"].append(item)
        time.sleep(2)
    with open("reports/wayback-probe.json","w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=2)
    print("\nSUMMARY",flush=True)
    for t in out["results"]:
        captures=t["cdx"].get("captures",[])
        print(f" {t['label']}: CDX {len(captures)} captures; CDX {t['cdx'].get('http_status',t['cdx'].get('error'))}",flush=True)
        for cap in captures[:10]:print("  "+cap["snapshot_url"],flush=True)
    print("Full metadata: Actions artifact wayback-capture-index",flush=True)

if __name__=="__main__":main()
