# TOKENS
from os import startfile
from unittest import skip


T_PYSCRIPT = 'ㄴ'
T_END = '동네사람들'
T_BREAK = '멈춰!'
T_RETURN = '무야호'
T_PRINT = '물어본사람'
T_PRINTALT = '물어본사람손'
T_INPUT = '안물'
T_IF = 'ㄹㅇ'
T_FOR = '묻고'
T_FUNC = '응~ 저쩔'
T_VAR = '어쩔'
T_DEF = '저쩔'
T_IS1 = '는 '
T_IS2 = '은 '
T_STR = '문자'
T_INT = '숫자'
T_MUL = '곱하기'
T_DIV = '나누기'
T_PLUS = '더하기'
T_MINUS = '빼기'
T_EQUALS = '¯\_(ツ)_/¯'
T_LARGER = '( ﾉ ﾟｰﾟ)ﾉ'
T_LARGERSAME = '(☞ﾟヮﾟ)☞'
T_REPEAT = '누구인가'

#변수
variables = {}

#반복 [시작줄, 남은반복횟수, 총반복횟수]
loop = []

#함수 {이름: 시작줄}
func = {}

#함수 실행 실행줄 저장
startFunc = []

#토큰 찾기
def get_type(c):

    if T_END in c:
        return 'END'

    if T_PYSCRIPT in c:
        return 'PYSCRIPT'

    if T_BREAK in c:
        return 'BREAK'
    if T_RETURN in c:
        return 'RETURN'

    if T_PRINTALT in c:
        return 'PRINTALT'
    if T_PRINT in c:
        return 'PRINT'
    if T_INPUT in c:
        return 'INPUT'
    if T_IF in c:
        return 'IF'
    if T_FOR in c:
        return 'FOR'

    if T_VAR in c:
        return 'VAR'
    if T_FUNC in c:
        return 'FUNC'
    if T_DEF in c:
        return 'DEF'

    if T_IS1 in c or T_IS2 in c:
        return 'IS'

    if T_MUL in c:
        return 'MUL'
    if T_DIV in c:
        return 'DIV'
    if T_PLUS in c:
        return 'PLUS'
    if T_MINUS in c:
        return 'MINUS'

    if T_EQUALS in c:
        return 'EQUALS'
    if T_LARGER in c:
        return 'LARGER'
    if T_LARGERSAME in c:
        return 'LARGERSAME'

    if T_STR in c:
        return 'STR'
    if T_INT in c:
        return 'INT'

    if T_REPEAT in c:
        return 'RPT'
    
    return 'NONE'

class Meme:
    def __init__(self, code):
        self.code = code
        self.skip = False

    def transfer_type(self, c):
        if get_type(c) == 'INT':
            return int(c.replace(T_INT,'').strip())
        elif get_type(c) == 'STR':
            return c.replace(T_STR,'')
        elif get_type(c) == 'RPT':
            cnt = c.strip().count('누구')-1
            return loop[cnt][2]-loop[cnt][1]
        elif get_type(c) == 'NONE':
            return variables[c.strip()]

    def compile_line(self, c, index):
        if c == '':
            return None
        Token = get_type(c)

        if Token == 'END':
            self.skip = False
            if len(loop) != 0:
                loop[len(loop)-1][1] -= 1
                if loop[len(loop)-1][1] <= 0:
                    loop.pop()
                    return None
                else:
                    return loop[len(loop)-1][0]
        
        if self.skip:
            return None

        if Token == 'PYSCRIPT':
            c = c[1:-1]
            execCode = compile(c, 'mulstring', 'exec')
            exec(execCode)

        if Token == 'BREAK':
            loop[len(loop)-1][1] = 0
            self.skip = True
        if Token == 'RETURN':
            l = startFunc[len(startFunc)-1]
            startFunc.pop()
            return l
        if Token == 'PRINT':
            c = c.split(T_PRINT)[0].strip()
            print(self.transfer_type(c))
        if Token == 'PRINTALT':
            c = c.split(T_PRINT)[0].strip()
            print(self.transfer_type(c), end='')
            
        if Token == 'INPUT':
            c = c.split(T_INPUT)[1]
            if get_type(c) == 'INT':
                variables[c.replace(T_INT,'').strip()] = int(input())
            else:
                variables[c.strip()] = input()

        if Token == 'IF':
            c = c.replace(T_IF,'').replace('?','').strip()
            if get_type(c) == 'EQUALS':
                a = self.transfer_type(c.split(T_EQUALS)[0].strip())
                b = self.transfer_type(c.split(T_EQUALS)[1].strip())
                if a == b:
                    self.skip = False
                else:
                    self.skip = True
            elif get_type(c) == 'LARGER':
                a = self.transfer_type(c.split(T_LARGER)[0].strip())
                b = self.transfer_type(c.split(T_LARGER)[1].strip())
                if a > b:
                    self.skip = False
                else:
                    self.skip = True
            elif get_type(c) == 'LARGERSAME':
                a = self.transfer_type(c.split(T_LARGERSAME)[0].strip())
                b = self.transfer_type(c.split(T_LARGERSAME)[1].strip())
                if a >= b:
                    self.skip = False
                else:
                    self.skip = True

        if Token == 'FOR':
            c = c.replace(T_FOR, '').replace('으로가','').replace('로가','').strip()
            loop.append([index, self.transfer_type(c), self.transfer_type(c)])
            

        if Token == 'VAR':
            c = c.split(T_VAR)[1]
            v = c.split(T_IS1)[0] if T_IS1 in c else c.split(T_IS2)[0]
            n = c.split(T_IS1)[1] if T_IS1 in c else c.split(T_IS2)[1]
            v = v.strip()
            n = n.strip()
            if get_type(n) == 'MUL':
                n = n.split(T_MUL)
                r = self.transfer_type(n[1])
                variables[v] = self.transfer_type(n[0].strip()) * r
            elif get_type(n) == 'DIV':
                n = n.split(T_DIV)
                r = self.transfer_type(n[1])
                variables[v] = self.transfer_type(n[0].strip()) // r
            elif get_type(n) == 'PLUS':
                n = n.split(T_PLUS)
                r = self.transfer_type(n[1])
                variables[v] = self.transfer_type(n[0].strip()) + r
            elif get_type(n) == 'MINUS':
                n = n.split(T_MINUS)
                r = self.transfer_type(n[1])
                variables[v] = self.transfer_type(n[0].strip()) - r
            elif get_type(n) == 'NONE':
                variables[v] = variables[n]
            elif get_type(n) == 'STR':
                variables[v] = n.split(T_STR)[1]
            elif get_type(n) == 'INT':
                variables[v] = int(n.split(T_INT)[1])
        
        if Token == 'FUNC':
            c = c.replace(T_FUNC,'').strip()
            startFunc.append(index)
            return func[c]

        if Token == 'DEF':
            c = c.split(T_DEF)[1].strip()
            func[c] = index
            self.skip = True
            return
    
    def compile(self):
        c = self.code
        c = c.strip().split('\n')
        index = 0
        while index < len(c):
            line = c[index].strip()
            res = self.compile_line(line, index)
            if isinstance(res, int):
                index = res
            index += 1


        

def run_file(path):
    with open(path, encoding='utf-8') as file:
        code = ''.join(file.readlines())
        m = Meme(code)
        m.compile()