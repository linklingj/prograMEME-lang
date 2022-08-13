# TOKENS
T_PYSCRIPT = 'ㄴ'
T_PRINT = '물어본사람'
T_INPUT = '안물'
T_VAR = '어쩔'
T_DEF = '저쩔'
T_IS1 = '는'
T_IS2 = '은'
T_STR = '문자'
T_INT = '숫자'
T_MUL = '곱하기'
T_DIV = '나누기'
T_PLUS = '더하기'
T_MINUS = '빼기'

#변수
variables = {}

#토큰 찾기
def get_type(c):

    if T_PYSCRIPT in c:
        return 'PYSCRIPT'

    if T_PRINT in c:
        return 'PRINT'
    if T_INPUT in c:
        return 'INPUT'
    if T_VAR in c:
        return 'VAR'
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

    if T_STR in c:
        return 'STR'
    if T_INT in c:
        return 'INT'
    
    return 'NONE'

class Meme:
    def __init__(self, code):
        self.code = code

    def compile_line(self, c):
        if c == '':
            return None
        Token = get_type(c)

        if Token == 'PYSCRIPT':
            c = c[1:-1]
            execCode = compile(c, 'mulstring', 'exec')
            exec(execCode)

        if Token == 'PRINT':
            c = c.split(T_PRINT)[0].strip()
            if get_type(c) == 'NONE':
                print(variables[c])
            elif get_type(c) == 'STR':
                print(c.split(T_STR)[1])
            elif get_type(c) == 'INT':
                print(int(c.split(T_INT)[1]))
            
        if Token == 'INPUT':
            c = c.split(T_INPUT)[1]
            if get_type(c) == 'INT':
                variables[c.split(T_INT)[0].strip()] = int(input())
            else:
                variables[c.strip()] = input()

        if Token == 'VAR':
            c = c.split(T_VAR)[1]
            v = c.split(T_IS1)[0] if T_IS1 in c else c.split(T_IS2)[0]
            n = c.split(T_IS1)[1] if T_IS1 in c else c.split(T_IS2)[1]
            v = v.strip()
            n = n.strip()
            if get_type(n) == 'MUL':
                n = n.split(T_MUL)
                if get_type(n[1]) == 'INT':
                    variables[v] = variables[n[1].strip()] * int(n[1].replace(T_INT,''))
                else:
                    variables[v] = variables[n[0].strip()] * variables[n[1].strip()]
            elif get_type(n) == 'DIV':
                n = n.split(T_DIV)
                if get_type(n[1]) == 'INT':
                    variables[v] = variables[n[0].strip()] // int(n[1].replace(T_INT,''))
                else:
                    variables[v] = variables[n[0].strip()] // variables[n[1].strip()]
            elif get_type(n) == 'PLUS':
                n = n.split(T_PLUS)
                if get_type(n[1]) == 'INT':
                    variables[v] = variables[n[0].strip()] + int(n[1].replace(T_INT,''))
                else:
                    variables[v] = variables[n[0].strip()] + variables[n[1].strip()]
            elif get_type(n) == 'MINUS':
                n = n.split(T_MINUS)
                if get_type(n[1]) == 'INT':
                    variables[v] = variables[n[0].strip()] - int(n[1].replace(T_INT,''))
                else:
                    variables[v] = variables[n[0].strip()] - variables[n[1].strip()]
            elif get_type(n) == 'NONE':
                variables[v] = variables[n]
            elif get_type(n) == 'STR':
                variables[v] = n.split(T_STR)[1]
            elif get_type(n) == 'INT':
                variables[v] = int(n.split(T_INT)[1])
        
        if Token == 'DEF':
            return 
    
    def compile(self):
        c = self.code
        c = c.strip().split('\n')
        index = 0
        while index < len(c):
            line = c[index].strip()
            res = self.compile_line(line)
            index += 1


        

def run_file(path):
    with open(path, encoding='utf-8') as file:
        code = ''.join(file.readlines())
        m = Meme(code)
        m.compile()