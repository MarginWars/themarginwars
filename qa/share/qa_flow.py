"""Share journeys in Chromium: X intent href, LinkedIn (popup + clipboard + note), copy, download, native share, events."""
import sys, json, urllib.parse
from playwright.sync_api import sync_playwright
sys.path.insert(0, '.'); from play import play
SHARE = 'http://localhost:8871/'; UNP = 'http://localhost:8872/'
GAMES = ['daily', 'leak', 'deal', 'quiz', 'ep1', 'ep2', 'tracewire', 'arcade']
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for g in GAMES:
        base = UNP if g in ('ep2', 'tracewire') else SHARE
        ctx = b.new_context(viewport={'width': 1440, 'height': 900}, permissions=['clipboard-read', 'clipboard-write'], accept_downloads=True)
        evs, reqs = [], []
        ctx.route('**/api/ev', lambda r: (evs.append(r.request.post_data), r.fulfill(status=204)))
        ctx.route(lambda u: 'x.com' in u or 'linkedin.com' in u, lambda r: (reqs.append(r.request.url), r.fulfill(status=200, body='ok')))
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(base + 'arcade.html?mk_test=1')  # mk.js QA flag for this session (preview/local only)
        play(pg, g, base)
        m = pg.query_selector_all('.mws')[-1]
        xh = m.query_selector('[data-s=x]').get_attribute('href'); lh = m.query_selector('[data-s=linkedin]').get_attribute('href')
        xt = urllib.parse.parse_qs(urllib.parse.urlsplit(xh).query)['text'][0]
        xl = pg.evaluate('t=>MWS.xlen(t)', xt)
        lu = urllib.parse.parse_qs(urllib.parse.urlsplit(lh).query)['url'][0]
        r = {'x_href': xh, 'x_text': xt, 'x_weighted': xl, 'li_href': lh, 'li_url': lu}
        with ctx.expect_page() as pp: m.query_selector('[data-s=x]').click()
        pop = pp.value; pop.wait_for_load_state(); r['x_popup'] = pop.url; pop.close()
        pg.evaluate("navigator.clipboard.writeText('')")
        with ctx.expect_page() as pp: m.query_selector('[data-s=linkedin]').click()
        pop = pp.value; pop.wait_for_load_state(); r['li_popup'] = pop.url; pop.close(); pg.bring_to_front(); pg.wait_for_timeout(300)
        r['li_clipboard'] = pg.evaluate('navigator.clipboard.readText()'); r['li_note'] = m.query_selector('.mws-n').inner_text()
        m.query_selector('[data-s=copy]').click(); pg.wait_for_timeout(300)
        r['copy_clipboard'] = pg.evaluate('navigator.clipboard.readText()'); r['copy_note'] = m.query_selector('.mws-n').inner_text()
        if m.query_selector('[data-s=card]'):
            with pg.expect_download() as dl: m.query_selector('[data-s=card]').click()
            path = f'qa/card_{g}.png'; dl.value.save_as(path); r['card'] = path
        pg.wait_for_timeout(500)
        r['events'] = [json.loads(e)['e'] + '@' + json.loads(e)['p'] for e in evs if 'share_' in e]
        r['errors'] = errs; ctx.close()
        # native share on a touch phone
        ctx = b.new_context(**p.devices['iPhone 15'] if False else {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True})
        ctx.add_init_script("navigator.share=function(d){window.__sh=d;return Promise.resolve()}")
        ctx.route('**/api/ev', lambda r: r.fulfill(status=204))
        pg = ctx.new_page(); play(pg, g, base); m = pg.query_selector_all('.mws')[-1]
        nb = m.query_selector('[data-s=native]'); r['native_visible'] = nb.is_visible()
        if r['native_visible']: nb.click(); pg.wait_for_timeout(200); r['native_payload'] = pg.evaluate('window.__sh')
        ctx.close()
        res[g] = r; print(g, 'xlen', xl, 'events', r['events'], 'errors', errs, flush=True)
    b.close()
json.dump(res, open('qa/flow.json', 'w'), indent=1, ensure_ascii=False)
