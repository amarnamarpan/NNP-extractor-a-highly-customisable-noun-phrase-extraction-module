# Use the start() method to extract the noun phrases and ensure that the nltk is installed


import nltk
from nltk.tag import pos_tag
from nltk.stem import *
from nltk.corpus import stopwords

def my_tokenizer(text,gram,legal_stopwords):
	for i in range(len(legal_stopwords)):
			legal_stopwords[i] = legal_stopwords[i].lower()
	text = text.replace('-\n','')
	text = text.replace('.',' ')
	text = text.replace(',',' ')
	text = text.replace('-',' ')
	text = text.lower()
	maxind=5
	ind=0
	while(ind<maxind):
		text=text.replace('  ',' ')
		ind+=1
	lines=text.split('\n')
	fin_unigrams=[]
	for line in lines:
		unigrams=line.split(' ')
		for unigram in unigrams:
			if (unigram in legal_stopwords):
				continue
			if all(c.isalpha() for c in unigram):
				fin_unigrams.append(unigram)
	if '' in unigrams:
		unigrams=unigrams.remove('')
	n_grams=[]
	ind=0
	maxind=len(fin_unigrams)
	while(ind<=maxind-gram):
		ctr=0
		n_gram=[]
		while(ctr<gram):
			n_gram.append(fin_unigrams[ind+ctr])
			ctr+=1
		n_grams.append(' '.join(n_gram))
		ind+=1
	return n_grams


def my_tokenizer1(text):
	sentences=[]
	exception_list=[' ','\n','-']
	new_text=''
	dot_count = text.count('.')
	#reading the text and keeping those dots that correspond to a full stop only
	curr_pos=0
	chk_range=5
	for letter in text:
		if letter=='.':
			not_in_range=True
			st_point=curr_pos-chk_range
			if st_point<0:
				st_point=0
			chk_text=text[st_point:curr_pos+chk_range]
			if chk_text.count('.')==1:
				chk_text = chk_text.replace('.',' ')
				for lt in chk_text:
					if not(lt.isalpha() or lt.isdigit() or lt in exception_list):
						not_in_range = False
			else:
				not_in_range = False
			if not_in_range:
				new_text += '.'
		else:
			new_text += letter
		curr_pos+=1
	sentences = [i.strip() for i in new_text.split('.')]
	for i in range(dot_count):
		if '' in sentences:
			sentences.remove('')
	n_sents=[]
	for sent in sentences:
		n_sents.append(my_tokenizer(sent,1,['']))
	return n_sents

def leaves(tree,target_tag):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label() == target_tag):
        #print subtree
        #print '***'
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    #word = stemmer.stem_word(word)
    #word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    stopwords=[]
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted


def get_terms(tree,target_tag):
    terms=[]
    for leaf in leaves(tree,target_tag):
        #term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        term = [ w for w,t in leaf if acceptable_word(w) ]
        terms.append(term)
    return terms

def post_process(phrases_list):
	new_list=[]
	text='\n'.join(phrases_list)
	determiners_list = open('list_of_determiners_from_wikipedia_page.txt','r').read().split('\n')
	text = '\n'+text
	for det in determiners_list:
		text=text.replace('\n'+det.lower()+' ','\n')
	new_list = text.split('\n')
	new_list.remove('')
	return new_list

def get_special_ppfied_phrases(NP6_terms):
	
	PP_tags=['IN','TO']
	actual_terms=[]
	actual_pos_lst=[]
	max_pps_lst=[1,2]
	
	while '' in NP6_terms:
		NP6_terms.remove('')
	
	#taking out the preceding prepositions if any in case of PP2 terms
	fin_terms=[]
	for term in NP6_terms:
		toks = my_tokenizer(term,1,[''])
		postoks = nltk.tag.pos_tag(toks)
		ctr=0
		prev_tag=postoks[0][1]
		#print prev_tag
		do_append = True
		if prev_tag in PP_tags:
			do_append=False
		
		formed_term=''
		for pos_tok in postoks:
			if do_append==False and not(pos_tok[1] in PP_tags):
				do_append=True
			if do_append:
				formed_term+=' '+pos_tok[0]
			
		fin_terms.append(formed_term.strip())
	NP6_terms=fin_terms
	for term in NP6_terms:
		actual_pos=[]
		no_of_pps=0
		toks = my_tokenizer(term,1,[''])
		postoks = nltk.tag.pos_tag(toks)
		prev_tag='NN'
		formed_term=''
		for pos_tok in postoks:
			if pos_tok[1] in PP_tags:
				if prev_tag=='PP':
					formed_term+=(' '+pos_tok[0])
					formed_term=formed_term.strip()
					prev_tag='PP'
				else:
					actual_pos.append((formed_term,'NN'))
					formed_term=pos_tok[0]
					prev_tag='PP'
			else:
				if prev_tag=='NN':
					formed_term+=(' '+pos_tok[0])
					formed_term=formed_term.strip()
					prev_tag='NN'
				else:
					actual_pos.append((formed_term,'PP'))
					no_of_pps+=1
					formed_term=pos_tok[0]
					prev_tag='NN'
		actual_pos.append((formed_term,prev_tag))
		actual_pos_lst.append(actual_pos)
		
		for max_pps in max_pps_lst:
			if not (max_pps<=no_of_pps):
				continue
			for i in range((no_of_pps+1)-max_pps): # this iterates the loop over the number of possible NN phrases with corresponding max_pps
				ctr=0		# stores the count of PP tags encountered
				index=i*2
				new_term=''
				for term in actual_pos:
					if i <= ctr and ctr < (max_pps+i):
						new_term+=' '+term[0]
						index+=1		#The valid terms are appended to form the NN phrases
					if term[1]=='PP':
						ctr+=1
					
				new_term+=' '+actual_pos[index][0]
				actual_terms.append(new_term)
	
	return actual_terms

def form_grammar(line):
	line='NP:{<'+line+'>}'
	line=line.replace(' ','><')
	return line

def start(text, legal_stopwords=[]):
	det_lst=[]
	lemmatizer = nltk.WordNetLemmatizer()
	stemmer = nltk.stem.porter.PorterStemmer()
	for i in range(len(legal_stopwords)):
		legal_stopwords[i] = legal_stopwords[i].lower()
	#Adding english stopwords from nltk corpus
	legal_stopwords=legal_stopwords + stopwords.words('english') ##Uncomment if you want to remove stopwords
	grammars=[]
	grammar="""
	N1:		{<NN|NNS>}
	AD0:	{<JJ|VBD|VBN|VBG>}
	ADV:	{<RB|RBS|RBR>}
	ADJ:	{<ADV>*<AD0>}
	ADJ1:	{<ADJ><CC>?<ADJ>}
	NP1:	{<N1>+}
	NP2:	{<DT><NP1>}
	NP4:	{<ADJ1|ADJ><NP2|NP1>}
	NP5:	{<DT>?<NP4|NP1>}
	NP35:	{<CC><NP5>}
	NP3:	{<NP5><NP35>?}
	PP1:	{<IN|TO>+<NP1|NP2|NP3|NP4|NP5>}
	PP2:	{<PP1>+<PP1>}
	NP6:	{<NP1|NP2|NP3|NP4|NP5><PP1|PP2>}
	"""
	grammars.append(grammar)
	actual_terms = []
	sentences=[]
	for text in text.split('\n\n'):
		sentences += my_tokenizer1(text)
	while [] in sentences:
		sentences.remove([])
	
	for grammar in grammars:
		for toks in sentences:
			terms_for_this_loop=[]
			postoks = nltk.tag.pos_tag(toks)
			chunker = nltk.RegexpParser(grammar)
			tree = chunker.parse(postoks)
			target_tags=['NP','NP1','NP2','NP3','NP4','NP5','NP6','N1']
			for target_tag in target_tags:
				terms = get_terms(tree, target_tag)
				for term in terms:
					terms_for_this_loop.append(' '.join(term))
			special_tags=['NP6','PP2']
			for n_tag in special_tags:
				temp_terms = get_terms(tree,n_tag)
				pass_term=[]
				for each in temp_terms:
					pass_term.append(' '.join(each))
				temp_terms = pass_term
				temp_terms = get_special_ppfied_phrases(temp_terms)
				terms_for_this_loop = terms_for_this_loop + temp_terms
			NN_NNS_list=[]
			VBN_VBG_list=[]
			for tok in postoks:
				if (tok[1]=='NN') or (tok[1]=='NNS'):
					NN_NNS_list.append(tok[0])
				elif (tok[1]=='VBN') or (tok[1]=='VBG'):
					VBN_VBG_list.append(tok[0])
			n_terms=[]
			for term in terms_for_this_loop:
				if len(term.split(' '))==1:
					if (term in NN_NNS_list) or (term in VBN_VBG_list):
						n_terms.append(term)
				else:
					flag=False
					for NN in NN_NNS_list:
						if NN in term:
							flag=True
					if flag:
						n_terms.append(term)
			terms_for_this_loop = n_terms
			actual_terms += terms_for_this_loop
	actual_terms=list(set(actual_terms))
	for i in range(3):
		actual_terms = post_process(actual_terms)
	actual_terms=list(set(actual_terms))
	actual_terms.sort()
	st_removed=[]
	for term in actual_terms:
		if not (term in legal_stopwords):
			st_removed.append(term)
	
	actual_terms=[]
	for term in st_removed:
		term1=' '+term+'$$'
		okay = True
		for st in legal_stopwords:
			if (' '+st+'$$' in term1):
				okay=False
		if okay:
			actual_terms.append(term)
	return actual_terms

