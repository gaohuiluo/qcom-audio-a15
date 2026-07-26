# -*- coding: utf-8 -*-
"""Extract clean Markdown skeleton (English) + images from rendered Qualcomm SPA pages."""
import os, re, base64, hashlib
from bs4 import BeautifulSoup, NavigableString, Tag, Comment

RAW = os.path.join(os.path.dirname(__file__), 'raw')
IMG = os.path.join(os.path.dirname(__file__), 'images')
OUT = os.path.join(os.path.dirname(__file__), 'md_en')
os.makedirs(IMG, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

PAGES = ['audio','overview','enable-audio','customize','agm','pal','tinyalsa','features','troubleshoot','references']

EXT_MAP = {'image/png':'png','image/jpeg':'jpg','image/gif':'gif','image/webp':'webp','image/svg+xml':'svg'}

def sniff_ext(data, mime):
    if mime in EXT_MAP: return EXT_MAP[mime]
    if data[:4]==b'RIFF' and data[8:12]==b'WEBP': return 'webp'
    if data[:8]==b'\x89PNG\r\n\x1a\n': return 'png'
    if data[:3]==b'\xff\xd8\xff': return 'jpg'
    return 'bin'

def save_data_uri(uri, page, hint):
    m = re.match(r'data:([^;]+);base64,(.*)', uri, re.S)
    if not m: return None
    mime, b64 = m.group(1), m.group(2).strip()
    try:
        data = base64.b64decode(b64)
    except Exception:
        return None
    ext = sniff_ext(data, mime)
    base = re.sub(r'\.(png|jpg|jpeg|gif|webp|svg)$','',hint,flags=re.I) if hint else ''
    base = re.sub(r'[^A-Za-z0-9_.-]','_', base).strip('_')
    if base:
        fname = f'{page}-{base}.{ext}'
    else:
        h = hashlib.md5(data).hexdigest()[:8]
        fname = f'{page}-img-{h}.{ext}'
    with open(os.path.join(IMG, fname), 'wb') as f:
        f.write(data)
    return fname, len(data)

def get_body(html):
    start = html.find('<div itemprop="articleBody">')
    if start < 0: return None
    end = html.find('<app-', start)
    return html[start:end if end>0 else None]

# state per page
class Ctx:
    def __init__(self, page):
        self.page = page
        self.imgc = 0
        self.imgs = []

def esc(t):
    return t.replace('|','\\|')

def render_table(tbl, ctx):
    rows = tbl.find_all('tr')
    if not rows: return ''
    out = []
    header_done = False
    for ri, tr in enumerate(rows):
        cells = tr.find_all(['th','td'])
        vals = [inline(c, ctx).strip().replace('\n',' ') for c in cells]
        out.append('| ' + ' | '.join(esc(v) for v in vals) + ' |')
        is_header = tr.find('th') is not None or (ri==0 and not header_done)
        if is_header and not header_done:
            out.append('| ' + ' | '.join('---' for _ in vals) + ' |')
            header_done = True
    if not header_done and out:
        ncol = out[0].count('|')-1
        out.insert(1, '| ' + ' | '.join('---' for _ in range(ncol)) + ' |')
    return '\n'.join(out) + '\n'

def inline(node, ctx):
    """Render inline content of a node to markdown text."""
    parts = []
    for c in node.children:
        if isinstance(c, NavigableString):
            parts.append(str(c))
        elif isinstance(c, Tag):
            name = c.name.lower()
            if name in ('code','tt','span') and 'hljs' not in ' '.join(c.get('class',[])):
                if name=='code':
                    parts.append('`'+c.get_text()+'`')
                else:
                    parts.append(inline(c, ctx))
            elif name in ('strong','b'):
                parts.append('**'+inline(c,ctx).strip()+'**')
            elif name in ('em','i'):
                parts.append('*'+inline(c,ctx).strip()+'*')
            elif name=='a':
                href = c.get('href','')
                txt = inline(c,ctx).strip()
                if href and not href.startswith('#') and txt:
                    parts.append(f'[{txt}]({href})')
                else:
                    parts.append(txt)
            elif name=='br':
                parts.append('  \n')
            elif name=='img':
                parts.append(handle_img(c, ctx))
            elif name=='svg':
                parts.append(handle_svg(c, ctx))
            else:
                parts.append(inline(c, ctx))
    return ''.join(parts)

def handle_img(c, ctx):
    src = c.get('src','')
    alt = c.get('alt','') or ''
    hint = re.sub(r'.*/','',alt) if alt else ''
    if src.startswith('data:'):
        ctx.imgc += 1
        r = save_data_uri(src, ctx.page, hint)
        if r:
            fname, sz = r
            ctx.imgs.append((fname, hint, sz))
            return f'![{hint or fname}](../images/{fname})'
    elif src:
        return f'![{alt}]({src})'
    return ''

def is_ui_icon(c):
    """Decorative UI icons (anchor link, copy, download, lucide, etc.) — skip."""
    cls = ' '.join(c.get('class', []))
    if re.search(r'lucide|copyclip|headerlink|download|shield|chevron|arrow-|icon-button', cls):
        return True
    # small decorative svg with no meaningful label
    label = c.get('aria-label','') or c.get('title','')
    def to_px(v):
        v = (v or '').replace('px','').strip()
        try: return float(v)
        except: return 9999
    w, h = to_px(c.get('width')), to_px(c.get('height'))
    if not label and w <= 40 and h <= 40:
        return True
    return False

def svg_name(c, ctx):
    label = c.get('aria-label','') or ''
    base = re.sub(r'.*/','',label)
    base = re.sub(r'\.svg$','',base, flags=re.I)
    base = re.sub(r'[^A-Za-z0-9_.-]','_', base).strip('_')
    if base:
        return f'{ctx.page}-{base}.svg'
    return None

def handle_svg(c, ctx):
    if is_ui_icon(c):
        return ''
    ctx.imgc += 1
    svg = str(c)
    if 'xmlns=' not in svg[:200]:
        svg = svg.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    data = svg.encode('utf-8')
    fname = svg_name(c, ctx)
    if not fname:
        h = hashlib.md5(data).hexdigest()[:8]
        fname = f'{ctx.page}-fig{ctx.imgc:02d}-{h}.svg'
    with open(os.path.join(IMG, fname),'w',encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'+svg)
    ctx.imgs.append((fname,'svg',len(data)))
    label = c.get('aria-label','')
    alt = re.sub(r'.*/','',label) or 'diagram'
    return f'![{alt}](../images/{fname})'

def block(node, ctx, depth=0):
    out = []
    for c in node.children:
        if isinstance(c, NavigableString):
            t = str(c).strip()
            if t: out.append(t)
            continue
        if not isinstance(c, Tag): continue
        name = c.name.lower()
        cls = ' '.join(c.get('class',[]))
        if name in ('h1','h2','h3','h4','h5','h6'):
            lvl = int(name[1])
            out.append('#'*lvl + ' ' + inline(c,ctx).strip())
        elif name=='section':
            out.append(block(c, ctx, depth))
        elif name in ('div',):
            if 'sphinx-tabs' in cls and 'container' in cls:
                out.append(render_tabs(c, ctx))
            elif 'highlight' in cls or 'codeblock' in cls:
                pre = c.find('pre')
                if pre: out.append(render_code(pre))
                else: out.append(block(c,ctx,depth))
            elif 'admonition' in cls or 'note' in cls or 'warning' in cls or 'tip' in cls or 'important' in cls or 'caution' in cls:
                out.append(render_admonition(c, ctx))
            else:
                out.append(block(c, ctx, depth))
        elif name=='pre':
            out.append(render_code(c))
        elif name=='p':
            txt = inline(c, ctx).strip()
            if txt: out.append(txt)
        elif name in ('ul','ol'):
            out.append(render_list(c, ctx, name, depth))
        elif name=='table':
            out.append(render_table(c, ctx))
        elif name=='figure':
            out.append(render_figure(c, ctx))
        elif name in ('img',):
            out.append(handle_img(c,ctx))
        elif name=='svg':
            out.append(handle_svg(c,ctx))
        elif name in ('dl',):
            if 'tabincludedirective' in c.get_text()[:80] or c.find(class_='sig-name'):
                out.append(render_tabincludedirective(c, ctx))
            else:
                out.append(render_dl(c, ctx))
        elif name in ('blockquote',):
            # sphinx wraps tab/step content in <blockquote> even when it isn't a quote.
            # If it only holds structural containers, render without the '>' prefix.
            only_struct = all(
                (isinstance(ch, NavigableString) and not str(ch).strip()) or
                (isinstance(ch, Tag) and (
                    ch.find(class_=re.compile('sphinx-tabs')) is not None or
                    ch.find('dl', class_='py') is not None or
                    (ch.name=='div' and ch.find(['ol','ul','pre','table']) is not None)
                ))
                for ch in c.children
            )
            inner = block(c, ctx, depth).strip()
            if only_struct:
                out.append(inner)
            else:
                out.append('\n'.join(('> '+l if l else '>') for l in inner.split('\n')))
        else:
            sub = block(c, ctx, depth)
            if sub.strip(): out.append(sub)
    return '\n\n'.join(x for x in out if x and x.strip())

def render_admonition(c, ctx):
    title_el = c.find(class_=re.compile('admonition-title|title'))
    title = title_el.get_text().strip() if title_el else 'Note'
    body_parts=[]
    for ch in c.children:
        if isinstance(ch,Tag) and ch is title_el: continue
        if isinstance(ch,Tag):
            body_parts.append(block(BeautifulSoup(str(ch),'html.parser'),ctx))
    txt=('\n\n'.join(p for p in body_parts if p.strip())).strip()
    lines=[f'> **{title}**','>']
    for l in txt.split('\n'):
        lines.append('> '+l)
    return '\n'.join(lines)

def render_figure(c, ctx):
    cap = c.find('figcaption')
    captext = inline(cap, ctx).strip() if cap else ''
    imgmd=''
    img = c.find('img')
    svg = c.find('svg')
    if img is not None:
        imgmd = handle_img(img, ctx)
    elif svg is not None:
        imgmd = handle_svg(svg, ctx)
    res = imgmd
    if captext:
        res += f'\n\n*{captext}*'
    return res

def render_tabs(c, ctx):
    """sphinx-tabs -> per-platform subsections keyed by tab label."""
    # buttons in tablist
    labels = {}
    tablist = c.find(attrs={'role':'tablist'})
    if tablist:
        for btn in tablist.find_all('button'):
            ctrl = btn.get('aria-controls','')
            labels[ctrl] = btn.get_text().strip()
    panels = c.find_all('div', class_=re.compile('sphinx-tabs-panel'))
    out = []
    seen_content = {}
    for p in panels:
        pid = p.get('id','')
        label = labels.get(pid, '')
        content = block(p, ctx).strip()
        if not content:
            continue
        # dedupe identical panel bodies (common: same steps for all platforms)
        key = re.sub(r'\s+','',content)
        if key in seen_content:
            seen_content[key].append(label)
            continue
        seen_content[key] = [label]
        out.append(('LABELS_PLACEHOLDER', label, content))
    # emit with combined labels
    result = []
    for placeholder, first_label, content in out:
        labs = seen_content[re.sub(r'\s+','',content)]
        labs = [l for l in labs if l]
        header = ' / '.join(labs)
        if header:
            result.append(f'**平台 {header}**\n\n{content}')
        else:
            result.append(content)
    return '\n\n'.join(result)

def render_tabincludedirective(c, ctx):
    """dl.py.class wrapping a fake 'tabincludedirective' — real content is in <dd>."""
    parts = []
    for dd in c.find_all('dd', recursive=False):
        parts.append(block(dd, ctx))
    if not parts:
        # fallback: any figures
        for f in c.find_all('figure'):
            parts.append(render_figure(f, ctx))
    return '\n\n'.join(x for x in parts if x.strip())
    out=[]
    for ch in c.children:
        if not isinstance(ch,Tag): continue
        if ch.name=='dt':
            out.append('**'+inline(ch,ctx).strip()+'**')
        elif ch.name=='dd':
            out.append(': '+inline(ch,ctx).strip())
    return '\n\n'.join(out)

def render_list(c, ctx, kind, depth):
    out=[]
    idx=1
    for li in c.find_all('li', recursive=False):
        marker = f'{idx}. ' if kind=='ol' else '- '
        nested=[]        # nested lists / code blocks / images -> own lines under the item
        inline_parts=[]  # inline text of the item itself
        def walk(el):
            for ch in el.children:
                if isinstance(ch, Tag):
                    nm = ch.name.lower()
                    if nm in ('ul','ol'):
                        nested.append(render_list(ch,ctx,nm,0))
                    elif nm=='pre':
                        nested.append(render_code(ch))
                    elif nm in ('div',) and ('highlight' in ' '.join(ch.get('class',[])) or 'codeblock' in ' '.join(ch.get('class',[]))):
                        pre=ch.find('pre')
                        nested.append(render_code(pre) if pre else '')
                    elif nm=='figure':
                        nested.append(render_figure(ch,ctx))
                    elif nm=='img':
                        nested.append(handle_img(ch,ctx))
                    elif nm=='svg':
                        s=handle_svg(ch,ctx)
                        if s: nested.append(s)
                    elif nm=='table':
                        nested.append(render_table(ch,ctx))
                    elif nm in ('p','dd','dt'):
                        # a paragraph inside li: text stays inline unless it holds blocks
                        if ch.find(['ul','ol','pre','figure','table']):
                            walk(ch)
                        else:
                            inline_parts.append(inline(ch,ctx))
                    else:
                        inline_parts.append(inline(ch,ctx))
                else:
                    inline_parts.append(str(ch))
        walk(li)
        text=re.sub(r'\s+',' ',''.join(inline_parts)).strip()
        pad='  '*depth
        out.append(pad+marker+text)
        cont_pad = pad + '   '  # continuation indent for ordered; fine for ul too
        for n in nested:
            if not n.strip(): continue
            out.append('')
            for nl in n.split('\n'):
                out.append(cont_pad+nl if nl else nl)
        idx+=1
    return '\n'.join(out)

def render_code(pre):
    code = pre.find('code')
    lang=''
    target = code if code else pre
    for cl in target.get('class',[]):
        if cl.startswith('language-'):
            lang=cl[len('language-'):]
    txt = target.get_text()
    txt = txt.rstrip('\n')
    if lang in ('undefined','none','text',''):
        lang=''
    return f'```{lang}\n{txt}\n```'

def main():
    summary=[]
    for page in PAGES:
        html=open(os.path.join(RAW,page+'.html'),encoding='utf-8').read()
        body=get_body(html)
        if body is None:
            print(f'{page}: NO BODY'); continue
        soup=BeautifulSoup(body,'html.parser')
        root=soup.find('div',itemprop='articleBody') or soup
        # strip HTML comments (Visio SVG export banners etc.)
        for cm in root.find_all(string=lambda t: isinstance(t, Comment)):
            cm.extract()
        # remove UI-only elements
        for junk in root.select('.copyclip, .headerlink, .download-icon, #DownloadImage, .no-action-icons'):
            junk.decompose()
        ctx=Ctx(page)
        md=block(root,ctx)
        md=re.sub(r'\n{3,}','\n\n',md).strip()+'\n'
        with open(os.path.join(OUT,page+'.md'),'w',encoding='utf-8') as f:
            f.write(md)
        summary.append((page,len(md),ctx.imgc,len(ctx.imgs)))
        print(f'{page:14} md={len(md):6} imgs_saved={len(ctx.imgs)}')
    print('\nDONE. Total pages:',len(summary))

if __name__=='__main__':
    main()
