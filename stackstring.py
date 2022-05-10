from pwn import *

string = b"ws2_32.dll"

full = "eax"
half = "ax"
little = "al"


pieces = []
for i in range(0, len(string), 4):
    chunk = string[i : i + 4]
    pieces.append((hex(unpack(chunk, "all")), chunk.decode("utf-8")))

counter = 0
for each in pieces[::-1]:
    piece, value = each
    if len(piece) <= 10:
        register = full
    if len(piece) <= 6:
        print(f'"xor {full}, {full};" # zero out {full}')
        register = half
        print(f'"mov {register}, {piece}"; # ensure nullbyte')
        print(f"\"push {full};\" # end of string '{value}' with nullbyte")
        counter += 1
        continue
    if len(piece) <= 4:
        print(f'"xor {full}, {full};" # zero out {full}')
        register = little
        print(f'"mov {register}, {piece};" # ensure nullbyte')
        print(f"\"push {full};\" # end of string '{value}' with nullbyte")
        counter += 1
        continue
    if counter == 0:
        print(f'"xor {full}, {full};" # zero out {full}')
        print(f'"push {full};" # ensure nullbyte')

    print(f"\"push {piece};\" # push '{value}' onto stack")
    counter += 1
