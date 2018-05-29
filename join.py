from utils import *

HASH_BUCKET_R = 0
HASH_BUCKET_S = 1
HASH_LEN = (64*blkSize)
HASH_N = 5

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
        BUFFER.writeBlockToDisk(resultPtr, './result/join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)


def sort_merge_join():
    sort_R()
    sort_S()
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
    while R_read_num < R_BLOCK_NUM or S_read_num < S_BLOCK_NUM:
        if BytesToInt(A_bytes) == BytesToInt(C_bytes):
            constant = BytesToInt(A_bytes)
            R_list = []
            S_list = []
            while True:
                A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
                if R_bytesPtr >= blkSize - 8:
                    R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
                    BUFFER.freeBlockInBuffer(R_blkPtr)
                    R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
                    R_read_num += 1
                    R_bytesPtr = 0

                if BytesToInt(A_bytes) == constant:
                    R_list.append((A_bytes, B_bytes))
                else:
                    break
            while True:
                C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_blkPtr, S_bytesPtr)

                if S_bytesPtr >= blkSize - 8:
                    S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
                    BUFFER.freeBlockInBuffer(S_blkPtr)
                    S_read_num += 1
                    S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
                    S_bytesPtr = 0
                if BytesToInt(C_bytes) == constant:
                    S_list.append((C_bytes, D_bytes))
                else:
                    break

            print('(A,C={},B={},D={})'.format(BytesToInt(A_bytes), BytesToInt(B_bytes), BytesToInt(D_bytes)))
            resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                               './result/sort_merge_join/', A_bytes + B_bytes + D_bytes)


        elif BytesToInt(A_bytes) > BytesToInt(C_bytes):
            C_bytes, D_bytes = getBytes_A_B(S_blkPtr, S_bytesPtr)
            S_bytesPtr += 8
        else:
            A_bytes, B_bytes = getBytes_A_B(R_blkPtr, R_bytesPtr)
            R_bytesPtr += 8
        if S_bytesPtr >= blkSize - 8:
            S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
            BUFFER.freeBlockInBuffer(S_blkPtr)
            S_read_num += 1
            S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
            S_bytesPtr = 0

        if R_bytesPtr >= blkSize - 8:
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
        BUFFER.writeBlockToDisk(resultPtr, './result/join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)

def hash_join():
    pass

if __name__ == '__main__':
    nest_loop_join()