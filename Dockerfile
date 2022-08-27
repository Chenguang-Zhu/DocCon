FROM debian:sid-slim

### add Souffle source
RUN apt update && apt install -y wget && \
	wget https://souffle-lang.github.io/ppa/souffle-key.public \
	-O /usr/share/keyrings/souffle-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" \
	| tee /etc/apt/sources.list.d/souffle.list

### install souffle and other dependencies
RUN apt update && apt install -y souffle tar python3-pip python3-dev git nodejs npm dc vim ripgrep

### install npx 
RUN npm install -g npx 

WORKDIR /opt/doccon

### copy python3 library requirement list
### and install them
COPY requirement.txt requirement.txt  
RUN pip3 install -r requirement.txt 

# COPY library-src library-src 
RUN mkdir -p library-src 

### get and build openzeppelin library
RUN cd  library-src && \
git clone https://github.com/OpenZeppelin/openzeppelin-contracts.git && \
mv openzeppelin-contracts openzeppelin &&\
cd openzeppelin && npm install 

### get and build erc721-ext.
RUN  cd library-src && \
git clone https://github.com/1001-digital/erc721-extensions.git && \ 
cd erc721-extensions && npm install 

### unpack (pre-built) dapphubs
COPY library-src/DappHublibs.tar.gz library-src/
RUN cd library-src && \
    tar -zxvf DappHublibs.tar.gz

### Codefacts Extraction Preparation
COPY legacy  legacy
COPY Code2Schema Code2Schema

### Docfacts Extraction Preparation
COPY smart_factbase smart_factbase

### copy datalog files
COPY datalog datalog

### copy scripts
COPY exp exp
COPY scripts scripts
COPY entry.sh .

CMD [ "bash", "./entry.sh" ]
