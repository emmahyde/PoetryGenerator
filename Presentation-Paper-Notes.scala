
Existing Research in this Topic:
	Poetry Generator: Python Program
	Got into journal - passes Turing Test
	Uses dictionary of words, special/specific categories like 'fruit'
	Also has some pre-set phrases in which one word is inserted
	Uses .bnf file for CFG instead of NLTK CFG / doesn't use NLTK at all

Goals to Improve Existing Research:
	Dynamic by using input words - classifying parts of speech

Implementation:
	CFG in NLTK in Python
	Grammar rules mapping to text input

Problems Faced:
	Some words get classified wrong
	Adverbs - ly and else
	Noun determiners a vs an
	Rhyming would be hard to implement using CFG by nature
	Actual generation of sentences from CFG in NLTK does DFS of word tree - 
		makes all sentences possible starting with same word
		this makes all sentences be almost the same - exponential blowup
		- Dealt with this by creating a method that makes random decisions navigating grammar tree
	Doesn't differenciate between words like she / her / herself, which are used in different contexts
	Doesn't differenciate between all/ a as determiners

Where we are trying to improve:
	Classifying the words more specially in pre-processing





Things to do to the program:
	Put a minimum on the number of words in input
	Split adverbs -ly and else
	Split nouns a/an
	Space before comma

