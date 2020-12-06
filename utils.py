import signal, sys

def handle_term():
    def handle(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle)
