import json, os, glob
from collections import Counter

files = sorted(glob.glob('/Users/johnny/.claude/projects/-Users-johnny-projects-omnibot-new/*.jsonl'),
               key=os.path.getmtime, reverse=True)[:50]

counts = Counter()
for fpath in files:
    try:
        with open(fpath) as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    for item in obj.get('message', {}).get('content', []):
                        if item.get('type') == 'tool_use':
                            name = item.get('name', '')
                            if name == 'Bash':
                                cmd = item.get('input', {}).get('command', '')
                                parts = cmd.strip().split()
                                if not parts:
                                    continue
                                first = parts[0]
                                if first in ('sudo', 'timeout'):
                                    if len(parts) > 1:
                                        first = parts[1].split('/')[-1]
                                elif '=' in first:
                                    for p in parts[1:]:
                                        if '=' not in p:
                                            first = p.split('/')[-1]
                                            break
                                    else:
                                        first = 'env'
                                else:
                                    first = first.split('/')[-1]
                                if len(parts) > 1 and parts[1] not in ('&&', '||', ';', '|'):
                                    key = f'{first} {parts[1]}'
                                else:
                                    key = first
                                counts[key] += 1
                            elif name.startswith('mcp__'):
                                counts[name] += 1
                except:
                    pass
    except:
        pass

for k, v in counts.most_common(30):
    print(f'{v}\t{k}')