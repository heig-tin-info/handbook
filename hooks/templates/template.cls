\documentclass[a4paper]{article}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{textcomp} % For ©, ™
\usepackage{amsmath} % For ±
\usepackage{amssymb} % For ®
\usepackage{gensymb} % For ±
\usepackage{wasysym} % For fractions
\usepackage{nicefrac}
\usepackage{hyperref}
\usepackage{ulem}
\usepackage{lipsum}
\usepackage{graphicx}
\usepackage{unicode-math} % For using Unicode math symbols
\usepackage{fontawesome5}
\usepackage{parskip}
\usepackage{stackengine}
\usepackage{booktabs}

\usepackage[many,minted]{tcolorbox}% version 3.03 or better

\usepackage{minted}
\usepackage[acronym]{glossaries}
\usepackage{fvextra} % Pour une meilleure gestion des verbatim inline
\usepackage{titlesec} % Pour la personnalisation des titres

% Redéfinir \paragraph et \subparagraph pour qu'ils soient numérotés et aient des sauts de ligne
\titleformat{\paragraph}{\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}
\titlespacing*{\paragraph}{0pt}{3.25ex plus 1ex minus .2ex}{1em}

\titleformat{\subparagraph}{\normalfont\normalsize\bfseries}{\thesubparagraph}{1em}{}
\titlespacing*{\subparagraph}{0pt}{3.25ex plus 1ex minus .2ex}{1em}

% Pour numérotation des paragraphes et subparagraphes
\setcounter{secnumdepth}{5}

\definecolor{darkblue}{rgb}{0.0, 0.0, 0.5}

\hypersetup{
    colorlinks=true, % Mettre les liens en couleur
    linkcolor=darkblue, % Couleur des liens internes
    filecolor=darkblue, % Couleur des liens vers les fichiers locaux
    urlcolor=darkblue, % Couleur des liens URL
    citecolor=darkblue % Couleur des liens de citation
}

\setmonofont{FiraMono}[
  Extension=.otf,
  UprightFont=*-Regular,
  BoldFont=*-Bold,
  Scale=0.9,
]

\usemintedstyle{tango}
\newtcblisting[auto counter,number within=section,
  list inside=mypyg]{code}[4][]{%
  listing only,
  enhanced,
  colframe=gray!40,
  colback=gray!10,
  boxrule=0.5pt,
  arc=0.5mm,
  toptitle=0.25em,
  bottomtitle=0.1em,
  lefttitle=0.5em,
  outer arc=0.5mm,
  minted language=#2,
  minted options={%
    tabsize=4,
    breaklines,
    xleftmargin=-0.75em,
    fontsize=\footnotesize,
    highlightcolor=gray!30,
    #4
  },
  coltitle=black,
  title={#3},
  list entry={\protect\numberline{\thetcbcounter}#3},
  #1
}


\newtcolorbox{goodbox}[1][]{
  colback=green!20,
  colframe=green!50!black,
  boxrule=0.5pt,
  arc=4mm,
  auto outer arc,
  #1
}

\newtcolorbox{badbox}[1][]{
  colback=red!20,
  colframe=red!50!black,
  boxrule=0.5pt,
  arc=4mm,
  auto outer arc,
  #1
}

\newtcolorbox{commentbox}[1][]{
  colback=gray!20,
  colframe=gray!50!black,
  boxrule=0.5pt,
  arc=4mm,
  auto outer arc,
  #1
}

\newtcolorbox{callout}[2][]{
    breakable,
    sharp corners,
    skin=enhancedmiddle
    jigsaw,
    parbox=false,
    boxrule=0mm,
    leftrule=2mm,
    boxsep=0mm,
    arc=0mm,
    outer arc=0mm,
    attach title to upper,
    after title={.\ },
    coltitle=black,
    colback=gray!10,
    colframe=black,
    title={\faLaptopCode\quad #2},
    fonttitle=\bfseries,
    #1
}

\usetikzlibrary{shadows}

\newcommand*\keystroke[1]{%
  \tikz[baseline=(key.base)]
    \node[%
      draw,
      fill=gray!10,
      drop shadow={shadow xshift=0.25ex,shadow yshift=-0.25ex,fill=black!70,opacity=0.75},
      rectangle,
      rounded corners=1.5pt,
      inner ysep=0.1em,
      inner xsep=0.5em,
      line width=0.5pt,

      font=\scriptsize\sffamily
    ](key) {#1\strut}
  ;
}

\newtcbox{\hl}{on line, boxrule=0.5pt, colframe=black, colback=yellow!30, sharp corners, boxsep=0pt, left=2pt, right=2pt, top=2pt, bottom=2pt}

\newcommand\correctchoice{\stackinset{c}{}{c}{}{$\times$}{$\bigcirc$}}
\newcommand\choice{$\bigcirc$}

\VAR{glossary}

\begin{document}

\VAR{content}

\end{document}
