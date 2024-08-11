FROM alpine:3.20.2

RUN apk add --no-cache \
    perl \
    wget \
    curl \
    xz \
    ghostscript \
    fontconfig \
    ttf-freefont \
    py3-pygments

# Installer TeX Live
ARG TL_MIRROR="https://texlive.info/CTAN/systems/texlive/tlnet"

RUN mkdir "/tmp/texlive" && cd "/tmp/texlive" && \
    wget "$TL_MIRROR/install-tl-unx.tar.gz" && \
    tar xzvf ./install-tl-unx.tar.gz && \
    ( \
        echo "selected_scheme scheme-small" && \
        echo "instopt_adjustpath 0" && \
        echo "tlpdbopt_install_docfiles 0" && \
        echo "tlpdbopt_install_srcfiles 0" && \
        echo "TEXDIR /opt/texlive/" && \
        echo "TEXMFLOCAL /opt/texlive/texmf-local" && \
        echo "TEXMFSYSCONFIG /opt/texlive/texmf-config" && \
        echo "TEXMFSYSVAR /opt/texlive/texmf-var" && \
        echo "TEXMFHOME ~/.texmf" \
    ) > "/tmp/texlive.profile" && \
    "./install-tl-"*"/install-tl" --location "$TL_MIRROR" -profile "/tmp/texlive.profile" && \
    rm -vf "/opt/texlive/install-tl" && \
    rm -vf "/opt/texlive/install-tl.log" && \
    rm -vrf /tmp/*

ENV PATH="${PATH}:/opt/texlive/bin/x86_64-linuxmusl"

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
