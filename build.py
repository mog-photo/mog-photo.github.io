#!/usr/bin/env python3
"""Generate static HTML from shared plan data. Run: python3 build.py"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'plans.json').read_text())
SCENES = json.loads((ROOT / 'scene-images.json').read_text())
PLANS = DATA['plans']

def render(template, values):
    def substitute(match):
        key = match.group(1)
        if key not in values:
            raise ValueError(f'Unresolved template key: {key}')
        return values[key]
    return re.sub(r'{{([a-z_]+)}}', substitute, template)

def plan_card(p):
    badge = escape(p.get('badge', ''))
    summary = [f'データ {p["count"]}枚']
    if p.get('duration'):
        summary.append(f'撮影 {p["duration"]}')
    summary.append('A4額装1点付き' if p['frame'] else '額装なし')
    fields = dict(p, backgrounds='または'.join(p.get('backgrounds', [])))
    facts = ''.join(f'<li>{escape(f.format(**fields))}</li>' for f in p['facts'])
    note = f'<p class="plan-note">{escape(p["note"].format(**fields))}</p>' if p.get('note') else ''
    return f'''<article class="plan-card{' featured' if badge else ''}" id="{escape(p['id'])}">
<div class="plan-label">{badge}</div><h3>{escape(p['name'])}</h3>
<p class="plan-catch">{escape(p['catch'])}</p>
<p class="price">{p['price']:,}<span>円（税込）</span></p>
<p class="plan-summary">{''.join(f'<span>{escape(v)}</span>' for v in summary)}</p>
<ul class="plan-facts">{facts}</ul>{note}
<p class="plan-recommend"><strong>こんな方に</strong>{escape(p['recommend'])}</p>
<a class="button{' secondary' if not badge else ''}" href="#booking" aria-label="{escape(p['name'])}の予約・相談">予約・相談する <span aria-hidden="true">↗</span></a>
</article>'''

def scene_image(key):
    image = SCENES[key]
    if not image:
        return ''
    path = ROOT / image['src']
    if not path.is_file() or not image.get('alt'):
        raise ValueError(f'Invalid scene image: {key}')
    return f'<figure class="scene-photo"><img src="{escape(image["src"])}" alt="{escape(image["alt"])}" width="{int(image["width"])}" height="{int(image["height"])}" loading="lazy"></figure>'

layout = (ROOT / 'templates/layout.html').read_text()
PAGES = {
    'index': ('mogフォトワーク｜龍ケ崎の記念撮影・七五三・愛犬・プロフィール撮影', '龍ケ崎のmogフォトワーク。七五三や愛犬との記念撮影、マッチングアプリ・仕事用プロフィール、店舗・介護施設向け撮影をご案内。料金と納品内容を比較して予約・相談できます。'),
    'business': ('店舗・事業者向け 写真撮影｜龍ケ崎のmogフォトワーク', '店舗紹介、採用・スタッフ撮影、SNS・定期撮影。龍ケ崎のmogフォトワークが、お店の空気や働く人の魅力を写真で伝えます。内容に応じてお見積もり。'),
    'facilities': ('介護施設・福祉施設向け 出張撮影｜mogフォトワーク', '敬老会・長寿祝い、個人ポートレート、家族撮影、職員撮影に対応。会場準備、当日の進行、撮影・掲載同意、納品方法を施設担当者向けにご案内します。')
}
values = {k:escape(v, quote=True) for k,v in DATA['booking'].items()}
values.update(memory_plans='\n'.join(plan_card(p) for p in PLANS if p['group']=='memory'), profile_plans='\n'.join(plan_card(p) for p in PLANS if p['group']=='profile'), shichigosan_image=scene_image('shichigosan'), dog_image=scene_image('dog'))
portrait = next(p for p in PLANS if p['id']=='memory-portrait')
values.update(portrait_capacity=str(portrait['max_people']), portrait_duration=portrait['duration'], portrait_venue_hours=str(portrait['venue_hours']), portrait_backgrounds='または'.join(portrait['backgrounds']))
for page, (title, description) in PAGES.items():
    content = render((ROOT / f'templates/{page}.html').read_text(), values)
    prefix = '' if page == 'index' else 'index.html'
    navigation = ''.join(f'<a href="{prefix}#{target}">{label}</a>' for target,label in [('menu','撮影メニュー'),('scenes','撮影シーン'),('corporate','法人・施設向け'),('about','撮影者について'),('booking','ご予約・ご相談 ↗')])
    document = render(layout, dict(title=escape(title), description=escape(description,quote=True), canonical='https://mog-photo.github.io/' + ('' if page=='index' else page+'.html'), content=content, navigation=navigation))
    (ROOT / f'{page}.html').write_text(document)
print('Built index.html, business.html, facilities.html from plans.json and templates.')
