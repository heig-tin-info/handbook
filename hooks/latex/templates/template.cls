\documentclass[11pt,a4paper,twoside]{book}
\usepackage{fontspec}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{textcomp} % For ©, ™
\usepackage{amsmath} % For ±
\usepackage{amssymb} % For ®
\usepackage{gensymb} % For ±
\usepackage{wasysym} % For fractions
\usepackage{nicefrac}
\usepackage{fancyhdr}
\usepackage[normalem]{ulem}
\usepackage{lipsum}
\usepackage{graphicx}
\usepackage{unicode-math} % For using Unicode math symbols
\usepackage{fontawesome5}
\usepackage{multicol}
\usepackage{parskip}
\usepackage{stackengine}
\usepackage{booktabs}
\usepackage[many,minted]{tcolorbox}% version 3.03 or better
\usepackage{minted}
\usepackage{capt-of}
\usepackage[acronym]{glossaries}
\usepackage{fvextra} % Pour une meilleure gestion des verbatim inline
\usepackage{titlesec} % Pour la personnalisation des titres
\usepackage{enumitem} % Pour personnaliser les listes
\usepackage{etoolbox}
\usepackage{tocloft}
\usepackage{adjustbox} % Auto resize tables to fit page width
\usepackage{caption}
\usepackage{polyglossia}

\setcounter{tocdepth}{2}
\setlength{\cftsubsubsecnumwidth}{6em}

\setdefaultlanguage{french}
\setotherlanguages{english}

\captionsetup[table]{skip=10pt}

\directlua{luaotfload.add_fallback
   ("fontfallback",
    {
      "NotoColorEmoji:mode=harf;",
      "Symbola:mode=harf;",
      "NotoNaskhArabic:mode=harf;",
      "NotoSerifHebrew:mode=harf;",
      "NotoSerifDevanagari:mode=harf;",
      "NotoSerifTamil:mode=harf;",
      "NotoSerifTibetan:mode=harf;",
      "NotoSerifCJKkr:mode=harf;",
      "DroidSansFallback:mode=harf;"
    }
   )}

\setmainfont{Noto Serif}[
  RawFeature={fallback=fontfallback}
]

\setmonofont{Noto Sans Mono}[
  Scale=0.8,
  RawFeature={fallback=fontfallback}
]

\newfontfamily\creativecommonfont{Creative Commons}
\DeclareTextFontCommand\creativecommon{\creativecommonfont}


\definecolor{linkcolor}{RGB}{34, 18, 104}
\definecolor{urlcolor}{RGB}{104, 18, 55}

\usepackage[
  colorlinks=true,
  plainpages=true,
  linkcolor=black,
  citecolor=black,
  plainpages=false,
  unicode=true,
  urlcolor=urlcolor]{hyperref}

\usepackage[
  a4paper,
  top=2.5cm,
  bottom=2.5cm,
  left=3cm,
  right=4cm,
  headheight=6mm,
  headsep=5mm,
  marginparwidth=3cm,
  marginparsep=4mm,
  heightrounded,
  includehead]{geometry}

\graphicspath{{assets/}}

% Redéfinir l'itemize pour utiliser des demi-cadratins (en-dash) comme puces
\setlist[itemize,1]{label=--}

% Pour numérotation des paragraphes et subparagraphes
\setcounter{secnumdepth}{5}

\fancypagestyle{partpagestyle}
{%
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
}

\fancypagestyle{onlycount}
{
  \fancyhf{}
  \renewcommand\headrulewidth{0pt}
  \renewcommand\footrulewidth{0pt}
  \fancyfoot[C]{\thepage}
}

\fancypagestyle{plain}{
  \fancyhf{}
  \lhead[\rm\thepage]{\fancyplain{}{\nouppercase{\textsl{\bfseries{\leftmark}}}}}
  \rhead[\rm\thepage]{\fancyplain{}{\nouppercase{\textsl{\bfseries{\rightmark}}}}}
  %\fancyhead[LO]{\textsl{\rightmark}}
  %\fancyhead[RE]{\textsl{\leftmark}}

  \chead{}\lfoot{}\rfoot{}\cfoot{}
  %\renewcommand{\headrulewidth}{0.1mm}%
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
  \fancyfoot[C]{\thepage}%
}

% Patch the `\thispagestyle` code within `\part
\xpatchcmd{\part}{\thispagestyle{plain}}{\thispagestyle{partpagestyle}}{}{}
\pagestyle{fancy}



\setlength{\parindent}{0pt}
\setlength\parskip{\medskipamount}

\definecolor{calloutNoteBg}{HTML}{ECF3FF}
\definecolor{calloutNoteFrame}{HTML}{448AFF}

\definecolor{calloutAbstractBg}{HTML}{E5F7FF}
\definecolor{calloutAbstractFrame}{HTML}{00B0FF}

\definecolor{calloutInfoBg}{HTML}{E5F8FB}
\definecolor{calloutInfoFrame}{HTML}{00B8D4}

\definecolor{calloutTipBg}{HTML}{E5F8F6}
\definecolor{calloutTipFrame}{HTML}{00BFA5}

\definecolor{calloutSuccessBg}{HTML}{E5F9ED}
\definecolor{calloutSuccessFrame}{HTML}{00C853}

\definecolor{calloutQuestionBg}{HTML}{EFFCE7}
\definecolor{calloutQuestionFrame}{HTML}{64DD17}

\definecolor{calloutWarningBg}{HTML}{FFF4E5}
\definecolor{calloutWarningFrame}{HTML}{FF9E1D}

\definecolor{calloutFailureBg}{HTML}{FFEDED}
\definecolor{calloutFailureFrame}{HTML}{FF5252}

\definecolor{calloutDangerBg}{HTML}{FFE7EC}
\definecolor{calloutDangerFrame}{HTML}{FF1744}

\definecolor{calloutBugBg}{HTML}{FEE5EE}
\definecolor{calloutBugFrame}{HTML}{F50057}

\definecolor{calloutExampleBg}{HTML}{F2EDFF}
\definecolor{calloutExampleFrame}{HTML}{7C4DFF}

\definecolor{calloutQuoteBg}{HTML}{F5F5F5}
\definecolor{calloutQuoteFrame}{HTML}{9E9E9E}

\definecolor{calloutExerciseBg}{HTML}{F5F5F5}
\definecolor{calloutExerciseFrame}{HTML}{9E9E9E}

\newcounter{exercisecounter}
\renewcommand{\theexercisecounter}{\arabic{exercisecounter}}

% Définir les styles pour différents types de callout
\tcbset{
    callout note/.style={
        colbacktitle=calloutNoteBg,
        colframe=calloutNoteFrame,
        title={\textcolor{calloutNoteFrame}{\faBookmark}\kern0.5em},
    },
    callout abstract/.style={
        colbacktitle=calloutAbstractBg,
        colframe=calloutAbstractFrame,
        title={\textcolor{calloutAbstractFrame}{\faLaptopCode}\kern0.5em},
    },
    callout info/.style={
        colbacktitle=calloutInfoBg,
        colframe=calloutInfoFrame,
        title={\textcolor{calloutInfoFrame}{\faBook}\kern0.5em},
    },
    callout tip/.style={
        colbacktitle=calloutTipBg,
        colframe=calloutTipFrame,
        title={\textcolor{calloutTipFrame}{\faLightbulb}\kern0.5em},
    },
    callout success/.style={
        colbacktitle=calloutSuccessBg,
        colframe=calloutSuccessFrame,
        title={\textcolor{calloutSuccessFrame}{\faCheck}\kern0.5em},
    },
    callout warning/.style={
        colbacktitle=calloutWarningBg,
        colframe=calloutWarningFrame,
        title={\textcolor{calloutWarningFrame}{\faExclamationTriangle}\kern0.5em},
    },
    callout failure/.style={
        colbacktitle=calloutFailureBg,
        colframe=calloutFailureFrame,
        title={\textcolor{calloutFailureFrame}{\faExclamationTriangle}\kern0.5em},
    },
    callout important/.style={
        colbacktitle=calloutDangerBg,
        colframe=calloutDangerFrame,
        title={\textcolor{calloutDangerFrame}{\faExclamationTriangle}\kern0.5em },
    },
    callout hint/.style={
        colbacktitle=calloutTipBg,
        colframe=calloutTipFrame,
        title={\textcolor{calloutTipFrame}{\faLightbulb}\kern0.5em},
    },
    callout danger/.style={
        colbacktitle=calloutDangerBg,
        colframe=calloutDangerFrame,
        title={\textcolor{calloutDangerFrame}{\faExclamationTriangle}\kern0.5em},
    },
    callout bug/.style={
        colbacktitle=calloutBugBg,
        colframe=calloutBugFrame,
        title={\textcolor{calloutBugFrame}{\faBug}\kern0.5em},
    },
    callout example/.style={
        colbacktitle=calloutExampleBg,
        colframe=calloutExampleFrame,
        title={\textcolor{calloutExampleFrame}{\faChalkboardTeacher}\kern0.5em },
    },
    callout quote/.style={
        colbacktitle=calloutQuoteBg,
        colframe=calloutQuoteFrame,
        title={\textcolor{calloutQuoteFrame}{\faQuestionCircle}\kern0.5em },
    },
    callout question/.style={
        colbacktitle=calloutQuestionBg,
        colframe=calloutQuestionFrame,
        title={\textcolor{calloutQuestionFrame}{\faQuestionCircle}\kern0.5em },
    },
    callout exercise/.style={
        colbacktitle=calloutExerciseBg,
        colframe=calloutExerciseFrame,
        title={\textcolor{calloutExerciseFrame}{\faChess}
            \refstepcounter{exercisecounter}
            \textbf{Exercice \theexercisecounter:}
        }
    },
    callout solution/.style={
        colbacktitle=gray!40!white,
        title={\textcolor{black}{\faComment}\kern0.5em},
    },
    callout default/.style={
        colbacktitle=gray!40!white,
        title={\textcolor{black}{\faComment}\kern0.5em},
    }
}

\newtcolorbox{callout}[2][]{%
    breakable,
    boxsep=1.5mm,
    arc=0.5mm,
    outer arc=0.5mm,
    colback=white,
    colframe=black,
    boxrule=0.7pt,
    titlerule=0mm,
    lefttitle=1mm,
    leftupper=1mm,
    coltitle=black,
    parbox=false, % Allow paragraph breaks inside the box
    #1,
    after title={~#2}
}

\setminted{style=trac}
\setmintedinline{style=trac} %,bgcolor=gray!20}

\newtcblisting[auto counter,number within=section,
  list inside=mypyg]{code}[4][]{%
  breakable,
  listing only,
  enhanced,
  colframe=gray!10!white,
  colback=gray!10!white,
  boxrule=0.5pt,
  arc=0.7mm,
  toptitle=0.25em,
  bottomtitle=0.2em,
  lefttitle=0.5em,
  outer arc=0.7mm,
  minted language=#2,
  minted options={%
    tabsize=4,
    breaklines,
    xleftmargin=-0.75em,
    fontsize=\footnotesize,
    highlightcolor=gray!30,
    ignorelexererrors,
    #4
  },
  coltitle=black,
  colbacktitle=gray!20!white,
  title={#3},
  list entry={\protect\numberline{\thetcbcounter}#3},
  #1
}

\NewTotalTCBox{\cde}{mv}{
  on line,
  boxsep=0pt,
  left=1.5pt,
  right=1.5pt,
  top=1pt,
  bottom=1pt,
  colframe=gray!20,
  colback=gray!20,
  minted options={%
    ignorelexererrors
  },
  rounded corners,
  boxrule=0pt,
}{\mintinline{#1}{#2}}

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

% Description item and text are displayed by default on the same line
% this is not very readable. This command changes the style to display
% the description text on the next line.
% https://tex.stackexchange.com/a/430454/85416
\setlist[description]{
    style=nextline,
    labelindent=0pt,
    leftmargin=1cm,
    itemindent=\dimexpr-5pt-\labelsep\relax
}

% Workaround for mintedinline in item
% https://tex.stackexchange.com/a/723530/85416
\NewDocumentCommand{\minteditem}{mv}{%
  \item[\mintinline{#1}{#2}]%
}

\newtcbox{\hl}{on line, boxrule=0.5pt, colframe=black, colback=yellow!30, sharp corners, boxsep=0pt, left=2pt, right=2pt, top=2pt, bottom=2pt}

\newcommand\correctchoice{\stackinset{c}{}{c}{}{$\times$}{$\bigcirc$}}
\newcommand\choice{$\bigcirc$}

\input{acronyms.tex}

\begin{document}

\begin{titlepage}
  \begin{center}
   {\huge\bfseries Le C pour l'ingénieur\\}
   \vspace{1.5cm}
   {\Large\bfseries Prof. Yves Chevallier}\\[5pt]
   yves.chevallier@heig-vd.ch\\[14pt]
   \vspace{2cm}
  {Cours d'informatique pour} \\[5pt]
  \emph{{La Haute École d'Ingénieurie et de Gestion du canton de Vaud}}\\[2cm]

   \vfill

  {Département des technologies industrielles (TIN)}\\[5pt]
  {Route de Cheseaux, 1}\\[5pt]
  {CH-1401 Yverdon-les-Bains,
   Suisse}\\
   \vfill
  {\today}
  \end{center}
\end{titlepage}
\clearpage

\thispagestyle{empty}

\begingroup
\footnotesize
\setlength{\parindent}{0pt}
\setlength{\parskip}{\baselineskip}

\begin{tabular}{@{} l l}
  \textcopyright{} 2019\:---\:2024 &Prof. Yves Chevallier \\
\end{tabular}

Creative Commons \par
\creativecommon{\huge L}

L'œuvre peut être librement utilisée, à la condition de l'attribuer à l'auteur en citant son nom. Le titulaire de droits peut autoriser tous les types d'utilisation ou au contraire restreindre aux utilisations non commerciales (les utilisations commerciales restant soumises à son autorisation).

HEIG-VD

Imprimé en Suisse
\vfil
\begin{center}
10 09 08 07 06 05 04 03 02 01\hspace{2em}19 18 17 16 15 14 13
\end{center}
\begin{center}
\begin{tabular}{ll}
Première édition avec Sphinx:                      & 1 Septembre 2019 \\
Première édition avec Sphinx, avec corrections:    & 15 Juillet 2020 \\
Seconde édition avec MkDocs Material:              & 30 Juillet 2024 \\
\end{tabular}
\end{center}
\vfil
\endgroup

\frontmatter

\tableofcontents

\mainmatter

\VAR{content}

\backmatter

\input{solutions.tex}

\listoffigures

\listoftables

\printglossary[type=\acronymtype]


\end{document}
