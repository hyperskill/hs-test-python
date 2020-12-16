import sys

print(len(sys.argv) - 1)
for arg in sys.argv[1:]:
    print(arg)
