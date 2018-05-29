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
    reslut_addr_list = [result_addr]
    for i in range(R_BLOCK_NUM):
        R_blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
        R_addr = int(''.join(BUFFER.data[R_blkPtr + 56: R_blkPtr + 60]), 16)
        S_addr = int(S_BASE_ADDR, 16)
        for j in range(S_BLOCK_NUM):
            S_blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
            S_addr = int(''.join(BUFFER.data[S_blkPtr + 56: S_blkPtr + 60]), 16)
            R_bytesPtr = 0
            while R_bytesPtr < blkSize - 8:
                A_bytes = BUFFER.data[R_blkPtr + R_bytesPtr:R_blkPtr + R_bytesPtr + 4]
                B_bytes = BUFFER.data[R_blkPtr + R_bytesPtr + 4:R_blkPtr + R_bytesPtr + 8]
                R_bytesPtr += 8
                S_bytesPtr = 0
                while S_bytesPtr < blkSize - 8:
                    C_bytes = BUFFER.data[S_blkPtr + S_bytesPtr:S_blkPtr + S_bytesPtr + 4]
                    D_bytes = BUFFER.data[S_blkPtr + S_bytesPtr + 4:S_blkPtr + S_bytesPtr + 8]
                    S_bytesPtr += 8
                    if BytesToInt(''.join(A_bytes)) == BytesToInt(''.join(C_bytes)):
                        print('(A,C={},B={},D={})'.format(BytesToInt(A_bytes), BytesToInt(B_bytes), BytesToInt(D_bytes)))
                        resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                           './result/join/', A_bytes + B_bytes + D_bytes)

            BUFFER.freeBlockInBuffer(S_blkPtr)
        BUFFER.freeBlockInBuffer(R_blkPtr)

    if result_offset !=0:
        result_next_addr = random.randint(int(RESULT_BASE_ADDR, 16), int(RESULT_MAX_ADDR, 16))
        while result_next_addr in reslut_addr_list:
            result_next_addr = random.randint(int(RESULT_BASE_ADDR, 16), int(RESULT_MAX_ADDR, 16))
        reslut_addr_list.append(result_next_addr)
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/join/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)

def sort_merge_join():
    pass

def hash_join():
    pass

if __name__ == '__main__':
    nest_loop_join()