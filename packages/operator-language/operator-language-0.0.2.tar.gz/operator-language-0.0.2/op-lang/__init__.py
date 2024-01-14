import sys
def runner(code,m=0,n=0):
    out=""
    loop_code=""
    LOOP=0
    NOTE=0
    begin_=[]
    end_=[]
    for i in range(len(code)):
        char=code[i]
        if NOTE:
            continue
        elif LOOP and char!="]":
            loop_code+=char
            continue
        if char=="+":
            m+=1
        elif char=="-":
            m-=1
        elif char=="*":
            if isinstance(n,str):
                n=1
            m*=n
        elif char=="/":
            if isinstance(n,str):
                n=1
            if n==0:
                out=""
                break
            m//=n
        elif char=="%":
            if isinstance(n,str):
                n=1
            if n==0:
                out=""
                break
            m%=n
        elif char=="|":
            m=abs(m)
        elif char=="^":
            if isinstance(n,str):
                n=1
            m**=n
        elif char=="=":
            n=m
        elif char=="\"":
            n=chr(m)
        elif char==".":
            m=0
            n=0
        elif char=="~":
            if isinstance(n,str):
                n=0
            m,n=n,m
        elif char==";":
            out+=str(n)
        elif char==":":
            m=input()
            if m.isdigit():
                m=int(m)
            else:
                m=0
        elif char=="`":
            NOTE=not NOTE
        elif char=="[":
            LOOP=1
        elif char=="]":
            for i in range([0,n][isinstance(n,int)]):
                end=runner(loop_code,m=m,n=n)
                out+=str(end["out"])
                m=end["m"]
                n=end["n"]
            LOOP=0
        else:
            if NOTE:
                pass
            else:
                out=""
                break
    return {
        "out":out,
        "m":m,
        "n":n
    }

def main():
    import os.path
    if len(sys.argv)==1:
        code=""
        m=0
        n=0
        while 1:
            char=input()
            if char=="_":
                end=runner(code,m=m,n=n)
                print(end["out"])
                m=end["m"]
                n=end["n"]
            else:
                code+=char
    elif len(sys.argv)==2:
        path=sys.argv[1]
        if not os.path.splitext(path)[0][1:]=="op":
            print("Failed...")
        else:
            try:
                file=open(path,"r")
                code=file.read()
                file.close()
            except:
                code=""
            code=code.replace(" ","").replace("\n","").replace("\t","")
            print(runner(code)["out"])
    else:
        print("Arguments?")
if __name__=="__main__":
    main()