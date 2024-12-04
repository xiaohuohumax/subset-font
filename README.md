# subset font

**这是一个精简字体的工具，只保留字体中常用的字，以减小字体体积**

> [!TIP]
> 常用字：英文 + 数字 + 符号 + 中文常用7000字，详见 [subset.txt](./subset.txt)

## ⏬ 精简字体

<!-- download_start -->
| 字体名称 | 文件名 | 精简前 | 精简后 | 许可证 |
| --- | --- | --- | --- | --- |
| 寒蝉圆黑体Regular | ChillRoundGothic.otf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/ChillRoundGothic.otf) 8.94MB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/ChillRoundGothic.otf) 2.46MB | [ChillRoundGothic.txt](licenses/ChillRoundGothic.txt) |
| HarmonyOS Sans | HarmonyOS_Sans.ttf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/HarmonyOS_Sans.ttf) 153.20KB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/HarmonyOS_Sans.ttf) 22.17KB | [HarmonyOS_Sans.txt](licenses/HarmonyOS_Sans.txt) |
| MiSans | MiSans.ttf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/MiSans.ttf) 7.70MB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/MiSans.ttf) 1.61MB | [MiSans.txt](licenses/MiSans.txt) |
| OPPO Sans 4.0 | OPPO Sans 4.0.ttf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/OPPO%20Sans%204.0.ttf) 21.69MB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/OPPO%20Sans%204.0.ttf) 4.54MB | [OPPO Sans 4.0.txt](licenses/OPPO%20Sans%204.0.txt) |
| 得意黑 斜体 | SmileySans-Oblique.ttf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/SmileySans-Oblique.ttf) 2.51MB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/SmileySans-Oblique.ttf) 1.87MB | [SmileySans-Oblique.txt](licenses/SmileySans-Oblique.txt) |
| 思源宋体 | SourceHanSerifSC.otf | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/fonts/SourceHanSerifSC.otf) 23.41MB | [下载](https://github.com/xiaohuohumax/subset-font/raw/main/dist/SourceHanSerifSC.otf) 4.54MB | [SourceHanSerifSC.txt](licenses/SourceHanSerifSC.txt) |
<!-- download_end -->

## 🔨 使用方法

### 1. 克隆仓库

```bash
git clone https://github.com/xiaohuohumax/subset-font.git
```

### 2. 安装依赖

```bash
# 项目使用 Rye 管理
rye sync

# 若未安装 Rye 则使用 pip 安装依赖
pip install --no-cache-dir -r requirements.lock
```
### 3. 自定义精简字库

修改 subset.txt 文件，添加或删除需要保留的字（注意：# 开头的行会被忽略）

### 4. 准备字体文件

将需要精简的字体文件（.otf，.ttf，.woff，.woff2）放到 fonts 目录下

### 5. 运行脚本

```bash
# -h 查看帮助
rye run start [-h]

# 或者
python -m subset-font [-h]
```

### 6. 输出结果

在 dist 目录下会生成精简后的字体文件，文件名与 fonts 目录下的文件名相同

### 7. 字体预览

dist 目录下会生成 index.html，用浏览器打开即可预览字体效果

## ℹ License

[MIT](./LICENSE)