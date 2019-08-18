"""
Convert Aiken question into Stepik dict.

The Aiken format is a very simple way of creating multiple choice questions using a clear human-readable format in a text file. 
https://docs.moodle.org/37/en/Aiken_format
* You have to save the file in a text format. Don't save it as a Word document or anything like that.
* Non-ASCII characters like 'quotes' can cause import errors. To avoid this always save your text file in UTF-8 format (most text editors, even Word, will ask you).
* The answer letters (A,B,C etc.) and the word "ANSWER" must be capitalised as shown below, otherwise the import will fail.

What is the correct answer to this question?
A. Is it this one?
B. Maybe this answer?
C. Possibly this one?
D. Must be this one!
ANSWER: D

"""


import copy
from enum import Enum
import markdown
import re


api_url = 'https://stepik.org/api/step-sources'
data_template = {
	'stepSource': {
		'block': {
			'name': 'choice',
			'text': 'Pick one!',                # question text in html
			'source': {
				'options': [],                  # add answer variants here, use option_template
				'is_always_correct': False,     
				'is_html_enabled': True,
				'sample_size': 0,               # len of 'options' list
				'is_multiple_choice': False,
				'preserve_order': False
			}
		},
		'lesson': None,
		'position': None
	}
}
option_template = {'is_correct': False, 'text': '2+2=3', 'feedback': ''}

class Status(Enum):
    QUESTION = 0
    VARIANT = 1
    ANSWER = 3
    
def html(text_md):
    if not isinstance(text_md, str):               # list of strings
        text_md = '\n'.join(text_md)
    return markdown.markdown(text_md, extensions=['extra', 'codehilite']) 

def commit_variant(source, variant_text):
    opt = source['block']['source']['options']  
    opt.append({'is_correct': False, 'text': html(variant_text), 'feedback': ''})    

def aiken_to_stepik(text):
    letter_seq = []             # letter sequence from aiken variant, A, B, C, D, etc
    md_part = []                
    status = Status.QUESTION
    data = copy.deepcopy(data_template)
    source = data['stepSource']
    
    for line in text.splitlines():
        
        # variant begin by A) or A.
        m = re.match('(\s*)([A-Z])([.)])(.*)', line)
        if m:
            letter = m.group(2)
            sep = m.group(3)
            txt = m.group(4)
            if status == Status.QUESTION:
                # first answer begin, question end
                status = Status.VARIANT
                source['block']['text'] = html(md_part)
            elif status == Status.VARIANT:
                # next variant, commit previous variant
                commit_variant(source, md_part)
            md_part = [txt]
            letter_seq.append(letter)
        else:
            m_answer = re.match('\s*ANSWER:\s*([A-Z])\s*', line)
            if m_answer and status == Status.VARIANT:
                # end of question
                commit_variant(source, md_part)

                letter == m_answer.group(1)
                ind = letter_seq.index(letter)
                source['block']['source']['options'][ind]['is_correct'] = True
                source['block']['source']['sample_size'] = len(letter_seq)
                return data
            else:
                # continue a question or answer
                md_part.append(line)


if __name__ == '__main__':
    text = '''
What is the correct answer to this question?
A. Is it this one?
B. Maybe this answer?
C. Possibly this one?
D. Must be this one!
ANSWER: D
    '''
    res = aiken_to_stepik(text)
    print(res)