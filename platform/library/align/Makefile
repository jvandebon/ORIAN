# Makefile.cpu ---- James Arram 2017

# ---- compiler settings -----


TARGET=align

CXX=g++
CFLAGS=-fPIC -fopenmp -Wall -Wextra -g -O3 -std=c++0x -I/usr/include/python3.4 -I/usr/include/boost -I${MAXCOMPILERDIR}/include -I${MAXCOMPILERDIR}/include/slic -I${MAXELEROSDIR}/include -D_XOPEN_SOURCE=600

LFLAGS=-L${MAXELEROSDIR}/lib -L${MAXCOMPILERDIR}/lib -lm -lpthread  -lpython3.4m -lboost_python-py34 -lgomp -lrt

$(TARGET).so: $(TARGET).o file.o match.o seq.o utils.o sa.o maxeler.o ExactMatch_dfe.o 
	$(CXX) -fPIC -fopenmp -shared -o $(TARGET).so $(TARGET).o file.o match.o sa.o seq.o utils.o maxeler.o ExactMatch_dfe.o -lslic -lmaxeleros $(LFLAGS)

$(TARGET).o: align.cpp
	$(CXX) -c align.cpp $(CFLAGS) -o $(TARGET).o

file.o: file.cpp
	$(CXX) -c file.cpp $(CFLAGS) -o file.o

maxeler.o: maxeler.cpp
	$(CXX) -c maxeler.cpp $(CFLAGS) -o maxeler.o

match.o: match.cpp
	$(CXX) -c match.cpp $(CFLAGS) -o match.o

sa.o: sa.cpp
	$(CXX) -c sa.cpp $(CFLAGS) -o sa.o

seq.o: seq.cpp
	$(CXX) -c seq.cpp $(CFLAGS) -o seq.o

utils.o : utils.cpp
	$(CXX) -c utils.cpp $(CFLAGS) -o utils.o

clean:
	rm -rf $(TARGET).so utils.o seq.o sa.o match.o maxeler.o file.o align.o 

.PHONY: clean
