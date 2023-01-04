import sys
from rimtoolbox.parser import Workspace, Path

if __name__ == '__main__':
    w = Workspace()

    defpath = sys.argv[1]
    w.digest_dir(defpath / 'ThingDefs_Items')
    w.digest_dir(defpath / 'ThingDefs_Buildings')
    w.digest_dir(defpath / 'ThingDefs_Plants')
    w.digest_dir(defpath / 'ThingDefs_Races')
    w.digest_dir(defpath / 'ThingDefs_Misc', filter=lambda p: 'Ethereal' not in p.name)
    w.digest_dir(defpath / 'Drugs')
    w.digest_dir(defpath / 'HediffDefs')

    langpath = sys.argv[2]
    w.digest_dir(langpath / 'DefInjected' / 'ThingDef')

    w.solve_inherit()
    w.inject_langdata(ignore_extra=True)
    w.clean()
    w.dump('dump.json', indent=4)