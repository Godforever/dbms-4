from extmem import TagBuffer
import random

# 设置关系R和关系S的地址范围
R_BASE_ADDR = '0x11111111'
R_MAX_ADDR = '0x22222222'
S_BASE_ADDR = '0x33333333'
S_MAX_ADDR = '0x44444444'
RESULT_BASE_ADDR = '0x55555555'
RESULT_MAX_ADDR = '0x66666666'
blkSize = 64
bufSize = 520

R_TUPLE_NUM = 112
TUPLE_SIZE = 8
S_TUPLE_NUM = 224
BLOCK_TUPLE_NUM = blkSize // TUPLE_SIZE - 1
R_BLOCK_NUM = R_TUPLE_NUM//(blkSize//TUPLE_SIZE - 1)
S_BLOCK_NUM = S_TUPLE_NUM//(blkSize//TUPLE_SIZE - 1)


# 定义缓冲区大小为520个字节，块大小为64字节的缓冲区
BUFFER = TagBuffer(bufSize, blkSize)

def IntToBytes(n):
    s = hex(n)
    s = s[2:]
    for i in range(8-len(s)):
        s = '0' + s
    return s

def BytesToInt(b):
    s = ''.join(b)
    return int(s, 16)

def generate_R_S():
    R = [{'A':random.randint(1,40),'B':random.randint(1, 1000)} for i in range(R_TUPLE_NUM)]
    S = [{'C':random.randint(20,60),'D':random.randint(1, 1000)} for i in range(S_TUPLE_NUM)]
    # R[0] = {'A':10,'B':100}
    # S[0] = {'C':10,'D':100}
    addr = int(R_BASE_ADDR, 16)
    for i in range(R_TUPLE_NUM//7):
        with open('./disk_block/'+str(addr)+'.blk', 'w') as f:
            for j in range(7):
                f.write(IntToBytes(R[i*7+j]['A']))
                f.write(IntToBytes(R[i * 7 + j]['B']))
            addr += 64
            f.write(IntToBytes(addr))

    addr = int(S_BASE_ADDR, 16)
    for i in range(S_TUPLE_NUM//7):
        with open('./disk_block/'+str(addr)+'.blk', 'w') as f:
            for j in range(7):
                f.write(IntToBytes(S[i*7+j]['C']))
                f.write(IntToBytes(S[i * 7 + j]['D']))
            addr += 64
            f.write(IntToBytes(addr))

def merge_sort(BASE_ADDR, BLOCK_NUM, blkSize):
    BUFFER.freeBuffer()
    addr = int(BASE_ADDR, 16)
    for k in range(BLOCK_NUM):
        blkPtr = BUFFER.readBlockFromDisk(addr=addr)
        resultPtr = BUFFER.getNewBlockInBuffer()
        BUFFER.data[resultPtr + 56:blkPtr + 60] = BUFFER.data[blkPtr + 56:blkPtr + 60]
        for i in range(blkSize//TUPLE_SIZE - 1):
            for j in range(i+1, blkSize//TUPLE_SIZE - 1):
                A_i_bytes = BUFFER.data[blkPtr + i * 8:blkPtr + i * 8 + 4]
                B_i_bytes = BUFFER.data[blkPtr + i * 8 + 4:blkPtr + i * 8 + 8]
                A_j_bytes = BUFFER.data[blkPtr + j * 8:blkPtr + j * 8 + 4]
                B_j_bytes = BUFFER.data[blkPtr + j * 8 + 4:blkPtr + j * 8 + 8]
                if BytesToInt(A_i_bytes) >BytesToInt(A_j_bytes):
                    BUFFER.data[blkPtr + i * 8 :blkPtr + i * 8 + 4] = A_j_bytes
                    BUFFER.data[blkPtr + i * 8 + 4:blkPtr + i * 8 + 8] = B_j_bytes
                    BUFFER.data[blkPtr + j * 8:blkPtr + j * 8 + 4] = A_i_bytes
                    BUFFER.data[blkPtr + j * 8 + 4:blkPtr + j * 8 + 8] = B_i_bytes
            BUFFER.data[resultPtr + i * 8 :blkPtr + i * 8 + 4] = BUFFER.data[blkPtr + i * 8 :blkPtr + i * 8 + 4]
            BUFFER.data[resultPtr + i * 8 + 4:blkPtr + i * 8 + 8] = BUFFER.data[blkPtr + i * 8 + 4:blkPtr + i * 8 + 8]
        # 将排序好的数据写回原磁盘
        BUFFER.writeBlockToDisk(resultPtr, './result/merge/', addr)
        BUFFER.freeBlockInBuffer(resultPtr)
        addr = int(''.join(BUFFER.data[blkPtr + 56 : blkPtr + 60]), 16)
        BUFFER.freeBlockInBuffer(blkPtr)

    addr = int(BASE_ADDR, 16)
    value_list =[]
    for k in range(BLOCK_NUM):
        blkPtr = BUFFER.readBlockFromDisk(addr=addr)
        for i in range(blkSize // TUPLE_SIZE - 1):
            A_i_bytes = BUFFER.data[blkPtr + i * 8:blkPtr + i * 8 + 4]
            B_i_bytes = BUFFER.data[blkPtr + i * 8 + 4:blkPtr + i * 8 + 8]
            value_list.append((A_i_bytes, B_i_bytes))

        addr = int(''.join(BUFFER.data[blkPtr + 56: blkPtr + 60]), 16)
        BUFFER.freeBlockInBuffer(blkPtr)

    # 先根据A进行排序，在根据B大小进行排序
    value_list = sorted(value_list, key=lambda v: BytesToInt(v[0]) + 0.0001*BytesToInt(v[1]))
    addr = int(BASE_ADDR, 16)
    count = 0
    for k in range(BLOCK_NUM):
        resultPtr = BUFFER.getNewBlockInBuffer()
        for i in range(blkSize // TUPLE_SIZE - 1):
            BUFFER.data[resultPtr + i * 8:resultPtr + i * 8 + 4] = value_list[count][0]
            BUFFER.data[resultPtr + i * 8 + 4:resultPtr + i * 8 + 8] = value_list[count][1]
            count += 1
        nx_addr = IntToBytes(addr+64)
        BUFFER.data[resultPtr + 56:resultPtr + 60] = [nx_addr[:2],nx_addr[2:4],nx_addr[4:6],nx_addr[6:8]]
        BUFFER.writeBlockToDisk(resultPtr, './disk_block/', addr)
        addr += 64
        BUFFER.freeBlockInBuffer(resultPtr)

def sort_R():
    merge_sort(R_BASE_ADDR, R_BLOCK_NUM, blkSize)

def sort_S():
    merge_sort(S_BASE_ADDR, S_BLOCK_NUM, blkSize)

def add_result(resultPtr, result_offset,result_addr, path, X_bytes):
    BUFFER.data[resultPtr + result_offset:resultPtr + result_offset + len(X_bytes)] = X_bytes
    result_offset += len(X_bytes)
    x = len(X_bytes)
    if len(X_bytes) == 12:
        x = 4
    if result_offset == blkSize - x:
        result_next_addr = result_addr + 64
        result_next_bytes_addr = IntToBytes(result_next_addr)
        for k in range(4):
            BUFFER.data[resultPtr + result_offset + k] = result_next_bytes_addr[2 * k:2 * (k + 1)]

        BUFFER.writeBlockToDisk(resultPtr, path, result_addr)
        BUFFER.freeBlockInBuffer(resultPtr)
        resultPtr = BUFFER.getNewBlockInBuffer()
        result_offset = 0
        result_addr = result_next_addr

    return resultPtr, result_offset, result_addr

def getBytes_A_B(blkPtr, bytesPtr):
    A_bytes = BUFFER.data[blkPtr + bytesPtr:blkPtr + bytesPtr + 4]
    B_bytes = BUFFER.data[blkPtr + bytesPtr + 4:blkPtr + bytesPtr + 8]
    bytesPtr += 8
    return A_bytes, B_bytes, bytesPtr


if __name__ =='__main__':
    generate_R_S()
    # sort_R()




