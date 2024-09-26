\documentclass{mkbook}

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
