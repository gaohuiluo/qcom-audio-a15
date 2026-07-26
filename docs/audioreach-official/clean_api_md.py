#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clean up API reference Markdown converted from Doxygen HTML.

Fixes two systematic readability defects in md_zh/api/*.md (and any file passed):
  1. Fragmented code spans -- every C token wrapped in its own backticks,
     e.g. **`typedef` `void` `*``gsl_handle_t`**  ->  `typedef void *gsl_handle_t`
  2. Run-on paragraphs -- labeled sub-sections glued onto one physical line,
     e.g. ...**相关数据类型**capi_proplist_t **详细说明**text ****text
     -> each label starts its own paragraph, **** becomes a paragraph break.

Content is preserved; only whitespace / delimiters are reshaped.
"""
import re
import sys

# Sub-section labels that should always begin their own block (bilingual).
LABELS = [
    "相关数据类型", "详细说明", "详细描述", "依赖项", "依赖",
    "返回值", "返回", "参数",
    "Related data types", "Detailed description", "Detailed Description",
    "Dependencies", "Returns", "Return", "Parameters", "Copyright",
    "Error code", "Error Code",
]


def merge_backtick_fragments(text: str) -> str:
    """Collapse a run of adjacent backtick fragments into one code span.

    Rule inside a run:
      ``  (two adjacent backticks) -> glue, no space
      ` ` (backtick space backtick) -> single space
    Applied only where 2+ backtick fragments touch (a real signature),
    so ordinary single `foo` spans are left untouched.
    """
    # Match a run of >=2 backtick-delimited fragments separated by
    # optional whitespace (the fragmented-signature pattern).
    frag = r"`[^`]*`"
    run = re.compile(r"(?:%s)(?:\s*%s)+" % (frag, frag))

    def repl(m):
        s = m.group(0)
        # glue: `` -> ''
        s = s.replace("``", "")
        # space separator: `<ws>` -> single space
        s = re.sub(r"`\s+`", " ", s)
        # remove any remaining internal backtick boundaries
        inner = s.strip("`")
        inner = inner.replace("`", "")
        inner = re.sub(r"[ \t]{2,}", " ", inner).strip()
        return "`%s`" % inner

    return run.sub(repl, text)


def split_glued_labels(line: str) -> str:
    """Insert paragraph breaks before glued bold labels and around ****."""
    # First, normalize runs of 4+ asterisks (collapsed empty bold pairs)
    # into a blank-line separator.
    line = re.sub(r"\*{4,}", "\n\n", line)

    # For each known label, ensure a blank line precedes **Label**
    # when it appears mid-line (i.e. preceded by non-newline text).
    for lbl in LABELS:
        # **Label** possibly followed directly by a colon variant
        pat = re.compile(r"(?<!\n)(?<!^)\s*(\*\*%s[：:]?\*\*)" % re.escape(lbl))
        line = pat.sub(lambda m: "\n\n" + m.group(1), line)
        # Some labels lost their closing ** and are glued to following text:
        # **详细说明text  -> **详细说明** text  (best-effort, label only)
        pat2 = re.compile(r"\*\*(%s[：:]?)\*\*[ \t]*" % re.escape(lbl))
        line = pat2.sub(lambda m: "**%s** " % m.group(1), line)
    return line


def clean(text: str) -> str:
    text = merge_backtick_fragments(text)
    out_lines = []
    for line in text.split("\n"):
        if "**" in line:
            line = split_glued_labels(line)
        out_lines.append(line)
    text = "\n".join(out_lines)
    # Strip trailing whitespace on every line.
    text = "\n".join(l.rstrip() for l in text.split("\n"))
    # Collapse 3+ blank lines into exactly one blank line.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main(paths):
    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            src = f.read()
        dst = clean(src)
        with open(p, "w", encoding="utf-8") as f:
            f.write(dst)
        print("cleaned:", p)


if __name__ == "__main__":
    main(sys.argv[1:])
