# stage_gedlibpy
Working over the repositories gedlibpy and gedlib

This repository has to be next to the gedlibpy repository
I myself have done modifications to some files in the gedlibpy local copy that I have, so for the moment this repository is not self-contained.

In the following commits I will link the gedlibpy project to this repository to make it ready to launch.


Instalation (what I have done so far to make things work):

1. Clone the gedlibpy repository from https://github.com/Ryurin/gedlibpy. The path to the gedlibpy folder can be changed in the files to make it work fine.

2. Follow the installation steps given in https://github.com/Ryurin/gedlibpy. This implies installing gedlib (contained in the gedlibpy repository)
You might encounter some problems:
    - gedlibpy.cpp:678:10: fatal error: numpy/arrayobject.h: No such file or directory
        678 | #include "numpy/arrayobject.h"
            |          ^~~~~~~~~~~~~~~~~~~~~
      compilation terminated.
      error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
    
    To solve this problem, go to the setup.py file and add numpy.get_include() in the include_dirs list.
    
    
    - In some examples used to "warm up", the module pygraph is used. I installed it using pip but instead got another module from the one needed. The files are available here https://github.com/jajupmochi/graphkit-learn/tree/master/gklearn/utils or here https://github.com/bgauzere/py-graph. If you want to run the examples, you can get the codes and make it work.
      
    - When using the method add_nx_graph from the gedlibpy module I found a problem:
      Traceback (most recent call last):
        File "ged.py", line 35, in <module>
          gedlibpy.add_nx_graph(graph, "A")
        File "gedlibpy.pyx", line 854, in gedlibpy.add_nx_graph
          add_node(id, str(node), g.node[node])
      AttributeError: 'Graph' object has no attribute 'node'
      To fix this locally, I changed the line 854 from the gedlibpy.pyx file and relaunched setup.py (so doing it before will save you one execution)
      Just add an s: dd_node(id, str(node), g.node[node]) -> dd_node(id, str(node), g.nodes[node])

3. Now the codes from this repository should execute just fine.
    
    
