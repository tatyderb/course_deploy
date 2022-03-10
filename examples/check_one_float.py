def get_word_seq(text):
    return text.split()
    

def check_float_seq(reply, clue, EPS=0.0001):
    try:
        reply_data = [float(x) for x in get_word_seq(reply)]
        clue_data = [float(x) for x in get_word_seq(clue)]
    except ValueError:
        return False, f'\nERROR: Only numbers are expected\nYou answer was: \n{reply}\nCorrect answer was: \n{clue}\n'

    reply_len = len(reply_data)
    clue_len = len(clue_data)
    res = True
    diff = ''
    if reply_len != clue_len:
        res = False
        diff = f'Answer = {reply_len} numbers, expected = {clue_len} numbers'
    else:
        i = 0
        for x, y in zip(reply_data, clue_data):
            i += 1
            if abs(x - y) > EPS:
                diff = f"Diff at {i}-th number: answer=<{x}>, expected=<{y}> accuracy={EPS}"
                res = False
                break
    feedback = f"\nYou answer was: \n{reply}\nCorrect answer was: \n{clue}\n{diff}\n"
    return res, feedback  # feedback will be shown to the learner

def check(reply, clue):
    return check_float_seq(reply, clue)


print(check("3.9999999999999964 1.9999999999999991", "3.9999999999999964 1.9999999999999991"))

print(check("3.9999999999999965 1.9999999999999991", "3.9999999999999964 1.9999999999999991"))

print(check("3.4999999999999964 1.9999999999999991", "3.9999999999999964 1.9999999999999991"))

print(check("3.9999999999999964 Text", "3.9999999999999964 1.9999999999999991"))