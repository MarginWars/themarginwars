from pathlib import Path
import feedparser,icalendar,json,xml.etree.ElementTree as ET
D=Path(__file__).parent.parent/'site_calm/feeds';errors=[];count=0
for p in list(D.glob('*.xml'))+list(D.glob('*.atom')):
 try:
  root=ET.parse(p).getroot();f=feedparser.parse(p.read_bytes());assert not f.bozo,str(f.get('bozo_exception'));assert f.feed.title;assert f.feed.link
  if p.suffix=='.atom':
   ns={'a':'http://www.w3.org/2005/Atom'};assert root.find('a:id',ns) is not None;assert root.find('a:updated',ns) is not None;assert root.find('a:author/a:name',ns) is not None;assert root.find('a:link[@rel="self"]',ns) is not None
  else:
   assert root.attrib['version']=='2.0'
   for el in ['title','link','description']:assert root.find('channel/'+el) is not None
  ids=set()
  for ent in f.entries:assert ent.id not in ids;ids.add(ent.id);assert ent.title;assert ent.link;assert ent.get('summary')
  count+=1
 except Exception as ex:errors.append(str(p)+': '+str(ex))
for p in D.glob('*.json'):
 d=json.loads(p.read_text());assert d['version']=='https://jsonfeed.org/version/1.1';assert len({x['id'] for x in d['items']})==len(d['items']);count+=1
raw=(D/'dates.ics').read_bytes();assert b'\r\n' in raw;assert max(map(len,raw.split(b'\r\n')))<=75
c=icalendar.Calendar.from_ical(raw);events=c.walk('VEVENT');ids=set()
for ev in events:
 assert ev['UID'] not in ids;ids.add(ev['UID']);assert ev.decoded('DTEND')>ev.decoded('DTSTART');assert ev['DTSTAMP'];assert ev['SUMMARY'];assert ev['URL']
print(json.dumps({'validated_feeds':count,'ics_events':len(events),'errors':errors},indent=2));assert not errors
