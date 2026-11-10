import json
from pathlib import Path
D=Path(__file__).resolve().parent.parent/'site_calm/assets/feeds';D.mkdir(parents=True,exist_ok=True)
S={
'rba':'https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/impact-and-implementation.html',
'rbafaq':'https://www.rba.gov.au/payments-and-infrastructure/review-of-retail-payments-regulation/2026-03/conclusions-paper/faqs/index.html',
'nacha':'https://www.nacha.org/content/summary-upcoming-rule-changes',
'funds':'https://www.nacha.org/rules/funds-availability-requirements-non-same-day-credit-entries',
'phase2':'https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2',
'psr':'https://www.psr.org.uk/publications/policy-statements/ps261-market-review-of-card-scheme-and-processing-fees-final-decision-information-transparency-and-complexity-remedy-pricing-governance-remedy/',
'psrext':'https://www.psr.org.uk/media/nqoettxg/ps26-1-sp-fees-market-review-extensions-decision-aug-2026.pdf',
'psd':'https://data.consilium.europa.eu/doc/document/ST-15154-2026-INIT/en/pdf',
'fca':'https://www.fca.org.uk/firms/emi-payment-institutions-safeguarding-requirements',
'emv':'https://www.emvco.com/news-publications/emvco-newsletter-q3-2026/',
'pix':'https://www.bcb.gov.br/content/estabilidadefinanceira/pix/changelog.html',
'ca':'https://www.payments.ca/canadas-real-time-rail-launch-confirmed-budget-2026',
'caeu':'https://www.payments.ca/payments-canada-welcomes-joint-canada-eu-commitment-interlink-real-time-payment-systems',
'nz':'https://www.comcom.govt.nz/regulated-industries/projects/interchange-fee-regulation/',
'boe':'https://www.bankofengland.co.uk/news/2026/august/delay-to-the-november-2026-rtgs-standards-release',
'regii':'https://www.federalreserve.gov/apps/proposals/FR-0000-0095-01/details',
'aus':'https://auspaynet.com.au/sites/default/files/2026-06/IAC%20Volume%207%20V18%20-%20Effective%2030%20June%202026%20-%20public%20version.pdf'
}
w=[];cal=[]
def add(id,market,typ,title,changed,hits,effective,source,source_date=None,kind='Effective',calendar=True):
 item=dict(id=id,date='2026-11-08',market=market,type=typ,title=title,changed=changed,hits=hits,effective=effective,source=S[source],source_date=source_date,date_kind=kind)
 w.append(item)
 if effective and calendar:cal.append(dict(id=id,date=effective,title=title,market=market,kind=kind,description=changed,source=S[source],wire_id=id))
add('au-surcharging','anz','regulation','Australia: card surcharge reset','eftpos, Mastercard and Visa no-surcharge rules apply from 1 October after the RBA removed its prohibition on those rules.','Australian merchants and acquirers','2026-10-01','rbafaq')
add('au-domestic-interchange','anz','regulation','Domestic interchange: lower caps','Revised interchange regulation applies to domestic-issued card transactions acquired in Australia.','Australian acquirers and issuers','2026-10-01','rba')
add('au-net-compensation','anz','regulation','Issuer compensation rules change','The amended net-compensation regime starts, with transitional arrangements for 2026/27.','Card networks and issuers','2026-10-01','rba')
add('au-network-disclosure','anz','regulation','Scheme fees come into view','First quarterly aggregate fee publications by designated card networks were due for the July–September period.','Card networks; acquiring teams','2026-10-30','rba',kind='Publication deadline')
add('au-acquirer-disclosure','anz','regulation','Acquirer fee disclosures begin','Qualifying large acquirers must publish merchant service fee data by merchant size and card type.','Large acquirers and merchants','2026-10-30','rba',kind='Publication deadline')
add('au-pass-through','anz','regulation','Next: prove interchange pass-through','First publication of large acquirers’ interchange pass-through measures covers October–December 2026.','Large acquirers and merchant finance teams','2027-01-30','rba',kind='Publication deadline')
add('au-foreign-cards','anz','regulation','Foreign-issued cards get a cap','Interchange caps extend to foreign-issued card transactions acquired in Australia.','Cross-border acquiring teams','2027-04-01','rba')
add('au-statements','anz','regulation','Merchant statements get sharper','More statement detail is required from the first full statement period starting on or after 1 April.','Australian acquirers and merchants','2027-04-01','rba')
add('au-scheme-roadmap','anz','policy','Scheme-fee roadmap expected','The RBA expects a scheme-fee roadmap by 1 April; this is an expectation, not a new fee cap.','Card networks and acquiring teams','2027-04-01','rba',kind='Policy expectation')
add('nz-commercial-cards','anz','regulation','NZ moves on commercial cards','The 22 October decision introduces commercial credit-card interchange limits on Mastercard and Visa.','New Zealand merchants and acquirers','2027-04-22','nz','2026-10-22')
add('nz-foreign-cards','anz','regulation','NZ foreign-card limits: baseline','Revised interchange limits for foreign-issued personal cards took effect in May. Kept here as an implementation baseline.','New Zealand merchants and acquirers','2026-05-01','nz')
add('ach-availability','us','network rule','ACH credits: 9am availability','Non-Same Day ACH credits must be available by 9am in the receiving bank’s local time on settlement date.','Receiving banks and payout teams','2026-09-18','funds')
add('ach-iat','us','network rule','ACH: IAT definition changes','Nacha lists its revised definition of International ACH Transactions among the September changes.','ACH originators and compliance teams','2026-09-18','nacha')
add('ach-availability-exceptions','us','network rule','ACH availability exceptions update','Nacha lists changes to funds-availability exceptions for Non-Same Day credit entries. Check the rule text before changing controls.','Receiving banks','2026-09-18','nacha')
add('ach-fraud-phase2','us','network rule','ACH fraud monitoring: no volume floor','Phase 2 extends risk-based monitoring to remaining non-consumer originators and receiving banks. June 19 is the rule date; June 22 is the practical banking-day deadline.','Originators, service providers and receiving banks','2026-06-22','phase2')
add('ach-fraud-phase1','us','network rule','ACH fraud monitoring: phase 1 baseline','Monitoring rules began for all originating banks and large originators and receiving banks.','ACH participants meeting phase-1 criteria','2026-03-20','nacha')
add('uk-pricing-governance','ukeu','regulation','UK scheme pricing: evidence required','Relevant scheme-fee decisions must comply with the PSR’s pricing-governance direction from the end of November.','Visa, Mastercard and UK acquirers','2026-11-30','psr')
add('uk-fee-transparency','ukeu','regulation','UK fee transparency: next stage','Substantive information, transparency and complexity requirements apply from the end of July 2027, subject to the limited fee-logic extension.','Visa, Mastercard and UK acquirers','2027-07-30','psr')
add('uk-fee-logic-extension','ukeu','regulation','Small fee lines: a limited extension','ITC Standard B is deferred for qualifying fee lines generating £850,000 or less in annual UK gross revenue. During the extension, acquirers can request that information without charge.','UK acquirers and scheme billing teams','2029-07-30','psrext')
add('uk-safeguarding','ukeu','regulation','Safeguarding: the operating baseline','Daily reconciliations, monthly reports and resolution packs form part of the strengthened safeguarding regime. Audit requirements have exceptions.','UK payment and e-money firms','2026-05-07','fca')
add('eu-psr-position','ukeu','regulation','EU PSR: Council first-reading position','The Council voting record documents adoption of its first-reading position on 29 October. This is a legislative milestone, not an application date. PSD3 and PSR must be tracked separately; no implementation date is asserted here.','EU payment providers; not automatically UK firms',None,'psd','2026-10-29',calendar=False)
cal.append(dict(id='eu-psr-position',date='2026-10-29',title='EU PSR: Council first-reading position',market='ukeu',kind='Legislative milestone',description=w[-1]['changed'],source=S['psd'],wire_id='eu-psr-position'))
add('uk-rtgs-delay','ukeu','policy','CHAPS: November release deferred','The Bank of England deferred its entire November 2026 RTGS standards release. This notice does not establish a replacement deadline.','CHAPS and RTGS participants',None,'boe','2026-08-27',calendar=False)
add('ca-rtr-launch','ca-latam','policy','Canada: RTR launch set for 9 November','Payments Canada confirms a scheduled 9 November launch. This preview does not describe the service as already live.','Canadian banks, PSPs and payment users','2026-11-09','ca','2026-11-05',kind='Scheduled launch')
add('ca-eu-interlink','ca-latam','policy','Canada–EU: interlink work supported','A joint commitment supports work toward connecting instant payment systems. It is not an operating cross-border route.','Cross-border product and treasury teams',None,'caeu','2026-11-02',calendar=False)
add('pix-dict-default','br','network rule','Pix DICT: refund monitoring default','DICT 2.13.0 changes the default value of Refund MonitorAccount to false. Review integrations for implicit defaults.','Pix participants and refund engineering teams',None,'pix','2026-10-26',calendar=False)
add('pix-dict-rc','br','network rule','Pix DICT: recovery API clarifications','The September release candidate adds FundsRecoveryId path-parameter documentation and clarifies refund-request restrictions. A release candidate is not a compliance deadline.','Pix participants and fraud operations',None,'pix','2026-09-28',calendar=False)
add('emv-3ds24','global','network rule','3DS 2.4: draft, not a mandate','EMVCo reports that draft Protocol and Core Functions v2.4 is available for Associate and Subscriber review. No global migration deadline is asserted.','3DS servers, SDK providers and authentication teams',None,'emv','2026-10-09',calendar=False)
add('emv-3ds-extensions','global','network rule','3DS approvals: conditional extension','EMVCo’s Q3 update reports conditional approval extensions for eligible products intending to migrate to v2.4.0.0. Confirm product-specific eligibility.','3DS product providers',None,'emv','2026-10-09',calendar=False)
add('emv-agentic-draft','global','policy','Agentic payments: intent framework draft','EMVCo’s draft framework introduces Intent Services for consumer-authorised intent. It is a specification-development step, not a deployed network mandate.','Agentic checkout and payment product teams',None,'emv','2026-10-09',calendar=False)
# Deliberately keep the proposal as a watch, without asserting a final rate or effective date.
add('us-regii-watch','us','regulation','Reg II: proposal watch, not a new rate','The Federal Reserve proposal docket is the source to monitor. No final rate, litigation outcome or effective date is asserted in this preview.','US debit economics and regulatory teams',None,'regii',calendar=False)
bp=[]
for id,title,impact,method,move,wire in [
 ('au-pass-through-test','Australia: audit the pass-through','Cost direction: lower interchange; net savings unquantified.','Direction follows the RBA’s cap reductions. Merchant impact needs transaction mix and contracted pass-through; no basis-point estimate is claimed.','Reconcile October fees against September, holding card mix constant.','au-domestic-interchange'),
 ('nz-commercial-readiness','NZ: price the commercial-card reset','Cost direction: lower regulated interchange; merchant savings unquantified.','Direction follows the Commission’s decision. No conversion to merchant basis points without commercial-card share and acquirer terms.','Ask for an April repricing plan and a commercial-card mix report.','nz-commercial-cards'),
 ('uk-fee-evidence','UK: make fee evidence usable','Impact direction: greater transparency; no guaranteed fee reduction.','Governance and disclosure duties do not themselves set merchant prices. No numeric savings estimate is claimed.','Build a fee-line inventory now; map each trigger to the acquiring invoice.','uk-pricing-governance')]:
 x=next(x for x in w if x['id']==wire);bp.append(dict(id=id,date='2026-11-08',title=title,impact=impact,method=method,move=move,source=x['source'],wire_id=wire,market=x['market']))
for name,data in [('wire',w),('calendar',cal),('bp-watch',bp),('route-briefs',[])]:
 p=D/(name+'.json')
 if not p.exists():p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(Path(__file__).parent/'source-registry.json').write_text(json.dumps({'checked':'2026-11-08','sources':S,'exclusions':['Non-primary commentary excluded','Unconfirmed deadlines omitted','Prohibited organisations excluded'],'notes':['Wire includes recent changes, upcoming dates and explicitly marked implementation baselines. Not 30 separate breaking-news announcements.','No PSD3 implementation deadline, global 3DS mandate, or Reg II final rate asserted.']},indent=2))
print('Seed',len(w),'wire',len(cal),'dates',len(bp),'watch')
