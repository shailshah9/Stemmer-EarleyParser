NLP - Programming Assignment 1

This is a working code of "Stemmer and Earley Parser" written in python3 using NLTK.


------------------------
How to execute the code:
------------------------
Run main.py
------------------------


------------
*Definition:
------------
->To implement  a stemmer and the Earley parser for parsing English natural language text in Python. 
->Stemmer should scan the input and divide into tokens. 
->The output contains one token per line including the token (as string), its type (INT, DOUBLE, STRING, OP, or ENDFILE), line number where the token appears, and the base form if not the same as the token.
->All possible	morphology need to be handled correctly, e.g., plural, tense, single third person verb, possess apostrophe, comparative, adverb, etc.
-> Earley parser for the given grammar and input string.


-----------------
*Flow of program:
-----------------
1)Scan the input from the input file
2)Tokenize the input file and process it to be ready for stemming
3)Print the input file grammar and input string
4)Stem the input file and output as given in the definition
5)Print the parser chart for the given string and grammar



---------------
Stemmer:
--------------
At the very basics of it, the major difference between the porter and lancaster stemming algorithms is that the lancaster stemmer is significantly more aggressive than the porter stemmer. The three major stemming algorithms in use today are Porter, Snowball(Porter2), and Lancaster (Paice-Husk), with the aggressiveness continuum basically following along those same lines. Porter is the least aggressive algorithm, with the specifics of each algorithm actually being fairly lengthy and technical. Here is a break down for you though:

Porter: Most commonly used stemmer without a doubt, also one of the most gentle stemmers. One of the few stemmers that actually has Java support which is a plus, though it is also the most computationally intensive of the algorithms(Granted not by a very significant margin). It is also the oldest stemming algorithm by a large margin.

Snowball(Porter2): Nearly universally regarded as an improvement over porter, and for good reason. Porter himself in fact admits that it is better than his original algorithm. Slightly faster computation time than porter, with a fairly large community around it.

Lancaster: Very aggressive stemming algorithm, sometimes to a fault. With porter and snowball, the stemmed representations are usually fairly intuitive to a reader, not so with Lancaster, as many shorter words will become totally obfuscated. The fastest algorithm here, and will reduce your working set of words hugely, but if you want more distinction, not the tool one would want.

I feel that Snowball is usually the way to go. There are certain circumstances in which Lancaster will hugely trim down our working set, which can be very useful, however the marginal speed increase over snowball in my opinion is not worth the lack of precision. Porter has the most implementations though and so is usually the default go-to algorithm, but if one can, use snowball.



--------------------------------
The Algorithm For Earley Parser:
--------------------------------
In the following descriptions, α, β, and γ represent any string of terminals/nonterminals (including the empty string), X and Y represent single nonterminals, and a represents a terminal symbol.

Earley's algorithm is a top-down dynamic programming algorithm. In the following, we use Earley's dot notation: given a production X → αβ, the notation X → α • β represents a condition in which α has already been parsed and β is expected.

Input position 0 is the position prior to input. Input position n is the position after accepting the nth token. (Informally, input positions can be thought of as locations at token boundaries.) For every input position, the parser generates a state set. Each state is a tuple (X → α • β, i), consisting of

the production currently being matched (X → α β)
our current position in that production (represented by the dot)
the position i in the input at which the matching of this production began: the origin position
(Earley's original algorithm included a look-ahead in the state; later research showed this to have little practical effect on the parsing efficiency, and it has subsequently been dropped from most implementations.)

The state set at input position k is called S(k). The parser is seeded with S(0) consisting of only the top-level rule. The parser then repeatedly executes three operations: prediction, scanning, and completion.

Prediction: For every state in S(k) of the form (X → α • Y β, j) (where j is the origin position as above), add (Y → • γ, k) to S(k) for every production in the grammar with Y on the left-hand side (Y → γ).
Scanning: If a is the next symbol in the input stream, for every state in S(k) of the form (X → α • a β, j), add (X → α a • β, j) to S(k+1).
Completion: For every state in S(k) of the form (X → γ •, j), find states in S(j) of the form (Y → α • X β, i) and add (Y → α X • β, i) to S(k).
It is important to note that duplicate states are not added to the state set, only new ones. These three operations are repeated until no new states can be added to the set. The set is generally implemented as a queue of states to process, with the operation to be performed depending on what kind of state it is.

The algorithm accepts if (X → γ •, 0) ends up in S(n), where (X → γ) is the top level-rule and n the input length, otherwise it rejects.

----------------------------
Pseudocode for Earley-Parser:
----------------------------
DECLARE ARRAY S;

function INIT(words)
    S ← CREATE-ARRAY(LENGTH(words))
    for k ← from 0 to LENGTH(words) do
        S[k] ← EMPTY-ORDERED-SET

function EARLEY-PARSE(words, grammar)
    INIT(words)
    ADD-TO-SET((γ → •S, 0), S[0])
    for k ← from 0 to LENGTH(words) do
        for each state in S[k] do  // S[k] can expand during this loop
            if not FINISHED(state) then
                if NEXT-ELEMENT-OF(state) is a nonterminal then
                    PREDICTOR(state, k, grammar)         // non-terminal
                else do
                    SCANNER(state, k, words)             // terminal
            else do
                COMPLETER(state, k)
        end
    end
    return chart

procedure PREDICTOR((A → α•Bβ, j), k, grammar)
    for each (B → γ) in GRAMMAR-RULES-FOR(B, grammar) do
        ADD-TO-SET((B → •γ, k), S[k])
    end

procedure SCANNER((A → α•aβ, j), k, words)
    if a ⊂ PARTS-OF-SPEECH(words[k]) then
        ADD-TO-SET((A → αa•β, j), S[k+1])
    end

procedure COMPLETER((B → γ•, x), k)
    for each (A → α•Bβ, j) in S[x] do
        ADD-TO-SET((A → αB•β, j), S[k])
    end

---------------
Implementation:
---------------

1) Implemented stemmer using Snowball Stemmer provided by NLTK
2) Implemented Earley - Parser as per the algorithm above

------------------
Run Time Analysis:
------------------

Based on research that has been done, the calculation time
complexity of the algorithm generated Porter(2) is O (7)
Reference from - "http://ijarcet.org/wp-content/uploads/IJARCET-VOL-6-ISSUE-7-1010-1012.pdf"

And 

Earley-Parser takes O(n^3)

Overall Complexity O(n^3)

--------------------
Function Definition:
--------------------

1) predictor(rule,state) : returns a dictionary
->predictor for parser

2)scanner(rule,next_input) : returns a dictionary
->scanner for parser

3)completer(rule,charts) : returns a list
->completer for parser

4)printCharts(charts,inp) :
->print the parser chart

5)stemKeywords(word,stemmer):
->identify the keywords that needs to be stemmed and stem them

6)checkInputType(token):
->tokenize the given input based on type of OP, STRING, INT, DOUBLE or ENDFILE

-------------
Sample Input:
-------------

S	: NP VP | Aux NP VP | VP ;
NP : Pronoun | Proper-Noun | Det Nominal ;
VP : Verb
	| Verb NP
	| Verb NP PP
	| Verb PP
	| VP PP
	;
Aux	: can | will ;
Det	: the | that ;
Pronoun : he | she ;
Proper-Noun : mary | john ;
Nominal : Noun | Nominal Noun | Nominal PP ;
Noun	: book | flight ;
Verb	: do | work | book ;
PP	: Prep NP ;
Prep	: in | on | at ;
W 	= Book that flight.

--------------
Sample Output:
--------------

Input:
--------------------------------------------------
S : NP VP | Aux NP VP | VP ;
NP : Pronoun | Proper-Noun | Det Nominal ;
VP : Verb
| Verb NP
| Verb NP PP
| Verb PP
| VP PP
;
Aux : can | will ;
Det : the | that ;
Pronoun : he | she ;
Proper-Noun : mary | john ;
Nominal : Noun | Nominal Noun | Nominal PP ;
Noun : book | flight ;
Verb : do | work | book ;
PP : Prep NP ;
Prep : in | on | at ;
W = Book that flight .


Stemmer:
------------------------------
	S STRING 1
	: OP 1
	NP STRING 1
	VP STRING 1
	| OP 1
	Aux STRING 1
	NP STRING 1
	VP STRING 1
	| OP 1
	VP STRING 1
	; OP 1
	NP STRING 2
	: OP 2
	Pronoun STRING 2
	| OP 2
	Proper-Noun STRING 2
	| OP 2
	Det STRING 2
	Nominal STRING 2
	; OP 2
	VP STRING 3
	: OP 3
	Verb STRING 3
	| OP 4
	Verb STRING 4
	NP STRING 4
	| OP 5
	Verb STRING 5
	NP STRING 5
	PP STRING 5
	| OP 6
	Verb STRING 6
	PP STRING 6
	| OP 7
	VP STRING 7
	PP STRING 7
	; OP 8
	Aux STRING 9
	: OP 9
	can STRING 9
	| OP 9
	will STRING 9
	; OP 9
	Det STRING 10
	: OP 10
	the STRING 10
	| OP 10
	that STRING 10
	; OP 10
	Pronoun STRING 11
	: OP 11
	he STRING 11
	| OP 11
	she STRING 11
	; OP 11
	Proper-Noun STRING 12
	: OP 12
	mary STRING 12
	| OP 12
	john STRING 12
	; OP 12
	Nominal STRING 13
	: OP 13
	Noun STRING 13
	| OP 13
	Nominal STRING 13
	Noun STRING 13
	| OP 13
	Nominal STRING 13
	PP STRING 13
	; OP 13
	Noun STRING 14
	: OP 14
	book STRING 14
	| OP 14
	flight STRING 14
	; OP 14
	Verb STRING 15
	: OP 15
	do STRING 15
	| OP 15
	work STRING 15
	| OP 15
	book STRING 15
	; OP 15
	PP STRING 16
	: OP 16
	Prep STRING 16
	NP STRING 16
	; OP 16
	Prep STRING 17
	: OP 17
	in STRING 17
	| OP 17
	on STRING 17
	| OP 17
	at STRING 17
	; OP 17
	W STRING w 18
	= OP = 18
	Book STRING book 18
	that STRING that 18
	flight STRING flight 18
	. OP 18
	ENDFILE


Parsed Chart:
Stemmed string to be parsed: book that flight
----------------------------------------------------------------------------------------------

Chart 0	         Root  -> * S                        [0,0]             Dummy Start State    	
	            S  -> * NP VP                    [0,0]                 Predictor        	
	            S  -> * aux NP VP                [0,0]                 Predictor        	
	            S  -> * VP                       [0,0]                 Predictor        	
	           NP  -> * pronoun                  [0,0]                 Predictor        	
	           NP  -> * proper-noun              [0,0]                 Predictor        	
	           NP  -> * det NOMINAL              [0,0]                 Predictor        	
	           VP  -> * verb                     [0,0]                 Predictor        	
	           VP  -> * verb NP                  [0,0]                 Predictor        	
	           VP  -> * verb NP PP               [0,0]                 Predictor        	
	           VP  -> * verb PP                  [0,0]                 Predictor        	
	           VP  -> * VP PP                    [0,0]                 Predictor        
Chart 1	         verb  -> book *                     [0,1]                  Scanner         	
	           VP  -> verb *                     [0,1]                 Completer        	
	           VP  -> verb * NP                  [0,1]                 Completer        	
	           VP  -> verb * NP PP               [0,1]                 Completer        	
	           VP  -> verb * PP                  [0,1]                 Completer        	
	            S  -> VP *                       [0,1]                 Completer        	
	           VP  -> VP * PP                    [0,1]                 Completer        	
	           NP  -> * pronoun                  [1,1]                 Predictor        	
	           NP  -> * proper-noun              [1,1]                 Predictor        	
	           NP  -> * det NOMINAL              [1,1]                 Predictor        	
	           PP  -> * prep NP                  [1,1]                 Predictor        	
	         Root  -> S *                        [0,1]                 Completer        
Chart 2	          det  -> that *                     [1,2]                  Scanner         	
	           NP  -> det * NOMINAL              [1,2]                 Completer        	
	      NOMINAL  -> * noun                     [2,2]                 Predictor        	
	      NOMINAL  -> * NOMINAL noun             [2,2]                 Predictor        	
	      NOMINAL  -> * NOMINAL PP               [2,2]                 Predictor        
Chart 3	         noun  -> flight *                   [2,3]                  Scanner         	
	      NOMINAL  -> noun *                     [2,3]                 Completer        	
	           NP  -> det NOMINAL *              [1,3]                 Completer        	
	      NOMINAL  -> NOMINAL * noun             [2,3]                 Completer        	
	      NOMINAL  -> NOMINAL * PP               [2,3]                 Completer        	
	           VP  -> verb NP *                  [0,3]                 Completer        	
	           VP  -> verb NP * PP               [0,3]                 Completer        	
	           PP  -> * prep NP                  [3,3]                 Predictor        	
	            S  -> VP *                       [0,3]                 Completer        	
	           VP  -> VP * PP                    [0,3]                 Completer        	
	         Root  -> S *                        [0,3]                 Completer        


----------------------------------------------------------------------------------------------



