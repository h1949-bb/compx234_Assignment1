import threading
import time
import random

from printDoc import printDoc
from printList import printList

class Assignment1:
    # Simulation Initialisation parameters
    NUM_MACHINES = 50        # Number of machines that issue print requests
    NUM_PRINTERS = 5         # Number of printers in the system
    SIMULATION_TIME = 30     # Total simulation time in seconds
    MAX_PRINTER_SLEEP = 3    # Maximum sleep time for printers
    MAX_MACHINE_SLEEP = 5    # Maximum sleep time for machines
    QUEUE_MAX_SIZE = 5       # Maximum length

    # Initialise simulation variables
    def __init__(self):
        self.sim_active = True
        self.print_list = printList()  # Create an empty list of print requests
        self.mThreads = []             # list for machine threads
        self.pThreads = []             # list for printer threads
        self.empty = threading.Semaphore(self.QUEUE_MAX_SIZE) 
        self.mutex = threading.Lock()     
    def startSimulation(self):
        # Create Machine and Printer threads
        # Write code here
        # Start all the threads
        # Write code here
        for machine_id in range(self.NUM_MACHINES):
            m_thread=self.machineThread(machine_id,self)
            self.mThreads.append(m_thread)
            m_thread.start()
        for printer_id in range(self.NUM_PRINTERS):
            p_thread=self.printerThread(printer_id,self)
            self.pThreads.append(p_thread) 
            p_thread.start()
            
        # Let the simulation run for some time
        time.sleep(self.SIMULATION_TIME)

        # Finish simulation
        self.sim_active = False

        # Wait until all printer threads finish by joining them
        # Write code here
        for m_thread in self.mThreads:
                    m_thread.join()
        for p_thread in self.pThreads:
                    p_thread.join()
        print("所有线程已经退出，模拟结束")

    # Printer class
    class printerThread(threading.Thread):
        def __init__(self, printerID, outer):
            threading.Thread.__init__(self)
            self.printerID = printerID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Simulate printer taking some time to print the document
                self.printerSleep()
                # Grab the request at the head of the queue and print it
                # Write code here
                self.printDox(self.printerID)
                self.outer.empty.release()
            print(f"打印机{self.printerID}:模拟结束，处理其他..")
            while True:
                    doc=self.outer.print_list.queuePrint(self.printerID)
                    if not doc:
                        break
                    self.printerSleep()
                    self.outer.empty.release()

        def printerSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_PRINTER_SLEEP)
            time.sleep(sleepSeconds)

        def printDox(self, printerID):
           print(f"Printer ID: {printerID} : now available")
            # Print from the queue
           self.outer.print_list.queuePrint(printerID)

    # Machine class
    class machineThread(threading.Thread):
        def __init__(self, machineID, outer):
            threading.Thread.__init__(self)
            self.machineID = machineID
            self.outer = outer  # Reference to the Assignment1 instance

        def run(self):
            while self.outer.sim_active:
                # Machine sleeps for a random amount of time
                self.machineSleep()
                # Machine wakes up and sends a print request
                # Write code here
                self.printRequest(self.machineID)
                #creat the document and insert it to the list
                doc=printDoc(f"my name is machine{self.machineID}",self.machineID)
                self.outer.print_list.queueInsert(doc)

        def machineSleep(self):
            sleepSeconds = random.randint(1, self.outer.MAX_MACHINE_SLEEP)
            time.sleep(sleepSeconds)

        def printRequest(self, id):
           print(f"Machine {id} Sent a print request")
          # Build a print document
           doc = printDoc(f"My name is machine {id}", id)
           self.outer.empty.acquire()
            # 2. 加锁保证安全
           with self.outer.mutex:
                self.outer.print_list.queueInsert(doc)
    