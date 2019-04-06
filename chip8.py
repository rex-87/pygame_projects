import os

ThisFolder = os.path.dirname(os.path.realpath(__file__))
RomPath = os.path.join(ThisFolder, r"roms\INVADERS")

with open(RomPath, 'rb') as f:
    RomStr = f.read()
mem = bytes(0x200*[0x00]) + RomStr

V = {}
for i in range(16):
    V[i] = 0x00

I = 0x00    
    
PC = 0x200
while True:
    w = (mem[PC] << 8) + mem[PC+1]
    print("${:04X} {:04X}".format(PC, w))
    print("V "+" ".join(["{:02X}".format(val) for key, val in V.items()])+"  I {:04X}".format(I))
    n3 = (w & 0xF000) >> 12
    x = (w & 0x0F00) >> 8
    y = (w & 0x00F0) >> 4
    n = w & 0x000F
    kk = w & 0x00FF
    nnn = w & 0x0FFF
    if ( n3 == 0x0 ) and (nnn == 0x0E0):
        """
        00E0 - CLS
        Clear the display.
        """
        pass # TODO
    if ( n3 == 0x0 ) and (nnn != 0x0EE):
        """
        0nnn - SYS addr
        Jump to a machine code routine at nnn.

        This instruction is only used on the old computers on which Chip-8 was originally implemented. It is ignored by modern interpreters.
        """
        pass    
    elif ( n3 == 0x1 ):
        """
        1nnn - JP addr
        Jump to location nnn.
        
        The interpreter sets the program counter to nnn.
        """
        PC = nnn
        continue
    elif ( n3 == 0x3 ):
        """
        3xkk - SE Vx, byte
        Skip next instruction if Vx = kk.

        The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
        """
        if V[x] == kk:
            PC += 2       
    elif ( n3 == 0x6 ):
        """
        6xkk - LD Vx, byte
        Set Vx = kk.
        
        The interpreter puts the value kk into register Vx.
        """
        V[x] = kk
    elif ( n3 == 0x7 ):
        """
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx. 
        """
        V[x] += kk
    elif ( n3 == 0xA ):
        """
        Annn - LD I, addr
        Set I = nnn.
        
        The value of register I is set to nnn.
        """
        I = nnn
    elif ( n3 == 0xD ):
        """
        Dxyn - DRW Vx, Vy, nibble
        Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory, starting at the address stored in I.
        These bytes are then displayed as sprites on screen at coordinates (Vx, Vy).
        Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0.
        If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen.
        See instruction 8xy3 for more information on XOR, and section 2.4, Display, for more information on the Chip-8 screen and sprites.
        """
        pass # TODO
    elif ( n3 == 0xF ) and (kk == 0x1E):
        """
        Fx1E - ADD I, Vx
        Set I = I + Vx.

        The values of I and Vx are added, and the results are stored in I.
        """
        I += V[x]        
    else:
        import pdb; pdb.set_trace() 
    PC += 2
