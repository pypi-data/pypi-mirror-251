import sys
from pathlib import Path

class StreamHandler:
    def handle(self, stream):
        pass

class Stream:
    def __init__(self, fh, *args, **kwargs):
        if isinstance(fh, (str, Path)):
            fh = open(str(fh), *args, **kwargs)
        self.fh = fh

    def __lshift__(self, other):
        if isinstance(other, StreamHandler):
            return other.handle(self)
        self.fh.write(str(other))
        return self
    
    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self.close()
        
    def close(self):
        self.fh.close()

class Endl(StreamHandler):
    def handle(self, stream):
        stream.fh.write('\n')
        stream.fh.flush()
        return stream

cout = Stream(sys.stdout)
cerr = Stream(sys.stderr)
endl = Endl()
