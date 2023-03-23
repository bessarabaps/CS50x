from cs50 import get_int

while True:

    height = get_int("Height(1...8): ")

    if height > 0 and height < 9:
        break

n = height - 1
b = 1
for i in range(height):
    for i in range(n):
        print(f" ",end="")
    n = n - 1
    for i in range(b):
        print(f"#",end="")
    print(f"  ",end="")
    for i in range(b):
        print(f"#",end="")
    b = b + 1
    print()