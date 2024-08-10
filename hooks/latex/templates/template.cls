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
\usepackage{csquotes}
\usepackage{capt-of}
\usepackage[acronym]{glossaries}
\usepackage{imakeidx}
% \usepackage{listings}
\usepackage{fvextra} % Pour une meilleure gestion des verbatim inline
\usepackage{titlesec} % Pour la personnalisation des titres
\usepackage{enumitem} % Pour personnaliser les listes
\usepackage{etoolbox}
\usepackage{tocloft}
\usepackage{adjustbox} % Auto resize tables to fit page width
\usepackage{caption}
\usepackage{microtype} % Avoid overfull with fonts
\usepackage{polyglossia}
\usepackage{emptypage} % Nothing on empty pages

\usetikzlibrary{shapes.geometric}
\usetikzlibrary{calc}
\usetikzlibrary{shadows}

\preto\frontmatter{\setcounter{secnumdepth}{0}}
\preto\mainmatter{\setcounter{secnumdepth}{2}}

\makeglossaries
\makeindex

\setcounter{tocdepth}{2}

% Give more spaces on Table of content (between numbers and text)
\setlength{\cftsecnumwidth}{3em}
\setlength{\cftsubsecnumwidth}{3.5em}
\setlength{\cftfignumwidth}{3em}
\setlength{\cfttabnumwidth}{3em}

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
      "NotoSans:mode=harf;",
      "FiraCode:mode=harf;",
    }
   )}

\setmainfont{Noto Serif}[
  RawFeature={fallback=fontfallback}
]

\setmonofont{Noto Sans Mono}[
  Scale=0.8,
  ItalicFont=lmmono10-italic.otf,
  BoldItalicFont=lmmonolt10-boldoblique.otf,
  RawFeature={fallback=fontfallback}
]

\newfontfamily\creativecommonfont{Creative Commons}
\DeclareTextFontCommand\creativecommon{\creativecommonfont}

% Make quotations italic and smaller
\AtBeginEnvironment{displayquote}{\small\itshape}



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


  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}

  \pagestyle{fancy}
  \fancyhf{}

  \fancyhead[LE]{\leftmark}
  \fancyfoot[LE,RO]{\thepage}

  \fancyhead[RO]{\rightmark}
  \fancyfoot[LE,RO]{\thepage}

  % plain : chapters
  \fancypagestyle{plain}{%
    \fancyhf{}
    \fancyfoot[LE,RO]{\thepage}
  }

  \fancypagestyle{part}{%
    \fancyhf{}
  }

  \patchcmd{\part}{\thispagestyle{plain}}{\thispagestyle{part}}{}{}


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
        borderline west={0.5mm}{0mm}{calloutNoteFrame},
        title={\makebox[1.3em][c]{\faBookmark}},
    },
    callout abstract/.style={
        colbacktitle=calloutAbstractBg,
        colframe=calloutAbstractFrame,
        coltitle=calloutAbstractFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutAbstractFrame},
        title={\makebox[1.3em][c]{\faLaptopCode}},
    },
    callout info/.style={
        colbacktitle=calloutInfoBg,
        colframe=calloutInfoFrame,
        coltitle=calloutInfoFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutInfoFrame},
        title={\makebox[1.3em][c]{\faComment}},
    },
    callout tip/.style={
        colbacktitle=calloutTipBg,
        colframe=calloutTipFrame,
        coltitle=calloutTipFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutTipFrame},
        title={\makebox[1.3em][c]{\faLightbulb}},
    },
    callout success/.style={
        colbacktitle=calloutSuccessBg,
        colframe=calloutSuccessFrame,
        coltitle=calloutSuccessFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutSuccessFrame},
        title={\makebox[1.3em][c]{\faCheck}},
    },
    callout warning/.style={
        colbacktitle=calloutWarningBg,
        colframe=calloutWarningFrame,
        coltitle=calloutWarningFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutWarningFrame},
        title={\makebox[1.3em][c]{\faBolt}},
    },
    callout failure/.style={
        colbacktitle=calloutFailureBg,
        colframe=calloutFailureFrame,
        coltitle=calloutFailureFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutFailureFrame},
        title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
    callout important/.style={
        colbacktitle=calloutDangerBg,
        colframe=calloutDangerFrame,
        coltitle=calloutDangerFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutDangerFrame},
        title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
    callout hint/.style={
        colbacktitle=calloutTipBg,
        colframe=calloutTipFrame,
        coltitle=calloutTipFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutTipFrame},
        title={\makebox[1.3em][c]{\faLightbulb}},
    },
    callout danger/.style={
        colbacktitle=calloutDangerBg,
        colframe=calloutDangerFrame,
        coltitle=calloutDangerFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutDangerFrame},
        title={\makebox[1.3em][c]{\faExclamationTriangle}},
    },
    callout bug/.style={
        colbacktitle=calloutBugBg,
        colframe=calloutBugFrame,
        coltitle=calloutBugFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutBugFrame},
        title={\makebox[1.3em][c]{\faBomb}},
    },
    callout example/.style={
        colbacktitle=calloutExampleBg,
        colframe=calloutExampleFrame,
        coltitle=calloutExampleFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutExampleFrame},
        title={\makebox[1.3em][c]{\faFlask}},
    },
    callout quote/.style={
        colbacktitle=calloutQuoteBg,
        colframe=calloutQuoteFrame,
        coltitle=calloutQuoteFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutQuoteFrame},
        title={\makebox[1.3em][c]{\faQuestionCircle}},
    },
    callout question/.style={
        colbacktitle=calloutQuestionBg,
        colframe=calloutQuestionFrame,
        coltitle=calloutQuestionFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutQuestionFrame},
        title={\makebox[1.3em][c]{\faQuestionCircle}},
    },
    callout exercise/.style={
        colbacktitle=calloutExerciseBg,
        colframe=calloutExerciseFrame,
        coltitle=calloutExerciseFrame!80!black,
        borderline west={0.5mm}{0mm}{calloutExerciseFrame},
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
    borderline west={0.5mm}{0mm}{black!70},
    #1,
    after title={~#2}
}

\setminted{style=trac}
\setmintedinline{style=trac} %,bgcolor=gray!20}

% \tcbuselibrary{listings}

% \definecolor{listingsKeyword}{HTML}{063970}
% \definecolor{listingsComment}{HTML}{5C6B77}
% \definecolor{listingsStrings}{HTML}{5C5B4C}

% \lstdefinelanguage{text}{
% }

% \lstdefinelanguage{console}{
%   morekeywords={\$},
%   morecomment=[l]{\#},
%   morestring=[b]",
% }

% \lstdefinelanguage{makefile}{
%   keywords={\$@, \$<, \$^, \$+, \$*, \$?, \$|},
%   ndkeywords={define, endef, export, override, private, vpath},
%   sensitive=false,
%   comment=[l]{\#},
%   morestring=[b]',
%   morestring=[b]"
% }

% \definecolor{diffstart}{named}{Grey}
% \definecolor{diffincl}{named}{Green}
% \definecolor{diffrem}{named}{OrangeRed}

% \lstdefinelanguage{yaml}{
%   keywords={true,false,null,y,n},
%   sensitive=false,
%   comment=[l]{\#},
%   morecomment=[s]{/*}{*/},
%   morestring=[b]',
%   morestring=[b]",
%   literate =    {---}{{\ProcessThreeDashes}}3
%                 {>}{{\textcolor{red}\textgreater}}1
%                 {|}{{\textcolor{red}\textbar}}1
%                 {\ -\ }{{\mdseries\ -\ }}3
% }

% \lstdefinelanguage{diff}{
%   basicstyle=\ttfamily\small,
%   morecomment=[f][\color{diffstart}]{@@},
%   morecomment=[f][\color{diffincl}]{+\ },
%   morecomment=[f][\color{diffrem}]{-\ },
% }

% \lstdefinelanguage{javascript}{
%   keywords={typeof, new, true, false, catch, function, return, null, catch, switch, var, if, in, while, do, else, case, break},
%   ndkeywords={class, export, boolean, throw, implements, import, this},
%   sensitive=false,
%   comment=[l]{//},
%   morecomment=[s]{/*}{*/},
%   morestring=[b]',
%   morestring=[b]"
% }

% \lstdefinelanguage{cpp}{
%   language=C++
% }

% \lstdefinelanguage{json}{
%   morestring=[b]",
% }

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
  % lefttitle=0.5em,
  frame hidden,
  %borderline west={0.25mm}{0mm}{black!70},
  % outer arc=0.7mm,
  minted language=#2,
  top=1mm,
  bottom=1mm,
  % listing options={
  %   language=#2,
  %   basicstyle=\ttfamily\footnotesize,
  %   keywordstyle=\bfseries\color{listingsKeyword},
  %   stringstyle=\color{listingsStrings},
  %   commentstyle=\itshape\color{listingsComment},
  %   ndkeywordstyle=\color{darkgray}\bfseries,
  %   identifierstyle=\color{black},
  %   breaklines=true,
  %   showstringspaces=false
  % },
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

\newcommand{\logoimg}[3]{
  \begin{tikzpicture}[remember picture, overlay, x=0.7pt, y=0.7pt]
      \begin{scope}[shift={($(current page.north west) + (#1, -#2) + (0, -75)$)}]
          \fill[#3]
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
              -- (69, 1) -- (74, 1) -- (74, 17) -- cycle;
          \fill[#3]
              (74, 47) -- (46, 47) -- (46, 56) -- (70, 56) -- (70, 61) --
              (46, 61) -- (46, 70) -- (74, 70) -- (74, 75) -- (40, 75) --
              (40, 42) -- (74, 42) -- cycle;
          \fill[#3]
              (27, 61) -- (5, 61) -- (5, 75) -- (0, 75) -- (0, 42) --
              (5, 42) -- (5, 56) -- (27, 56) -- (27, 42) -- (33, 42) --
              (33, 75) -- (27, 75) -- cycle;
          \fill[#3]
              (19, 6) -- (19, 29) -- (33, 29) -- (33, 34) -- (-0, 34) --
              (-0, 29) -- (13, 29) -- (13, 6) -- (-0, 6) -- (-0, 1) --
              (33, 1) -- (33, 6) -- cycle;
          \fill[#3]
              (88, 75) -- (90, 75) -- (87, 65) -- (85, 65) -- (81, 75) --
              (83, 75) -- (86, 68) -- cycle;
          \fill[#3, even odd rule]
              (92, 65) -- (92, 75) -- (95, 75)
              .. controls (98, 75) and (100, 73) .. (100, 70)
              .. controls (100, 67) and (98, 65) .. (95, 65)
              -- cycle
              (95, 67)
              .. controls (97, 67) and (98, 68) .. (98, 70)
              .. controls (98, 72) and (97, 73) .. (95, 73)
              -- (94, 73)
              -- (94, 67)
              -- cycle;
      \end{scope}
  \end{tikzpicture}
}




\def\title{\VAR{title}}
\def\subtitle{Programmation en C}

\definecolor{indigo(dye)}{rgb}{0.0, 0.25, 0.42}

\def\covercolor{indigo(dye)}
\def\author{\VAR{author}}

\newcommand{\changelocaltocdepth}[1]{%
  \addtocontents{toc}{\protect\setcounter{tocdepth}{#1}}%
  \setcounter{tocdepth}{#1}%
}

\pretocmd{\frontmatter}{%
  \pagestyle{plain}%
  \changelocaltocdepth{1}%
}{}{}

\pretocmd{\mainmatter}{%
  \pagestyle{fancy}%
}{}{}

\pretocmd{\mainmatter}{%
  \changelocaltocdepth{2}%
}{}{}

\input{glossary.tex}
\input{acronyms.tex}

\begin{document}

\begin{tikzpicture}[remember picture,overlay]
\fill[\covercolor] (current page.south west) rectangle (current page.north east);

\foreach \i in {2.5,...,20}{
    \node[rounded corners,\covercolor!60,draw,regular polygon,regular polygon sides=6, minimum size=\i cm,ultra thick,rotate=30] at ($(current page.west)+(3.5,-5)$) {} ;
}

\foreach \i in {0.5,...,20}{
\node[rounded corners,\covercolor!90,draw,regular polygon,regular polygon sides=6, minimum size=\i cm,ultra thick] at ($(current page.north west)+(2.5,0)$) {} ;
}

\foreach \i in {0.5,...,20}{
\node[rounded corners,\covercolor!90,draw,regular polygon,regular polygon sides=6, minimum size=\i cm,ultra thick] at ($(current page.north east)+(0,-9.5)$) {} ;
}


\foreach \i in {21,...,6}{
\node[\covercolor!85,rounded corners,draw,regular polygon,regular polygon sides=6, minimum size=\i cm,ultra thick] at ($(current page.south east)+(-0.2,-0.45)$) {} ;
}

\node[
  left,
  \covercolor!5,
  minimum width=150mm,
  text width=150mm,
  minimum height=1cm,
  align=right] at ($(current page.north east)+(-2,-10)$)
{
{\fontsize{25}{30} \selectfont \bfseries \title}
};

\node[
  left,
  \covercolor!10,
  minimum width=150mm,
  text width=150mm,
  minimum height=1cm,
  align=right] at ($(current page.north east)+(-2,-11.3)$)
{
{\huge \textit{\subtitle}}
};

\node[left,\covercolor!5,minimum width=80mm,minimum height=1cm,text width=80mm, align=right, rounded corners] at ($(current page.south east)+(-2,2)$)
{
{\Large \textsc{\author}}
};


\node[fill=\covercolor, rounded corners,text =\covercolor!5,regular polygon,regular polygon sides=6, minimum size=6 cm,inner sep=0,ultra thick,rotate=30] at ($(current page.west)+(3.5,-5)$) {

};

\node[] at ($(current page.west)+(3.5,-5)$) {
  \includegraphics[width=5cm]{c-logo.pdf}
};

\end{tikzpicture}

\logoimg{10mm}{10mm}{\covercolor!5}

\cleardoublepage
\begin{titlepage}
  \logoimg{1cm}{1cm}{black}
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

L'œuvre peut être librement utilisée, à la condition de l'attribuer à l'auteur en citant son nom. Le titulaire de droits peut autoriser tous les types d'utilisation ou au contraire restreindre aux utilisations non commerciales (les utilisations commerciales restant soumises à son autorisation). En sommes vous êtges libre de :

\begin{description}
    \item[Partager] copier, distribuer et communiquer le matériel par tous moyens et sous tous formats
    \item[Adapter] remixer, transformer et créer à partir du matériel
\end{description}

Sous les conditions suivantes :

\begin{description}
    \item[Attribution] Vous devez créditer l'Œuvre, intégrer un lien vers la licence et indiquer si des modifications ont été effectuées à l'Œuvre. Vous devez indiquer ces informations par tous les moyens raisonnables, sans toutefois suggérer que l'Offrant vous soutient ou soutient la façon dont vous avez utilisé son œuvre.
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
Première édition avec Sphinx:                      & 1 Septembre 2019 \\
Première édition avec Sphinx, avec corrections:    & 15 Juillet 2020 \\
Seconde édition avec MkDocs Material:              & 30 Juillet 2024 \\
\end{tabular}
\end{center}
\vfil
\endgroup

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
