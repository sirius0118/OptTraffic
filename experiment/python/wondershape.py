import os
import sys

if sys.argv[1] == 'set':
    os.system(f"ssh skv-node2 'sudo wondershaper -a eno1  -d {int(sys.argv[2]) * 1024} -u {int(sys.argv[2]) * 1024}'")
    os.system(f"ssh skv-node3 'wondershaper eno1 {int(sys.argv[2]) * 1024} {int(sys.argv[2]) * 1024}'")
    os.system(f"ssh skv-node4 'wondershaper eno1 {int(sys.argv[2]) * 1024} {int(sys.argv[2]) * 1024}'")
    os.system(f"ssh skv-node6 'wondershaper eno1 {int(sys.argv[2]) * 1024} {int(sys.argv[2]) * 1024}'")
    os.system(f"ssh skv-node7 'wondershaper eno1 {int(sys.argv[2]) * 1024} {int(sys.argv[2]) * 1024}'")
elif sys.argv[1] == 'clean':
    os.system(f"ssh skv-node2 'sudo wondershaper -c -a eno1'")
    os.system(f"ssh skv-node3 'wondershaper clear eno1'")
    os.system(f"ssh skv-node4 'wondershaper clear eno1'")
    os.system(f"ssh skv-node6 'wondershaper clear eno1'")
    os.system(f"ssh skv-node7 'wondershaper clear eno1'")
