#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert crawled AudioReach Sphinx HTML pages to clean Markdown."""
import os, re, sys
from bs4 import BeautifulSoup, NavigableString, Tag

RAW = r"e:/Android/qcom-audio-a15/qcom-audio/qualcomm-audioreach-blog/audioreach-docs-site/raw"
OUT = r"e:/Android/qcom-audio-a15/qcom-audio/qualcomm-audioreach-blog/audioreach-docs-site/md_en"

SKIP = {"genindex.html", "search.html", "py-modindex.html"}

def rel_images_prefix(page_rel):
    # page_rel like "design/index.html" -> depth 1 -> "../_images"
    depth = page_rel.count("/")
    return ("../" * depth) + "_images"

def clean_text(s):
    return re.sub(r"[ \t]+", " ", s.replace("\u00a0", " ")).strip()

def clean_inline(s):
    # collapse internal whitespace/newlines to single spaces, but PRESERVE
    # a single leading/trailing space so inter-element spacing survives.
    s = s.replace("\u00a0", " ")
    lead = " " if s[:1].isspace() else ""
    trail = " " if s[-1:].isspace() else ""
    core = re.sub(r"\s+", " ", s).strip()
    if not core:
        return " " if (lead or trail) else ""
    return lead + core + trail

class Converter:
    def __init__(self, page_rel):
        self.page_rel = page_rel
        self.imgpref = rel_images_prefix(page_rel)

    def conv_children(self, node, indent=""):
        out = []
        for c in node.children:
            out.append(self.conv(c, indent))
        return "".join(out)

    def inline(self, node):
        # inline rendering (no block breaks)
        if isinstance(node, NavigableString):
            return clean_inline(str(node))
        if not isinstance(node, Tag):
            return ""
        name = node.name
        if name in ("strong", "b"):
            return "**" + self.inline_children(node).strip() + "**"
        if name in ("em", "i"):
            return "*" + self.inline_children(node).strip() + "*"
        if name in ("sup", "sub"):
            return self.inline_children(node).strip()
        if name == "code" or (name == "span" and "pre" in node.get("class", [])):
            return "`" + node.get_text().strip() + "`"
        if name == "a":
            txt = self.inline_children(node).strip()
            href = node.get("href", "")
            if not txt:
                return ""
            if href.startswith("#") or not href:
                return txt
            return f"[{txt}]({href})"
        if name == "br":
            return " "
        if name == "img":
            return self.img(node)
        return self.inline_children(node)

    def inline_children(self, node):
        return "".join(self.inline(c) for c in node.children)

    def img(self, node):
        src = node.get("src", "")
        alt = node.get("alt", "").strip()
        m = re.search(r"_images/(.+)$", src)
        fname = m.group(1) if m else src
        if m:
            src = f"{self.imgpref}/{m.group(1)}"
        # Sphinx often sets alt to the src path; make a cleaner alt.
        if not alt or "_images/" in alt or alt == fname:
            alt = os.path.splitext(os.path.basename(fname))[0].replace("_", " ")
        return f"![{alt}]({src})"

    def conv(self, node, indent=""):
        if isinstance(node, NavigableString):
            t = str(node)
            if t.strip() == "":
                return ""
            return clean_text(t)
        if not isinstance(node, Tag):
            return ""
        name = node.name
        cls = node.get("class", [])

        # headings
        if name in ("h1","h2","h3","h4","h5","h6"):
            # strip headerlink anchor
            for a in node.select("a.headerlink"):
                a.decompose()
            level = int(name[1])
            txt = self.inline_children(node).strip()
            txt = txt.rstrip("¶").strip()
            return f"\n{'#'*level} {txt}\n\n"

        # admonitions (note / warning)
        if name == "div" and "admonition" in cls:
            kind = "NOTE"
            if "warning" in cls: kind = "WARNING"
            elif "note" in cls: kind = "NOTE"
            title_el = node.find(class_="admonition-title")
            if title_el:
                title = title_el.get_text().strip()
                title_el.extract()
            else:
                title = kind.title()
            inner = self.conv_children(node).strip()
            lines = inner.splitlines()
            quoted = "\n".join(("> " + l) if l.strip() else ">" for l in lines)
            return f"\n> **{title}**\n>\n{quoted}\n\n"

        # code blocks
        if name == "div" and any(c.startswith("highlight") for c in cls):
            lang = ""
            for c in cls:
                if c.startswith("highlight-"):
                    lang = c[len("highlight-"):]
            if lang in ("default","text"): lang = ""
            pre = node.find("pre")
            code = pre.get_text() if pre else node.get_text()
            code = code.rstrip("\n")
            return f"\n```{lang}\n{code}\n```\n\n"
        if name == "pre":
            return f"\n```\n{node.get_text().rstrip()}\n```\n\n"

        # tables
        if name == "table":
            return self.table(node)

        # lists
        if name == "ul":
            return self.list(node, indent, ordered=False)
        if name == "ol":
            return self.list(node, indent, ordered=True)

        # paragraphs
        if name == "p":
            txt = self.inline_children(node).strip()
            return txt + "\n\n" if txt else ""

        # figure / image standalone
        if name == "img":
            return "\n" + self.img(node) + "\n\n"
        if name in ("figure",):
            img = node.find("img")
            cap = node.find("figcaption")
            s = "\n" + (self.img(img) if img else "")
            if cap:
                s += "\n*" + cap.get_text().strip() + "*"
            return s + "\n\n"

        # definition lists -> rendered as bold term + desc
        if name == "dl":
            return self.dl(node, indent)

        # blockquote: Sphinx uses these as indentation wrappers, not real
        # quotes. Unwrap and render children as normal blocks.
        if name == "blockquote":
            return self.conv_children(node, indent)

        # section / div / span / others -> recurse
        if name in ("section","div","span","article","main","dd","dt"):
            return self.conv_children(node, indent)

        # inline fallbacks
        if name in ("strong","b","em","i","code","a","br"):
            return self.inline(node)

        return self.conv_children(node, indent)

    def list(self, node, indent, ordered):
        out = ["\n"]
        i = 1
        for li in node.find_all("li", recursive=False):
            marker = f"{i}. " if ordered else "- "
            inline_parts = []
            block_parts = []
            # unwrap blockquote>div wrappers that Sphinx adds around nested lists
            children = list(li.children)
            for c in children:
                if isinstance(c, Tag) and c.name in ("ul", "ol"):
                    block_parts.append(self.list(c, indent + "  ", c.name == "ol"))
                elif isinstance(c, Tag) and c.name == "blockquote":
                    # nested list wrapped in blockquote>div
                    for sub in c.find_all(["ul", "ol"], recursive=True):
                        block_parts.append(self.list(sub, indent + "  ", sub.name == "ol"))
                        break
                elif isinstance(c, Tag) and c.name == "p":
                    # a paragraph inside <li> is the item's own text
                    if inline_parts or block_parts:
                        block_parts.append(self.inline_children(c).strip())
                    else:
                        inline_parts.append(self.inline_children(c))
                elif isinstance(c, Tag) and c.name in ("div", "pre", "table", "dl"):
                    block_parts.append(self.conv(c, indent + "  "))
                else:
                    inline_parts.append(self.inline(c))
            head = clean_inline("".join(inline_parts)).strip()
            line = f"{indent}{marker}{head}".rstrip()
            out.append(line + "\n")
            for b in block_parts:
                b = b.strip("\n")
                if not b:
                    continue
                for bl in b.splitlines():
                    out.append(f"{indent}  {bl}\n" if bl.strip() else "\n")
            i += 1
        out.append("\n")
        return "".join(out)

    def dl(self, node, indent):
        out = ["\n"]
        for child in node.find_all(["dt","dd"], recursive=False):
            if child.name == "dt":
                for a in child.select("a.headerlink"): a.decompose()
                term = self.inline_children(child).strip().rstrip("¶").strip()
                if term:
                    out.append(f"**{term}**\n\n")
            else:
                out.append(self.conv_children(child, indent).strip() + "\n\n")
        return "".join(out)

    def table(self, node):
        rows = []
        # collect header
        thead = node.find("thead")
        header = []
        if thead:
            for th in thead.find_all(["th","td"]):
                header.append(self.inline_children(th).strip().replace("\n"," "))
        body_rows = []
        tbody = node.find("tbody") or node
        for tr in tbody.find_all("tr", recursive=False):
            cells = tr.find_all(["td","th"], recursive=False)
            if not cells: continue
            body_rows.append([self.inline_children(c).strip().replace("\n"," ").replace("|","\\|") for c in cells])
        if not header and body_rows:
            header = body_rows[0]; body_rows = body_rows[1:]
        if not header:
            return ""
        ncol = len(header)
        header = [h.replace("|","\\|") for h in header]
        out = ["\n| " + " | ".join(header) + " |\n"]
        out.append("| " + " | ".join(["---"]*ncol) + " |\n")
        for r in body_rows:
            while len(r) < ncol: r.append("")
            out.append("| " + " | ".join(r[:ncol]) + " |\n")
        out.append("\n")
        return "".join(out)

def convert_file(page_rel):
    src = os.path.join(RAW, page_rel)
    with open(src, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    body = soup.find("div", itemprop="articleBody")
    if not body:
        body = soup.find("div", role="main") or soup.body
    conv = Converter(page_rel.replace("\\","/"))
    md = conv.conv_children(body)
    # cleanup: collapse >2 blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    # normalize trademark: "AudioReachTM" -> "AudioReach™"
    md = md.replace("AudioReachTM", "AudioReach™")
    return md.strip() + "\n"

def main():
    pages = []
    for root, _, files in os.walk(RAW):
        for fn in files:
            if fn.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, fn), RAW).replace("\\","/")
                if rel in SKIP: continue
                pages.append(rel)
    pages.sort()
    for rel in pages:
        md = convert_file(rel)
        outpath = os.path.join(OUT, rel[:-5] + ".md")
        os.makedirs(os.path.dirname(outpath), exist_ok=True)
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"OK {rel} -> {len(md)} chars")

if __name__ == "__main__":
    main()
