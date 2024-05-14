# Round Robin CPU Scheduling in Python
This program simulates the Round Robin CPU scheduling algorithm for 3 to 10 processes. 
![image](https://github.com/ChannKK/rr-cpu-scheduling/assets/91399951/890d1e36-5e31-45a7-a534-47a9735e6edb)


## Features

- Collects process information (ID, arrival time, burst time) and time quantum from the user.
- Calculates the scheduling timeline using the specified time quantum.
- Outputs a table displaying various process metrics including turnaround time and waiting time.
- Generates a Gantt chart visualizing the execution order of processes.

## Dependencies

- Python 3.x
- `tabulate` library
- `matplotlib` library
- `pandas` library

## Usage
1. Run the script.
```
python RoundRobin.py
```
2. Enter the number of processes (between 3 and 10).
3. For each process, enter:
   - Process ID
   - Arrival Time
   - Burst Time
4. Enter time quantum.
   
   ![image](https://github.com/ChannKK/rr-cpu-scheduling/assets/91399951/11d84a74-9e19-4681-a5da-1c5ca252826e)
6. The program will calculate and display the following:
   - A table with process information, including turnaround time and waiting time.
   - The average turnaround time and waiting time.
   - A Gantt chart showing the execution order of processes.
     
   ![image](https://github.com/ChannKK/rr-cpu-scheduling/assets/91399951/0f5aff6b-2ccd-43bd-b267-eb21d7da3c48)
  ![image](https://github.com/ChannKK/rr-cpu-scheduling/assets/91399951/7b3951da-53f9-4eb6-9389-62392b8963b8)


