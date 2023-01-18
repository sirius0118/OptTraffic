

for i in "skv-node2 skv-node3 skv-node4 skv-node6 skv-node7" ; do
  ssh $i "sudo wondershaper -a eno1 -d 100000 -u 100000"
#  echo $i
done