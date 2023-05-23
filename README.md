# Algorithm-1
To create the container in Windows (Powershell), MacOS (intel zsh) 
  and Linux (Bash):

  docker build -t algorithm-1 -f Dockerfile .


OPTIONAL BUILD ARGUMENTS (system dependent):
    --build-arg OS_TYPE={host architecture} 
    --build-arg OS={linux distro}
    --build-arg OS_VER={os version}


E.G. If you run an apple silicon machine (enter the following lines as 1 command):
  docker build -t algorithm-1 -f Dockerfile . 
    --build-arg OS_TYPE=aarch64 
    --build-arg OS=ubuntu 
    --build-arg=OS_VER=22.04
  
  

To run the container: 

  docker container run -it {container id hash}



To run the virtual environment inside the container:

  source activate algo1



To configure the virtual environment in the container:

  pip3 install -r requirements.txt


***NOTE***
Closing shells running the container will *not* shut down the container. 
To shut down the container please type 'exit' into the container shell
to close the container properly. Improper shut down could lead to 
performance or other kinds of issues on your computer if you have a 
large number of containers running.

