FROM kjarosh/latex:2024.2-basic

RUN tlmgr update --self --all
RUN tlmgr install latexmk fontspec minted babel-french adjustbox capt-of \
    csquotes datatool emptypage enumitem environ epigraph fontawesome5 gensymb \
    glossaries imakeidx listofitems minitoc stackengine tcolorbox titlesec \
    tocloft wasysym booktabs caption euenc filehook lm makecmds microtype \
    parskip ulem unicode-math lualatex-math tikzfill units pdfcol nextpage \
    hyphen-french noto notomath luatexbase memoir xpatch

RUN apk --no-cache add font-noto font-noto-music font-noto-emoji font-noto-cjk \
    font-noto-naskh-arabic font-noto-devanagari font-noto-hebrew font-noto-tamil \
    font-noto-tibetan font-noto-math font-noto-symbols

RUN mkdir -p /usr/share/fonts/truetype/creativecommons && \
    wget https://github.com/cc-icons/cc-icons/raw/master/fonts/cc-icons.otf \
    -P /usr/share/fonts/truetype/creativecommons

RUN apk add --no-cache \
    make ghostscript fontconfig ttf-freefont py3-pygments ncurses

RUN mkdir -p /tmp/texmf-cache
ENV TEXMFCACHE=/tmp/texmf-cache
ENV TERM=xterm

RUN fc-cache -fv
RUN updmap-sys
RUN luaotfload-tool -u -v

RUN chmod -R 777 /tmp/texmf-cache

#USER $(id -u):$(id -g)
