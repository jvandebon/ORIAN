CFLAGS  = -Wall -Wextra -g -O3 -I/usr/include/python3.4 -I/usr/include/boost -I${MAXCOMPILERDIR}/include -I/vol/cc/opt/maxeler/maxcompiler-2014.2/include/slic -I${MAXELEROSDIR}/include 
LFLAGS   = -g -O3 -L${MAXELEROSDIR}/lib -L/vol/cc/opt/maxeler/maxcompiler-2014.2/lib -lslic -lmaxeleros -lpthread -lm -lrt -lpython3.4m -lboost_python-py34

nbody.so: nbody.o slic_NBody.o
	g++ -fPIC -fopenmp -shared -o nbody.so $^ $(LFLAGS) 

nbody.o: nbody.cpp
	g++ -fPIC -fopenmp -c nbody.cpp $(CFLAGS) $(LFLAGS) -o nbody.o slic_NBody.o

clean:
	rm -rf nbody.o
