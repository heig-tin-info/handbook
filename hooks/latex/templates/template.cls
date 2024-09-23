\documentclass[9pt,twoside]{memoir}
\usepackage{fontspec}
\usepackage[svgnames,dvipsnames,x11names]{xcolor}
\usepackage{tikz}
\usepackage{textcomp} % For ©, ™
\usepackage{amsmath} % For ±
\usepackage{amssymb} % For ®
\usepackage{gensymb} % For ±
%\usepackage{wasysym} % For fractions
\usepackage{nicefrac}
\usepackage{fancyhdr}
\usepackage[normalem]{ulem}
\usepackage{graphicx}
\usepackage{unicode-math} % For using Unicode math symbols
\usepackage{fontawesome5}
\usepackage{multicol}
%\usepackage{parskip}  % For no paragraph indentation
\usepackage{stackengine}
\usepackage{booktabs}
\usepackage[many,minted]{tcolorbox}% version 3.03 or better
\usepackage{minted}
%\usepackage[french]{minitoc}
\usepackage{csquotes}
\usepackage{epigraph}
\usepackage{capt-of}
\usepackage[acronym]{glossaries}
\usepackage{imakeidx}
\usepackage{fvextra} % For better verbatim environments
\usepackage{titlesec} % Pour la personnalisation des titres
\usepackage{enumitem} % Pour personnaliser les listes
\usepackage{etoolbox}
\usepackage{tocloft}
\usepackage{adjustbox} % Auto resize tables to fit page width
\usepackage{caption}
\usepackage{microtype} % Avoid overfull with fonts
\usepackage[french]{babel}
\usepackage{emptypage} % Nothing on empty pages
\usepackage{heiglogo}
\usetikzlibrary{shapes.geometric}
\usetikzlibrary{calc}
\usetikzlibrary{shadows}

\makeglossaries
\makeindex
%\dominitoc

% Prevent too many overful \hbox (with some fonts)
\tolerance=2000
\emergencystretch=10pt

% Give more spaces on Table of content (between numbers and text)
\setlength{\cftpartnumwidth}{4em}
\setlength{\cftsectionnumwidth}{3em}
\setlength{\cftsubsectionnumwidth}{3.5em}
\setlength{\cftfigurenumwidth}{3em}
\setlength{\cfttablenumwidth}{3em}

\captionsetup[table]{skip=10pt}

\directlua{luaotfload.add_fallback
  ("fontfallback",
  {
      "NotoColorEmoji:mode=harf;",
      "NotoNaskhArabic:mode=harf;",
      "NotoSerifHebrew:mode=harf;",
      "NotoSerifDevanagari:mode=harf;",
      "NotoSerifTamil:mode=harf;",
      "NotoSerifTibetan:mode=harf;",
      "NotoSerifCJKkr:mode=harf;",
      "NotoSans:mode=harf;",
      "NotoSansSymbols2-Regular:mode=harf;",
      "NotoSansMath-Regular:mode=harf;",
      "NotoMusic-Regular:mode=harf;",
    }
  )}

\setmainfont{Latin Modern Roman}[
  RawFeature={fallback=fontfallback}
]

\setsansfont{Latin Modern Sans}[
  RawFeature={fallback=fontfallback}
]

% \setmainfont{Noto Serif}[
%   RawFeature={fallback=fontfallback}
% ]

% \setsansfont{Noto Sans}[
%   RawFeature={fallback=fontfallback}
% ]

\setmonofont{Noto Sans Mono}[
  Scale=0.9,
  ItalicFont=lmmono10-italic.otf,
  BoldItalicFont=lmmonolt10-boldoblique.otf,
  RawFeature={fallback=fontfallback}
]

\newfontfamily\creativecommonfont{Creative Commons}
\DeclareTextFontCommand\creativecommon{\creativecommonfont}

% Make quotations italic and smaller
\AtBeginEnvironment{displayquote}{\small\itshape}

% Make tables slightly smaller
%\AtBeginEnvironment{tabular}{\small}

% Fit table to page width
\let\oldtabular\tabular
\let\endoldtabular\endtabular

\newsavebox{\mytablebox}
\renewenvironment{tabular}[1]
  {\begin{lrbox}{\mytablebox}\small\oldtabular{#1}} % Temporary box to store table
  {\endoldtabular\end{lrbox}%
   \ifdim\wd\mytablebox>\linewidth
     \resizebox{\linewidth}{!}{\usebox{\mytablebox}} % Adjust to fit line width
   \else
     \usebox{\mytablebox} % Otherwise, use the table as is
   \fi
  }

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
  paperwidth=160mm,
  paperheight=240mm,
  top=20mm,
  bottom=20mm,
  left=20mm,
  right=15mm, % Margin for binding
  headheight=6mm,
  headsep=5mm,
  marginparsep=4mm,
  heightrounded]{geometry}


% Custom epigraph style
\setlength\epigraphwidth{.8\textwidth}
\setlength\epigraphrule{0pt}


\renewcommand{\footrulewidth}{0pt}

% All pages of mainmatter
\fancypagestyle{fancy}{%
  \fancyhf{}
  \renewcommand{\headrulewidth}{0.5pt}
  \fancyhead[LE]{\leftmark}
  \fancyhead[RO]{\rightmark}
  \fancyfoot[LE,RO]{\thepage}
}

% Chapter pages
\fancypagestyle{plain}{%
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[LE,RO]{\thepage}
}

% Part pages
\fancypagestyle{part}{%
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
}

% \apptocmd{\chapter}{\minitoc}{}{}

\patchcmd{\part}{\thispagestyle{plain}}{\thispagestyle{part}}{}{}

\newcommand{\changelocaltocdepth}[1]{%
  \addtocontents{toc}{\protect\setcounter{tocdepth}{#1}}%
  \setcounter{tocdepth}{#1}%
}

\apptocmd{\frontmatter}{%
  \pagestyle{plain}%
  \changelocaltocdepth{1}%
  \setcounter{secnumdepth}{0}
}{}{}

\apptocmd{\mainmatter}{%
  \pagestyle{fancy}%
  \changelocaltocdepth{2}%
  \setcounter{secnumdepth}{2}
}{}{}


\graphicspath{{assets/}}

% Allow hyphenation after a hyphen
\providecommand{\allowhyphens}{\ifvmode\else\nobreak\hspace{0pt}\fi}

% Redéfinir l'itemize pour utiliser des demi-cadratins (en-dash) comme puces
\setlist[itemize,1]{label=--}

% Pour numérotation des paragraphes et subparagraphes
\setcounter{secnumdepth}{5}

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
\definecolor{calloutExerciseFrame}{HTML}{202020}

\newcounter{exercisecounter}
\renewcommand{\theexercisecounter}{\arabic{exercisecounter}}

\tcbset{
  callout note/.style={
      colbacktitle=calloutNoteBg,
      colframe=calloutNoteFrame,
      coltitle=calloutNoteFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutNoteFrame},
      title={\makebox[1.3em][c]{\faBookmark}},
    },
  callout abstract/.style={
      colbacktitle=calloutAbstractBg,
      colframe=calloutAbstractFrame,
      coltitle=calloutAbstractFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutAbstractFrame},
      title={\makebox[1.3em][c]{\faLaptopCode}},
    },
  callout info/.style={
      colbacktitle=calloutInfoBg,
      colframe=calloutInfoFrame,
      coltitle=calloutInfoFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutInfoFrame},
      title={\makebox[1.3em][c]{\faComment}},
    },
  callout tip/.style={
      colbacktitle=calloutTipBg,
      colframe=calloutTipFrame,
      coltitle=calloutTipFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutTipFrame},
      title={\makebox[1.3em][c]{\faLightbulb}},
    },
  callout success/.style={
      colbacktitle=calloutSuccessBg,
      colframe=calloutSuccessFrame,
      coltitle=calloutSuccessFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutSuccessFrame},
      title={\makebox[1.3em][c]{\faCheck}},
    },
  callout warning/.style={
      colbacktitle=calloutWarningBg,
      colframe=calloutWarningFrame,
      coltitle=calloutWarningFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutWarningFrame},
      title={\makebox[1.3em][c]{\faBolt}},
    },
  callout failure/.style={
      colbacktitle=calloutFailureBg,
      colframe=calloutFailureFrame,
      coltitle=calloutFailureFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutFailureFrame},
      title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
  callout important/.style={
      colbacktitle=calloutDangerBg,
      colframe=calloutDangerFrame,
      coltitle=calloutDangerFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutDangerFrame},
      title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
  callout hint/.style={
      colbacktitle=calloutTipBg,
      colframe=calloutTipFrame,
      coltitle=calloutTipFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutTipFrame},
      title={\makebox[1.3em][c]{\faLightbulb}},
    },
  callout danger/.style={
      colbacktitle=calloutDangerBg,
      colframe=calloutDangerFrame,
      coltitle=calloutDangerFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutDangerFrame},
      title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
  callout bug/.style={
      colbacktitle=calloutBugBg,
      colframe=calloutBugFrame,
      coltitle=calloutBugFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutBugFrame},
      title={\makebox[1.3em][c]{\faBomb}},
    },
  callout example/.style={
      colbacktitle=calloutExampleBg,
      colframe=calloutExampleFrame,
      coltitle=calloutExampleFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutExampleFrame},
      title={\makebox[1.3em][c]{\faFlask}},
    },
  callout quote/.style={
      colbacktitle=calloutQuoteBg,
      colframe=calloutQuoteFrame,
      coltitle=calloutQuoteFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutQuoteFrame},
      title={\makebox[1.3em][c]{\faQuestionCircle}},
    },
  callout question/.style={
      colbacktitle=calloutQuestionBg,
      colframe=calloutQuestionFrame,
      coltitle=calloutQuestionFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutQuestionFrame},
      title={\makebox[1.3em][c]{\faQuestionCircle}},
    },
  callout exercise/.style={
      colbacktitle=calloutExerciseBg,
      colframe=calloutExerciseFrame,
      coltitle=calloutExerciseFrame!80!black,
      borderline west={0.3mm}{0mm}{calloutExerciseFrame},
      title={\faChess
          \refstepcounter{exercisecounter}
          \textbf{Exercice \theexercisecounter:}
        }
    },
  callout solution/.style={
      colbacktitle=gray!40!white,
      title={\textcolor{black}{\makebox[1.3em][l]{\faComment}}},
    },
  callout default/.style={
      colbacktitle=gray!40!white,

      title={\textcolor{black}{\makebox[1.3em][l]{\faComment}}},
    }
}

\newtcolorbox{callout}[2][]{%
  breakable,
  enhanced,
  arc=0mm,
  boxrule=0mm,
  titlerule=0mm,
  lefttitle=1mm,
  leftupper=1mm,
  colback=white,
  parbox=false, % Allow paragraph breaks inside the box
  frame hidden,
  borderline west={0.3mm}{0mm}{black!70},
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
  colback=white,
  pad at break*=1mm,
  toptitle=0.15em,
  bottomtitle=0.1em,
  boxrule=0mm,
  frame hidden,
  minted language=#2,
  top=1mm,
  bottom=1mm,
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

% Avoid orphans at the end of a page, encourage page breaks if there are
% a section with less than 3 lines
% https://tex.stackexchange.com/a/723704/85416
\makeatletter
\patchcmd\@afterheading{\clubpenalty \@M}{\clubpenalties 3 \@M\@M 5000 }{%
  \typeout{patched}}{\typeout{patch failed}
}
\makeatother

% Allow for short text below parts
% https://tex.stackexchange.com/a/336401/85416
% \makeatletter
% \newcommand{\extraPartText}[1]{\def\@extraPartText{#1}}
% \pretocmd{\@endpart}{\vspace{8ex}\begingroup\centering\@extraPartText\par\endgroup\let\@extraPartText\relax}{}{}
% \makeatother


% Description item and text are displayed by default on the same line
% this is not very readable. This command changes the style to display
% the description text on the next line.
% https://tex.stackexchange.com/a/430454/85416
% https://tex.stackexchange.com/a/726879/85416
\AddToHook{cmd/descriptionlabel/after}{\rule[-8pt]{0pt}{0pt}}
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

\def\title{\VAR{title}}
\def\subtitle{\VAR{subtitle}}

\definecolor{indigo(dye)}{rgb}{0.0, 0.25, 0.42}

\def\author{\VAR{author}}

\input{glossary}
\input{acronyms}

\begin{document}

\input{cover}

\cleardoublepage
\begin{titlingpage}
  \heiglogo[color=black]
  \vspace{6cm}
  \vfil
  \begin{center}
    {\huge\bfseries \VAR{title}\\}
    \vspace{1.5cm}
    {\Large\bfseries \VAR{author}}\\[5pt]
    \VAR{email}\\[14pt]
    \vspace{2cm}
    {Cours d'informatique pour} \\[5pt]
    \emph{{La Haute École d'Ingénierie et de Gestion du canton de Vaud}}\\[2cm]

    \vfill

    {Département des technologies industrielles (TIN)}\\[5pt]
    {Route de Cheseaux, 1}\\[5pt]
    {CH-1401 Yverdon-les-Bains,
    Suisse}\\
    \vfill
    {\today}
  \end{center}
\end{titlingpage}

\thispagestyle{empty}

\begingroup
\footnotesize
\setlength{\parindent}{0pt}
\setlength{\parskip}{\baselineskip}

\begin{tabular}{@{} l l}
  \textcopyright{} 2019\:---\:2024 & \author \\
\end{tabular}

Creative Commons \par
\creativecommon{\huge L}

L'œuvre peut être librement utilisée, à la condition de l'attribuer à l'auteur en citant son nom. Le titulaire de droits peut autoriser tous les types d'utilisation ou au contraire restreindre aux utilisations non commerciales (les utilisations commerciales restant soumises à son autorisation). En sommes vous êtes libre de :

\begin{description}
  \item[Partager] copier, distribuer et communiquer le matériel par tous moyens et sous tous formats
  \item[Adapter] remixer, transformer et créer à partir du matériel
\end{description}

Sous les conditions suivantes :

\begin{description}
  \item[Attribution] Vous devez créditer l'Œuvre, intégrer un lien vers la licence et indiquer si des modifications ont été effectuées à l'œuvre. Vous devez indiquer ces informations par tous les moyens raisonnables, sans toutefois suggérer que l'offrant vous soutient ou soutient la façon dont vous avez utilisé son œuvre.
  \item[Partage dans les mêmes conditions] Si vous modifiez, transformez ou adaptez cette œuvre, vous n'avez le droit de distribuer votre création que sous une licence identique ou similaire à celle-ci.
\end{description}

HEIG-VD

Imprimé en Suisse
\vfil
\begin{center}
  10 09 08 07 06 05 04 03 02 01\hspace{2em}19 18 17 16 15 14 13
\end{center}
\begin{center}
  \begin{tabular}{ll}
    Première édition avec Sphinx:                   & 1 Septembre 2019 \\
    Première édition avec Sphinx, avec corrections: & 15 Juillet 2020  \\
    Seconde édition avec MkDocs Material:           & 30 Juillet 2024  \\
  \end{tabular}
\end{center}
\vfil
\endgroup

% Avoid discusting pages
\raggedbottom

\frontmatter

\VAR{frontmatter}

\clearpage
\tableofcontents

\mainmatter

\VAR{mainmatter}

\backmatter

\input{solutions.tex}

\VAR{backmatter}

\clearpage

\listoffigures

\clearpage

\listoftables

\clearpage

\printglossary[type=\acronymtype, title=Liste des acronymes]
\printglossary[title=Termes et définitions]

\printindex

\end{document}
