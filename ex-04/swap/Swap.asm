// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.


@R14
D = M
@i
M = D
@R14
A = M
D = M 
@minvalue
M  = D
@R14
D = M 

@maxadress
M = D
@minadress
M = D
@R14
A = M
D = M 
@maxvalue
M  = D

(LOOP)
@i
A = M
D = M
@minvalue
D = M - D
@SWITCHMIN
D;JGE
(COMEBACK1)
@i
A = M
D = M
@maxvalue
D = M - D
@SWITCHMAX
D;JLT
(COMEBACK2)
@R14
D = M
@R15
D = D+M
@i
M = M + 1
D = M - D
@LOOP
D;JLT

@AEND
0;JMP

(SWITCHMIN)
@i
D = M
@minadress
M = D
@i
A = M
D = M
@minvalue
M = D
@COMEBACK1
0;JMP



(SWITCHMAX)
@i
D = M
@maxadress
M = D
@i
A = M
D = M
@maxvalue
M = D
@COMEBACK2
0;JMP


(AEND)

@maxvalue
D = M
@minadress
A = M
M = D
@minvalue
D = M
@maxadress
A = M
M = D

(END)
@END    
0;JMP