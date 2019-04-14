'''
CS5250 Assignment 4, Scheduling policies simulator
Sample skeleton program
Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''

import sys
import logging

input_file = 'input.txt'

class Process:
    last_scheduled_time = 0

    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time

    # for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))


def FCFS_scheduling(process_list):
    # store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for process in process_list:
        if(current_time < process.arrive_time):
            current_time = process.arrive_time
        schedule.append((current_time,process.id))
        waiting_time = waiting_time + (current_time - process.arrive_time)
        current_time = current_time + process.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time


# Input: process_list, time_quantum (Positive Integer)
# Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
# Output_2 : Average Waiting Time
def RR_scheduling(process_list, time_quantum):
    # store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    ready_queue = []
    isCompleted = 0
    first = 0
    proc_length = len(process_list)

    while isCompleted < proc_length:
        allocated_list = []
        # a quantum end, read all arrived processes to the tail of ready queue
        for process in process_list:
            if current_time >= process.arrive_time:
                ready_queue.append(process)
                allocated_list.append(process)
                # process_list.remove(process)
                logging.debug("ready_queue info: %s", ready_queue)
                logging.info("process: [%s, %s, %s] -- append to the queue.", process.id, process.arrive_time, process.burst_time)
                logging.debug("cur waiting time: %s, cur time: %s", waiting_time, current_time)
                waiting_time = waiting_time + (current_time - process.arrive_time)

        # an extreme case, ready queue is null? later process arrive at future
        if not ready_queue:
            current_time = process_list[first].arrive_time
            for process in process_list:
                if current_time == process.arrive_time:
                    ready_queue.append(process)
                    # process_list.remove(process)
                    if process not in allocated_list:
                        allocated_list.append(process)

        for process in allocated_list:
            if process in process_list:
                process_list.remove(process)
        allocated_list = []

        # RR read the first process in the ready queue, process it with a quantum
        cur_process = ready_queue[first]
        ready_queue.remove(cur_process)

        schedule.append((current_time,cur_process.id))
        
        if cur_process.burst_time <= time_quantum:
            current_time = current_time + cur_process.burst_time
            # remove completed process from ready_queue, and complete ++
            isCompleted = isCompleted + 1
            waiting_time = waiting_time + len(ready_queue) * cur_process.burst_time
            logging.debug("ready_queue info: %s", ready_queue)
            logging.info("process: [%s, %s, %s]  -- Completed! cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
        else:
            # append to the tail of ready queue
            current_time = current_time + time_quantum
            # compute the remaining time of cur_process
            cur_process.burst_time = cur_process.burst_time - time_quantum

            waiting_time = waiting_time + len(ready_queue) * time_quantum

            # a quantum end, read all arrived processes to the tail of ready queue
            for process in process_list:
                if current_time >= process.arrive_time:
                    ready_queue.append(process)
                    # process_list.remove(process)
                    if process not in allocated_list:
                        allocated_list.append(process)
                    logging.debug("ready_queue info: %s", ready_queue)
                    logging.info("process: [%s, %s, %s] -- append to the queue.", process.id, process.arrive_time, process.burst_time)
                    logging.debug("cur waiting time: %s, cur time: %s", waiting_time, current_time)
                    waiting_time = waiting_time + (current_time - process.arrive_time)

            ready_queue.append(cur_process)
            logging.debug("ready_queue info: %s", ready_queue)
            logging.info("process: [%s, %s, %s]  -- a quantum processed. cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
        # remove allocated processes from process_list
        for process in allocated_list:
            if process in process_list:
                process_list.remove(process)

    average_waiting_time = waiting_time/float(proc_length)
    return schedule, average_waiting_time

def SRTF_scheduling(process_list):
    # store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    ready_queue = []
    isCompleted = 0
    isQueued = False
    first = 0
    proc_length = len(process_list)
    cur_process = process_list[first]
    schedule.append((current_time,cur_process.id))
    process_list.remove(cur_process)
    # print(cur_process)
    # print(" -- first process directly run.")
    logging.info("process: [%s, %s, %s]  -- first process directly run.", cur_process.id, cur_process.arrive_time, cur_process.burst_time)

    # initial operation
    for process in process_list:
        # 1. before new process arrive, schedule processes in CPU and ready queue
        while cur_process.burst_time < process.arrive_time - current_time:
            isCompleted = isCompleted + 1
            current_time = current_time + cur_process.burst_time
            waiting_time = waiting_time + cur_process.burst_time * len(ready_queue)
            cur_process.burst_time = 0
            # print(cur_process)
            # print(" -- Completed! cur_time: %s" % current_time)
            logging.info("process: [%s, %s, %s]  -- Completed! cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
            if ready_queue:
                # find smallest one from queue, remove process from ready queue
                smallest_burst_time = 10000
                for ready_process in ready_queue:
                    if ready_process.burst_time < smallest_burst_time:
                        smallest_burst_time = ready_process.burst_time
                        cur_process = ready_process
                ready_queue.remove(cur_process)
                schedule.append((current_time,cur_process.id))
                # print(cur_process)
                # print(" -- new process run. cur_time: %s" % current_time)
                logging.info("process: [%s, %s, %s]   -- new process run. cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
            else:
                # print("before new arrival, all schedule Completed! cur_time: %s" % current_time)
                logging.info("before new arrival, all schedule Completed! cur_time: cur_time: %s", current_time)
                break
        # 2. when new process arrive
        # 2.1: all previous process completed, schedule process
        if cur_process.burst_time == 0:
            cur_process = process
            schedule.append((current_time,cur_process.id))
            current_time = cur_process.arrive_time
            # print(cur_process)
            # print(" -- no previous process, schedule new coming one. cur_time: %s" % current_time)
            logging.info("process: [%s, %s, %s]  -- no previous process, schedule new coming one. cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
        # 2.2: exist current process, schedule smaller process
        else:
            cur_process.burst_time = cur_process.burst_time - (process.arrive_time - current_time)
            waiting_time = waiting_time + (process.arrive_time - current_time) * len(ready_queue)
            current_time = process.arrive_time
            if cur_process.burst_time > process.burst_time:
                ready_queue.append(cur_process)
                cur_process = process
                schedule.append((current_time,cur_process.id))
                # print(cur_process)
                # print(" -- new process is smaller preempt. cur_time: %s" % current_time)
                logging.info("process: [%s, %s, %s]  -- new process is smaller preempt. cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)
            else:
                ready_queue.append(process)
                # print(process)
                # print(" -- new process is bigger wait in ready_queue. cur_time: %s" % current_time)
                logging.info("process: [%s, %s, %s]  -- new process is bigger wait in ready_queue. cur_time: %s", process.id, process.arrive_time, process.burst_time, current_time)

    if cur_process.burst_time != 0:
        current_time = current_time + cur_process.burst_time
        waiting_time = waiting_time + len(ready_queue) * cur_process.burst_time
        isCompleted = isCompleted + 1
        # print(cur_process)
        # print(" -- Completed! cur_time: %s" % current_time)
        logging.info("process: [%s, %s, %s]  -- Completed! cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)

    while isCompleted < proc_length:
        # find smallest proc from ready_queue
        smallest_burst_time = 10000
        for ready_process in ready_queue:
            if ready_process.burst_time < smallest_burst_time:
                smallest_burst_time = ready_process.burst_time
                cur_process = ready_process
        ready_queue.remove(cur_process)
        schedule.append((current_time,cur_process.id))
        current_time = current_time + cur_process.burst_time
        waiting_time = waiting_time + len(ready_queue) * cur_process.burst_time
        isCompleted = isCompleted + 1
        # print(cur_process)
        # print(" -- Completed! cur_time: %s" % current_time)
        logging.info("process: [%s, %s, %s]  -- Completed! cur_time: %s", cur_process.id, cur_process.arrive_time, cur_process.burst_time, current_time)

    average_waiting_time = waiting_time/float(proc_length)
    return schedule, average_waiting_time


def SJF_scheduling(process_list, alpha):
    # predict equation: y_{n+1} = \alpha * t_n + (1 - \alpha) * y_n
    schedule = []
    current_time = 0
    waiting_time = 0
    ready_queue = []
    isCompleted = 0
    isQueued = False
    first = 0
    proc_length = len(process_list)
    cur_process = process_list[first]

    pid_set = set([process.id for process in process_list])
    prev_est_time = dict.fromkeys(pid_set, 10)
    prev_act_time = dict.fromkeys(pid_set, 0)

    while isCompleted < proc_length:
        allocated_list = []
        # Current process completed, append arrived process to the ready_queue
        for process in process_list:
            if current_time >= process.arrive_time:
                ready_queue.append(process)
                # process_list.remove(process)
                if process not in allocated_list:
                    allocated_list.append(process)
                waiting_time = waiting_time + (current_time - process.arrive_time)
                print(process)
                print(" -- append to the queue. cur_time: %s" % current_time)

        # an extreme case, ready queue is null? later process arrive at future
        if not ready_queue:
            current_time = process_list[first].arrive_time
            for process in process_list:
                if current_time == process.arrive_time:
                    ready_queue.append(process)
                    # process_list.remove(process)
                    if process not in allocated_list:
                        allocated_list.append(process)

        for process in allocated_list:
            if process in process_list:
                process_list.remove(process)

        allocated_list = []

        # find shortest process in ready queue, update the shortest process prev esti time
        smallest_burst_time = 10000
        for ready_process in ready_queue:
            if prev_act_time[ready_process.id] == 0:
                est_time = prev_est_time[ready_process.id]
            # est_time = cur_process.burst_time * alpha + (1 - alpha) * prev_est_time[ready_process.id]
            else:
                est_time = prev_act_time[ready_process.id] * alpha + (1 - alpha) * prev_est_time[ready_process.id]
            if est_time < smallest_burst_time:
                smallest_burst_time = est_time
                cur_process = ready_process
        ready_queue.remove(cur_process)
        prev_est_time[cur_process.id] = smallest_burst_time
        prev_act_time[cur_process.id] = cur_process.burst_time
        schedule.append((current_time,cur_process.id))
        current_time = current_time + cur_process.burst_time
        waiting_time = waiting_time + len(ready_queue) * cur_process.burst_time
        isCompleted = isCompleted + 1
        print(cur_process)
        print(" -- Completed! prev_est_time: %s, prev_act_time: %s, cur_time: %s" % (cur_process.burst_time ,smallest_burst_time , current_time))
        # remove allocated processes from process_list
        for process in allocated_list:
            if process in process_list:
                process_list.remove(process)

    average_waiting_time = waiting_time/float(proc_length)
    return schedule, average_waiting_time


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array)!= 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result


def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)
    # print ("simulating FCFS ----")
    # FCFS_schedule, FCFS_avg_waiting_time =  FCFS_scheduling(process_list)
    # write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )

    # print ("simulating RR ----")
    # process_list = read_input()
    # RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum=2)
    # write_output('RR.txt', RR_schedule, RR_avg_waiting_time)

    # find optimal time quantum
    # minimum_RR_avg_waiting_time = 10000
    # minimum_RR_schedule = []
    # minimum_time_quantum = 0
    # for time_quantum in range(1, 11):
    #     print ("simulating RR ----")
    #     process_list = read_input()
    #     RR_schedule, RR_avg_waiting_time =  RR_scheduling(process_list,time_quantum)
    #     if RR_avg_waiting_time < minimum_RR_avg_waiting_time:
    #         minimum_RR_avg_waiting_time = RR_avg_waiting_time
    #         minimum_RR_schedule = RR_schedule
    #         minimum_time_quantum = time_quantum
    # print("minimum time quantum: %s" % minimum_time_quantum)
    # write_output('RR.txt', minimum_RR_schedule, minimum_RR_avg_waiting_time)

    # print ("simulating SRTF ----")
    # process_list = read_input()
    # SRTF_schedule, SRTF_avg_waiting_time =  SRTF_scheduling(process_list)
    # write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )

    # print ("simulating SJF ----")
    # process_list = read_input()
    # SJF_schedule, SJF_avg_waiting_time =  SJF_scheduling(process_list, alpha = 0.5)
    # write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

    # find optimal alpha
    minimum_SJF_avg_waiting_time = 10000
    minimum_SJF_schedule = []
    minimum_alpha = 0.0
    for alpha in range(0, 11):
        print("simulating SJF ----")
        process_list = read_input()
        SJF_schedule, SJF_avg_waiting_time = SJF_scheduling(process_list, alpha/float(10))
        if SJF_avg_waiting_time < minimum_SJF_avg_waiting_time:
            minimum_SJF_avg_waiting_time = SJF_avg_waiting_time
            minimum_SJF_schedule = SJF_schedule
            minimum_alpha = alpha/float(10)
        print("minimum alpha: %s" % minimum_alpha)
        write_output('SJF.txt', minimum_SJF_schedule, minimum_SJF_avg_waiting_time)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])

