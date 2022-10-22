﻿# Creamos diccionario de operaciones:
opcodes = dict(
    "MOV A, B": "00010000100000000000",
    "MOV B, A": "00001100000000000000",
    "MOV A, Lit": "00010001100000000000",
    "MOV B,	Lit": "00001001100000000000",
    "MOV A,	(Dir)": "00010001000000010000",
    "MOV B,	(Dir)": "00001001000000010000",
    "MOV (Dir),	A": "00000100000001010000",
    "MOV (Dir),	B": "00000000100001010000",
    "MOV A,	(B)": "00010001000000100000",
    "MOV B, (B)": "00001001000000100000",
    "MOV (B), A": "00000100000001000000",
    "MOV (B), Lit": "00000001100001100000",
    "ADD A,	B": "00010100100000000000",
    "ADD B,	A": "00001100100000000000",
    "ADD A,	Lit": "00010101100000000000",
    "ADD B,	Lit": "00001101100000000000",
    "ADD A,	(Dir)": "00010111000000010000",
    "ADD B,	(Dir)": "00001111000000010000",
    "ADD (Dir)": "00000100100001010000",	
    "ADD A, (B)": "00010101000000100000",
    "ADD B, (B)": "00001101000000100000",
    "SUB A, B": "00010100100010000000",
    "SUB B, A": "00001100100010000000",
    "SUB A, Lit": "00010101100010000000",
    "SUB B, Lit": "00001101100010000000",
    "SUB A, (Dir)": "00010111000010010000",
    "SUB B, (Dir)": "00001111000010010000",
    "SUB (Dir)": "00000100100011010000",
    "SUB A, (B)": "00010101000010100000",
    "SUB B, (B)": "00001101000010100000",
    "AND A, B": "00010100100100000000",
    "AND B, A": "00001100100100000000",
    "AND A, Lit": "00010101100100000000",
    "AND B, Lit": "00001101100100000000",
    "AND A, (Dir)": "00010111000100010000",
    "AND B, (Dir)": "00001111000100010000",
    "AND (Dir)"	: "00000100100101010000",
    "AND A, (B)": "00010101000100100000",
    "AND B, (B)": "00001101000100100000",
    "OR	A, B": "00010100100110000000",
    "OR B, A": "00001100100110000000",
    "OR A, Lit": "00010101100110000000",
    "OR B, Lit": "00001101100110000000",
    "OR A, (Dir)": "00010111000110010000",
    "OR B, (Dir)": "00001111000110010000",
    "OR (Dir)": "00000100100111010000",
    "OR A, (B)": "00010101000110100000",
    "OR B, (B)": "00001101000110100000",
    "XOR A, B": "00010100101000000000",
    "XOR B, A": "00001100101000000000",
    "XOR A, Lit": "00010101101000000000",
    "XOR B,	Lit": "00001101101000000000",
    "XOR A,	(Dir)": "00010111001000010000",
    "XOR B,	(Dir)": "00001111001000010000",
    "XOR (Dir)": "00000100101001010000",	
    "XOR A,	(B)": "00010101001000100000",
    "XOR B,	(B)": "00001101001000100000",
    "NOT A": "00010100001010000000",
    "NOT B,	A": "00001100001010000000",
    "NOT (Dir) A": "00000100001011010000",
    "NOT (B) A": "00000100001011100000",
    "SHL A": "00010100001110000000",	
    "SHL B,	A": "00001100001110000000",
    "SHL (Dir),	A": "00000100001111000000",
    "SHL (B), A": "00000100001111100000",
    "SHR A": "00010100001100000000",	
    "SHR B,	A": "00001100001100000000",
    "SHR (Dir),	A": "00000100001101000000",
    "SHR (B), A": "00000100001101100000",
    "INC A": "00010101100000000000",
    "INC B": "00001110100000000000",
    "INC (Dir)": "00111000001010000",
    "INC (B)": "00000111000001100000",
    "DEC A	": "00010101100010000000",
    "CMP A, B": "00000100100010000000",
    "CMP A, Lit": "00000101100010000000",
    "CMP A, (Dir)": "00101000010000000",
    "CMP A, (B)": "00000100000010100000",
    "JMP Ins": "00000000010000000010",	
    "JEQ Ins": "00000000010010000010",	
    "JNE Ins": "00000000010100000010",	
    "JGT Ins": "00000000011000000010",	
    "JGE Ins": "00000000010110000010",
    "JLT Ins": "00000000011010000010",
    "JLE Ins": "00000000011100000010",
    "JCR Ins": "00000000011110000010",
    "PUSH A": "00000100000001000100",
    "PUSH B": "00000000100001000100",
    "POP A": ("00000000000000001000", "00010001000000000000"),
    "POP B": ("00000000000000001000", "00001001000000000000"),
    "CALL Ins": "00000000000000000111",
    "RET": ("00000000000000001000", "00000000010000000000")		
)