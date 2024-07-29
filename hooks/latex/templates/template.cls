\documentclass[11pt,a4paper,twoside]{article}
\usepackage{fontspec}
\usepackage{polyglossia}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{textcomp} % For ©, ™
\usepackage{amsmath} % For ±
\usepackage{amssymb} % For ®
\usepackage{gensymb} % For ±
\usepackage{wasysym} % For fractions
\usepackage{nicefrac}
\usepackage{fancyhdr}
\usepackage{ulem}
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
\usepackage[acronym]{glossaries}
\usepackage{fvextra} % Pour une meilleure gestion des verbatim inline
\usepackage{titlesec} % Pour la personnalisation des titres
\usepackage{enumitem} % Pour personnaliser les listes

\definecolor{darkblue}{rgb}{0.0, 0.0, 0.5}
\definecolor{linkcolor}{RGB}{219, 48, 122}

\usepackage[
  colorlinks=true,
  plainpages=true,
  linkcolor=black,
  citecolor=black,
  plainpages=false,
  unicode=true,
  urlcolor=linkcolor]{hyperref}
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

\setmainlanguage{french}
\setotherlanguage{english}

\setmonofont{FiraMono}[
  Extension=.otf,
  UprightFont=*-Regular,
  BoldFont=*-Bold,
  Scale=0.9,
]

\graphicspath{{images/}}

% Redéfinir l'itemize pour utiliser des demi-cadratins (en-dash) comme puces
\setlist[itemize,1]{label=--}

% Redéfinir \paragraph et \subparagraph pour qu'ils soient numérotés et aient des sauts de ligne
\titleformat{\paragraph}{\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}
\titlespacing*{\paragraph}{0pt}{3.25ex plus 1ex minus .2ex}{1em}

\titleformat{\subparagraph}{\normalfont\normalsize\bfseries}{\thesubparagraph}{1em}{}
\titlespacing*{\subparagraph}{0pt}{3.25ex plus 1ex minus .2ex}{1em}

% Pour numérotation des paragraphes et subparagraphes
\setcounter{secnumdepth}{5}

\fancypagestyle{headings}{
\fancyhf{}
\fancyhead[LO]{\textsl{\rightmark}}
\fancyhead[RE]{\textsl{\leftmark}}
\ifdefined\@confidential
\fancyfoot[LE]{\MakeUppercase{\@confidential}}
\fancyfoot[RO]{\MakeUppercase{\@confidential}}
\fi
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}}

% \pagestyle{headings}


% \renewcommand\section{\@startsection {section}{1}{\z@}%
%                                    {-2.5ex \@plus -1ex \@minus -.2ex}%
%                                    {2.0ex \@plus.2ex}%
%                                    {\normalfont\Large\bfseries\itshape}}
% \renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
%                                      {-2.5ex\@plus -1ex \@minus -.2ex}%
%                                      {1.0ex \@plus .2ex}%
%                                      {\normalfont\large\bfseries\itshape}}
% \renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
%                                      {-2.25ex\@plus -1ex \@minus -.2ex}%
%                                      {1.0ex \@plus .2ex}%
%                                      {\normalfont\normalsize\bfseries\itshape}}


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


% Définir les styles pour différents types de callout
\tcbset{
    callout note/.style={
        colbacktitle=calloutNoteBg,
        colframe=calloutNoteFrame,
        title={\textcolor{calloutNoteFrame}{\faBookmark}\kern0.5em \textbf{Note :}},
    },
    callout abstract/.style={
        colbacktitle=calloutAbstractBg,
        colframe=calloutAbstractFrame,
        title={\textcolor{calloutAbstractFrame}{\faLaptopCode}\kern0.5em \textbf{Résumé :}},
    },
    callout info/.style={
        colbacktitle=calloutInfoBg,
        colframe=calloutInfoFrame,
        title={\textcolor{calloutInfoFrame}{\faBook}\kern0.5em \textbf{Information :}},
    },
    callout tip/.style={
        colbacktitle=calloutTipBg,
        colframe=calloutTipFrame,
        title={\textcolor{calloutTipFrame}{\faLightbulb}\kern0.5em \textbf{Astuce :}},
    },
    callout success/.style={
        colbacktitle=calloutSuccessBg,
        colframe=calloutSuccessFrame,
        title={\textcolor{calloutSuccessFrame}{\faCheck}\kern0.5em \textbf{Succès :}},
    },
    callout warning/.style={
        colbacktitle=calloutWarningBg,
        colframe=calloutWarningFrame,
        title={\textcolor{calloutWarningFrame}{\faExclamationTriangle}\kern0.5em \textbf{Avertissement :}},
    },
    callout failure/.style={
        colbacktitle=calloutFailureBg,
        colframe=calloutFailureFrame,
        title={\textcolor{calloutFailureFrame}{\faExclamationTriangle}\kern0.5em \textbf{Échec :}},
    },
    callout danger/.style={
        colbacktitle=calloutDangerBg,
        colframe=calloutDangerFrame,
        title={\textcolor{calloutDangerFrame}{\faExclamationTriangle}\kern0.5em \textbf{Danger :}},
    },
    callout bug/.style={
        colbacktitle=calloutBugBg,
        colframe=calloutBugFrame,
        title={\textcolor{calloutBugFrame}{\faBug}\kern0.5em \textbf{Bogue :}},
    },
    callout example/.style={
        colbacktitle=calloutExampleBg,
        colframe=calloutExampleFrame,
        title={\textcolor{calloutExampleFrame}{\faChalkboardTeacher}\kern0.5em \textbf{Exemple :}},
    },
    callout quote/.style={
        colbacktitle=calloutQuoteBg,
        colframe=calloutQuoteFrame,
        title={\textcolor{calloutQuoteFrame}{\faQuestionCircle}\kern0.5em \textbf{Citation :}},
    },
    callout question/.style={
        colbacktitle=calloutQuestionBg,
        colframe=calloutQuestionFrame,
        title={\textcolor{calloutQuestionFrame}{\faQuestionCircle}\kern0.5em \textbf{Question :}},
    },
    callout exercise/.style={
        colbacktitle=calloutExerciseBg,
        colframe=calloutExerciseFrame,
        title={\textcolor{calloutExerciseFrame}{\faChess}\kern0.5em \textbf{Exercice :}},
    },
    callout default/.style={
        colbacktitle=gray!40!white,
        title={\textcolor{black}{\faComment}\kern0.5em \textbf{Note :}},
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
    #1,
    after title={~#2}
}

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
