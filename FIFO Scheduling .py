

class process:
    def __init__(self):
        self.process_no = -1
        self.exe_time = -1
        self.arival_time = -1
        self.departure_time = -1
        self.exe_left = -1
        self.input = -1
        self.input_left = -1
        self.take_input = -1
        self.waiting_time = -1
        self.waiting_time_left = -1


def time_increment(time):
    t=0
    for i in range(10000):
        t=0
    time+=1
    return time



class process_queue:

    def __init__(self):
        self.max_size = 100
        self.data = [process() for i in range(100)]
        self.front = -1
        self.rear = -1
        self.average_waiting_time = 0
        self.average_turnaround_time = 0


    def enqueue(self,x):                        # add an element to the rear of queue
        self.rear = (self.rear + 1) % self.max_size
        self.data[self.rear] = x
        if self.front == -1:
            self.front = 0

    def dequeue(self):                          # delete the element at the front of queue
        if self.front == -1:
            print"Queue Is Empty...\n"
        elif self.front != self.rear:
            temp = self.front
            self.front = (self.front + 1) % self.max_size
            return self.data[temp]
        else:
            temp = self.front
            self.front = -1
            self.rear = -1
            return self.data[temp]

    def clear(self):                             # clear the queue
        self.front = -1
        self.rear = -1


    def is_empty(self):
        return self.front == -1

    def decrement(self,time):
        if self.is_empty():
            return

        while self.front <= self.rear:
            if self.data[self.front].exe_left == 0:
                self.data[self.front].departure_time = time
                print("  %d              %d                  %d                   %d                   %d                    %d" % ( self.data[self.front].process_no , self.data[self.front].exe_time , self.data[self.front].arival_time , self.data[self.front].departure_time , self.data[self.front].departure_time - self.data[self.front].arival_time - self.data[self.front].exe_time , self.data[self.front].departure_time - self.data[self.front].arival_time))

                self.average_waiting_time += self.data[self.front].departure_time - self.data[self.front].arival_time - self.data[self.front].exe_time
                self.average_turnaround_time += self.data[self.front].departure_time - self.data[self.front].arival_time

                if self.front != self.rear:
                    self.front += 1
                else:
                    self.front = -1
                    self.rear = -1
            else:
                self.data[self.front].exe_left -= 1
                if self.data[self.front].take_input > 0:
                    self.data[self.front].input_left -= 1
                return




time = 0
ready_queue = process_queue()
new_queue = [process() for i in range(100)]
waiting_queue = [process() for i1 in range(100)]

no_of_process = input("Enter Number of Process : ")

for i in range(no_of_process):                                     # Taking input
    print "Enter Process " , i , " Information"
    new_queue[i].exe_time = input("Enter Burst Time : ")
    new_queue[i].arival_time = input("Enter Arrival Time : ")
    new_queue[i].take_input = input("Is the Process Takes Input (0/1): ")
    if new_queue[i].take_input:
        new_queue[i].input = input("Enter The Time After Which The Process goes for Input : ")
        new_queue[i].waiting_time = input("How Much Time It Will Spend in Waiting Queue : ")
    else:
        new_queue[i].input = -1
    new_queue[i].exe_left = new_queue[i].exe_time
    new_queue[i].input_left = new_queue[i].input
    new_queue[i].process_no = i
    #print("  %d              %d                  %d                   %d                   %d                    %d" % ( temp.process_no , temp.exe_time , temp.arival_time ,temp.departure_time , temp.departure_time - temp.arival_time - temp.exe_time ,temp.departure_time - temp.arival_time))
    #new_queue[i] = temp                                          # After Input Each Process is in new queue

print("Process        Bust Time        Arrival Time        Departure Time        Waiting Time        Turnaround Time")


#for i3 in range(no_of_process):
    #print("  %d              %d                  %d                   %d                   %d                    %d" % ( new_queue[i3].process_no , new_queue[i3].exe_time , new_queue[i3].arival_time ,new_queue[i3].departure_time , new_queue[i3].departure_time - new_queue[i3].arival_time - new_queue[i3].exe_time ,new_queue[i3].departure_time - new_queue[i3].arival_time))


count = 0                       #It Will contain the no of process transfer from new queue to ready queue
no_of_processes_in_waiting_queue = 0

while (count != no_of_process) or  (not ready_queue.is_empty()) or (no_of_processes_in_waiting_queue > 0):             # Checking That if All Queues Are empty just stop
    # This Loop Will Load Process from new queue to ready queue
    for i in range(no_of_process):
        if new_queue[i].arival_time == time:
            ready_queue.enqueue(new_queue[i])
            count+=1
    
    
    # this loop will transfer the process from waiting queue to ready queue
    for i in range(no_of_processes_in_waiting_queue):
        if waiting_queue[i].waiting_time_left == 0:
            ready_queue.enqueue(waiting_queue[i])
            no_of_processes_in_waiting_queue -= 1
            for i2 in range(i , no_of_processes_in_waiting_queue):
                waiting_queue[i2] = waiting_queue[i2+1]


    # This Condition Will Shift A process from ready queue to waiting queue
    if ready_queue.data[ready_queue.front].take_input > 0:
       if ready_queue.data[ready_queue.front].input_left <= 0 and ready_queue.data[ready_queue.front].exe_left != 0:
            if ready_queue.data[ready_queue.front].waiting_time > 0:
                waiting_queue[no_of_processes_in_waiting_queue] = ready_queue.dequeue()
                waiting_queue[no_of_processes_in_waiting_queue].input_left = waiting_queue[no_of_processes_in_waiting_queue].input              # Again Assigning input time so it can come back for input
                waiting_queue[no_of_processes_in_waiting_queue].waiting_time_left = waiting_queue[no_of_processes_in_waiting_queue].waiting_time
                no_of_processes_in_waiting_queue += 1

    # This Loop Will Decrement the waiting time left of all processes by 1 in waiting queue
    for i in range(no_of_processes_in_waiting_queue):
        waiting_queue[i].waiting_time_left -= 1
        #print "Waiting queue process time left : " , waiting_queue[i].waiting_time_left

    ready_queue.decrement(time)

    time = time_increment(time)  # Increment in clock

# For Average Waiting And Turnaround time

print
print
print("Average Waiting Time = %f"  % ( float (ready_queue.average_waiting_time)/ float (no_of_process)))
print("Average Turnaround Time = %f"  % ( float (ready_queue.average_turnaround_time)/ float (no_of_process)))

