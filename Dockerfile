FROM alpine:3.20.2

ARG TL_YEAR=2023
ARG TL_SCHEME="scheme-minimal"

ARG TL_MIRROR="http://ftp.math.utah.edu/pub/tex/historic/systems/texlive/${TL_YEAR}/tlnet-final"
ARG TL_PREFIX="/opt/texlive"
RUN apk add --no-cache perl curl fontconfig libgcc gnupg
RUN mkdir "/tmp/texlive" && cd "/tmp/texlive" && \
    wget "$TL_MIRROR/install-tl-unx.tar.gz" && \
    tar xzvf ./install-tl-unx.tar.gz && \
    ( \
    echo "selected_scheme ${TL_SCHEME}" && \
    echo "instopt_adjustpath 0" && \
    echo "tlpdbopt_install_docfiles 0" && \
    echo "tlpdbopt_install_srcfiles 0" && \
    echo "TEXDIR ${TL_PREFIX}/" && \
    echo "TEXMFLOCAL ${TL_PREFIX}/texmf-local" && \
    echo "TEXMFSYSCONFIG ${TL_PREFIX}/texmf-config" && \
    echo "TEXMFSYSVAR ${TL_PREFIX}/texmf-var" && \
    echo "TEXMFHOME ~/.texmf" \
    ) > "/tmp/texlive.profile" && \
    "./install-tl-"*"/install-tl" --location "$TL_MIRROR" -profile "/tmp/texlive.profile" && \
    rm -vf "${TL_PREFIX}/install-tl" && \
    rm -vf "${TL_PREFIX}/install-tl.log" && \
    rm -vrf /tmp/*
ENV PATH="${PATH}:${TL_PREFIX}/bin/x86_64-linuxmusl"

RUN tlmgr install latexmk fontspec minted babel-french adjustbox capt-of \
    csquotes datatool emptypage enumitem environ epigraph fontawesome5 gensymb \
    glossaries imakeidx listofitems minitoc stackengine tcolorbox titlesec \
    tocloft wasysym booktabs caption euenc filehook lm makecmds microtype \
    parskip ulem unicode-math lualatex-math tikzfill units pdfcol nextpage \
    hyphen-french noto notomath luatexbase memoir xpatch xindy latex2pydata \
    pgfopts upquote luaotfload latex-bin hyperref infwarerr fancyhdr fancyvrb \
    carlisle geometry epstopdf-pkg

RUN apk --no-cache add font-noto font-noto-music font-noto-emoji font-noto-cjk \
    font-noto-naskh-arabic font-noto-devanagari font-noto-hebrew font-noto-tamil \
    font-noto-tibetan font-noto-math font-noto-symbols

RUN mkdir -p /usr/share/fonts/truetype/creativecommons && \
    wget https://github.com/cc-icons/cc-icons/raw/master/fonts/cc-icons.otf \
    -P /usr/share/fonts/truetype/creativecommons

RUN mkdir -p /tmp/texmf-cache
RUN chmod -R 777 /tmp/texmf-cache
ENV TEXMFCACHE=/tmp/texmf-cache
ENV TERM=xterm

RUN fc-cache -fv
RUN updmap-sys
RUN luaotfload-tool -u -v

RUN apk add --no-cache \
    make ghostscript fontconfig ttf-freefont py3-pygments ncurses clisp

# Install Xindy binary not available from tlmgr :(
RUN apk add --no-cache rcs musl-dev flex-dev gcc
RUN ln -sf /opt/texlive/texmf-dist/scripts/xindy/xindy.pl /opt/texlive/bin/x86_64-linuxmusl/xindy
RUN ln -sf /opt/texlive/texmf-dist/scripts/xindy/texindy.pl /opt/texlive/bin/x86_64-linuxmusl/texindy
RUN wget https://sourceforge.net/projects/xindy/files/xindy-source-components/2.4/xindy-kernel-3.0.tar.gz
RUN tar xf xindy-kernel-3.0.tar.gz
RUN cd xindy-kernel-3.0/src && make && cp -f xindy.mem /opt/texlive/bin/x86_64-linuxmusl/
RUN cd xindy-kernel-3.0/tex2xindy && make && cp -f tex2xindy /opt/texlive/bin/x86_64-linuxmusl/
RUN apk del rcs musl-dev flex-dev gcc
