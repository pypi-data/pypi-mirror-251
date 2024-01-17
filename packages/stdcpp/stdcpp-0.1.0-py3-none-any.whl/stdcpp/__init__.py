import sys

class StreamHandler:
    def handle(self, stream):
        pass

class Stream:
    def __init__(self, fh):
        self.fh = fh

    def __lshift__(self, other):
        if isinstance(other, StreamHandler):
            return other.handle(self)
        self.fh.write(str(other))
        return self

class Endl(StreamHandler):
    def handle(self, stream):
        stream.fh.write('\n')
        stream.fh.flush()
        return stream

cout = Stream(sys.stdout)
cerr = Stream(sys.stderr)
endl = Endl()
