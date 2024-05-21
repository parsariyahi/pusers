import struct

print("__________")
print("__________\n\n")

block_size = 384 #Bytes

with open("./utmp", "rb") as file:
    file = file.read()
    file_len = len(file)
    pointer = 0
    block = {}
    while pointer < file_len:
        block[pointer] = []
        for char_indx in range(pointer, pointer + block_size):
            block[pointer].append(chr(file[char_indx]))
            # block[pointer].append(
            #     struct.unpack("@c", bytes(file[char_indx]))
            # )
        pointer = pointer + block_size

UT_TYPE = (0, 0+4)
UT_PID = (4, 4+4)
UT_LINE = (8, 8+32)
UT_ID = (40, 40+4)
UT_USER = (44, 44+32)
UT_HOST = (76, 76+256)
UT_EXIT = (332, 332+4)
UT_SESSION = (336, 336+4)
UT_TV = (340, 340+8)
UT_ADDR_V6 = (348, 348+16)

for k, v in block.items():
    print("---------\n")
    print("ut type: ", v[UT_TYPE[0]:UT_TYPE[1]])
    print("ut pid: ", v[UT_PID[0]:UT_PID[1]])
    print("ut line: ", v[UT_LINE[0]:UT_LINE[1]])
    print("ut id: ", v[UT_ID[0]:UT_ID[1]])
    print("ut user: ", v[UT_USER[0]:UT_USER[1]])
    print("ut host: ", v[UT_HOST[0]:UT_HOST[1]])
    print("ut exit: ", v[UT_EXIT[0]:UT_EXIT[1]])
    print("ut session: ", v[UT_SESSION[0]:UT_SESSION[1]])
    print("ut tv: ", v[UT_TV[0]:UT_TV[1]])
    print("ut addr v6: ", v[UT_ADDR_V6[0]:UT_ADDR_V6[1]])
    print("---------\n")