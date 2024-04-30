# Question 1:

#### Difference between CMD and ENTRYPOINT?

- **CMD**: When used separately, whatever is passed from the command line interface (CLI) will completely replace the specified command.
- **ENTRYPOINT**: When used separately, whatever is passed from the CLI will be appended to the specified command.
- **Combined Usage**:
  
  - **Case 1 (No argument passed from CLI)**:
    - `ENTRYPOINT ["ls"]`
    - `CMD ["-l"]`
    - Command executed: `ls -l`
  - **Case 2 (Argument "-S" passed from CLI)**:
    - `ENTRYPOINT ["ls","-a"]`
    - `CMD ["-l"]`
    - Command executed: `ls -a -S`
- In Case 1, when no argument is passed from the CLI, the command `ls -l` is executed, where `-l` is provided by the CMD.
- In Case 2, when the argument `-S` is passed from the CLI, it is appended to the ENTRYPOINT command `ls -a`, resulting in the command `ls -a -S`. The CMD part (`-l`) remains unchanged.


