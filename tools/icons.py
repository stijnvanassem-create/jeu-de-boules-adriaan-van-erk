#!/usr/bin/env python3
"""Tekent de app-iconen (PNG) zonder externe libraries: donkerblauw vlak,
twee blauwe boules en een wit cochonnetje."""
import struct, zlib, math

NAVY=(0x0D,0x29,0x50); BLUE=(0x00,0x9A,0xDC); WHITE=(255,255,255)

def png(path, size, pad=0.0):
    s=size; px=[[NAVY]*s for _ in range(s)]
    def disc(cx,cy,r,col,ring=None):
        for y in range(s):
            for x in range(s):
                # 4x supersampling voor zachte randen
                hit=0
                for sy in (0.25,0.75):
                    for sx in (0.25,0.75):
                        if (x+sx-cx)**2+(y+sy-cy)**2<=r*r: hit+=1
                if hit:
                    a=hit/4; b=px[y][x]
                    px[y][x]=tuple(round(b[i]*(1-a)+col[i]*a) for i in range(3))
    k=s*(1-2*pad); o=s*pad
    disc(o+k*0.38,o+k*0.56,k*0.25,WHITE); disc(o+k*0.38,o+k*0.56,k*0.215,BLUE)
    disc(o+k*0.68,o+k*0.42,k*0.19,WHITE); disc(o+k*0.68,o+k*0.42,k*0.155,BLUE)
    disc(o+k*0.70,o+k*0.74,k*0.07,WHITE)
    raw=b"".join(b"\x00"+bytes(c for p in row for c in p) for row in px)
    def chunk(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",s,s,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
    open(path,"wb").write(data)

png("icons/icon-192.png",192)
png("icons/icon-512.png",512)
png("icons/icon-maskable-512.png",512,pad=0.1)
png("icons/apple-touch-icon.png",180)
