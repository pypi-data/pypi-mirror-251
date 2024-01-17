from .ekz_data import Tasks
from fuzzywuzzy import fuzz, process
import pyperclip


data = Tasks.data
datalst = []
for Q, nums in data.items():
    for num, v in nums.items():
        datalst.append(f"{num};; {v[0]};; {v[1]}")


def find(s, number=0, clip=True, find_all=False, limit=5):
    '''
    s:str - строка для поиска
    number:int - номер по порядку для вывода ответа
    clip:bool - буфер
    find_all:bool - вопрос + ответ
    limit:int - кол-во результатов в поиске'''
    ans = process.extract(s, datalst, scorer=fuzz.partial_ratio, limit=limit)
    ans = sorted(ans, key=lambda x: x[1], reverse=True)
    answer = ans[number][0]
    if find_all:
        answer = answer[answer.find(';;') + 3:].replace(';;', '''

**Ответ**
<br>
''')
    else:
        answer = answer[answer.rfind(';;') + 3:]

    if clip:
        pyperclip.copy(answer)

    return type("TempClass", (), {"__doc__": answer})()
