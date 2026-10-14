# 字体

字体文件不进仓库。排版前把 `fonts-list.txt` 里的 8 个 .ttf 下载到本目录（`book/` 的 style.css 以 `../fonts/` 引用）：

```bash
cd fonts
while read name url; do curl -sSfL -o "$name" "$url"; done < fonts-list.txt
```

Noto Serif SC / Noto Sans SC / JetBrains Mono，均为 SIL OFL 开源字体。
