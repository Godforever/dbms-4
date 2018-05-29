
from utils import *


# 线性搜索算法
def linear_search(R_A=40, S_C=60):
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
            A_bytes, B_bytes = BUFFER.data[blkPtr+bytesPtr:blkPtr+bytesPtr+4], BUFFER.data[blkPtr+bytesPtr+4:blkPtr+bytesPtr+8]
            bytesPtr += 8
            if BytesToInt(''.join(A_bytes)) == R_A:
                print('('+str(BytesToInt(''.join(A_bytes)))+',' +str(BytesToInt(''.join(B_bytes)))+')')
                resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                   './result/linear_select', A_bytes + B_bytes)
        BUFFER.freeBlockInBuffer(blkPtr)

    S_addr = int(S_BASE_ADDR, 16)
    for i in range(S_BLOCK_NUM):
        blkPtr = BUFFER.readBlockFromDisk(addr=S_addr)
        S_addr = int(''.join(BUFFER.data[blkPtr + 56:blkPtr + 60]), 16)
        bytesPtr = 0
        while bytesPtr < blkSize - 8:
            C_bytes, D_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4], BUFFER.data[
                                                                                     blkPtr + bytesPtr + 4:blkPtr + bytesPtr + 8]
            bytesPtr += 8
            if BytesToInt(''.join(C_bytes)) == S_C:
                print('(' + str(BytesToInt(''.join(C_bytes))) + ',' + str(BytesToInt(''.join(D_bytes))) + ')')
                resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                   './result/linear_select', C_bytes+ D_bytes)
        BUFFER.freeBlockInBuffer(blkPtr)


    # 将result的剩余部分写入磁盘中
    if result_offset !=0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 8 +i ] = result_next_bytes_addr[2*i:2*(i+1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/linear_select/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)


# 二元搜索算法
def binary_select(BASE_ADDR, BLOCK_NUM, A_C, resultPtr, result_offset, result_addr):
    low_addr = int(BASE_ADDR, 16)
    high_addr = int(BASE_ADDR, 16) + 64 * (BLOCK_NUM - 1)

    while high_addr >= low_addr:
        low_Ptr = BUFFER.readBlockFromDisk(addr=low_addr)
        high_Ptr = BUFFER.readBlockFromDisk(addr=high_addr)
        low_max_bytes = BUFFER.data[low_Ptr + blkSize - 2 * TUPLE_SIZE:low_Ptr + blkSize - 2 * TUPLE_SIZE + 4]
        high_min_bytes = BUFFER.data[high_Ptr: high_Ptr + 4]
        if BytesToInt(low_max_bytes) >= A_C or BytesToInt(high_min_bytes) <= A_C:
            if BytesToInt(low_max_bytes) >= A_C:
                blkPtr = low_Ptr
            else:
                blkPtr = high_Ptr
            bytesPtr = 0
            while bytesPtr < blkSize - 8:
                A_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4]
                B_bytes = BUFFER.data[blkPtr + bytesPtr + 4:blkPtr + bytesPtr + 8]
                bytesPtr += 8
                if BytesToInt(A_bytes) == A_C:
                    print('(' + str(BytesToInt(''.join(A_bytes))) + ',' + str(BytesToInt(''.join(B_bytes))) + ')')
                    resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                       './result/binary_select', A_bytes + B_bytes)
                elif BytesToInt(A_bytes) > A_C:
                    BUFFER.freeBlockInBuffer(blkPtr)
                    break
            break
        else:
            low_addr = low_addr + 64
            high_addr = high_addr - 64
            # 计算中间块地址
            mid_addr = 64 * (((low_addr - high_addr) // 64) >> 1) + low_addr
            mid_Ptr = BUFFER.readBlockFromDisk(addr=mid_addr)
            mid_max_bytes = BUFFER.data[mid_Ptr + blkSize - 2 * TUPLE_SIZE:mid_Ptr + blkSize - 2 * TUPLE_SIZE + 4]
            mid_min_bytes = BUFFER.data[mid_Ptr: mid_Ptr + 4]
            if BytesToInt(mid_min_bytes) > A_C:
                high_addr = mid_addr - 64
            elif BytesToInt(mid_max_bytes) < A_C:
                low_addr = mid_addr + 64
            else:
                if BytesToInt(mid_min_bytes) == A_C:
                    blk_addr = mid_addr - 64
                    flag = True
                    while flag:
                        blkPtr = BUFFER.readBlockFromDisk(addr=blk_addr)
                        bytesPtr = 0
                        while bytesPtr < blkSize - 8:
                            A_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4]
                            B_bytes = BUFFER.data[blkPtr + bytesPtr + 4:blkPtr + bytesPtr + 8]
                            bytesPtr += 8
                            if BytesToInt(A_bytes) < A_C:
                                flag = False

                            elif BytesToInt(A_bytes) == A_C:
                                print('(' + str(BytesToInt(''.join(A_bytes))) + ',' + str(
                                    BytesToInt(''.join(B_bytes))) + ')')
                                resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset,
                                                                                   result_addr,
                                                                                   './result/binary_select',
                                                                                   A_bytes + B_bytes)
                        blk_addr = blk_addr - 64

                if BytesToInt(mid_max_bytes) == A_C:
                    blk_addr = mid_addr + 64
                    flag = True
                    while flag:
                        blkPtr = BUFFER.readBlockFromDisk(addr=blk_addr)
                        bytesPtr = 0
                        while bytesPtr < blkSize - 8:
                            A_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4]
                            B_bytes = BUFFER.data[blkPtr + bytesPtr + 4:blkPtr + bytesPtr + 8]
                            bytesPtr += 8
                            if BytesToInt(A_bytes) < A_C:
                                flag = False

                            elif BytesToInt(A_bytes) == A_C:
                                print('(' + str(BytesToInt(''.join(A_bytes))) + ',' + str(
                                    BytesToInt(''.join(B_bytes))) + ')')
                                resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset,
                                                                                   result_addr,
                                                                                   './result/binary_select',
                                                                                   A_bytes + B_bytes)
                        blk_addr = blk_addr + 64

                bytesPtr = 0
                while bytesPtr < blkSize - 8:
                    A_bytes = BUFFER.data[mid_Ptr + bytesPtr:mid_Ptr + bytesPtr + 4]
                    B_bytes = BUFFER.data[mid_Ptr + bytesPtr + 4:mid_Ptr + bytesPtr + 8]
                    bytesPtr += 8
                    if BytesToInt(A_bytes) == A_C:
                        print('(' + str(BytesToInt(''.join(A_bytes))) + ',' + str(BytesToInt(''.join(B_bytes))) + ')')
                        resultPtr, result_offset, result_addr = add_result(resultPtr, result_offset, result_addr,
                                                                           './result/binary_select', A_bytes + B_bytes)
                    elif BytesToInt(A_bytes) > A_C:
                        BUFFER.freeBlockInBuffer(mid_Ptr)
                        break

    return resultPtr, result_offset, result_addr

# 二元搜索 R_S，采用的二分查找的思想
def binary_select_R_S(A=40, C=60):

    # 对R进行搜索
    result_addr = int(RESULT_BASE_ADDR, 16)
    resultPtr = BUFFER.getNewBlockInBuffer()
    result_offset = 0
    sort_R()
    resultPtr, result_offset, result_addr = binary_select(R_BASE_ADDR, R_BLOCK_NUM, A, resultPtr, result_offset, result_addr)
    sort_S()
    resultPtr, result_offset, result_addr = binary_select(S_BASE_ADDR, S_BLOCK_NUM, C, resultPtr, result_offset,
                                                          result_addr)
    # 将result的剩余部分写入磁盘中
    if result_offset != 0:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for i in range(4):
            BUFFER.data[resultPtr + blkSize - 8 + i] = result_next_bytes_addr[2 * i:2 * (i + 1)]
        BUFFER.writeBlockToDisk(resultPtr, './result/linear_select/', result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)

    print('The num of IO is', BUFFER.numIO)



if __name__ == '__main__':
    linear_search()
    binary_select_R_S()

