FROM kjarosh/latex:2024.2-basic

RUN apk add --no-cache \
    perl \
    wget \
    curl \
    xz \
    ghostscript \
    fontconfig \
    ttf-freefont \
    py3-pygments

RUN tlmgr update --self --all
RUN tlmgr install latexmk fontspec minted babel-french adjustbox capt-of \
  csquotes datatool emptypage enumitem environ epigraph fontawesome5 gensymb \
  glossaries imakeidx listofitems minitoc stackengine tcolorbox titlesec \
  tocloft wasysym booktabs caption euenc filehook lm makecmds microtype \
  parskip ulem unicode-math lualatex-math tikzfill units pdfcol nextpage \
  hyphen-french noto notomath luatexbase

RUN apk add font-noto font-noto-music font-noto-emoji font-noto-cjk font-noto-naskh-arabic \
    font-noto-devanagari font-noto-hebrew font-noto-tamil font-noto-tibetan font-noto-math font-noto-symbols

RUN wget https://github.com/cc-icons/cc-icons/raw/master/fonts/cc-icons.otf -P /usr/share/fonts/truetype/creativecommons

RUN fc-cache -fv
RUN updmap-sys
RUN luaotfload-tool -u -v
