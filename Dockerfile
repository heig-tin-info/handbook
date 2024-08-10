FROM ubuntu:noble

RUN apt-get update && \
    apt-get install -y \
    perl wget curl \
    tzdata xz-utils \
    ghostscript pngquant fontconfig \
    pipx

RUN echo "Europe/Zurich" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz && \
    tar -xzf install-tl-unx.tar.gz && \
    cd install-tl-20* && \
    echo "selected_scheme scheme-minimal" > /tmp/texlive.profile && \
    ./install-tl --profile=/tmp/texlive.profile && \
    cd .. && rm -rf install-tl*

ENV PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"

RUN tlmgr install latex latexmk minted adjustbox capt-of collectbox csquotes \
  datatool emptypage enumitem environ epigraph fontawesome5 gensymb \
  glossaries imakeidx listofitems mfirstuc minitoc stackengine substr \
  tcolorbox titlesec tocloft tracklang trimspaces wasysym xfor booktabs \
  caption euenc fancyhdr filehook fontspec l3backend l3kernel l3packages \
  lm lm-math makecmds microtype parskip polyglossia tipa ulem unicode-math xunicode \
  luatex lualatex-math luatexbase fontspec collection-luatex tikzfill \
  babel firstaid latex-bin latex-fonts latexconfig luatexbase units ltxcmds kvsetkeys \
  oberdiek pdfcol etexcmds nextpage hyphen-french noto notomath hyperref geometry epstopdf \
  epstopdf-pkg babel-french psnfss carlisle

RUN apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pipx install pigments && pipx ensurepath

RUN mkdir -p /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-Bold.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-Italic.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-BoldItalic.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-Medium.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-SemiCondensed.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerif/unhinted/otf/NotoSerif-MediumItalic.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerifTibetan/unhinted/ttf/NotoSerifTibetan-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerifTamil/unhinted/otf/NotoSerifTamil-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerifDevanagari/unhinted/otf/NotoSerifDevanagari-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSerifHebrew/unhinted/otf/NotoSerifHebrew-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoKufiArabic/unhinted/otf/NotoKufiArabic-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoNaskhArabic/unhinted/ttf/NotoNaskhArabic-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoMusic/unhinted/ttf/NotoMusic-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSansMath/unhinted/ttf/NotoSansMath-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSansSymbols/full/ttf/NotoSansSymbols-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://cdn.jsdelivr.net/gh/notofonts/notofonts.github.io/fonts/NotoSansSymbols2/full/ttf/NotoSansSymbols2-Regular.ttf -P /usr/share/fonts/truetype/noto && \
    wget https://github.com/notofonts/noto-cjk/raw/main/Serif/OTF/Japanese/NotoSerifCJKjp-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://github.com/notofonts/noto-cjk/raw/main/Serif/OTF/Korean/NotoSerifCJKkr-Regular.otf -P /usr/share/fonts/truetype/noto && \
    wget https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf -P /usr/share/fonts/truetype/noto

RUN wget https://github.com/cc-icons/cc-icons/raw/master/fonts/cc-icons.otf -P /usr/share/fonts/truetype/creativecommons

RUN fc-cache -fv
RUN updmap-sys
RUN luaotfload-tool -u -v
