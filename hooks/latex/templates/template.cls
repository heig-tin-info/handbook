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
\usepackage{emptypage} % Nothing on empty pages

\setcounter{tocdepth}{2}

% Give more spaces on Table of content (between numbers and text)
\setlength{\cftsecnumwidth}{4em}
\setlength{\cftsubsecnumwidth}{4em}
\setlength{\cftfignumwidth}{4em}
\setlength{\cfttabnumwidth}{4em}

\setdefaultlanguage{french}
\setotherlanguages{english}

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
      "NotoSans:mode=harf;"
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


\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\pagestyle{fancy}
\fancyhf{} % Efface les en-têtes et pieds de page par défaut


% Définition des en-têtes et pieds de page pour les pages paires (gauche)
\fancyhead[LE]{\leftmark} % Section en haut à gauche
\fancyfoot[LE,RO]{\thepage} % Numéro de page en bas au centre

% Définition des en-têtes et pieds de page pour les pages impaires (droite)
\fancyhead[RO]{\rightmark} % Chapitre en haut à droite
\fancyfoot[LE,RO]{\thepage} % Numéro de page en bas au centre

% plain : parts
\fancypagestyle{plain}{%
  \fancyhf{} % Efface les en-têtes et pieds de page par défaut
  \fancyfoot[C]{\thepage} % Numéro de page en bas au centre
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

% Avoid orphans at the end of a page, encourage page breaks if there are
% a section with less than 3 lines
% https://tex.stackexchange.com/a/723704/85416
\makeatletter
\patchcmd\@afterheading{\clubpenalty \@M}{\clubpenalties 3 \@M\@M 5000 }{%
  \typeout{patched}}{\typeout{patch failed}
}
\makeatother

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




\newcommand{\logoimg}[2]{
    \begin{tikzpicture}[x=0.7pt,y=0.7pt]%
        \fill[black]
            (74, 18) -- (56, 18) -- (56, 12) -- (68, 12) -- (68, 12)
            .. controls (67, 7) and (63, 5) .. (57, 5)
            .. controls (50, 5) and (45, 10) .. (45, 17)
            .. controls (45, 24) and (50, 30) .. (57, 30)
            .. controls (63, 30) and (67, 27) .. (69, 23)
            -- (74, 25)
            .. controls (71, 32) and (65, 35) .. (57, 35)
            .. controls (47, 35) and (39, 27) .. (39, 17)
            .. controls (39, 7) and (47, 0) .. (57, 0)
            .. controls (62, 0) and (66, 2) .. (69, 5)
            -- (69, 1) -- (74, 1) -- (74, 17) -- cycle ;
        \fill[black]
            (74, 47) -- (46, 47) -- (46, 56) -- (70, 56) -- (70, 61) --
            (46, 61) -- (46, 70) -- (74, 70) -- (74, 75) -- (40, 75) --
            (40, 42) -- (74, 42) -- cycle ;
        \fill[black]
            (27, 61) -- (5, 61) -- (5, 75) -- (0, 75) -- (0, 42) --
            (5, 42) -- (5, 56) -- (27, 56) -- (27, 42) -- (33, 42) --
            (33, 75) -- (27, 75) -- cycle ;
        \fill[black]
            (19, 6) -- (19, 29) -- (33, 29) -- (33, 34) -- (-0, 34) --
            (-0, 29) -- (13, 29) -- (13, 6) -- (-0, 6) -- (-0, 1) --
            (33, 1) -- (33, 6) -- cycle;
        \fill[black]
            (88, 75) -- (90, 75) -- (87, 65) -- (85, 65) -- (81, 75) --
            (83, 75) -- (86, 68) -- cycle;
        \fill[black]
            (92, 65) -- (92, 75) -- (95, 75)
            .. controls (98, 75) and (100, 73) .. (100, 70)
            .. controls (100, 67) and (98, 65) .. (95, 65)
            -- cycle;
        \fill[white]
            (95, 67)
            .. controls (97, 67) and (98, 68) .. (98, 70)
            .. controls (98, 72) and (97, 73) .. (95, 73)
            -- (94, 73)
            -- (94, 67)
            -- cycle;
    \end{tikzpicture}
}

\newcommand{\logo}[2]{% \logo{<left>}{<top>}
    \begin{tikzpicture}[remember picture,overlay, align=center,]
        \node(logo) at ([xshift=#1, yshift=-#2] current page.north west)
        [anchor=north west] {\logoimg{#1}{#2}};
    \end{tikzpicture}\vspace*{-\baselineskip}}



\input{acronyms.tex}

\begin{document}

\begin{titlepage}
  \logo{1cm}{1cm}
  \vspace{6cm}
  \vfil
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

\clearpage

\listoffigures

\clearpage

\listoftables

\clearpage

\printacronyms[title=Liste des acronymes]

\end{document}
