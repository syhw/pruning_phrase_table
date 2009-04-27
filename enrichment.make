PYTHON_INCLUDE_DIR=/opt/local/include/python2.5
PYTHON_LIB_DIR=/opt/local/lib/
PYTHON_LIB_NAME=python2.5

all: enrichment_.so

enrichment_.so: enrichment_.o
	gcc -L$(PYTHON_LIB_DIR) -l$(PYTHON_LIB_NAME) -dynamiclib enrichment_.o -o enrichment_.so

enrichment_.o: enrichment.c
	gcc -c enrichment.c -o enrichment_.o -I$(PYTHON_INCLUDE_DIR)

clean:
	rm -f enrichment_.so
	rm -f enrichment_.o

standalone:
	gcc -g -I$(PYTHON_INCLUDE_DIR) -l$(PYTHON_LIB_NAME) enrichment.c -o enrichment
