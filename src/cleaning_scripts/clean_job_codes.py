import re

lines = []
with open('../../data/raw/job_codes/job_codes.txt') as f:
    [lines.append(l[:-7]) for l in f.readlines() if re.match(r'^\d{3}.*<br />\n$', l)]

lines = [l[:3] + ',' + l[4:]for l in lines]
lines.insert(0, 'code,name')

with open('../../data/clean/job_codes/job_codes.csv', 'w') as f:
    f.write('\n'.join(lines))
