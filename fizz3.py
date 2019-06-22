# Interactive python client for fizzbot

import json
import urllib.request
import urllib.error
import requests

domain = 'https://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })

    print('*** POST %s %s' % (question_url, body))
    try:
        req = requests.post(domain + question_url, json=({'answer': answer}))
        # req = urllib.request.Request(domain + question_url, data=body.encode('utf8'), headers={'Content-Type': 'application/json'})
        # res = urllib.request.urlopen(req)
        response = req.json()
        print_response(response)
        print_sep()
        return response

    except urllib.error.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

def fizzbuzz(numbers, rules):
    answer = []
    for num in numbers:
        # if num == 0:
        #     answer.append("0")
        #     continue

        temp = ""
        for rule in rules:
            fact, resp = rule['number'], rule['response']
            if num % fact == 0:
                temp += resp
        if temp:
            answer.append(temp)
        else:
            answer.append(str(num))

    return " ".join(answer)

# keep trying answers until a correct one is given
def get_correct_answer(question_url, rules, nums):
    while True:


        if question_url.split('/')[-1] == "1":
            answer = 'COBOL'
            response = try_answer(question_url, answer)
        else:
            # do FizzBuzz code
            answer = fizzbuzz(nums, rules)
            print(answer)
            response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        elif (response.get('result') == 'correct'):
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)

    request = urllib.request.urlopen( ('%s%s' % (domain, question_url)) )
    question_data = json.load(request)
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    rules = question_data.get('rules')
    nums = question_data.get('numbers')
    print(rules, nums)
    if next_question:
        return next_question

    return get_correct_answer(question_url, rules, nums)


def main():
    question_url = '/fizzbot'
    while question_url:
        question_url = do_question(domain, question_url)

if __name__ == '__main__': main()
