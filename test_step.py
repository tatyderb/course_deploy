"""
Test function to update stepik steps.
"""
from stepik import fetch_objects, fetch_object
from step import Step #, put_step_dict

import re

course_id = 55690

expected_lesson_ids = [239930, 239927, 239366, 239929]
expected_step_ids = [761415, 770595, 781288]                            # for lesson = 239930

expected_step_text='<p>Lesson 239930, step 761415. Don\'t change it!</p>'

def test_get_lesson_ids(course_id=course_id, expected=expected_lesson_ids):
    print('----- test_get_lesson_ids')
    course = fetch_object('course', course_id)
    sections = fetch_objects('section', course['sections'])

    unit_ids = [unit for section in sections for unit in section['units']]
    units = fetch_objects('unit', unit_ids)

    lesson_ids = [unit['lesson'] for unit in units]
    print('lesson_ids =', lesson_ids)
    
    assert(lesson_ids == expected)
    return lesson_ids
    
def test_get_step_ids(lesson_id=expected_lesson_ids[0], expected=expected_step_ids):
    print('----- test_get_step_ids')
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    print(f'lesson = {lesson_id} -> steps={step_ids}')
    
    assert(step_ids == expected)
    return step_ids
    
def test_get_step(step_ids, ind=0, expected=expected_step_text):
    print('----- test_get_step')
    step_id = step_ids[ind]
    st = Step.get(step_id)
    print('TEXT =', st.text)
    
    assert(st.text == expected)
    return st, ind + 1
    
def text_next_counter(text):
    m = re.search(r'\d+', text)
    # if m:
        # print('Number')
    # else:
        # print('No match')
        
    x = int(m.group())
    # print(x)
    new_text = re.sub(r'\d+', str(x+1), text)
    # print('From: ', text)
    # print('To   :', new_text)
    return new_text
    
def test_step_update(step_ids, ind=0):
    """ get text, increase counter++, put text with new counter"""
    print('----- test_step_update: TEXT')
    text_step_id = step_ids[ind]
    st = Step.get(text_step_id)
    new_text = text_next_counter(st.text)
    st.update(new_text)
    
    stu = Step.get(text_step_id)
    assert(st == stu)
    
    print('----- test_step_update: QUIZ')
    print('Not implemented yet')
    return st, ind + 1
    
    
    
   

'''
less_id = 239930
step_id = 761415 

# "create_date":"2019-06-26T05:01:47.000Z"
modification_time = strftime("%Y-%m-%dT%H:%M:%S.000Z", gmtime())
resp = get_step_text(less_id, step_id)
print(resp)
print(resp['step-sources'][0]['block'])
print('TEXT =', resp['step-sources'][0]['block']['text'])

put_step_text(less_id, step_id, f'Lesson {less_id}, step {step_id} has been modified at {modification_time}')
resp = get_step_text(less_id, step_id)
print('TEXT =', resp['step-sources'][0]['block']['text'])
 
exit(0)
'''


def test_step_push(lesson_id, text='New step by scripts'):
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    position = len(step_ids) + 1
    step = Step()
    step.lesson_id = lesson_id
    step.position = position
    step.text = text

    id = step.create()
    assert(id == step.id)

    st1 = step.get(id)
    assert(st1.text == text)
    assert(step == st1)

    return id


def test_step_pop(lesson_id):
    step_ids = Step.get_step_ids_for_lesson(lesson_id)
    st = Step.get(step_ids[-1])
    st.delete()
    step_ids_del = Step.get_step_ids_for_lesson(lesson_id)
    assert (step_ids_del == step_ids[:-1])


if __name__ == '__main__':
    update_test = True
    add_delete_test = True

    lesson_ids = test_get_lesson_ids()
    lesson_id = lesson_ids[0]

    if update_test:
        step_ids = test_get_step_ids(lesson_id)
        indx = 0

        # first step - test get
        resp, indx = test_get_step(step_ids, indx)

        # next steps - test update text, test, ....
        text_step_id = step_ids[indx]
        question_step_id = step_ids[indx]
        indx = test_step_update(step_ids, indx)

    if add_delete_test:
        expected_text = 'Popped step'
        id = test_step_push(lesson_id, expected_text)   # add last
        test_step_push(lesson_id, 'TO BE DELETED')      # add last for pop

        test_step_pop(lesson_id)                        # delete last

        step_ids = Step.get_step_ids_for_lesson(lesson_id)
        assert(id == step_ids[-1])

        st = Step.get(id)
        assert (st.text == expected_text)

