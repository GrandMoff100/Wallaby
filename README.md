# Wallaby

A markup language that compiles to sound.

## Example

```latex
\tag{Artist}{Foobar}
\tag{Title}{A Winter Ball}
\tag{Year}{2018}

\begin{stream}  # Begin a synchronized stream
    
  \begin{tempo}{60}  # 60 bpm
    \begin{timesignature}{4}{4}
      \play{Ab}{2}{f}
      \begin{define}{mymotif}  # Define a repeatable sequence
        \begin{dynamic}{p}  # Apply dynamic to the following notes
          \play{C}{6}
          \play{D}{2}
          \play{E}{2}
        \end{dynamic}
      \end{define}
      \mymotif{3}  # play the motif 3 times
    \end{timesignature}
  \end{tempo}
\end{stream}
```
