import sys
import os

BLOCK_AVAILABLE = '00'
BLOCK_UNAVAILABLE = '01'
class TagBuffer():
    def __init__(self, bufSize, blkSize):
        self.numIO = 0
        self.bufSize = bufSize
        self.blkSize = blkSize
        self.numAllBlk = bufSize//(blkSize + 1)
        self.numFreeBlk = self.numAllBlk
        self.data = ['00' for i in range(bufSize)]

    def freeBuffer(self):
        self.data = ['00' for i in range(self.bufSize)]


    def getNewBlockInBuffer(self):
        if self.numFreeBlk == 0:
            print("Buffer is full!")
            return None
        blkPtr = 0
        while blkPtr < self.numAllBlk*(self.blkSize + 1):
            if self.data[blkPtr] == BLOCK_AVAILABLE:
                break
            else:
                blkPtr += self.blkSize + 1
        self.data[blkPtr] = BLOCK_UNAVAILABLE
        self.numFreeBlk -= 1
        return blkPtr + 1

    def freeBlockInBuffer(self, blk):
        self.data[blk-1] = BLOCK_AVAILABLE
        for i in range(self.blkSize):
            self.data[blk + i]= '00'
        self.numFreeBlk += 1

    def dropBlockOnDisk(self, addr):
        filename = str(addr) + '.blk'
        if os.path.exists(filename):
            os.remove(filename)
            return -1
        return 0
    def readBlockFromDisk(self, path='./disk_block/', addr=0):
        filename = path+str(addr) + '.blk'

        if self.numFreeBlk == 0:
            print("Buffer Overflows!\n")
            return None

        blkPtr = 0
        while blkPtr < self.numAllBlk*(self.blkSize + 1):
            if self.data[blkPtr] == BLOCK_AVAILABLE:
                break
            else:
                blkPtr += self.blkSize + 1
        with open(filename, 'r') as f:
            self.data[blkPtr] = BLOCK_UNAVAILABLE
            blkPtr += 1
            bytePtr = blkPtr
            while bytePtr < blkPtr + self.blkSize:
                ch = f.read(2)
                self.data[bytePtr] = ch
                bytePtr += 1
        self.numFreeBlk -= 1
        self.numIO += 1
        return blkPtr

    def writeBlockToDisk(self, blkPtr, path, addr):
        filename = path + str(addr) + '.blk'
        with open(filename, 'w') as f:
            for i in range(self.blkSize):
                f.write(self.data[blkPtr + i])
        self.data[blkPtr-1] = BLOCK_AVAILABLE
        self.numFreeBlk += 1
        self.numIO += 1
        return 0

