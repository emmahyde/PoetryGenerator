import nltk
from nltk.data import load
from nltk import CFG
from nltk.parse.generate import generate
from nltk.grammar import Nonterminal, Production, is_nonterminal
import random
import re

# Dictionary contains:
# grammar: list of lists mapping lists of words to their part of speech (pos) tag
# tags: a list of all possible pos tags
class Dictionary:

    def __init__(self,words):
        self.grammar = {}
        self.tags = load('help/tagsets/upenn_tagset.pickle')
        tagged = nltk.pos_tag(words) # get pos tags for each word
        for tag in self.tags: # initialize list of words for each tag
            self.grammar[tag] = []
        for tuple in tagged: 
            print(tuple[1]," ",tuple[0])
            # add word to grammar[pos]
            if (tuple[1] == 'NNP'):
                self.grammar[tuple[1]].append(tuple[0])
            else:
                self.grammar[tuple[1]].append(tuple[0].lower())

# Grammar contains:
# dictionary: Dictionary
# cfg: CFG with dictionary words as 'Terminals' 
class Grammar:

    def __init__(self,dictionary):
        self.dictionary = dictionary
        # create base of cfg
        """ CC   - conjunction
            DT   - determiner: an / the / both
            IN   - preposition
            JJ   - adjective
            JJS  - adjective: -est
            JJR  - adjective: -er
            MD   - can / dare / should / will
            NN   - common singular noun
            NNS  - common plural noun
            NNP  - proper singular noun
            NNPS - proper plural noun
            PDT  - all / both / quite / many
            PRP  - hers / himself/ thy / us
            PRPP - his / mine / our / my
            RB   - adverb: -ly ... or not
            RBR  - adverb comparative: -er
            RBS  - adverb superlative: -est
            RP   - participle: for / go / later / across / by
            UH   - interjection
            VB   - vocative verb: to ___ 
            VBD  - past verb: -ed
            VBG  - present verb: -ing
            VBN  - past verb descriptive: -ed: mutated / flourished
            VBP  - present verb: not -s
            VBZ  - present verb: -s
            WDT  - what / which / who
            WRB  - how / whenever / where / why
        """
        
        g = CFG.fromstring("""
            S -> T | T CC comma T | UH comma T | WRB T comma T | T comma WRB T | UH '!' T
            S -> PR comma T | RP NPS comma T | VBG PR comma T | T | T | T
            S -> 'to' VB 'is to' VB PR | RB 'the' NN comma T | VBG comma T
            
            T -> NPS VPS | NPP VPP
            
            NPS -> DT NN | DT JJ NN | DT JJS NN | DT VBG NN | NNP | PDT NNPS | DT VBG NN
            NPS -> 'the' JJR 'of the two' NNS | DT VBN NN | PDT NNS | PRPP NN | DT RBS NN
            NPS -> NPS comma VBD IN NN comma | DT RBS JJ NN | DT VBN NN | DT VBN NN |
            NPS -> PRPP JJ NN | DT JJ JJ NN | DT RB VBG NN | 'my' RB VBG NN | 'that' JJ NN
            NPS -> 'this' | 'that'
            
            VPS -> VBD | VBD NPS | VBD IN NPS | VBZ NP | VPS IN PRP | VBD NPS IN NPS
            VPS -> 'was' VBG NPS | VBD RP NPS | VBZ 'as' NPS VBZ | VBZ 'like' NPS VBZ
            VPS -> VBZ PR | VBZ NPS | 'was' VBG | 'has been' VBG | 'is' RB VBG
            VPS -> VBZ JJ CC JJ | VBD comma VBG comma VBG | 'was' VBD | 'is' DT NN 
            VPS -> 'is' JJ and JJ | 'was' VBG RB
            
            NPP -> NNPS | 'the' NNS | 'the' JJ NNS | 'the' JJS NNS | 'the' VBG NNS 
            NPP -> 'the' JJ NNS 'the' RBS JJ NNS | 'the' VBN NNS | 'the' JJ JJ NNS
            NPP -> PDT 'of those' NNS | PRPP NN | 'those' | 'these'
            
            VPP -> VB NPS | VBD | VB | VB PR | VB NPS | VBP NPS | VBP RP | 'are' VBG
            VPP -> VB 'like' NPP VPP | VPP 'as' NPP VPP | VBP | 'have been' VBG | VB NPS
            VPP -> 'were' VBG | 'were' VBG RP | 'were' RB VBG | 'were' RB VBG RP
            VPP -> 'were' VBD | 'are' NNS | 'are' JJ NNS | 'were so' VBG | 'were' VBG RB
            
            PR  -> IN NPS | IN NPP | RP NPP | RP NPS
            """)
        for tag in dictionary.tags:
            # create 'Nonterminal' for each tag
            # some tags need to be changed because they include special characters
            if (tag == ','):
                nt = Nonterminal('comma')
            elif (tag == 'PRP$'):
                nt = Nonterminal('PRPP')
            elif (tag == '.'):
                nt = Nonterminal('period')
            elif (tag == '...'):
                nt = Nonterminal('ddd')
            elif (tag == '$'):
                nt = Nonterminal('dollar')
            elif (tag == '('):
                nt = Nonterminal('oparen')
            elif (tag == ')'):
                nt = Nonterminal('cparen')
            elif (tag == '--'):
                nt = Nonterminal('dash')
            elif (tag == ':'):
                nt = Nonterminal('colon')
            elif (tag == 'WP$'):
                nt = Nonterminal('WP')
            elif (tag == '"'):
                nt = Nonterminal('quote')
            elif (tag == '\'\''):
                nt = Nonterminal('dt')
            elif (tag == '\''):
                nt = Nonterminal('t')
            elif (tag == '``'):
                nt = Nonterminal('dbt')
            elif (tag == '`'):
                nt = Nonterminal('bt')
            # the rest of the tags don't need to be changed
            else:
                nt = Nonterminal(tag)
            # create 'Production' from tag to word for each word of that pos
            for word in dictionary.grammar[tag]:
                if word != '[' and word != ']' and None == re.compile('^\'').search(word):
                    if tag == 'RB' and not word.endswith('ly'):
                        pass
                    if tag == 'JJR' and word == 'more':
                        pass
                    else:
                        t = [word]
                        p = nltk.grammar.Production(nt,t)
                        g._productions.append(p)
        # save grammar to self.cfg
        self.cfg = CFG.fromstring(str(g).split('\n')[1:])
        self.cfg._start = g.start()     

    def gen_random(self, nt):
        sentence = ''
        prods = random.sample(self.cfg.productions(lhs=nt),len(self.cfg.productions(lhs=nt)))
        valid = True
        for prod in prods:
            valid = True
            for sym in prod.rhs():
                if is_nonterminal(sym):
                    if len(self.cfg.productions(lhs=sym)) < 1:
                        valid = False
            if valid == True:
                for sym in prod.rhs():
                    if is_nonterminal(sym):
                        sentence += self.gen_random(sym)
                    else:
                        sentence += sym + ' '
                break
        if valid == False:
            return "sentence could not be generated"
        else:
            #list = sentence.split(' ')
            #list[0] = list[0].title()
            #sentence = ' '.join(list)
            return sentence.capitalize()    

if __name__== "__main__":
    #text = input('Enter text: ')
    file = open('Alice.txt','r+')
    text = file.read()
    text_array = nltk.word_tokenize(text)
    dictionary = Dictionary(text_array)
    grammar = Grammar(dictionary)
    print(dictionary.grammar)
    print(grammar.cfg.productions())

    print()
    for x in range(0,12):
        print(grammar.gen_random(Nonterminal('S')))
