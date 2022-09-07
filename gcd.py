def gcdr(a,b):
    if b==0:
        return a
    else:
        return gcdr(b,a%b)
def gcd(a,b):
    while b:
        a,b=b,a%b
    return a
if __name__ == "__main__":
    import fib
    for i in range(963):
        print(i,' ', gcd(fib.fib(i),fib.fib(i+1)))
         
        
        
