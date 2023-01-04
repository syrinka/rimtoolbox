game data root at `../steamapps/common/RimWorld/Data/Core/`

## ThingDefs

- `/Defs/ThingDefs_*/`
- `/Defs/Drugs/` 药物与酒精
- `/Defs/HediffDefs/` 器官与植入物

## LangData

- `/Languages/{LANG}/DefInjected/ThingDef/`

## Sample

```python
w = Workspace()

defpath = root / 'Defs'
w.digest_dir(defpath / 'ThingDefs_Items')
w.digest_dir(defpath / 'ThingDefs_Buildings')
w.digest_dir(defpath / 'ThingDefs_Plants')
w.digest_dir(defpath / 'ThingDefs_Races')
w.digest_dir(defpath / 'ThingDefs_Misc', filter=lambda p: 'Ethereal' not in p.name)
w.digest_dir(defpath / 'Drugs')
w.digest(defpath / 'HediffDefs' / 'Hediffs_Psycasts.xml')
w.digest_dir(defpath / 'HediffDefs' / 'BodyParts')

langpath = root / 'Languages'
w.digest_dir(langpath / 'ChineseSimplified (简体中文)' / 'DefInjected' / 'ThingDef')
```
