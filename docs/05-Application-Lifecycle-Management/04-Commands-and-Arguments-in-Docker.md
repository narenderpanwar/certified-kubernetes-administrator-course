# Commands and Arguments in Docker

- Take me to [Video Tutorial](https://kodekloud.com/topic/commands-and-arguments-in-docker/)

In this section, we will take a look at commands and arguments in docker

- To run a docker container
  
  ```
  $ docker run ubuntu
  ```
- To list running containers
  
  ```
  $ docker ps
  ```
- To list all containers including that are stopped
  
  ```
  $ docker ps -a
  ```
  
  ![dc](../../images/dc.PNG)

#### Unlike virtual machines, containers are not meant to host operating system.

- Containers are meant to run a specific task or process such as to host an instance of a webserver or application server or a database server etc.
  
  ![ex](../../images/ex.PNG)

#### How do you specify a different command to start the container?

- One Option is to append a command to the docker run command and that way it overrides the default command specified within the image.
  
  ```
  $ docker run ubuntu sleep 5
  ```
- This way when the container starts it runs the sleep program, waits for 5 seconds and then exists. How do you make that change permanent?
  
  ![sleep](../../images/sleep.PNG)
- There are different ways of specifying the command either the command simply as is in a shell form or in a JSON array format.
  
  ![sleep1](../../images/sleep1.PNG)
- Now, build the docker image
  
  ```
  $ docker build -t ubuntu-sleeper .
  ```
- Run docker container
  
  ```
  $ docker run ubuntu-sleeper
  ```
  
  ![sleep2](../../images/sleep2.PNG)

---

# Commands and Arguments in Docker Containers

## 1. Introduction to Containers:

- Containers are not meant to host an entire operating system but to execute specific tasks or processes.
- They exit once the task is complete.

## 2. Defining Processes in Containers:

- Docker files contain instructions like CMD which specify the program to run inside the container.
- Examples - NGINX's CMD is `["nginx"]` and MySQL's CMD `["mysqld"]`

## 3. Default Command Behavior:

- Default behavior for running a plain Ubuntu container involves launching the bash program.
- Bash exits if no terminal is found, causing the container to exit.

## 4. Overriding Default Commands:

- To specify a different command, append it to the Docker run command, overriding the default.
- Example: `docker run Ubuntu sleep 5` runs the sleep program for five seconds.

## 5. Permanent Changes with Custom Images:

- Create a custom image from the base Ubuntu image with a new command.
- Specify commands in JSON array format or shell form.
- Ensure command and parameters are separate elements in the list.

## 6. Entry Point Instruction:

- Similar to CMD, specifies the program to run at container start.
- Command line parameters are appended to the entry point.
- Difference: CMD parameters replace entirely, while entrypoint parameters are appended.

## 7. Configuring Default Values:

- Use both entry point and command instructions.
- Command instruction is appended to the entry point.
- Specify default values in JSON format, overriding with command line parameters.

## 8. Runtime Modifications:

- Override entry point during runtime using the entry point option in Docker run command.
- Allows for modifying the command at startup.

  

----

- https://docs.docker.com/engine/reference/builder/#cmd

