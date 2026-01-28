import os
import time
from multiprocessing import Process, Pipe

# ---------------- CHILD FUNCTIONS (TOP-LEVEL ONLY) ---------------- #

def child_task(task_name, duration):
    """Task executed by child process"""
    pid = os.getpid()
    ppid = os.getppid()
    print(f"[Child Process] {task_name}")
    print(f"  PID: {pid}, Parent PID: {ppid}")
    print(f"  Executing for {duration} seconds...")
    time.sleep(duration)
    print(f"[Child Process] {task_name} completed!")


def child_sender(conn, message):
    """Child process sends data to parent using Pipe"""
    pid = os.getpid()
    result = f"Processed by PID {pid}: {message.upper()}"
    conn.send(result)
    conn.close()


def worker():
    """Worker process for process states demo"""
    time.sleep(2)


# ---------------- DEMONSTRATION FUNCTIONS ---------------- #

def demonstrate_process_creation():
    print("\n=== Process Creation Demonstration ===")
    print(f"Parent Process PID: {os.getpid()}\n")

    tasks = [
        ("Database Backup", 2),
        ("Log Analysis", 1),
        ("Cache Cleanup", 3)
    ]

    processes = []

    for task_name, duration in tasks:
        p = Process(target=child_task, args=(task_name, duration))
        p.start()
        processes.append(p)
        print(f"Created process {p.pid} for {task_name}")

    print("\n[Parent] Waiting for child processes...\n")

    for p in processes:
        p.join()
        print(f"[Parent] Process {p.pid} exited with code {p.exitcode}")

    print("[Parent] All child processes completed!")


def demonstrate_process_communication():
    print("\n=== Process Communication (Pipe) ===")

    parent_conn, child_conn = Pipe()

    p = Process(
        target=child_sender,
        args=(child_conn, "hello from parent")
    )
    p.start()

    received = parent_conn.recv()
    print(f"Parent received: {received}")

    p.join()
    print(f"Child process {p.pid} completed")


def demonstrate_process_states():
    print("\n=== Process States Demonstration ===")

    p = Process(target=worker)

    print(f"State after creation: {'Alive' if p.is_alive() else 'Not started'}")

    p.start()
    print(f"State after start: {'Running' if p.is_alive() else 'Terminated'}")
    print(f"Process PID: {p.pid}")

    p.join(timeout=1)
    print(f"State during execution: {'Still running' if p.is_alive() else 'Completed'}")

    p.join()
    print(f"State after termination: {'Running' if p.is_alive() else 'Terminated'}")
    print(f"Exit code: {p.exitcode}")


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    print("OPERATING SYSTEMS - PROCESS CONTROL DEMONSTRATION")
    print("=" * 60)

    demonstrate_process_creation()
    demonstrate_process_communication()
    demonstrate_process_states()

    print("=" * 60)
    print("Process Control Demonstration Completed!")
