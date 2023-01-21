import sys
import json
from pathlib import Path

if __name__ == '__main__':
    dump = Path('dump')
    (dump / 'ThingDef').mkdir(exist_ok=True)

    data = json.loads((dump / 'thingdef.json').read_text(encoding='utf-8'))
    for k, xml in data.items():
        (dump / 'ThingDef' / (k+'.json')).write_text(json.dumps(xml, ensure_ascii=False))
