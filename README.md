# AE Motion Packaging · AE 动效包装工作流

面向赛事回顾、产品片、活动视频等品牌内容的 Agent Skill：从脚本、品牌和参考出发，设计视觉系统，制作可编辑的 Adobe After Effects 动效，并完成分段预览、局部修改与便携交付。

## 工作流程

需求与素材梳理 → 风格图集合 → 代表段动效 → 分段制作 → 预览审阅 → 工程与媒体验证 → 紧凑打包。

每个新项目重新确定视觉方向、画幅、帧率、字体与音乐节奏。文字和数据保留编辑能力，素材放入清楚命名的替换预合成。运镜关注空间关系、明确落点和阅读停留。

## 安装与调用

将此仓库交给支持 Agent Skills 的客户端安装，Skill 入口为根目录 `SKILL.md`。在支持 skill-installer 的 Codex 环境中，可以提供本仓库链接并说：

> 使用 $skill-installer，从 https://github.com/MilesHuang-EDIT/ae-motion-packaging 安装根目录的 Skill，安装名称为 ae-motion-packaging。

安装后使用：

```text
使用 $ae-motion-packaging，帮我制作这个视频的动效包装。

项目内容：……
脚本或粗剪：……
素材路径：……
品牌与视觉参考：……
画幅、分辨率、帧率与总时长：……
BGM：音频路径，或暂未确定
语言与字体：……
交付要求：原生 AE 工程、分段预览视频和工程压缩包。

先提供风格图集合，确认后做一个代表段动效，再完成其他段落。
```

也可以单独使用：设计风格图、给粗剪添加包装、调整某段版式、中文化、提取单段工程，或核查已有交付。

## 所需环境

- 支持读取 Skill 的 AI 客户端，具有任务所需的本地文件和 AE 操作能力。
- 制作原生工程时需要本机可运行的 Adobe After Effects；具体自动化方式由执行环境决定。
- 辅助脚本使用 Python 3.9+ 标准库。
- 验片需要已安装的 `ffprobe`；完整解码另需 `ffmpeg`，支持明确指定路径。

此 Skill 提供工作方法和辅助脚本。AE 场景、JSX 构建/修改脚本和项目素材在实际任务中按需求准备。

## 文件结构

```text
SKILL.md                         工作流入口
agents/openai.yaml               Skill 显示名称与调用提示
references/design-and-review.md  设计、音乐与审阅
references/ae-implementation.md  原生 AE 实现与操作经验
references/verification-and-delivery.md
                                验证与交付
references/make-a-sign-case.md   历史案例中的方法取舍
scripts/verify_media.py          检查实际视频与输出约定
scripts/package_project.py       按清单打包并核对文件完整性
examples/                       两个辅助脚本的输入示例
```

## 验片示例

`examples/output-contract.json` 的文件名和数值需要按当前项目调整：

```sh
python3 scripts/verify_media.py /path/to/delivery \
  --contract examples/output-contract.json \
  --ffprobe /path/to/ffprobe --ffmpeg /path/to/ffmpeg \
  --decode --report /path/to/video-audit.json
```

检查尺寸、帧率、帧数、时长与音轨，并可完整解码。发现不匹配时返回非零退出码。

## 工程打包示例

先按实际项目编辑 `examples/package-files.json`：

```sh
python3 scripts/package_project.py /path/to/delivery \
  --manifest examples/package-files.json \
  --output /path/to/project-v1.zip \
  --report /path/to/package-audit.json
```

打包工具核对所选文件的 ZIP CRC 和成员哈希。AE 素材完整性还需复制到独立目录，实际打开原生工程核查。

## 验证范围

辅助脚本经过实际 4K/30fps 视频完整解码、错误帧数要求和打包完整性测试。每个新项目的视觉质量、AE工程与素材便携性仍按该项目实际产物验证。
