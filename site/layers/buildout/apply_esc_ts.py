"""Turnstile on the assistant escalation form (in place on site_calm, idempotent)."""
import pathlib, shutil
ROOT = pathlib.Path("@MW_ROOT@/site_calm"); H = pathlib.Path(__file__).parent
shutil.copyfile(H / "esc-ts.js", ROOT / "assets/esc-ts.js")
TAG = '<script defer="" src="/assets/esc-ts.js"></script>'
REPL = [
 ("if(window.TMW_TS&&!TMW_TS.get(E)){st.textContent='Checking you are human…';TMW_TS.whenReady(E,function(){E.requestSubmit?E.requestSubmit():E.dispatchEvent(new Event('submit',{cancelable:true}))});return}var b=E.querySelector('.go');b.disabled=true;st.textContent='Sending...';", "if(window.TMW_TS&&!TMW_TS.get(E)){st.textContent='Checking you are human…';TMW_TS.whenReady(E,function(){E.requestSubmit?E.requestSubmit():E.dispatchEvent(new Event('submit',{cancelable:true}))},function(){st.textContent='Please complete the human check above, then send again.'});return}var b=E.querySelector('.go');b.disabled=true;st.textContent='Sending...';"),
 ('<p aria-live="polite" class="st" role="status"></p><div class="row"><button class="bk"', '<div class="ts"></div><p aria-live="polite" class="st" role="status"></p><div class="row"><button class="bk"'),
 ("if(h)E.querySelector('input').focus();", "if(h){E.querySelector('input').focus();if(window.TMW_TS)TMW_TS.load(E)}"),
 ("var b=E.querySelector('.go');b.disabled=true;st.textContent='Sending...';",
  "if(window.TMW_TS&&!TMW_TS.get(E)){st.textContent='Checking you are human…';TMW_TS.whenReady(E,function(){E.requestSubmit?E.requestSubmit():E.dispatchEvent(new Event('submit',{cancelable:true}))},function(){st.textContent='Please complete the human check above, then send again.'});return}var b=E.querySelector('.go');b.disabled=true;st.textContent='Sending...';"),
 ("page:location.href,attribution:window.TMW_ATTR?TMW_ATTR():null})", "page:location.href,attribution:window.TMW_ATTR?TMW_ATTR():null,'cf-turnstile-response':window.TMW_TS?TMW_TS.get(E):''})"),
 (".then(function(j){b.disabled=false;if(j.s===429)", ".then(function(j){b.disabled=false;if(window.TMW_TS)TMW_TS.reset(E);if(j.s===429)"),
 (".catch(function(){b.disabled=false;st.textContent='Comms down. Try again, or use Contact.'})})}", ".catch(function(){b.disabled=false;if(window.TMW_TS)TMW_TS.reset(E);st.textContent='Comms down. Try again, or use Contact.'})})}"),
]
n = 0
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(); o = t
    if "/api/escalate" not in t: continue
    for a, b in REPL:
        if b in t: continue
        if a in t: t = t.replace(a, b)
    if 'class="esc"' in t and TAG not in t: t = t.replace("</body>", TAG + "</body>", 1)
    if t != o: p.write_text(t); n += 1
w = (ROOT / "warroom.html").read_text()
assert '<div class="ts"></div>' in w and TAG in w and "TMW_TS.get(E)" in w and "TMW_TS.reset(E)" in w, "escalation Turnstile patch incomplete"
print(f"ESC-TS: patched {n} pages")
