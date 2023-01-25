# Rimtoolbox

用于提取 [Rimworld](https://rimworldgame.com/) 游戏数据的小工具

> 由于泰南设计的游戏数据格式太自由了，不能保证提取的数据是完全正确的，只能说是大部分

## Usage

复制一份 `.env.dist` 重命名为 `.env`，填写其中的路径，其中

- `RIM_DATA_PATH` 是游戏数据，一般是 `.../RimWorld/Data/Core/Defs`
- `RIM_TRANS_PATH` 是翻译数据，用于替换 `label` 与 `description` 部分，一般是 `.../RimWorld/Data/Core/Languages/{LANG}.tar/DefInjected/ThingDef/` 解压后的内容 (optional)

使用 [go-task](https://github.com/go-task/task) 做了自动化，详细见 Taskfile.yml
