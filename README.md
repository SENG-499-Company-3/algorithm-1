# Algorithm-1
To create the container in Windows (Powershell), MacOS (intel zsh) 
  and Linux (Bash):

```
  docker compose up
```
  
  

To run the container: 
```
  docker compose run api
```


To create a virtual environment and download the necessary packages inside:
```
  conda create --name algo1 python=3.10
  conda activate algo1
  pip3 install -r requirements.txt 
```



***NOTE***:
Closing shells running the container will *not* shut down the container. 
To shut down the container please type 'exit' into the container shell
to close the container properly. Improper shut down could lead to 
performance or other kinds of issues on your computer if you have a 
large number of containers running.

