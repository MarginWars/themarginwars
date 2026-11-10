import json
from pathlib import Path
D=Path(__file__).parent.parent/'site_calm/assets/feeds';w=json.loads((D/'wire.json').read_text());cal=json.loads((D/'calendar.json').read_text())
replace={
'ach-fraud-phase1':('ach-iat-contacts','2027-01-01','ACH: register IAT contacts','Registration of IAT contacts in the ACH Contact Registry is listed for 1 January 2027.','ACH participants handling international entries'),
'ach-fraud-phase2':('ach-iat-date-of-birth','2027-03-19','IAT: optional date-of-birth field','Nacha lists the optional date-of-birth field for IAT entries for 19 March 2027.','IAT originators, banks and service providers'),
'nz-foreign-cards':('ach-same-day-limit','2027-09-17','Same Day ACH: $10 million limit','Nacha lists an increase of the Same Day ACH dollar limit to $10 million for 17 September 2027.','US treasury, payout and originating-bank teams')}
for old,(ident,date,title,change,hits) in replace.items():
 for x in w:
  if x['id']==old:x.update(id=ident,effective=date,title=title,changed=change,hits=hits,source='https://www.nacha.org/content/summary-upcoming-rule-changes',source_date=None,market='us',type='network rule',date_kind='Effective')
 for x in cal:
  if x['id']==old:x.update(id=ident,wire_id=ident,date=date,title=title,description=change,source='https://www.nacha.org/content/summary-upcoming-rule-changes',market='us',kind='Effective')
(D/'wire.json').write_text(json.dumps(w,ensure_ascii=False,indent=2)+'\n');(D/'calendar.json').write_text(json.dumps(cal,ensure_ascii=False,indent=2)+'\n')
