#!/usr/bin/env python
import os, sys, glob
import decay_exper1

decay_exper1.run_experiments()

# Write LaTeX report
do = open('tmp_report.tex', 'w')
# raw strings are important since LaTeX makes heavy use of backslashes
do.write(r'''
\documentclass[twoside]{article}
\usepackage{relsize,epsfig,makeidx,amsmath,amsfonts}
\usepackage[latin1]{inputenc}
%% Hyperlinks in PDF:
\usepackage[colorlinks=true,linkcolor=black,citecolor=black,
    filecolor=black,urlcolor=black,pdfmenubar=true,pdftoolbar=true,
    urlcolor=black,bookmarksdepth=3]{hyperref}

\makeindex

\begin{document}
\title{Experiments with Schemes for Exponential Decay}
\author{Hans Petter Langtangen\footnote{
Center for Biomedical Computing, Simula Research Laboratory, and
Department of Informatics, University of Oslo.}}
\date{\today}

\begin{abstract}
This report investigates the accuracy of three finite difference
schemes for the ordinary differential equation $u'=-au$ with the
aid of numerical experiments. Numerical artifacts are in particular
demonstrated.
\end{abstract}

\tableofcontents

\section{Mathematical problem}
\label{math:problem}
\index{model problem}\index{exponential decay}

We address the initial-value problem

\begin{align}
u'(t) &= -au(t), \quad t \in (0,T], \label{ode}\\
u(0)  &= I,                         \label{initial:value}
\end{align}
where $a$, $I$, and $T$ are prescribed parameters, and $u(t)$ is
the unknown function to be estimated. This mathematical model
is relevant for physical phenomena featuring exponential decay
in time.

\section{Numerical solution method}
\label{numerical:problem}
\index{mesh in time} \index{$\theta$-rule} \index{numerical scheme}
\index{finite difference scheme}

We introduce a mesh in time with points $0= t_0< t_1 \cdots < t_N=T$.
For simplicity, we assume constant spacing $\Delta t$ between the
mesh points: $\Delta t = t_{n}-t_{n-1}$, $n=1,\ldots,N$. Let
$u^n$ be the numerical approximation to the exact solution at $t_n$.

The $\theta$-rule is used to solve (\ref{ode}) numerically:

\[
u^{n+1} = \frac{1 - (1-\theta) a\Delta t}{1 + \theta a\Delta t}u^n,
\]
for $n=0,1,\ldots,N-1$. This scheme corresponds to

\begin{itemize}
  \item The Forward Euler scheme when $\theta=0$
  \item The Backward Euler scheme when $\theta=1$
  \item The Crank-Nicolson scheme when $\theta=1/2$
\end{itemize}

\section{Implementation}

The numerical method is implemented in a Python function:

\begin{quote}
\begin{verbatim}
def solver(I, a, T, dt, theta):
    """Solve u'=-a*u, u(0)=I, for t in (0,T] with steps of dt."""
    dt = float(dt)           # avoid integer division
    N = int(round(T/dt))     # no of time intervals
    T = N*dt                 # adjust T to fit time step dt
    u = zeros(N+1)           # array of u[n] values
    t = linspace(0, T, N+1)  # time mesh

    u[0] = I                 # assign initial condition
    for n in range(0, N):    # n=0,1,...,N-1
        u[n+1] = (1 - (1-theta)*a*dt)/(1 + theta*dt*a)*u[n]
    return u, t
\end{verbatim}
\end{quote}

\section{Numerical experiments}
\index{numerical experiments}

We define a set of numerical experiments where $I$, $a$, and $T$ are
fixed, while $\Delta t$ and $\theta$ are varied.
In particular, $I=%s$, $a=%s$, $\Delta t = %s$.

\subsection{The Backward Euler method}
\index{BE}

\begin{center}  %% inline figure
  \centerline{\includegraphics[width=0.9\linewidth]{BE.png}}
\end{center}

\subsection{The Crank-Nicolson method}
\index{CN}

\begin{center}  %% inline figure
  \centerline{\includegraphics[width=0.9\linewidth]{CN.png}}
\end{center}

\subsection{The Forward Euler method}
\index{FE}

\begin{center}  %% inline figure
  \centerline{\includegraphics[width=0.9\linewidth]{FE.png}}
\end{center}

\subsection{Error vs $\Delta t$}
\index{error vs time step}

How $E$ varies with $\Delta t$ for $\theta=0,0.5,1$
is shown in Figure~\ref{fig:E}.

\begin{figure}[!ht]
  \centerline{\includegraphics[width=0.9\linewidth]{error.png}}
  \caption{
  Error versus time step. \label{fig:E}
  }
\end{figure}

\printindex
\end{document}
''' % (decay_exper1.I, decay_exper1.a, ', '.join(sys.argv[1:])))