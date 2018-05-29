from utils import *

def projection():
    BUFFER.freeBuffer()
    R_addr = int(R_BASE_ADDR, 16)
    resultPtr = BUFFER.getNewBlockInBuffer()
    result_offset = 0
    result_addr = int(RESULT_BASE_ADDR, 16)
    for i in range(R_BLOCK_NUM):
        blkPtr = BUFFER.readBlockFromDisk(addr=R_addr)
        R_addr = int(''.join(BUFFER.data[blkPtr + 56:blkPtr + 60]), 16)
        bytesPtr = 0
        while bytesPtr < blkSize - 8:
            A_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4]
            bytesPtr += 8
            print('(' + str(BytesToInt(''.join(A_bytes)))+')')
            resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                               './result/projection/', A_bytes)
        BUFFER.freeBlockInBuffer(blkPtr)

    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 4 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/projection/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)
    BUFFER.freeBuffer()


if __name__ == '__main__':
    projection()