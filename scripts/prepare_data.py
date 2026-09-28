import csv, json, pathlib, re
root=pathlib.Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'data/source.csv').open(encoding='utf-8-sig',newline='')))
links={
 'Northern Virginia ("Data Center Alley")':('CBRE, H1 2026','https://www.cbre.com/insights/books/north-america-data-center-trends-h1-2026','Primary report checked'),
 'OpenAI "PORTS-Pike"':('OpenAI, PORTS-Pike project','https://openai.com/index/openai-joins-ports-pike-project/','Operator checked'),
 'Bell AI Fabric Data Centre':('Bell, March 2026','https://explore.business.bell.ca/artificial-intelligence-spotlight/bell-ai-fabric-expands-national-network-300-mw-data-centre-saskatchewan','Operator checked'),
 'AWS / Talen Susquehanna campus':('Talen Energy, Amazon agreement','https://ir.talenenergy.com/news-releases/news-release-details/talen-energy-expands-nuclear-energy-relationship-amazon','Operator checked'),
 'Google data center|West Memphis':('Google data center locations','https://datacenters.google/locations/','Operator status checked'),
 'AWS expansion (Warren County / Vicksburg)':('Amazon, Northern Indiana announcement','https://www.aboutamazon.com/news/company-news/amazon-15-billion-indiana-data-centers','Regional plan checked; site MW not verified'),
}
manual={
 'AWS / Talen Susquehanna campus':{'capacity':None,'basis':'Facility capacity undisclosed','qualification':'The source file’s 960 MW is a power agreement, not operating IT load. Talen describes a ramp to 1,920 MW contracted supply.','status':'Operational'},
 'Stargate I (OpenAI / Oracle, built by Crusoe)':{'capacity':None,'basis':'Operating capacity undisclosed','qualification':'The input claims 843 MW live; no directly attributable operator measurement was verified.','status':'Operational'},
 'AWS Project Rainier':{'capacity':None,'basis':'Operating capacity undisclosed','qualification':'The input claims 1,725 MW live; that estimate requires a dated operator or utility source.','status':'Operational'},
 'AWS Project Rainier — Mississippi campus':{'capacity':None,'basis':'Current capacity unclear','qualification':'The input mixes 350+ MW “today” with a 1,034–1,725 MW target.','status':'Under construction'},
 'Google data center|West Memphis':{'capacity':None,'basis':'Data center capacity undisclosed','qualification':'Google lists West Memphis as in development. The input’s 600 MW describes secured power and is not a confirmed live IT load.','status':'Proposed / planned'},
 'Microsoft Fairwater':{'capacity':None,'basis':'Capacity requires confirmation','qualification':'The input’s 3,300 MW target is not supported by a specific primary source in the source notes.','status':'Under construction'},
 'Beacon AI Centres (5 sites)':{'capacity':2000,'basis':'Multi-site portfolio target','qualification':'Five proposed 400 MW hubs in the input. Representative regional marker; this is not a single site.','status':'Proposed / planned'},
 'Amazon Mattameade / Cosner campuses':{'capacity':1220,'basis':'Two-campus planned total','qualification':'The input combines 770 MW and 450 MW across two adjacent campuses.','status':'Proposed / planned'},
 'OpenAI "PORTS-Pike"':{'capacity':8000,'basis':'Agreed planned IT capacity','qualification':'OpenAI says approximately 8 GW of IT capacity under agreement, delivered in phases; first 800 MW expected in 2028.','status':'Proposed / planned'},
 'Bell AI Fabric Data Centre':{'capacity':300,'basis':'Announced project capacity','qualification':'Bell announced the 300 MW Sherwood project on March 16, 2026. The source file incorrectly says May.','status':'Proposed / planned'},
 'Atlanta market':{'capacity':1459.2,'basis':'Reported market inventory','qualification':'The input lists 2,076 MW under construction; CBRE H1 2026 reports 2,882 MW. Market inventory value needs a row-level figure check.','status':'Operational'},
 'Dallas–Fort Worth market':{'capacity':1067.3,'basis':'Reported market inventory','qualification':'Tracker definitions vary. The input’s “#3” ranking should not be inferred from this mixed dataset.','status':'Operational'},
 'Northern Virginia ("Data Center Alley")':{'capacity':4496.5,'basis':'CBRE wholesale market inventory','qualification':'CBRE H1 2026: 4,496.5 MW inventory and 2,420.2 MW under construction. Market inventory excludes some privately operated capacity.','status':'Operational'},
 'Phoenix market':{'capacity':1200,'basis':'Reported market inventory','qualification':'Dataset estimate; market boundary and capacity definition need row-level validation.','status':'Operational'},
 'Toronto market':{'capacity':370,'basis':'Reported market inventory','qualification':'Input describes 370+ MW; a precise market boundary and source date need confirmation.','status':'Operational'},
 'Querétaro market':{'capacity':201,'basis':'Reported market inventory','qualification':'Input estimate; do not add the KIO campus to this market total.','status':'Operational'},
}

def key(r):
    n=r['name']
    return n+'|West Memphis' if n=='Google data center' and r['city']=='West Memphis' else n

def convert(r,i):
    k=key(r); m=manual.get(k,{})
    raw=float(r['capacity_mw']) if r['capacity_mw'] else None
    cap=m.get('capacity',raw)
    if cap is not None and cap.is_integer() if isinstance(cap,float) else False: cap=int(cap)
    status=m.get('status',r['status'])
    kind='Market' if r['category']=='Market' else 'Project'
    if 'basis' in m: basis=m['basis']
    elif cap is None: basis='Capacity undisclosed'
    elif kind=='Market': basis='Reported market inventory'
    elif status=='Operational': basis='Reported operating estimate'
    elif status=='Under construction': basis='Reported project figure / target'
    else: basis='Planned project capacity / target'
    source=links.get(k)
    if source is None: source=('Original source notes',None,'Row-level verification pending')
    return dict(id=f'dc-{i:02d}',name=r['name'],kind=kind,status=status,city=r['city'],region=r['state_province'],country=r['country'],lat=float(r['latitude']),lon=float(r['longitude']),capacity=cap,basis=basis,qualification=m.get('qualification',''),originalDescription=r['capacity_description'],operator=r['operator'],notes=r['notes'],sourceTitle=source[0],sourceUrl=source[1],sourceQuality=source[2])

out=[convert(r,i) for i,r in enumerate(rows,1)]
# The source combines two distant cities into one marker; represent them separately.
for j,r in enumerate(out):
    if r['name']=='KIO Data Centers expansion':
        r.update(name='KIO expansion — Mexico City',city='Mexico City',region='Mexico City',lat=19.4326,lon=-99.1332,qualification='Original row names Mexico City and Monterrey together. Site-specific capacity undisclosed.')
        other={**r,'id':'dc-52','name':'KIO expansion — Monterrey','city':'Monterrey','region':'Nuevo León','lat':25.6866,'lon':-100.3161}
        out.append(other)
        break
(root/'dist/data.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print('Records:',len(out),'Unknown:',sum(r['capacity'] is None for r in out),'Markets:',sum(r['kind']=='Market' for r in out))
