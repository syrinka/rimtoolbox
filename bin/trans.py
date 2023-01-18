import sys
import json


# 抽取中英对照，csv形式输出
if __name__ == '__main__':
    dup = set()
    data = json.load(open(sys.argv[1]))
    print('en,zh')
    for k, v in data.items():
        if 'label' in v and 'label-zh' in v:
            if v['label'] in dup:
                continue
            else:
                print(f'{v["label"]},{v["label-zh"]}')
                dup.add(v['label'])
