import sys

print(len(sys.argv[1:]))
print(*sys.argv[1:], sep="\n")
