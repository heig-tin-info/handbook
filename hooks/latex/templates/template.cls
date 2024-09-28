\documentclass{mkbook}

\def\title{\VAR{title}}
\def\subtitle{\VAR{subtitle}}
\def\author{\VAR{author}}
\def\email{\VAR{email}}

\definecolor{indigo(dye)}{rgb}{0.0, 0.25, 0.42}


\makeglossaries
\makeindex

\input{glossary}
\input{acronyms}

\begin{document}

\input{cover}

\cleardoublepage
\input{titlepage}

\thispagestyle{empty}
\input{imprint}

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
