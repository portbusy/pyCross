# Python Encrypted-Crossword Solver

An encrypted crosswords solver written in Python.
Uses numpy for the array-2D representation of a crossword matrix.

## Method
The algorithm tries to find the most easy encrypted word to solve in the matrix (the longest word with less unknown characters) 
and matches it against the vocabulary to find all the valid solutions for the encrypted word (a word is a valid solution only if
the characters it solves are not already matched in the matrix).

All the valid words defines new number-letter matches in the original matrix.
By replacing the new number-letter matches, a set of branched matrix from the original matrix is created, 
each sorted from the most correct to the least (*correctness* of a matrix is defined as the ratio between the
number of valid and solved word cells in the matrix against the total number of character of each word, both in the rows and in the columns).

The branch matrix set is then recursively solved in a loop. The recursion stops only if the matrix is completely solved or if
it contains encrypted words that cannot be matched with valid words.

The algorithm can also prompts the user to *recognize* some completed but unrecognized words,
or to *solve* some almost-solved words that it cannot find in the given vocabulary.

Once a solution is found, the program stops and the solution is printed.

## Example

Example of outputs and prompts using the 'crossword.csv' test file:

~~~
Loading vocabulary..
Loading matrix from text..
Filling matrix..
Solving..
1) Solving: in?on?ro
2) Solving: ?oco
- Can you solve the word 'sr*no'? (leave empty to skip) 
3) Solving: sr?no
3) Solving: fr?no
4) Solving: cr?n
5) Solving: conterr?nei
4) Solving: cr?n
- Can you solve the word 'contarr*nai'? (leave empty to skip) 
5) Solving: contarr?nai
3) Solving: pr?no
4) Solving: cr?n
5) Solving: conterr?nei
6) Solving: co?onie
- Can you solve the word 'olio*iricino'? (leave empty to skip) oliodiricino
7) Solving: olio?iricino
8) Solving: ?inacce
- Can you solve the word 'pe*cimendolo'? (leave empty to skip) 
9) Solving: pe?cimendolo
9) Solving: pe?civendolo
- Do you recognize the word 'scevola'? (Y/N) y
10) Solving: va?ito
11) Solving: c?anel

Solution found:
-	-	-	-	-	-	-	-	-	-	-	-
u	v	a	█	v	a	g	i	t	o	█	s
t	i	r	r	e	n	i	c	a	█	h	a
█	n	o	i	r	█	o	s	█	p	o	s
█	a	█	█	s	s	█	█	s	r	█	s
a	c	c	i	a	c	c	a	t	u	r	a
█	c	o	n	t	e	r	r	a	n	e	i
p	e	s	c	i	v	e	n	d	o	l	o
o	█	c	o	l	o	n	i	e	█	e	l
c	h	a	n	e	l	█	e	r	a	█	a
o	a	█	t	█	a	p	█	a	g	e	█
█	l	o	r	d	█	g	n	█	h	i	t
o	l	i	o	d	i	r	i	c	i	n	o
-	-	-	-	-	-	-	-	-	-	-	-
~~~