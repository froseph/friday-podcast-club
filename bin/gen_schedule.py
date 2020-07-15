#!/usr/bin/env python3
import argparse
from collections import OrderedDict
import csv
import datetime
import re

import chevron

parser = argparse.ArgumentParser(description='Generate schedule for podcast club from CSV')
#parser.add_argument('input', metavar='N', type=int, nargs='+',
#                   help='an integer for the accumulator')
parser.add_argument('--all', dest='all', action='store_true',
                   default=False, help='regenerate all schedules')
parser.add_argument('-c', dest='csv_file', action='store',
                    help='input csv file')
parser.add_argument('-t', dest='tmpl_file', action='store',
                    help='input template file')
parser.add_argument('-o', dest='out_dir', action='store',
                    default='.',
                    help='output directory')

def render_item(d, template_file, out_dir):
    # join string
    filename = ''.join([
        re.sub(r'[^\w]', '', d['date']),
        '_', d['episode'], '_-_', d['podcast']])
    # strip bad characters
    filename = re.sub(r'[^0-9a-zA-Z-_ ]', '', filename)
    # replace spaces with underscore
    filename = re.sub(r'\ ', '_', filename)
    # normalize & add suffix
    filename = filename.lower() + '.md'

    # generate sources
    sources = []
    # unfortuneately tied to order
    start_sources = False
    for k,v in d.items():
        if 'tags' == k:
            start_sources = True
            continue
        if start_sources and v:
            #sources[k] = {'source': k, 'url':v}
            sources.append({'source': k.title(), 'url':v})
    d['sources'] = sources

    # generate tags
    d['tags'] = d['tags'].split(',')

    # generate-post_date
    d['post_date'] = d['date']

    # generate date string
    parse_date = datetime.datetime.strptime(d['date'], '%Y-%m-%d')
    out_date = datetime.datetime.strftime(parse_date, '%A, %B %-d, %Y')
    d['meeting_date'] = out_date

    # TODO lots of file io-- we could cache template into a string
    with open(template_file, 'r') as f:
        render = chevron.render(f, d)
        with open(''.join([out_dir, '/', filename]), 'w') as o:
            o.write(render)

args = parser.parse_args()
with open(args.csv_file, newline='') as f:
    reader = csv.DictReader(f, quoting=csv.QUOTE_MINIMAL)
    if not args.all:
        item = list(reader)[-1]
        render_item(item, args.tmpl_file, args.out_dir)
    else:
        for row in reader:
            render_item(row, args.tmpl_file, args.out_dir)
