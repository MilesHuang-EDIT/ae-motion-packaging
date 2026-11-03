---
name: ae-motion-packaging
description: Design and produce editable Adobe After Effects motion packaging for product films, event recaps, award videos and comparable branded videos, from scripts and references through style frames, animation, previews and portable AE delivery. Also use for scoped revisions and localization of those projects. A browser preview is a review surface; an AE request requires a native AE project.
---

# AE 动效包装工作流

根据视频内容、品牌与参考，设计视觉系统并交付可编辑、素材可替换的 AE 工程。每次重新定义视觉，不默认复刻某个历史赛事或工业科技风格。

## 先确定制作约定

判断是新项目、延续工程，还是有限范围修改。延续项目先定位用户指定版本及原生工程，核对合成、素材和画面；预览地址与修改日期只作为线索。

从已给材料整理以下信息，不重复询问已经确认的事项：

- 目标、观众、平台/画幅、分辨率、帧率、时长与语言。
- 脚本和段落、品牌/参考、素材质量、真实内容还是可替换占位。
- BGM、节拍原点、关键重音、段落切点和允许误差。
- 仅画面还是包含声音；工程/视频交付范围；用户约定的审阅节点。

会改变制作方向的缺失信息优先确认；常规制作选择自行判断。用户授权直接制作或跳过审阅节点时照办。

## 设计与审阅

需要脚本拆解、风格图、运镜或音乐节奏设计时，读 [设计与审阅](references/design-and-review.md)。

1. 提炼每段的核心信息、素材主次、阅读动作及开始/结束状态，再建立全片结构。
2. 根据品牌与参考建立视觉系统。方向有分歧时先用效果图比较；多段视频可交付风格图集合。
3. 按约定确认关键帧，再做代表段动效，验证运动、阅读与素材适配后扩展。批准风格的局部修改直接延续。
4. 变化来自信息层级、空间、载体与剪辑节奏，不只是换颜色；避免全片套同一背景与左右版式。

## AE 制作

制作或修改原生 AE 工程前，读 [AE 实现](references/ae-implementation.md)。

- 用户要求 AE 时，实际保存可打开的 `.aep`；HTML、Remotion、视频可以辅助预览，不能替代 AE 工程。
- 延续本工作流时优先独立分段合成，可另设整片审片合成。用户有其他明确要求时遵循其选择。
- 文字、数据与主要包装尽量原生可编辑；素材放在清晰命名的替换预合成中，考虑横/竖比例和画质。
- 以背景、前景、展示载体和光影建立空间。运镜要有目标、加减速与稳定阅读停留，避免持续无目的摇摆。
- 新项目重新确定规格，不自动沿用旧工程的 1080p、字体、BPM、压暗比例或赛事数据。
- 生图可辅助环境、材质与概念图；需要编辑的标题/数据保留为原生文字。按当前可用的工具/技能生成图片。

## 迭代与交付

验证、渲染、局部改版或打包时，读 [验证与交付](references/verification-and-delivery.md)。

- 反馈定位到合成、图层与时间点；保留批准的结构和运动。只改一段时，只渲染变更段。
- 除技术规格，还检查小播放器中的文字可读性、出现顺序、边界、镜头落点、阅读时间、背景露边与替换框适配。
- 原生工程保存、媒体规格、播放/解码和便携工程重开分别验证，不能互相替代。
- 交付本轮明确的工程/预览/ZIP 链接，简述变化。单段交付不打入整个历史项目。

## 工具与案例

辅助脚本使用 Python 3.9+ 标准库；不依赖本案例的 Node 工程或私有目录。

- `scripts/verify_media.py`：按明确输出约定核对尺寸、帧率、帧数、时长和音轨，可完整解码。需要 `ffprobe`，解码另需 `ffmpeg`；支持参数指定工具路径。
- `scripts/package_project.py`：按明确文件清单打包，核对 ZIP CRC 和成员哈希；不代替原生便携重开验证。
- [Make a Sign 案例](references/make-a-sign-case.md)：只在需要理解历史取舍或查找实例时读取；案例参数不是通用默认值。
