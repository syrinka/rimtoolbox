import sys
import xmltodict
from pathlib import Path


if __name__ == '__main__':
    print('from,key,cn')
    for path in Path(sys.argv[1]).iterdir():
        if not path.is_file() or path.suffix != '.xml':
            continue
        data = xmltodict.parse(path.read_text('utf-8'))
        for k, v in data['LanguageData'].items():
            print(','.join([path.name.split('.')[0], k, v or '']))
