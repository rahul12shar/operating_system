import os
import sys
import platform
import subprocess

class DeviceManager:
    """Manages device access and system I/O operations"""
    
    def __init__(self):
        self.platform = platform.system()
    
    def get_system_info(self):
        """Retrieve comprehensive system information"""
        print("=== SYSTEM INFORMATION ===")
        print(f"Platform: {platform.system()}")
        print(f"Platform Version: {platform.version()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Processor: {platform.processor()}")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Hostname: {platform.node()}")
    
    def list_mounted_devices(self):
        """List all mounted devices/partitions"""
        print("\n=== MOUNTED DEVICES/PARTITIONS ===")
        
        try:
            import psutil
            
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                print(f"\nDevice: {partition.device}")
                print(f"  Mountpoint: {partition.mountpoint}")
                print(f"  Filesystem: {partition.fstype}")
                print(f"  Options: {partition.opts}")
                
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    print(f"  Total: {usage.total / (1024**3):.2f} GB")
                    print(f"  Used: {usage.used / (1024**3):.2f} GB ({usage.percent}%)")
                    print(f"  Free: {usage.free / (1024**3):.2f} GB")
                except PermissionError:
                    print(f"  (Access denied)")
        
        except ImportError:
            print("Install 'psutil' for detailed device info: pip install psutil")
            print("\nFalling back to basic disk info...")
            self._basic_disk_info()
    
    def _basic_disk_info(self):
        """Basic disk information without psutil"""
        if self.platform == "Windows":
            import string
            from ctypes import windll
            
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(letter)
                bitmask >>= 1
            
            for drive in drives:
                drive_path = f"{drive}:\\"
                print(f"\nDrive: {drive_path}")
        else:
            # Unix-like systems
            disk_usage = os.statvfs('/')
            total = disk_usage.f_blocks * disk_usage.f_frsize
            free = disk_usage.f_bfree * disk_usage.f_frsize
            used = total - free
            
            print(f"\nRoot Filesystem (/):")
            print(f"  Total: {total / (1024**3):.2f} GB")
            print(f"  Used: {used / (1024**3):.2f} GB")
            print(f"  Free: {free / (1024**3):.2f} GB")
    
    def get_cpu_info(self):
        """Get CPU information"""
        print("\n=== CPU INFORMATION ===")
        
        try:
            import psutil
            
            print(f"Physical Cores: {psutil.cpu_count(logical=False)}")
            print(f"Logical Cores: {psutil.cpu_count(logical=True)}")
            print(f"CPU Frequency: {psutil.cpu_freq().current:.2f} MHz")
            print(f"CPU Usage: {psutil.cpu_percent(interval=1)}%")
            
            # Per-core usage
            core_usage = psutil.cpu_percent(interval=1, percpu=True)
            print("\nPer-Core Usage:")
            for i, usage in enumerate(core_usage):
                bar = "█" * int(usage / 5)
                print(f"  Core {i}: {usage:5.1f}% |{bar}")
        
        except ImportError:
            print("Install 'psutil' for detailed CPU info: pip install psutil")
            print(f"CPU Count: {os.cpu_count()}")
    
    def get_memory_info(self):
        """Get memory information"""
        print("\n=== MEMORY INFORMATION ===")
        
        try:
            import psutil
            
            vm = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            print("Virtual Memory:")
            print(f"  Total: {vm.total / (1024**3):.2f} GB")
            print(f"  Available: {vm.available / (1024**3):.2f} GB")
            print(f"  Used: {vm.used / (1024**3):.2f} GB ({vm.percent}%)")
            print(f"  Free: {vm.free / (1024**3):.2f} GB")
            
            print("\nSwap Memory:")
            print(f"  Total: {swap.total / (1024**3):.2f} GB")
            print(f"  Used: {swap.used / (1024**3):.2f} GB ({swap.percent}%)")
            print(f"  Free: {swap.free / (1024**3):.2f} GB")
        
        except ImportError:
            print("Install 'psutil' for detailed memory info: pip install psutil")
    
    def get_network_interfaces(self):
        """Get network interface information"""
        print("\n=== NETWORK INTERFACES ===")
        
        try:
            import psutil
            
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            for interface, addresses in interfaces.items():
                print(f"\n{interface}:")
                
                if interface in stats:
                    stat = stats[interface]
                    print(f"  Status: {'UP' if stat.isup else 'DOWN'}")
                    print(f"  Speed: {stat.speed} Mbps")
                
                for addr in addresses:
                    if addr.family == 2:  # IPv4
                        print(f"  IPv4: {addr.address}")
                        if addr.netmask:
                            print(f"  Netmask: {addr.netmask}")
                    elif addr.family == 23 or addr.family == 30:  # IPv6
                        print(f"  IPv6: {addr.address}")
        
        except ImportError:
            print("Install 'psutil' for network info: pip install psutil")
    
    def get_io_stats(self):
        """Get disk I/O statistics"""
        print("\n=== DISK I/O STATISTICS ===")
        
        try:
            import psutil
            
            io_counters = psutil.disk_io_counters(perdisk=True)
            
            for disk, counters in io_counters.items():
                print(f"\n{disk}:")
                print(f"  Read Count: {counters.read_count:,}")
                print(f"  Write Count: {counters.write_count:,}")
                print(f"  Bytes Read: {counters.read_bytes / (1024**2):.2f} MB")
                print(f"  Bytes Written: {counters.write_bytes / (1024**2):.2f} MB")
                print(f"  Read Time: {counters.read_time / 1000:.2f} sec")
                print(f"  Write Time: {counters.write_time / 1000:.2f} sec")
        
        except ImportError:
            print("Install 'psutil' for I/O stats: pip install psutil")
    
    def demonstrate_file_io(self):
        """Demonstrate file I/O operations"""
        print("\n=== FILE I/O DEMONSTRATION ===")
        
        import time
        
        filename = "io_test.dat"
        data_size = 10 * 1024 * 1024  # 10 MB
        
        # Write test
        print(f"\nWriting {data_size / (1024**2):.1f} MB to disk...")
        data = b'X' * data_size
        
        start_time = time.time()
        with open(filename, 'wb') as f:
            f.write(data)
        write_time = time.time() - start_time
        
        write_speed = data_size / write_time / (1024**2)
        print(f"Write Time: {write_time:.3f} seconds")
        print(f"Write Speed: {write_speed:.2f} MB/s")
        
        # Read test
        print(f"\nReading {data_size / (1024**2):.1f} MB from disk...")
        
        start_time = time.time()
        with open(filename, 'rb') as f:
            read_data = f.read()
        read_time = time.time() - start_time
        
        read_speed = data_size / read_time / (1024**2)
        print(f"Read Time: {read_time:.3f} seconds")
        print(f"Read Speed: {read_speed:.2f} MB/s")
        
        # Cleanup
        os.remove(filename)
        print(f"\nFile deleted: {filename}")
    
    def get_running_processes(self, limit=10):
        """List running processes"""
        print(f"\n=== TOP {limit} PROCESSES (by memory) ===")
        
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by memory usage
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
            
            print(f"{'PID':<8} {'Name':<30} {'Memory %':<12} {'CPU %'}")
            print("-" * 62)
            
            for proc in processes[:limit]:
                print(f"{proc['pid']:<8} {proc['name']:<30} {proc['memory_percent']:<12.2f} {proc['cpu_percent']}")
        
        except ImportError:
            print("Install 'psutil' for process info: pip install psutil")

def main():
    """Main demonstration function"""
    print("OPERATING SYSTEMS - DEVICE ACCESS AND I/O")
    print("=" * 60 + "\n")
    
    dm = DeviceManager()
    
    dm.get_system_info()
    dm.list_mounted_devices()
    dm.get_cpu_info()
    dm.get_memory_info()
    dm.get_network_interfaces()
    dm.get_io_stats()
    dm.demonstrate_file_io()
    dm.get_running_processes()
    
    print("\n" + "=" * 60)
    print("Device Access and I/O Demonstration Completed!")
    print("\nNote: Install psutil for complete functionality:")
    print("  pip install psutil")

if __name__ == "__main__":
    main()