#!/bin/bash

for f in {1..122}
do
	b=$(printf http://lotrtcgdb.com/images/LOTR03%03d.jpg ${f%.*})
	wget -q $b
	echo $b
done


echo; echo
