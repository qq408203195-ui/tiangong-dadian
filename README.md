# 天工大典发布仓库

`site/data/master.json` 是网站发布所用的主库。网站显示该文件的版本，不会自动读取聊天里的附件。`proposals.json` 和 `geo-notes.json` 是独立的未审核研究建议；`source-audit.json` 为来源工作包的审计记录。

向 main 分支提交更新后，GitHub Actions 会先运行校验，再部署到 GitHub Pages。同一链接显示成功部署的最新版本，失败则保留上一版。Git 提交历史用于回溯历史版本。

更新流程：以完整新主库替换 master.json，并同步本版建议、旁注和审计；在提交前运行 `python scripts/validate.py`。校验保留 V0.2.40 基线全部 ID、检查重复 ID、空名称和前向链接，发现问题时拒绝发布。若确需删除基线 ID，应先经过项目审核，并有意识地修改 `scripts/baseline-ids.json`；不要为了通过检查而随意修改该文件。H06 的“进口显微镜”为主库已知待判断前置条件，不应自动修复或冒充实体引用。

网站部署需要仓库为公开、启用 Pages 且发布来源选择 GitHub Actions。仓库和网站为公开内容，不应提交无意公开的数据。研究候选不视为已经核验的史实。
