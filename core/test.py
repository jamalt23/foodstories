from os import system
with open(__file__, "w") as file: [file.write(f"print({i})\n") for i in range(5,10000)]
system("python3 test.py")
