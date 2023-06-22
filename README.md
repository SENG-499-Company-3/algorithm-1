# Algorithm-1
To create the container in Windows (Powershell), macOS (intel zsh) 
  and Linux (Bash) - DEPLOYMENT:

```shell
  docker compose up
```

To create a virtual environment and download the necessary packages inside - LOCAL TESTING:
```shell
  conda create --name algo1 python=3.10
  conda activate algo1
  pip3 install -r requirements.txt 
```


To create an apptainer container on a DRAC cluster - TRAINING:
```shell
  cd ~/scratch
  salloc --mem-per-cpu=2000 --cpus-per-task=4 --time=2:0:0
  module load singularity
  singularity build ray.sif docker://ray:latest
  singularity run ray.sif
```


###### ***NOTE***:
Closing shells running the container will *not* shut down the container. 
To shut down the container please type 'exit' into the container shell
to close the container properly. Improper shut down could lead to 
performance or other kinds of issues on your computer if you have a 
large number of containers running.




Please check GitHub Actions to see linting warnings.

[![GitHub Super-Linter](https://github.com/SENG-499-Company-3/algorithm-1/actions/workflows/gh-super-linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)
