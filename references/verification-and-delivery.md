# 验证与交付

## 输出约定

把批准的输出记录为 JSON。下例数值仅为历史单段示例：

```json
{"segments": [{"file": "previews/02.mp4", "width": 3840, "height": 2160,
  "fps": "30/1", "frames": 446, "audio": "none"}]}
```

`audio` 为 `none`、`required` 或 `any`。仅当用户明确不要声音时用 `none`，没有要求时为 `any`。

```sh
python3 scripts/verify_media.py /absolute/delivery --contract /absolute/contract.json \
  --ffprobe /absolute/ffprobe --ffmpeg /absolute/ffmpeg --decode \
  --report /absolute/video-audit.json
```

不匹配返回非零状态。修复对应产物，不改预期值迁就错误输出。

## 分别验证四类证据

1. 原生工程：可打开的 AEP，正确合成规格、可编辑文字/替换槽位，无缺失素材与相关表达式错误。
2. 媒体：实际尺寸、帧率、总帧数、时长与音轨符合约定；关键变更段完整解码。需要 Alpha 时检查编码与真实透明通道。
3. 画面/运动：静帧加播放，检查阅读、顺序、边界、镜头落点与音乐。静帧不能证明运镜顺畅或卡点准确。
4. 便携：复制到独立目录，在 AE 实际打开副本，素材路径位于副本内，无缺失/对原工作区的依赖。字体文件存在不等于系统已安装或没有回退。

窄范围改版只渲染变更段；未变视频按哈希核验。必要时同一时刻做区域画面对比，检查修改范围外是否一致。不为增加检查数量重复渲染未变内容。

## 预览

浏览器播放真实 AE 渲染视频，可加分段导航/时间点按钮；需要定位时本地服务支持 HTTP Range。实际确认视频与字体能加载、播放。另提供本地媒体，不把临时 localhost 链接作为唯一成品。

## 紧凑打包

生成明确的交付文件清单，路径相对交付根：

```json
{"files": ["project.aep", "assets/background.png", "previews/02.mp4", "使用说明.md"]}
```

仅包含本次需要的工程、依赖、适用字体许可、预览和说明，不默认复制所有历史版本、缓存、Auto-Save 或原素材库。

```sh
python3 scripts/package_project.py /absolute/delivery --manifest /absolute/package-files.json \
  --output /absolute/project.zip --report /absolute/package-audit.json
```

ZIP 校验只证明所选文件完整打入包，不证明清单完整、视频规格正确或工程能独立打开。包内说明主合成/分段名、替换位置、字体要求及异地解压后重新指定输出路径的方式。
