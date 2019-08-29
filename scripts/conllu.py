#!/usr/bin/env python

"""
Convert bipolar corpus conllu 1.0 to 2.0. may work on other conll data,
but this is not tested, this is just a very quick and dirty script for
a once off job

./fixed contains the conll-u v2 data
./fresh makes a new version of the plain texts for parsing
"""

import os
import re


def _get_wordclass(p):
    if p == ".":
        return "PUNCT"
    trans = dict(n="NOUN", v="VERB", j="ADJ", r="ADV", i="ADP", m="AUX", d="DET", p='-PRON-')
    return trans.get(p[0].lower(), p.lower())


def _parse_to_text(line):
    text = line.split("=", 1)[-1]
    text = re.sub(r"\([^\s]+", "", text)
    text = re.sub(r"\)+ ", " ", text)
    text = re.sub(" +", " ", text)
    return text.strip()


def _make_line(line, meta):
    out = line.strip() + " <metadata "
    for k, v in sorted(meta.items()):
        out += '{}="{}" '.format(k, v)
    out = out.strip() + ">"
    return out


if not os.path.isdir('fixed'):
    os.makedirs("fixed")
if not os.path.isdir('fresh'):
    os.makedirs("fresh")

listed = os.listdir(".")

for i, fname in enumerate(listed, start=1):
    print(f'Doing {i}/{len(listed)}: {fname}')
    if not fname.endswith(".conll"):
        continue
    with open(fname, "r") as fo:
        data = fo.read()

    out_sents = list()
    sents = data.split("\n\n")
    to_reparse = list()
    for sent in sents:
        parse = None
        comments = []
        rows = []
        lines = sent.splitlines()
        for line in lines:
            if line.startswith("#"):
                # line is really broken
                if line.startswith('# speaker') and len(line) and '<metadata' in line:
                    # print('broke as')
                    line = line.split('<metadata ', 1)[-1]
                    #  <metadata currentpost="6" date="2007-01-31" gender="F" joined="2
                if 'currentpost' in line and 'gender' in line and 'postgroup' in line:
                    # print('big fix')
                    speak = next((i for i in comments if i.startswith('# speaker')), None)
                    if speak:
                        comments.remove(speak)
                    line = line.split(' ', 1)[-1]
                    bits = line.split('" ')
                    for bit in bits:
                        key, val = bit.split('=', 1)
                        key = key.strip()
                        val = val.strip('"').strip()
                        # print('FIXING', key, val)
                        comments.append(f'# {key} = {val}')
                    continue
                # fix sent id
                if "sent_id " in line:
                    line = line.replace("sent_id ", "sent_id=")
                # add text
                elif "parse=" in line:
                    text = _parse_to_text(line)
                    comments.append("# text = {}".format(text))
                # fix equals
                line = line.replace("=", " = ", 1)
                comments.append(line)
            elif line.split("\t", 1)[0].isdigit():
                _, i, w, l, p, _, g, f, c, e = line.split("\t")
                x = _get_wordclass(p)
                row = "\t".join([i, w, l, x, p, '_', g, f, c, e])
                rows.append(row)

        # for our reparsing
        meta = dict()
        plain = ""
        for line in comments:
            if line.startswith("# text"):
                plain = line.split(" = ", 1)[-1]
                continue
            if line.startswith("# sent_id = "):
                continue
            key, val = line.split(" = ", 1)
            key = key.strip("# ").strip()
            val = val.strip('"').strip("'").strip()
            meta[key] = val
        to_reparse.append(_make_line(plain, meta))

        # for our fixing
        comments = "\n".join(comments)
        rows = "\n".join(rows)
        fixed = comments.strip() + "\n" + rows.strip()
        out_sents.append(fixed)

    to_reparse = "\n".join(to_reparse)
    fixed = "\n\n".join(out_sents)

    outpath = os.path.join("fixed", fname + "u")
    newpath = os.path.join("fresh", os.path.splitext(fname)[0])

    with open(newpath, "w") as fo:
        fo.write(to_reparse.strip() + "\n")
    with open(outpath, "w") as fo:
        fo.write(fixed)
