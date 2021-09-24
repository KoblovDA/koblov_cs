import turtle


L1 = 10
L2 = 10*2**0.5
L3 = 20
d0 = [(L1, 90), (L1, -90), (L3, -90), (L1, -90), (L1, -90), (1, 1), (L3, -90), (0, 0)]
d1 = [(L2, 45), (L3, -135), (1, 1), (L1, 90), (L1, 90), (0, -90), (0, 0)]

dfont = [d0, d1]

def turtle_print(i):
    for length, angle in dfont[i]:
        if (angle == length):
            if (angle == 1):
                turtle.penup()
            else:
                turtle.pendown()
        else:
            turtle.left(angle)
            turtle.forward(length)         
x = int(input())
s = bin(x)
new_s = s[2:]
print(new_s)
digits = [int(d) for d in new_s]
for i in digits:
    turtle_print(i)
    
        
    
