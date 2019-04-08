import os
import pygame
import time

class Chip8(object):

    def __init__(self, RomPath = None):
        
        with open(RomPath, 'rb') as f:
            RomStr = f.read()
        self.mem = bytes(0x200*[0x00]) + RomStr        
        
        self.V = {}
        for i in range(16):
            self.V[i] = 0x00

        self.KEYS = {}
        for i in range(16):
            self.KEYS[i] = False           
            
        self.STACK = 16*[0x0000]    
            
        self.I = 0x00    

        self.SP = 0x0
        self.PC = 0x200
    
    def emulateCycle(self):
        w = (self.mem[self.PC] << 8) + self.mem[self.PC+1]
        print("${:04X} {:04X}".format(self.PC, w))
        print(
            "V "+
            " ".join(["{:02X}".format(val) for key, val in self.V.items()])+
            "  I {:04X}".format(self.I)
        )
        print(        
            "S "+
            " ".join(["{:04X}".format(add) for add in self.STACK])
        )
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
        elif ( n3 == 0x0 ) and (nnn != 0x0EE):
            """
            0nnn - SYS addr
            Jump to a machine code routine at nnn.

            This instruction is only used on the old computers on which Chip-8 was originally implemented. It is ignored by modern interpreters.
            """
            pass    
        elif ( n3 == 0x0 ) and (nnn == 0x0EE):
            """
            00EE - RET
            Return from a subroutine.

            The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
            """
            self.PC = self.STACK[self.SP]
            self.SP -= 1
            return
        elif ( n3 == 0x1 ):
            """
            1nnn - JP addr
            Jump to location nnn.
            
            The interpreter sets the program counter to nnn.
            """
            self.PC = nnn
            return
        elif ( n3 == 0x2 ):
            """
            2nnn - CALL addr
            Call subroutine at nnn.

            The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
            """
            self.SP += 1
            self.STACK[self.SP] = self.PC
            self.PC = nnn
            return
        elif ( n3 == 0x3 ):
            """
            3xkk - SE Vx, byte
            Skip next instruction if Vx = kk.

            The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
            """
            if self.V[x] == kk:
                self.PC += 2       
        elif ( n3 == 0x6 ):
            """
            6xkk - LD Vx, byte
            Set Vx = kk.
            
            The interpreter puts the value kk into register Vx.
            """
            self.V[x] = kk
        elif ( n3 == 0x7 ):
            """
            7xkk - ADD Vx, byte
            Set Vx = Vx + kk.

            Adds the value kk to the value of register Vx, then stores the result in Vx. 
            """
            self.V[x] += kk
        elif ( n3 == 0x8 ) and ( n == 0x0 ):
            """
            8xy0 - LD Vx, Vy
            Set Vx = Vy.

            Stores the value of register Vy in register Vx.
            """
            self.V[x] = self.V[y]
        elif ( n3 == 0xA ):
            """
            Annn - LD I, addr
            Set I = nnn.
            
            The value of register I is set to nnn.
            """
            self.I = nnn
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
        elif ( n3 == 0xE ) and ( kk == 0xA1 ):
            """
            ExA1 - SKNP Vx
            Skip next instruction if key with the value of Vx is not pressed.

            Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
            """
            if not self.KEYS[x]:
                self.PC += 2
        elif ( n3 == 0xF ) and (kk == 0x1E):
            """
            Fx1E - ADD I, Vx
            Set I = I + Vx.

            The values of I and Vx are added, and the results are stored in I.
            """
            self.I += self.V[x]
        elif ( n3 == 0xF ) and (kk == 0x65):
            """
            Fx65 - LD Vx, [I]
            Read registers V0 through Vx from memory starting at location I.

            The interpreter reads values from memory starting at location I into registers V0 through Vx.
            """
            for loc in range(x+1):
                self.V[loc] = self.mem[self.I + loc]
        else:
            import pdb; pdb.set_trace() 
            # pass
        self.PC += 2
        # input("DBG")

display_width_pixel = 64
display_height_pixel = 32
zoom = 10

screen_width = display_width_pixel*zoom
screen_height = display_height_pixel*zoom

BLACK_COLOUR = (0, 0, 0)
WHITE_COLOUR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface(screen.get_size())
background.fill(BLACK_COLOUR)
background = background.convert()
screen.blit(background, (0,0))
clock = pygame.time.Clock()
surface = pygame.Surface((10, 10))
surface.set_colorkey((0, 0, 0))
pygame.draw.rect(
    surface,
    WHITE_COLOUR,
    (0, 0, 10, 10),
)
FPS = 60
bPlaying = True

ThisFolder = os.path.dirname(os.path.realpath(__file__))
RomPath = os.path.join(ThisFolder, r"roms\INVADERS")

keymap = {}

chip8 = Chip8(RomPath = RomPath)

while bPlaying:
    milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
    seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
    screen.blit(background, (0,0))     #draw background on screen (overwriting all)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bPlaying = False # pygame window closed by user
        elif event.type == pygame.KEYDOWN:          
            # print(event.unicode+" DOWN")
            keymap[event.scancode] = event.unicode
            if event.unicode == "&": chip8.KEYS[0x1] = True
            elif event.unicode == "é": chip8.KEYS[0x2] = True
            elif event.unicode == '"': chip8.KEYS[0x3] = True
            elif event.unicode == "'": chip8.KEYS[0xC] = True
            elif event.unicode == "a": chip8.KEYS[0x4] = True
            elif event.unicode == "z": chip8.KEYS[0x5] = True
            elif event.unicode == "e": chip8.KEYS[0x6] = True
            elif event.unicode == "r": chip8.KEYS[0xD] = True
            elif event.unicode == "q": chip8.KEYS[0x7] = True
            elif event.unicode == "s": chip8.KEYS[0x8] = True
            elif event.unicode == "d": chip8.KEYS[0x9] = True
            elif event.unicode == "f": chip8.KEYS[0xE] = True
            elif event.unicode == "w": chip8.KEYS[0xA] = True
            elif event.unicode == "x": chip8.KEYS[0x0] = True
            elif event.unicode == "c": chip8.KEYS[0xB] = True
            elif event.unicode == "v": chip8.KEYS[0xF] = True
        elif event.type == pygame.KEYUP:          
            event.unicode = keymap[event.scancode]
            # print(event.unicode+" UP")
            if event.unicode == "&": chip8.KEYS[0x1] = False
            elif event.unicode == "é": chip8.KEYS[0x2] = False
            elif event.unicode == '"': chip8.KEYS[0x3] = False
            elif event.unicode == "'": chip8.KEYS[0xC] = False
            elif event.unicode == "a": chip8.KEYS[0x4] = False
            elif event.unicode == "z": chip8.KEYS[0x5] = False
            elif event.unicode == "e": chip8.KEYS[0x6] = False
            elif event.unicode == "r": chip8.KEYS[0xD] = False
            elif event.unicode == "q": chip8.KEYS[0x7] = False
            elif event.unicode == "s": chip8.KEYS[0x8] = False
            elif event.unicode == "d": chip8.KEYS[0x9] = False
            elif event.unicode == "f": chip8.KEYS[0xE] = False
            elif event.unicode == "w": chip8.KEYS[0xA] = False
            elif event.unicode == "x": chip8.KEYS[0x0] = False
            elif event.unicode == "c": chip8.KEYS[0xB] = False
            elif event.unicode == "v": chip8.KEYS[0xF] = False
    for i in range(10):
        chip8.emulateCycle()
    screen.blit(surface, (0, 0))
    pygame.display.flip()        
    
