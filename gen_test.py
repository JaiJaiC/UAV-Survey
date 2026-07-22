#!/usr/bin/env python3
import os

OUT = r"F:\backup\【NUDT】\【NUDT】program\UAV-Survey\2.Scholar\Huazhe Xu\files\10382\note.html"

def w(f, s):
    f.write(s + chr(10))

with open(OUT, "w", encoding="utf-8") as f:
    w(f, "test")

print("Script test done")
