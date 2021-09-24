import turtle


inp = open('fonts.txt', 'r')
d0 = []
d1 = []
d_font = [d0, d1]
for i in range (0, 2, 1):
    s = inp.readline()
    while (s != "!\n"):
        new_length = float(s)
        new_angle = float(inp.readline())
        d_font[i].append((new_length, new_angle))
        s = inp.readline()
inp.close()

def turtle_print(i):
    for length, angle in d_font[i]:
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
    
        
    
