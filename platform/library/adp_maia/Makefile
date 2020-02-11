TARGET = adp

LFLAGS=-L${MAXELEROSDIR}/lib -L${MAXCOMPILERDIR}/lib -lm  -lpthread -fopenmp -lpython3.4m -lboost_python-py34 -lgomp -lrt

CFLAGS=-fPIC -fopenmp -O3 -Wall -I/usr/include/python3.4 -I/usr/include/boost -I${MAXCOMPILERDIR}/include -I${MAXCOMPILERDIR}/include/slic -I${MAXELEROSDIR}/include -D_XOPEN_SOURCE=600

$(TARGET).so: $(TARGET).o RandomVariable.o Adp_dfe.o
	g++ -fPIC -shared -o $(TARGET).so $(TARGET).o RandomVariable.o Adp_dfe.o -lslic -lmaxeleros   $(LFLAGS) 

$(TARGET).o: adp.cpp
	g++ -c adp.cpp $(CFLAGS) -o $(TARGET).o

RandomVariable.o: RandomVariable.cpp
	g++ -c RandomVariable.cpp $(CFLAGS) -o RandomVariable.o

clean:
	rm -rf $(TARGET).so RandomVariable.o $(TARGET).o
