import json,re,urllib.parse,urllib.request
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
BASE='https://gamma-api.polymarket.com'
def get(path,params=None):
 url=BASE+path+('?' + urllib.parse.urlencode(params) if params else '')
 req=urllib.request.Request(url,headers={'User-Agent':'live-swing-desk/1.0'})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def loads(v):return json.loads(v) if isinstance(v,str) else v
nfl=next(x for x in get('/sports') if x.get('sport')=='nfl')
events=get('/events',{'active':'true','closed':'false','limit':100,'series_id':nfl['series']})
now=datetime.now(ZoneInfo('America/Los_Angeles')); dates={(now+timedelta(days=i)).date().isoformat() for i in range(3)}
games=[]
for e in events:
 slug=e.get('slug','')
 if e.get('eventDate') not in dates or not re.fullmatch(r'nfl-[a-z0-9]+-[a-z0-9]+-\d{4}-\d{2}-\d{2}',slug):continue
 m=next((x for x in e.get('markets',[]) if x.get('sportsMarketType')=='moneyline' and x.get('clobTokenIds')),None)
 if not m:continue
 outcomes=loads(m['outcomes']); prices=[float(x) for x in loads(m['outcomePrices'])]; tokens=loads(m['clobTokenIds']); parts=slug.split('-')
 games.append({'slug':slug,'title':e['title'],'date':e.get('eventDate'),'start':m.get('gameStartTime'),'away':parts[1].upper(),'home':parts[2].upper(),'outcomes':outcomes,'prices':prices,'tokens':tokens,'score':e.get('score'),'period':e.get('period'),'live':bool(e.get('live')),'ended':bool(e.get('ended')),'volume':float(m.get('volume') or 0),'url':'https://polymarket.com/sports/nfl/'+slug})
games.sort(key=lambda x:(x['date'],x['start'] or '',x['slug']))
out={'generatedAt':datetime.now(ZoneInfo('UTC')).isoformat(),'league':'NFL','source':'Polymarket Gamma API','games':games}
Path('data').mkdir(exist_ok=True);Path('data/current.json').write_text(json.dumps(out,separators=(',',':')))
print(f'wrote {len(games)} games')
