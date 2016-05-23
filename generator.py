import nltk
from nltk.data import load
from nltk import CFG
from nltk.parse.generate import generate
from nltk.grammar import Nonterminal, Production, is_nonterminal
import random
import re
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.corpus import stopwords

class Text:
    def __init__(self,raw_text):
        self.text_array = nltk.word_tokenize(raw_text)
        self.POS_buckets = {}
        tagged_text_array = nltk.pos_tag(self.text_array)
        self.tags = load('help/tagsets/upenn_tagset.pickle')
        for tag in self.tags:
            self.POS_buckets[tag] = []
        for tuple in tagged_text_array:
            self.POS_buckets[tuple[1]].append(tuple[0].lower())
        self.before = {}
        self.after = {}
        for word in self.text_array:
            self.before[word] = []
            self.after[word] = []
        for i in range(len(self.text_array)): #range goes to one less than given value
            if i > 0:
                self.before[self.text_array[i]].append(self.text_array[i-1])
            if i < len(self.text_array)-1:
                self.after[self.text_array[i]].append(self.text_array[i+1])

    # return list of two word collocation lists
    def get_collocations(self):
        ignored_words = stopwords.words('english')
        finder = BigramCollocationFinder.from_words(self.text_array,2)
        finder.apply_freq_filter(3)
        finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
        bigram_measures = BigramAssocMeasures()
        return finder.nbest(bigram_measures.likelihood_ratio,40)

class Grammar:

    def __init__(self):
        
        #comment about what each part of speach is:
        """ CC   - conjunction: or, but, and, either
            CD   - number: one, two, three
            DT   - determiner: a, an, the, both, all, these, any, some
            EX   - the word 'there'
            IN   - preposition: in, of, with, for, under, among, upon, at
            JJ   - adjective: certain, curious, little, golden, other, offended
            JJS  - adjective: -est : best, loveliest, largest
            JJR  - adjective: -er : lerger, smaller, worse
            MD   - can, dare, should, will*, might, could, must
            NN   - common singular noun
            NNS  - common plural noun
            NNP  - proper singular noun
            NNPS - proper plural noun
            PDT  - all, both, quite, many, half
            PRP  - hers, her, himself, thy, us, it, I, him, you, they
            PRPP - possesive: his, mine, our, my, her, its, your
            RB   - adverb: very, not, here, there, first, just, down, again, beautifully, -ly
            RBR  - more
            RBS  - adverb superlative: -est
            RP   - participle: up, down, out, away, over, off
            TO   - the word 'to'
            UH   - interjection
            VB   - vocative verb: to ___ 
            VBD  - past verb: -ed : was*(freq. occur), had, dipped, were, said, seemed
            VBG  - present verb: -ing: trembling, trying, getting, running, swimming
            VBN  - past verb descriptive: crowded, mutated, fallen, lit, lost, forgtten
            VBP  - present verb: not -s: am, wish, make, know, do, find
            VBZ  - present verb: -s : is*, has, seems
            WDT  - what, which, that*
            WP   - who, what
            WRB  - how, whenever, where, why, when
        """

        # create base of cfg
        g = CFG.fromstring("""
            S -> NPS VPS | NPS VPS | NPS VPS | NPP VPP | VPO | NPO
            S -> NPS VPS | NPP VPP | NPS VPS

            NPS -> 'DT' 'NN' | 'DT' 'NN' | 'DT' 'JJ' 'NN' | 'DT' 'JJ' 'NN'
            NPS -> 'EX' 'the' 'NN' | 'the' 'JJS' 'NN'
            NPS -> 'she' | 'he' | 'it' | 'I'
            NPS -> NPS INP | INP NPS

            NPP -> 'the' 'NNS' | 'the' 'NNS' | 'NNS'
            NPP -> 'the' 'JJ' 'NNS'
            NPP -> 'they' | 'you' | 'we'

            VING -> 'VBG' | 'VBG' | 'RB' 'VBG'
            VBB -> 'VB' | 'VB' | 'VBP' 

            SM -> 'is' | 'was' | 'has been'

            VPS -> SM 'VBN' | SM 'VBN' 'like the' 'JJ' 'NN'
            VPS -> SM VING | SM VING INP
            VPS -> SM VING 'like' 'DT' 'JJ' 'NN'
            VPS -> SM VING 'like a' 'NN' INP
            VPS -> SM 'as' 'JJ' 'as' 'JJ'
            VPS -> SM 'a' 'JJ' 'NN'
            VPS -> SM 'a' 'NN' INP
            VPS -> 'MD' 'have been' VING
            VPS -> 'is' 'JJ' 'and' 'JJ'
            VPS -> 'VBD' INP | 'RB' 'VBD'
            VPS -> SM 'VBD' 'like' 'DT' 'JJ' 'NN'
            VPS -> SM 'as' 'JJ' 'as the' 'NN'
            VPS -> 'VBD' 'NN' | 'VBD' 'DT' 'NN'
            VPS -> 'VBD' 'and' 'VBD' INP 'until' 'VBN'
            VPS -> VPS 'and' S
            VPS -> 'VBD' 'JJR' 'than' 'a' 'NN'
            VPS -> 'VBD' 'EX'
            VPS -> SM 'JJ' | 'SM' 'VB' INP

            NPO -> 'a' 'NN' 'IN' 'NNP'
            NPO -> 'the' 'NN' 'IN' 'the' 'JJ' 'NNP'
            NPO -> 'the' 'NNS' 'IN' 'the' 'NN'

            VPO -> 'VBG' 'like' 'NNP' 'RP' 'DT' 'JJ' 'NN' 'IN' 'DT' 'NN'
            VPO -> 'has been' 'VBG' 'RP' 'and' 'VBG'
            
            PM -> 'are' | 'were' | 'have been'

            VPP -> PM VING | PM VING INP
            VPP -> PM VING 'like the' 'NNS' INP
            VPP -> PM 'as' 'JJ' 'as' NPS INP | PM 'JJ' 'like' 'NNS' | PM 'JJ' 'like' VBG 'NNS'
            VPP -> PM 'VBN' | PM 'VBN' INP
            VPP -> PM 'as' 'JJ' 'as' 'JJ' | PM 'as' 'JJ' 'as' 'VBG' 'NNS'
            VPP -> PM 'NNS' INP
            VPP -> PM 'JJ' 'NNS'
            VPP -> 'are' 'JJ' 'and' 'JJ'
            VPP -> 'VBD' INP | 'VBD' 'RP' INP
            VPP -> PM 'JJ' | PM 'VB' INP
            
            INP -> 'IN' 'DT' 'NN' | 'IN' 'the' 'NNS' | 'IN' 'the' 'JJ' 'NNS'
            INP -> 'IN' 'DT' 'NN' 'IN' 'DT' 'NN'
            INP -> 'IN' 'DT' 'JJ' 'NN' | 'RP' 'IN' 'DT' 'JJ' 'NN'
            INP -> 'RP' 'IN' 'DT' 'NN' | 'IN' 'JJ' 'NNS'
            INP -> 'IN' 'DT' 'NN' | 'RP' 'DT' 'NNS'
            """)

        # save grammar to self.cfg
        self.cfg = CFG.fromstring(str(g).split('\n')[1:])
        self.cfg._start = g.start()       

    def gen_frame_line(self, nt):
        sentence = ''
        prods = random.sample(self.cfg.productions(lhs=nt),len(self.cfg.productions(lhs=nt)))
        valid = True
        for prod in prods:
            #valid = True
            for sym in prod.rhs():
                if is_nonterminal(sym):
                    if len(self.cfg.productions(lhs=sym)) < 1:
                        valid = False
            if valid == True:
                for sym in prod.rhs():
                    if is_nonterminal(sym):
                        sentence += self.gen_frame_line(sym)
                    else:
                        sentence += sym + ' '
                break
        if valid == False:
            return "ERROR"
        else:
            return sentence #removed capitalize

class Spot:

    def __init__(self,wop,line,column,content):
        if content == 'POS':
            self.word = ''
            self.POS = wop
            self.line = line
            self.column = column
            self.filled = False
            self.preset = False
        elif content == 'word':
            self.word = wop
            self.POS = ''
            self.line = line
            self.column = column
            self.filled = True
            self.preset =  True
        else:
            print("spot content error")

    def fill(self,word):
        self.word = word
        self.filled = True

    def add_POS(self,pos):
        self.POS = pos

class Frame:

    def __init__(self,grammar,tags):
        self.lines = []
        repeat_line_array = nltk.word_tokenize(grammar.gen_frame_line(grammar.cfg.start()))
        x = random.randint(0,8)
        y = random.randint(0,8)
        for i in range(8):
            if (i == x or i == y):
                spot_array = []
                j = 0
                noun_set = set(['he','she','it','I'])
                for wop in repeat_line_array:
                    if wop in set(tags):
                        spot = Spot(wop,i,j,'POS')
                        if (wop in noun_set):
                            spot.add_POS('NN')
                        spot_array.append(spot)
                    else:
                        spot = Spot(wop,i,j,'word')
                        spot_array.append(spot)
                    j += 1
                self.lines.append(spot_array)
            else:
                line_array = nltk.word_tokenize(grammar.gen_frame_line(grammar.cfg.start()))
                spot_array = []
                j = 0
                for wop in line_array:
                    if wop in set(tags):
                        spot = Spot(wop,i,j,'POS')
                        spot_array.append(spot)
                    else:
                        spot = Spot(wop,i,j,'word')
                        spot_array.append(spot)
                    j += 1
                self.lines.append(spot_array)
        

    def add_collocations(self,text):
        collocations = text.get_collocations()
        tagged_collocation_list = []
        for collocation in collocations:
            tagged_collocation_list.append(nltk.pos_tag(collocation))
        for tagged_collocation in tagged_collocation_list:
            POS_pair = [tagged_collocation[0][1], tagged_collocation[1][1]]
            word_pair = [tagged_collocation[0][0], tagged_collocation[1][0]]
        j = 0
        collocation_used = False
        for line in self.lines:
            if collocation_used == False:
                for i in range(len(line)-1): # 0 to line.length-2
                    if POS_pair == [line[i],line[i+1]]:
                        line[i].fill(word_pair[0])
                        line[i+1].fill(word_pair[1])
                        collocation_used = True
                        break
                j += 1

    def add_big_words(self,text):
        fdist = nltk.FreqDist(text.text_array)
        big_words = []
        for w in set(text.text_array):
            if len(w) > 6 and fdist[w] > 2:
                big_words.append(w)
        big_words_with_tags = nltk.pos_tag(big_words)
        big_word_buckets = {}
        for tag in text.tags: # initialize list of words for each tag
            big_word_buckets[tag] = []
        for big_word_tuple in big_words_with_tags:
            big_word_buckets[big_word_tuple[1]].append(big_word_tuple[0])
        used_words = []
        for line in self.lines:
            for spot in line:
                if spot.filled == False and len(big_word_buckets[spot.POS]) > 0:
                    n = random.randint(0,len(big_word_buckets[spot.POS])-1)
                    big_word = big_word_buckets[spot.POS][n]
                    if big_word in set(used_words):
                        pass
                    else:
                        spot.fill(big_word)
                        used_words.append(big_word)

    def repeat_nouns(self):
        noun = ''
        for spot in self.lines[0]:
            if spot.POS == 'NN' and spot.filled == True:
                noun = spot.word
                break
        if noun == '': return
        for i in range(1,8):
            for spot in self.lines[i]:
                if spot.POS == 'NN' and spot.filled == False:
                    spot.fill(noun)
                    break

    def add_context_words(self,text):
        for line in self.lines:
            for spot in line:
                if spot.filled == True:
                    if spot.column > 0 and line[spot.column-1].filled == False and spot.preset == False:
                        for before_word in text.before[spot.word]:
                            if line[spot.column-1].POS == nltk.pos_tag([before_word])[0][1]:
                                line[spot.column-1].fill(before_word)
                                break
                    if spot.column < len(line)-1 and line[spot.column+1].filled == False and spot.preset == False:
                        for after_word in text.after[spot.word]:
                            if line[spot.column+1].POS == nltk.pos_tag([after_word])[0][1]:
                                line[spot.column+1].fill(after_word)
                                break

    def add_random(self,text):
        while(True):
            x = random.randint(0,8)
            y = random.randint(0,len(self.lines[x]))
            spot = self.lines[x][y]
            if spot.filled == False:
                n = random.randint(0,len(text.POS_buckets[spot.POS])-1)
                word = text.POS_buckets[spot.POS][n]
                spot.fill(word)
                return

    def add_first_unfilled(self,text):
        for line in self.lines:
            for spot in line:
                if spot.filled == False:
                    n = random.randint(0,len(text.POS_buckets[spot.POS])-1)
                    word = text.POS_buckets[spot.POS][n]
                    spot.fill(word)
                    break

    def fill_remaining(self,text):
        for line in self.lines:
            for spot in line:
                if spot.filled == False:
                    n = random.randint(0,len(text.POS_buckets[spot.POS])-1)
                    word = text.POS_buckets[spot.POS][n]
                    spot.fill(word)

    def print(self):
        for line in self.lines:
            for spot in line:
                if spot.filled == True:
                    print(spot.word,end=" ")
                else:
                    print(spot.POS,end=" ")
            print()
        print()



if __name__== "__main__":
    file = open('input.txt','r+')
    raw_text = file.read() # gets file contents as string
    text = Text(raw_text) # seperates words into POS buckets
    grammar = Grammar() # makes CFG

    frame = Frame(grammar,text.tags) # create "frame" of poem: list of lists of POS tags
    frame.add_collocations(text)
    frame.add_big_words(text)
    frame.repeat_nouns()
    for x in range(3):
        frame.add_context_words(text)
    frame.add_first_unfilled(text)
    frame.repeat_nouns()
    frame.add_context_words(text)
    frame.fill_remaining(text)

    frame.print()

