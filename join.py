from utils import *


R_HASH_BASE_ADDR = '0x11111111'
S_HASH_BASE_ADDR = '0x33333333'
BUCKET_NUM = 7

def nest_loop_join():
    BUFFER.freeBuffer()
    R_addr = int(R_BASE_ADDR, 16)
    resultPtr = BUFFER.getNewBlockInBuffer()
    result_offset = 0
    result_addr = int(RESULT_BASE_ADDR, 16)
    for i in range(R_BLOCK_NUM):
        R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
        R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
        S_addr = int(S_BASE_ADDR, 16)
        for j in range(S_BLOCK_NUM):
            S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
            S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
            R_bytesPtr = 0
            while R_bytesPtr < blkSize - 8:
                A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
                S_bytesPtr = 0
                while S_bytesPtr < blkSize - 8:
                    C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_blkPtr, S_bytesPtr)
                    if BytesToInt(A_bytes) == BytesToInt(C_bytes):
                        print('(A,C={},B={},D={})'.format(BytesToInt(A_bytes), BytesToInt(B_bytes), BytesToInt(D_bytes)))
                        resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                           './result/nest_loop_join/', A_bytes + B_bytes + D_bytes)

            BUFFER.freeBlockInBuffer(S_blkPtr)
        BUFFER.freeBlockInBuffer(R_blkPtr)

    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/nest_loop_join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)
    BUFFER.freeBuffer()

def sort_merge_join():
    sort_R()
    sort_S()
    # BUFFER.freeBuffer()
    R_addr = int(R_BASE_ADDR, 16)
    S_addr = int(S_BASE_ADDR, 16)
    R_read_num = 0
    S_read_num = 0
    resultPtr = BUFFER.getNewBlockInBuffer()
    result_offset = 0
    result_addr = int(RESULT_BASE_ADDR, 16)
    R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
    S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
    R_bytesPtr = 0
    S_bytesPtr = 0
    R_read_num += 1
    S_read_num += 1
    A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
    C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_blkPtr, S_bytesPtr)
    while not(R_read_num == R_BLOCK_NUM and R_bytesPtr >= blkSize - 8 and S_read_num == S_BLOCK_NUM and S_bytesPtr >= blkSize - 8):
        if BytesToInt(A_bytes) == BytesToInt(C_bytes):
            constant = A_bytes
            R_list = [B_bytes]
            S_list = [D_bytes]
            while True:
                A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
                if R_bytesPtr >= blkSize - 8 and R_read_num < R_BLOCK_NUM:
                    R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
                    BUFFER.freeBlockInBuffer(R_blkPtr)
                    R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
                    R_read_num += 1
                    R_bytesPtr = 0

                if BytesToInt(A_bytes) == BytesToInt(constant):
                    R_list.append(B_bytes)
                else:
                    break

            while True:
                C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_blkPtr, S_bytesPtr)

                if S_bytesPtr >= blkSize - 8 and S_read_num < S_BLOCK_NUM:
                    S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
                    BUFFER.freeBlockInBuffer(S_blkPtr)
                    S_read_num += 1
                    S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
                    S_bytesPtr = 0
                if BytesToInt(C_bytes) == BytesToInt(constant):
                    S_list.append(D_bytes)
                else:
                    break

            for B in R_list:
                for D in S_list:
                    print('(A,C={},B={},D={})'.format(BytesToInt(constant), BytesToInt(B), BytesToInt(D)))
                    resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                               './result/sort_merge_join/', constant + B + D)

        elif BytesToInt(A_bytes) > BytesToInt(C_bytes):
            C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_blkPtr, S_bytesPtr)
        else:
            A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
        if S_bytesPtr >= blkSize - 8 and S_read_num < S_BLOCK_NUM:
            S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
            BUFFER.freeBlockInBuffer(S_blkPtr)
            S_read_num += 1
            S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
            S_bytesPtr = 0

        if R_bytesPtr >= blkSize - 8 and R_read_num < R_BLOCK_NUM:
            R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
            BUFFER.freeBlockInBuffer(R_blkPtr)
            R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
            R_read_num += 1
            R_bytesPtr = 0

    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/sort_merge_join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)
    BUFFER.freeBuffer()

def my_hash(n):
    return n % BUCKET_NUM

def hash_Block(BASE_ADDR, BLOCK_NUM, HASH_BASE_ADDR):
    addr = int(BASE_ADDR, 16)
    hash_buckets = [(BUFFER.getNewBlockInBuffer(),0,int(HASH_BASE_ADDR, 16)) for i in range(BUCKET_NUM)]
    for i in range(BLOCK_NUM):
        blkPtr = BUFFER.readBlockFromDisk(addr=addr)
        bytesPtr = 0
        while bytesPtr < blkSize - 8:
            A_bytes, B_bytes, bytesPtr = getBytes_A_B(blkPtr, bytesPtr)
            t = my_hash(BytesToInt(A_bytes))
            hash_buckets[t] = add_result(hash_buckets[t][0],hash_buckets[t][1],hash_buckets[t][2],'./hash/bucket'+str(t)+'/', A_bytes+ B_bytes)
        addr = int(''.join(BUFFER.data[blkPtr + 56:blkPtr + 60]), 16)
        BUFFER.freeBlockInBuffer(blkPtr)

    for k in range(len(hash_buckets)):
        resultPtr, result_offset, result_addr = hash_buckets[k]
        if result_offset != 0:
            result_next_addr = 0
            result_next_bytes_addr = IntToBytes(result_next_addr)
            for i in range(4):
                BUFFER.data[resultPtr + blkSize - 8 + i] = result_next_bytes_addr[2 * i:2 * (i + 1)]
            BUFFER.writeBlockToDisk(resultPtr, './hash/bucket'+str(k)+'/', result_addr)
            BUFFER.freeBlockInBuffer(resultPtr)
        else:
            BUFFER.writeBlockToDisk(resultPtr, './hash/bucket'+str(k)+'/', result_addr)
            BUFFER.freeBlockInBuffer(resultPtr)

def get_R_S(addr, i):
    R_list = []
    while addr != 0:
        blkPtr = BUFFER.readBlockFromDisk(path='./hash/bucket' + str(i) + '/', addr=addr)
        addr = int(''.join(BUFFER.data[blkPtr + 56: blkPtr + 60]), 16)
        bytesPtr = 0
        A = 10
        while bytesPtr < blkSize - 8 and A > 0:
            A_bytes, B_bytes, bytesPtr = getBytes_A_B(blkPtr, bytesPtr)
            A = BytesToInt(A_bytes)
            if A > 0:
                R_list.append((A_bytes, B_bytes))

        BUFFER.freeBlockInBuffer(blkPtr)
        if A == 0:
            break

    return R_list

def hash_join():
    hash_Block(R_BASE_ADDR, R_BLOCK_NUM, R_HASH_BASE_ADDR)
    hash_Block(S_BASE_ADDR, S_BLOCK_NUM, S_HASH_BASE_ADDR)
    BUFFER.freeBuffer()
    resultPtr = BUFFER.getNewBlockInBuffer()
    result_offset = 0
    result_addr = int(RESULT_BASE_ADDR, 16)
    for i in range(BUCKET_NUM):
        R_addr = int(R_HASH_BASE_ADDR, 16)
        S_addr = int(S_HASH_BASE_ADDR, 16)
        R_list = get_R_S(R_addr, i)
        S_list = get_R_S(S_addr, i)
        for A_bytes, B_bytes in R_list:
            for C_bytes, D_bytes in S_list:
                if BytesToInt(A_bytes) == BytesToInt(C_bytes):
                    print('(A,C={},B={},D={})'.format(BytesToInt(A_bytes), BytesToInt(B_bytes), BytesToInt(D_bytes)))
                    resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                       './result/hash_join/',
                                                                       A_bytes + B_bytes + D_bytes)
    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/nest_loop_join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)
    BUFFER.freeBuffer()

if __name__ == '__main__':
    # nest_loop_join()
    # sort_merge_join()
    hash_join()