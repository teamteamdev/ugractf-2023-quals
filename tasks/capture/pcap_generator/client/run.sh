# wait for server to start
success=
for i in `seq 1 10`; do
	if curl http://server; then
		success=1
		break
	fi
	sleep 1
done

if [ -z "$success" ]; then
	echo "Timeout on curl" >&2
	exit 1
fi

fail_grep=1

for i in `seq 1 3`; do

	# start traffic capture
	tcpdump -vv -i eth0 -w /data/capture.pcap &
	tpid=$!
	# wait for tcpdump to initialize
	sleep 1

	# download picture
	curl http://server/hacker.jpg -o /tmp/picture.jpg

	# extra request for integrity
	curl http://server/favicon.ico >&2
	
	# wait for capture integrity and kill tcpdump
	sleep 1
	kill $tpid
	wait $tpid
	
	grep -q favicon /data/capture.pcap
	fail_grep_ico=$?

	grep -q hacker.jpg /data/capture.pcap
	fail_grep_jpg=$?
	
	if [ $fail_grep_ico = 0 ] && [ $fail_grep_jpg = 0 ]; then
		fail_grep=0
		break
	else
		rm -f /data/capture.pcap
	fi
done

if [ $fail_grep != 0 ]; then
	echo "Timeout on download" >&2
	exit 1
fi
