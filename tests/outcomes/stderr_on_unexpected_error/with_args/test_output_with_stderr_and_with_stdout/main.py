import sys

for _ in range(3):
    print("User stderr output!", file=sys.stderr)

for _ in range(3):
    print("User stdout output!")
