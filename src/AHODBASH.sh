$ cat AHODBASH
PROG_NAME=/usr/bin/AHODCLX.py

# Start function implementation
do_start() {
		echo "Starting ${PROG_NAME}"
		python ${PROG_NAME} &
}

do_stop() {
		echo "Stopping ${PROG_NAME}"
		PID=$(ps aux | grep -v grep | grep AHODCLX.py | awk '{print $2}')
		echo "killing $PID"
		kill -15 $PID
}

case "$1" in
			start)
					do_start
					;;
			stop)
					do_stop
					;;
			restart)
					$0 stop
					sleep 10
					$0 start
					;;
			*)
					echo "Usage: $0 {start|stop|restart}"
					exit1
esac