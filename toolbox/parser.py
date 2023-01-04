import json
import re
from typing import Optional, Union, Dict, List
from pathlib import Path
from collections import OrderedDict

import xmltodict

from . import log
from .schemas.base import ThingDefsMixin

__all__ = ['Workspace']


class Workspace(object):
    defs: Dict[str, Dict]
    _refs: Dict[str, Dict]
    langdata: Dict[str, str]

    def __init__(self):
        self.defs = {}
        self._refs = {}
        self.langdata = {}

    def digest(self, path: Union[str, Path]):
        if isinstance(path, str):
            path = Path(path)

        assert path.is_file(), 'Digest path %s not file' % path
        assert path.suffix == '.xml', 'Digest file must be xml file'

        data = xmltodict.parse(path.read_text('utf-8'), force_list=('ThingDef', 'li'))

        if data.get('Defs') and data['Defs'].get('ThingDef'):
            logger.debug('digest file as thingdefs: %s' % path)
            thingdefs = data['Defs']['ThingDef']
            for thingdef in thingdefs:
                # thingdef.pop('comps', None) # uncomment if to ignore comps
                if '@Name' in thingdef:
                    logger.trace('parent name load: [%s]' % thingdef['@Name'])
                    self._refs[thingdef['@Name']] = thingdef
                if not '@Abstract' in thingdef:
                    self.defs[thingdef['defName']] = thingdef
        elif data.get('LanguageData'):
            logger.debug('digest file as langdata: %s' % path)
            self.langdata.update(data['LanguageData'])
        else:
            logger.warning('unknown file content, ignore: %s' % path)

    def digest_dir(self, path: Union[str, Path], depth=-1):
        if isinstance(path, str):
            path = Path(path)

        assert path.is_dir(), 'Digest path %s not dir' % path

        for path in path.iterdir():
            if path.is_file() and path.suffix == '.xml':
                self.digest(path)
            elif path.is_dir():
                if depth > 0:
                    self.digest_dir(path, depth-1)
                elif depth == -1:
                    self.digest_dir(path, -1)

    def solve_inherit(self):
        def merge_comp(li, base):
            # 合并两个 comp 列表：
            # 若两个元素有相同的 compClass 键，则使用 li 中的元素
            to_extend = []
            for item in li:
                if isinstance(item, dict) and 'compClass' in item:
                    for i in li:
                        if i.get('compClass') == item['compClass']:
                            logger.warning('collide')
                            break
                    else:
                        to_extend.append(item)
                else:
                    to_extend.append(item)
            li.extend(to_extend)

        def cut_inherit(child, parent):
            # 解耦两个 thingdef 间的继承关系
            assert child['@ParentName'] == parent['@Name']
            assert not parent.get('@ParentName')
            child.pop('@ParentName')

            logger.trace('cut [%s] --> [%s]'
                % (child.get('defName') or child['@Name'], parent['@Name']))

            for k, v in parent.items():
                if k in ('@Abstract', '@Name', '@ParentName'):
                    # 特殊 key 不予覆盖
                    pass
                elif k not in child:
                    # 该 key 在子类未定义，遂覆盖之
                    child[k] = v
                elif isinstance(child[k], dict):
                    if child[k].get('@Inherit', '').lower() == 'false':
                        # 该 key 有不继承标注，移除该标注，若移除标注后 key 内无内容，则将该 key 也移除
                        # Note:
                        #   有时子类会给父类并没有的 key 打上不继承标注
                        #   这些仅子类拥有的 key 无法被遍历到
                        #   因此 dump 的结果依然会有非预期的 @Inherit 存在
                        child[k].pop('@Inherit')
                        if not child[k].keys():
                            child.pop(k)

                    elif child[k].get('li') and parent[k].get('li'):
                        # 该 key 指向一个列表，尝试合并
                        if k == 'comp':
                            merge_comp(child[k]['li'], parent[k]['li'])
                        else:
                            child[k]['li'].extend(parent[k]['li'])

        logger.info('cut inherit')
        for name, data in self.defs.items():
            if '@ParentName' not in data:
                continue

            mro = [data] # inherit link: child <---> parent
            while True:
                parent_name = mro[-1].get('@ParentName')
                if parent_name is None:
                    break

                try:
                    parent = self._refs[parent_name]
                except KeyError:
                    logger.warning('when solving inherit for [%s], parent [%s] is missing' % (name, parent_name))
                    break
                mro.append(parent)

            # 倒序覆盖
            for index in range(len(mro)-1):
                cut_inherit(mro[-index-2], mro[-index-1])

    def inject_langdata(self, ignore_extra=False):
        logger.info('inject langdata')
        for k, v in self.langdata.items():
            name, part = k.split('.', 1)
            if part not in ('label', 'description'):
                continue

            logger.trace('langdata %s' % k)
            try:
                data = self.defs[name]
            except KeyError:
                if not ignore_extra:
                    logger.warning('dangling langdata for [%s]' % name)
                continue
            data[part] = v

    def clean(self):
        logger.info('clean')

        for data in self.defs.values():
            data.pop('@Name', None)
            data.pop('@ParentName', None)
            # 将 <li> 转换成正常的列表
            for k, v in data.items():
                if isinstance(v, dict) and v.get('li'):
                    data[k] = v['li']

    def dump(self, path, indent=0):
        if isinstance(path, str):
            path = Path(path)

        text = json.dumps(self.defs, indent=indent, ensure_ascii=False)
        path.write_text(text)
