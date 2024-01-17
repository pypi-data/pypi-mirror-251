# cout & cerr like in C++

Usge:

```py
from stdcpp import cout, cerr, endl

cout << "Hello" << " " << "world!" << endl
cerr << "Hello" << " " << "world!" << endl
```

Bonus 1:

```py
from stdcpp import Stream

s = Stream('log.txt', 'a+')
s << "Hello "
s.close()

with Stream('log.txt', 'a+') as s:
    s << "world!" << endl
```

Bonus 2:

```py
import io
from stdcpp import Stream, cout

ios = io.StringIO()
s = Stream(ios)
s << "Hello world!" << endl
ios.seek(0)
cout << ios.read()
```

Bonus 3:
```py
from stdcpp import cdbg

x = 123
y = 'foobar'

cdbg << x << y
```
