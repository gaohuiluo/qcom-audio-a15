#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite intra-site .html links to .md in zh docs so they work locally.
Only touches relative links (not http/https). Drops #anchors (en anchors
don't match zh headings)."""
import os, re

ZH = r"e:/Android/qcom-audio-a15/qcom-audio/qualcomm-audioreach-blog/audioreach-docs-site/md_zh"

# match markdown link targets: ](target)
LINK = re.compile(r'\]\(([^)]+)\)')

def fix_target(t):
    # skip external / absolute / mail
    if re.match(r'^[a-zA-Z]+://', t) or t.startswith('//') or t.startswith('mailto:'):
        return t
    # skip pure anchors and images (images handled separately, but _images won't end in .html)
    # only rewrite if it points at an .html page
    m = re.match(r'^([^#?]*\.html)(#.*)?$', t)
    if not m:
        return t
    path = m.group(1)
    # drop anchor, switch extension
    return path[:-5] + '.md'

def process(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    def repl(mo):
        return '](' + fix_target(mo.group(1)) + ')'
    ns = LINK.sub(repl, s)
    if ns != s:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(ns)
        return True
    return False

changed = 0
for root, _, files in os.walk(ZH):
    for fn in files:
        if fn.endswith('.md'):
            if process(os.path.join(root, fn)):
                changed += 1
print(f"rewrote links in {changed} files")
