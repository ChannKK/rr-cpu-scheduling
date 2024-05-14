# RoundRobin.py
# Round Robin Scheduling - KK

from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

class RoundRobin:

    def process_Info(self, noOfProcess):
        processInfo = []
        for n in range(noOfProcess):
            temp = []
            processID = input("Enter Process ID: ")
            arrivalTime = int(input(f"Enter Arrival Time for Process {processID}: "))
            burstTime = int(input(f"Enter Burst Time for Process {processID}: "))
            temp.extend([processID, arrivalTime, burstTime, 0, burstTime]) # 0 = not executed, 1 = executed
            processInfo.append(temp)

        timeQuantum = int(input("Enter Time Quantum: "))
        startTime, endTime, execProcess = RoundRobin.calc_process(self, processInfo, timeQuantum)

        taTime = RoundRobin.calc_ta_time(self, processInfo)
        waitTime = RoundRobin.calc_wait_time(self, processInfo)

        print()
        print("Calculation table: ")
        # print calc table
        RoundRobin.res_table(self, processInfo, taTime, waitTime, execProcess)

        # generate gantt chart
        timeline = self.generate_timeline(startTime, endTime)
        gantt_chart(execProcess, timeline)

    def calc_process(self, processInfo, timeQuantum):
        startTime = []
        endTime = []
        execProcess = []
        readyQueue = []
        currentTime = min(processInfo, key=lambda x: x[1])[1] 
        processInfo.sort(key=lambda x: x[1]) # sort process in ascending arrival time
        while 1:
            oriQueue = []
            temp = []

            for a in range(len(processInfo)):
                if processInfo[a][1] <= currentTime and processInfo[a][3] == 0:
                    exist = 0
                    if len(readyQueue) != 0:
                        for c in range(len(readyQueue)):
                            if processInfo[a][0] == readyQueue[c][0]:
                                exist = 1
                    
                    # add to readyQueue if not in it
                    if exist == 0: 
                        temp.extend([processInfo[a][0], processInfo[a][1], processInfo[a][2], processInfo[a][4]])
                        readyQueue.append(temp)
                        temp = []
                    
                    if len(readyQueue) != 0 and len(execProcess) != 0:
                        for c in range(len(readyQueue)):
                            if readyQueue[c][0] == execProcess[len(execProcess) - 1]:
                                readyQueue.insert((len(readyQueue) - 1), readyQueue.pop(c))

                elif processInfo[a][3] == 0:
                    temp.extend([processInfo[a][0], processInfo[a][1], processInfo[a][2], processInfo[a][4]])
                    oriQueue.append(temp)
                    temp = []
            if len(readyQueue) == 0 and len(oriQueue) == 0:
                break
            if len(readyQueue) != 0:
                if readyQueue[0][2] > timeQuantum:
                    # if burstTime > timeQuantum -> execute timeQuantum
                    startTime.append(currentTime)
                    currentTime = currentTime + timeQuantum
                    finExecTime = currentTime
                    endTime.append(finExecTime)
                    execProcess.append(readyQueue[0][0])
                    for b in range(len(processInfo)):
                        if processInfo[b][0] == readyQueue[0][0]:
                            break
                    processInfo[b][2] = processInfo[b][2] - timeQuantum
                    readyQueue.pop(0)
                
                # if burstTime < timeQuantum -> execute burstTime
                elif readyQueue[0][2] <= timeQuantum:
                    startTime.append(currentTime)
                    currentTime = currentTime + readyQueue[0][2]
                    finExecTime = currentTime
                    endTime.append(finExecTime)
                    execProcess.append(readyQueue[0][0])
                    for b in range(len(processInfo)):
                        if processInfo[b][0] == readyQueue[0][0]:
                            break
                    processInfo[b][2] = 0
                    processInfo[b][3] = 1
                    processInfo[b].append(finExecTime)
                    readyQueue.pop(0)
            elif len(readyQueue) == 0:
                if currentTime < oriQueue[0][1]:
                    currentTime = oriQueue[0][1]

                # if bt > time quantum
                if oriQueue[0][2] > timeQuantum: 
                    startTime.append(currentTime)
                    currentTime = currentTime + timeQuantum
                    finExecTime = currentTime
                    endTime.append(finExecTime)
                    execProcess.append(oriQueue[0][0])
                    for b in range(len(processInfo)):
                        if processInfo[b][0] == oriQueue[0][0]:
                            break
                    processInfo[b][2] = processInfo[b][2] - timeQuantum

                # bt < time quantum
                elif oriQueue[0][2] <= timeQuantum: 
                    startTime.append(currentTime)
                    currentTime = currentTime + oriQueue[0][2]
                    finExecTime = currentTime
                    endTime.append(finExecTime)
                    execProcess.append(oriQueue[0][0])
                    for b in range(len(processInfo)):
                        if processInfo[b][0] == oriQueue[0][0]:
                            break
                    processInfo[b][2] = 0 #bt = 0
                    processInfo[b][3] = 1 #state of process (1=executed, 0=not executed)
                    processInfo[b].append(finExecTime)
        taTime = RoundRobin.calc_ta_time(self, processInfo)
        waitTime = RoundRobin.calc_wait_time(self, processInfo)
        return startTime, endTime, execProcess

    def calc_ta_time(self, processInfo):
        totalTA = 0
        for n in range(len(processInfo)):
            turnaround_time = processInfo[n][5] - processInfo[n][1] # ta = et - at
            totalTA = totalTA + turnaround_time
            processInfo[n].append(turnaround_time)
        avgTA = totalTA / len(processInfo)
        return avgTA

    def calc_wait_time(self, processInfo):
        totalWait = 0
        for n in range(len(processInfo)):
            wt = processInfo[n][6] - processInfo[n][4] # wt = ta - bt
            totalWait = totalWait + wt
            processInfo[n].append(wt)
        avgWT = totalWait / len(processInfo)
        return avgWT

    def res_table(self, processInfo, avgTA, avgWT, execProcess):
        processInfo.sort(key=lambda x: x[0]) # sort according processID
        headers = ["Process ID", "Arrival Time", "Burst Time", "Finishing Time", "Turnaround Time", "Waiting Time"]
        data = [[
            processInfo[n][0],
            processInfo[n][1],
            processInfo[n][4],
            processInfo[n][5],
            processInfo[n][6],
            processInfo[n][7]
        ] for n in range(len(processInfo))]

        sumTA = sum(p[6] for p in processInfo)
        sumWT = sum(p[7] for p in processInfo)

        sumRow = ["Total", "", "", "", sumTA, sumWT]
        data.append(sumRow)

        colalign = ['center'] * len(headers)
        print(tabulate(data, headers=headers, tablefmt="grid", colalign=colalign))

        print(f"\nAverage Turnaround Time: {sumTA} / {len(processInfo)} = {avgTA}\n")
        print(f'Average Waiting Time: {sumWT} / {len(processInfo)} = {avgWT}')
        print()

    def generate_timeline(self, startTime, endTime):
        timeline = []
        for a in range(len(startTime)):
            timeline.extend([startTime[a], endTime[a]])
        return timeline

def gantt_chart(execProcess, timeline):
    gantt_chart = []
    dataFrame = pd.DataFrame({'Start': timeline[::2], 'End': timeline[1::2], 'Process': execProcess})
    
    fig, axis = plt.subplots()
    axis.set_title("Round Robin Gantt Chart")

    for row in dataFrame.index:
        xStart = dataFrame['Start'][row]  # x axis for starting
        xWidth = abs(dataFrame['End'][row] - xStart)
        rectColor = 'Blue' if row % 2 == 0 else 'Orange'   
        rect = Rectangle(xy=(xStart, 0),
                         width=xWidth,
                         height=0.5,
                         color=rectColor)
        axis.add_patch(rect)
        processID = dataFrame['Process'][row]
        text = axis.text(xStart + xWidth/ 2, 0.25, f'P{processID}', ha='center', va='center', color='white', fontsize=10)
       
    axis.set_xlim([0, max(dataFrame['End']) + 1])
    axis.set_ylim([0, 3])

    # x-axis label
    axis.set_xticks(range(1, max(dataFrame['End']) + 2))  # Start from 1 and ascend by 1 unit
    axis.set_xticklabels(range(1, max(dataFrame['End']) + 2))

    plt.show()

if __name__ == "__main__":
    while True:
        noOfProcess = int(input("Enter number of processes (between 3 and 10): "))
        if 3 <= noOfProcess <= 10:
            break
        else:
            print("Please enter a number of processes between 3 and 10.\n")

    rr = RoundRobin()
    rr.process_Info(noOfProcess)
    
