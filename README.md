# Algorithm-1
To create the container in Windows (Powershell), MacOS (apple silicon zsh) and Linux (Bash):

  docker build -t algorithm-1 -f Dockerfile .
    --build-arg OS_TYPE={host architecture} 
    --build-arg OS={linux distro}
    --build-arg OS_VER={os version}

To run the container: 

  "cd <path/to/directory/with/Dockerile/>"
  "docker container run -it <container id hash>"


To run the virtual environment inside the container:

  "source activate algo1"


***NOTE***
Closing shells running the container will *not* shut down the container. 
To shut down the container please type 'exit' into the container shell
to close the container properly. Improper shut down could lead to 
performance or other kinds of issues on your computer if you have a 
large number of containers running.

