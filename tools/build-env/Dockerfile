# 教材生成环境：复刻原 Linux 沙箱的路径（/opt/node22、/root/.wine64b、/root/cstudy），仓库脚本不用改。
# 构建上下文需放 RedPanda.C++.3.4.win64.MinGW64_11.5.0.Portable.7z（GitHub royqh1979/RedPanda-CPP v3.4）。
FROM node:24-bookworm
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
      python3 python3-pip python3-lxml python3-pil libreoffice-writer poppler-utils \
      wine wine64 xvfb xauth zip unzip p7zip-full fonts-noto-cjk fontconfig locales \
 && sed -i 's/^# *\(zh_CN.UTF-8\)/\1/' /etc/locale.gen && locale-gen \
 && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir --break-system-packages -i https://mirrors.aliyun.com/pypi/simple/ \
      "pypdf<7" python-docx pdfplumber defusedxml
# pypdf 7 删掉了 build.py 用的 PageObject.replace_contents() 旧用法
# render.js、shot.js、build_docx.js 按 /opt/node22/lib/node_modules/… 引用
RUN npm install -g --prefix /opt/node22 playwright docx@9.7.1 \
 && /opt/node22/bin/playwright install --with-deps chromium \
 && rm -rf /var/lib/apt/lists/* /root/.npm
# wrun.sh：Wine 前缀 /root/.wine64b，小熊猫C++ 装在 C:\Program Files\RedPanda-Cpp，D: 映射 /root/cstudy
ENV WINEPREFIX=/root/.wine64b WINEARCH=win64 WINEDEBUG=-all
COPY RedPanda.C++.3.4.win64.MinGW64_11.5.0.Portable.7z /tmp/rp.7z
RUN xvfb-run -a wineboot --init && wineserver -w \
 && 7z x -o/tmp/rp /tmp/rp.7z >/dev/null \
 && src=$(dirname "$(find /tmp/rp -maxdepth 3 -type d -name mingw64 | head -1)") \
 && mv "$src" "$WINEPREFIX/drive_c/Program Files/RedPanda-Cpp" \
 && { test -f "$WINEPREFIX/drive_c/Program Files/RedPanda-Cpp/mingw64/bin/gcc.exe" \
      || { find /tmp/rp "$WINEPREFIX/drive_c/Program Files" -maxdepth 3 | head -40; exit 1; }; } \
 && mkdir -p /root/cstudy/wb && ln -sfn /root/cstudy "$WINEPREFIX/dosdevices/d:" \
 && rm -rf /tmp/rp /tmp/rp.7z
COPY entry.sh /entry.sh
WORKDIR /work
ENTRYPOINT ["/bin/sh", "/entry.sh"]
CMD ["bash"]
