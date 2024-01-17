import ast
import inspect
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


class CdbgDummy:
    def __lshift__(self, other):
        return self

class Cdbg:

    def __lshift__(self, other):
        try:
            f = inspect.currentframe().f_back
            curr_line = f.f_lineno - 1
            lines = Path(f.f_code.co_filename).read_text().splitlines()
            line = lines[curr_line]
            indent = len(line) - len(line.lstrip(' ').lstrip('\t'))
            
            code = ''
            for line in lines[curr_line:]:
                if not line.strip():
                    break

                code += line[indent:] + '\n'
                try:
                    tree = ast.parse(code)
                except SyntaxError as e:
                    pass
                else:
                    self._show(f.f_locals, f.f_globals, tree)
        except Exception as exc:
            raise RuntimeError("Inspection failed") from exc

        return CdbgDummy()

    def _show(self, loc, glo, tree):
        expr = tree.body[0]
        if not isinstance(expr, ast.Expr):
            raise RuntimeError("ast.Expr expected")
        
        binop = expr.value
        varnames = []
        while True:
            try:
                if not isinstance(binop, ast.BinOp):
                    raise RuntimeError("ast.BinOp expected")
                if not isinstance(binop.op, ast.LShift):
                    raise RuntimeError("ast.LShift expected")
                if not isinstance(binop.right, ast.Name):
                    raise RuntimeError("ast.Name expected")
            except Exception as exc:
                raise RuntimeError("Unexpected syntax") from exc
            
            varnames.append(binop.right.id)
            if isinstance(binop.left, ast.BinOp):
                binop = binop.left
            else:
                break
     
        gloloc = {**glo, **loc}
        for varname in reversed(varnames):
            try:
                val = gloloc[varname]
            except KeyError as exc:
                cerr << varname << " # Inaccessible" << endl
            else:
                cerr << varname << ": " << type(val).__name__ << " = " << repr(val) << endl
     
cdbg = Cdbg()
