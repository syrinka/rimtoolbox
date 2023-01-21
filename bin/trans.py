import sys
import json


# 抽取中英对照，csv形式输出
if __name__ == '__main__':
    data = json.load(open(sys.argv[1], encoding='utf-8'))
    print('defName,zh')
    for k, v in data.items():
        if 'label' in v:
            print(f'{k},{v["label"]}')
