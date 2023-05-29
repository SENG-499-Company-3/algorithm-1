# Algorithm-1
To create the container in Windows (Powershell), MacOS (intel zsh) 
  and Linux (Bash):

```
  docker build -t algorithm-1 -f Dockerfile . \
    --build-arg OS_TYPE={host architecture} \
    --build-arg OS={linux distro} \
    --build-arg OS_VER={os version}
```
  
  

To run the container: 
```
  docker compose up
```


To create a virtual environment and download the necessary packages:
```
  conda create --name algo1 python=3.10
  pip3 install -r requirements.txt 
```



***NOTE***
Closing shells running the container will *not* shut down the container. 
To shut down the container please type 'exit' into the container shell
to close the container properly. Improper shut down could lead to 
performance or other kinds of issues on your computer if you have a 
large number of containers running.

