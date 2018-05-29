from utils import *


def setDifference():
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
    while not (R_read_num == R_BLOCK_NUM and R_bytesPtr >= blkSize - 8 and S_read_num == S_BLOCK_NUM and S_bytesPtr >= blkSize - 8):

        R = False
        S = False
        if BytesToInt(A_bytes)<BytesToInt(C_bytes):
            R = True
        elif BytesToInt(A_bytes) == BytesToInt(C_bytes) and BytesToInt(B_bytes) < BytesToInt(D_bytes):
            R = True
        elif BytesToInt(A_bytes) == BytesToInt(C_bytes) and BytesToInt(B_bytes) == BytesToInt(D_bytes):
            R = True
            S = True
        else :
            S = True

        if R and not S:
            resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                               './result/difference/', A_bytes + B_bytes)
        if R_read_num == R_BLOCK_NUM and R_bytesPtr >= blkSize - 8:
            C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_bytesPtr, S_bytesPtr)
            if S_bytesPtr >= blkSize - 8 and S_read_num < S_BLOCK_NUM:
                S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
                BUFFER.freeBlockInBuffer(S_blkPtr)
                S_read_num += 1
                S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
                S_bytesPtr = 0
            continue

        if S_read_num == S_BLOCK_NUM and S_bytesPtr >= blkSize - 8:
            A_bytes, B_bytes, S_bytesPtr = getBytes_A_B(R_bytesPtr, R_bytesPtr)
            if R_bytesPtr >= blkSize - 8 and R_read_num < R_BLOCK_NUM:
                R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
                BUFFER.freeBlockInBuffer(R_blkPtr)
                R_read_num += 1
                R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
                R_bytesPtr = 0
            continue

        if R:
            A_bytes, B_bytes, R_bytesPtr = getBytes_A_B(R_blkPtr, R_bytesPtr)
            if R_bytesPtr >= blkSize - 8 and R_read_num < R_BLOCK_NUM:
                R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
                BUFFER.freeBlockInBuffer(R_blkPtr)
                R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
                R_read_num += 1
                R_bytesPtr = 0

        if S:
            C_bytes, D_bytes, S_bytesPtr = getBytes_A_B(S_bytesPtr, S_bytesPtr)
            if S_bytesPtr >= blkSize - 8 and S_read_num < S_BLOCK_NUM:
                S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
                BUFFER.freeBlockInBuffer(S_blkPtr)
                S_read_num += 1
                S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
                S_bytesPtr = 0

    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/difference/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)
    BUFFER.freeBuffer()

if __name__ == '__main__':
    setDifference()
