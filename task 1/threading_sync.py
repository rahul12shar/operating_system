import threading
import time
import random
from queue import Queue

# Shared resource (demonstrates race condition)
shared_counter = 0
counter_lock = threading.Lock()

# Bank account for demonstrating synchronization
class BankAccount:
    def __init__(self, balance=1000):
        self.balance = balance
        self.lock = threading.Lock()
    
    def deposit(self, amount, customer):
        with self.lock:  # Acquire lock
            print(f"[{customer}] Depositing ${amount}")
            current = self.balance
            time.sleep(0.1)  # Simulate processing delay
            self.balance = current + amount
            print(f"[{customer}] New balance: ${self.balance}")
    
    def withdraw(self, amount, customer):
        with self.lock:  # Acquire lock
            print(f"[{customer}] Withdrawing ${amount}")
            if self.balance >= amount:
                current = self.balance
                time.sleep(0.1)  # Simulate processing delay
                self.balance = current - amount
                print(f"[{customer}] New balance: ${self.balance}")
            else:
                print(f"[{customer}] Insufficient funds!")

def demonstrate_basic_threads():
    """Demonstrate basic thread creation and execution"""
    print("=== Basic Threading ===")
    
    def worker(name, duration):
        print(f"Thread {name}: Starting")
        time.sleep(duration)
        print(f"Thread {name}: Finished after {duration}s")
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"T{i+1}", i+1))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print("All threads completed!\n")

def demonstrate_race_condition():
    """Demonstrate race condition without synchronization"""
    print("=== Race Condition (Without Lock) ===")
    
    global shared_counter
    shared_counter = 0
    
    def increment_unsafe():
        global shared_counter
        for _ in range(100000):
            temp = shared_counter
            temp += 1
            shared_counter = temp
    
    threads = [threading.Thread(target=increment_unsafe) for _ in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Expected: 500000, Got: {shared_counter}")
    print(f"Lost updates due to race condition!\n")

def demonstrate_mutex_lock():
    """Demonstrate proper synchronization with mutex"""
    print("=== Mutex Lock (Safe Increment) ===")
    
    global shared_counter
    shared_counter = 0
    
    def increment_safe():
        global shared_counter
        for _ in range(100000):
            with counter_lock:
                temp = shared_counter
                temp += 1
                shared_counter = temp
    
    threads = [threading.Thread(target=increment_safe) for _ in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"Expected: 500000, Got: {shared_counter}")
    print(f"Correct result with mutex!\n")

def demonstrate_bank_transactions():
    """Demonstrate thread-safe bank operations"""
    print("=== Bank Account (Thread-Safe) ===")
    
    account = BankAccount(balance=1000)
    
    def customer_transactions(name):
        account.deposit(100, name)
        time.sleep(0.05)
        account.withdraw(50, name)
    
    customers = ["Alice", "Bob", "Charlie"]
    threads = [threading.Thread(target=customer_transactions, args=(name,)) 
               for name in customers]
    
    print(f"Initial balance: ${account.balance}\n")
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"\nFinal balance: ${account.balance}")
    print(f"Expected: ${1000 + (100-50)*3} = $1150\n")

def demonstrate_semaphore():
    """Demonstrate semaphore for limiting concurrent access"""
    print("=== Semaphore (Limited Resources) ===")
    
    # Only 2 threads can access resource simultaneously
    semaphore = threading.Semaphore(2)
    
    def access_resource(thread_id):
        print(f"Thread {thread_id}: Waiting for resource...")
        
        with semaphore:
            print(f"Thread {thread_id}: ✓ Acquired resource")
            time.sleep(2)  # Use resource
            print(f"Thread {thread_id}: ✗ Released resource")
    
    threads = [threading.Thread(target=access_resource, args=(i,)) 
               for i in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print("All threads completed!\n")

def demonstrate_producer_consumer():
    """Demonstrate producer-consumer pattern"""
    print("=== Producer-Consumer Pattern ===")
    
    buffer = Queue(maxsize=3)
    
    def producer():
        for i in range(5):
            item = f"Item-{i}"
            buffer.put(item)
            print(f"Producer: Added {item} (Buffer size: {buffer.qsize()})")
            time.sleep(random.uniform(0.1, 0.5))
    
    def consumer(name):
        while True:
            try:
                item = buffer.get(timeout=2)
                print(f"Consumer {name}: Consumed {item}")
                buffer.task_done()
                time.sleep(random.uniform(0.2, 0.8))
            except:
                break
    
    # Start producer
    p_thread = threading.Thread(target=producer)
    p_thread.start()
    
    # Start consumers
    c_threads = [threading.Thread(target=consumer, args=(f"C{i}",)) 
                 for i in range(2)]
    for t in c_threads:
        t.start()
    
    # Wait for completion
    p_thread.join()
    buffer.join()
    
    print("Production and consumption completed!\n")

def demonstrate_thread_info():
    """Display thread information"""
    print("=== Thread Information ===")
    
    def sample_thread():
        print(f"Thread Name: {threading.current_thread().name}")
        print(f"Thread ID: {threading.get_ident()}")
        print(f"Active Threads: {threading.active_count()}")
    
    t = threading.Thread(target=sample_thread, name="SampleWorker")
    t.start()
    t.join()
    
    print()

if __name__ == "__main__":
    print("OPERATING SYSTEMS - THREADING AND SYNCHRONIZATION")
    print("=" * 60 + "\n")
    
    demonstrate_basic_threads()
    demonstrate_race_condition()
    demonstrate_mutex_lock()
    demonstrate_bank_transactions()
    demonstrate_semaphore()
    demonstrate_producer_consumer()
    demonstrate_thread_info()
    
    print("=" * 60)
    print("Threading and Synchronization Demonstration Completed!")