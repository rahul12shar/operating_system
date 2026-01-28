import sys
from collections import OrderedDict

class MemoryBlock:
    """Represents a block of memory"""
    def __init__(self, start, size, process_id=None):
        self.start = start
        self.size = size
        self.process_id = process_id
        self.is_free = process_id is None
    
    def __repr__(self):
        status = "FREE" if self.is_free else f"P{self.process_id}"
        return f"[{self.start}-{self.start+self.size-1}] {status} ({self.size}KB)"

class MemoryManager:
    """Simulates memory allocation and fragmentation"""
    
    def __init__(self, total_size=1024):
        self.total_size = total_size
        self.blocks = [MemoryBlock(0, total_size)]
        self.allocated_processes = {}
    
    def display_memory(self):
        """Visualize memory state"""
        print("\n--- Memory Map ---")
        for block in self.blocks:
            bar_length = int(block.size / self.total_size * 40)
            bar = "█" * bar_length
            status = "FREE" if block.is_free else f"P{block.process_id}"
            print(f"{block.start:4d}-{block.start+block.size:4d} {status:6s} |{bar}")
        
        free_memory = sum(b.size for b in self.blocks if b.is_free)
        used_memory = self.total_size - free_memory
        print(f"\nUsed: {used_memory}KB / Free: {free_memory}KB / Total: {self.total_size}KB")
        print(f"Fragmentation: {len([b for b in self.blocks if b.is_free])} free blocks")
    
    def allocate_first_fit(self, process_id, size):
        """First-fit allocation algorithm"""
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                # Allocate memory
                allocated = MemoryBlock(block.start, size, process_id)
                
                if block.size > size:
                    # Split block
                    remaining = MemoryBlock(block.start + size, block.size - size)
                    self.blocks[i:i+1] = [allocated, remaining]
                else:
                    # Use entire block
                    self.blocks[i] = allocated
                
                self.allocated_processes[process_id] = allocated
                print(f"✓ Allocated {size}KB to Process {process_id} at address {allocated.start}")
                return True
        
        print(f"✗ Cannot allocate {size}KB to Process {process_id} - Insufficient memory")
        return False
    
    def allocate_best_fit(self, process_id, size):
        """Best-fit allocation algorithm"""
        best_idx = -1
        best_size = float('inf')
        
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size and block.size < best_size:
                best_idx = i
                best_size = block.size
        
        if best_idx != -1:
            block = self.blocks[best_idx]
            allocated = MemoryBlock(block.start, size, process_id)
            
            if block.size > size:
                remaining = MemoryBlock(block.start + size, block.size - size)
                self.blocks[best_idx:best_idx+1] = [allocated, remaining]
            else:
                self.blocks[best_idx] = allocated
            
            self.allocated_processes[process_id] = allocated
            print(f"✓ Allocated {size}KB to Process {process_id} at address {allocated.start}")
            return True
        
        print(f"✗ Cannot allocate {size}KB to Process {process_id} - Insufficient memory")
        return False
    
    def deallocate(self, process_id):
        """Free memory and coalesce adjacent free blocks"""
        if process_id not in self.allocated_processes:
            print(f"✗ Process {process_id} not found")
            return False
        
        # Find and free the block
        for i, block in enumerate(self.blocks):
            if block.process_id == process_id:
                print(f"✓ Deallocated Process {process_id} ({block.size}KB)")
                block.is_free = True
                block.process_id = None
                
                # Coalesce with adjacent free blocks
                self._coalesce(i)
                del self.allocated_processes[process_id]
                return True
        
        return False
    
    def _coalesce(self, index):
        """Merge adjacent free blocks"""
        merged = True
        while merged:
            merged = False
            
            # Try to merge with next block
            if index < len(self.blocks) - 1:
                current = self.blocks[index]
                next_block = self.blocks[index + 1]
                
                if current.is_free and next_block.is_free:
                    current.size += next_block.size
                    self.blocks.pop(index + 1)
                    merged = True
            
            # Try to merge with previous block
            if index > 0:
                prev_block = self.blocks[index - 1]
                current = self.blocks[index]
                
                if prev_block.is_free and current.is_free:
                    prev_block.size += current.size
                    self.blocks.pop(index)
                    index -= 1
                    merged = True

class PageTable:
    """Simulates paging and page replacement"""
    
    def __init__(self, num_frames=4):
        self.num_frames = num_frames
        self.frames = [None] * num_frames
        self.page_faults = 0
        self.page_hits = 0
    
    def access_page_fifo(self, page):
        """FIFO page replacement algorithm"""
        if page in self.frames:
            self.page_hits += 1
            print(f"Page {page}: HIT")
            return
        
        self.page_faults += 1
        
        if None in self.frames:
            # Empty frame available
            idx = self.frames.index(None)
            self.frames[idx] = page
            print(f"Page {page}: FAULT (loaded into frame {idx})")
        else:
            # Replace oldest page (FIFO)
            replaced = self.frames.pop(0)
            self.frames.append(page)
            print(f"Page {page}: FAULT (replaced page {replaced})")
    
    def access_page_lru(self, pages_sequence):
        """LRU page replacement algorithm"""
        print("\n=== LRU Page Replacement ===")
        frames = []
        page_faults = 0
        
        for page in pages_sequence:
            if page in frames:
                # Page hit - move to end (most recently used)
                frames.remove(page)
                frames.append(page)
                print(f"Page {page}: HIT  | Frames: {frames}")
            else:
                # Page fault
                page_faults += 1
                if len(frames) < self.num_frames:
                    frames.append(page)
                else:
                    # Remove least recently used (first element)
                    replaced = frames.pop(0)
                    frames.append(page)
                    print(f"Page {page}: FAULT (replaced {replaced}) | Frames: {frames}")
                    continue
                print(f"Page {page}: FAULT | Frames: {frames}")
        
        print(f"\nTotal Page Faults: {page_faults}/{len(pages_sequence)}")
        print(f"Hit Rate: {((len(pages_sequence)-page_faults)/len(pages_sequence)*100):.1f}%")
    
    def display_stats(self):
        """Display page table statistics"""
        total = self.page_hits + self.page_faults
        hit_rate = (self.page_hits / total * 100) if total > 0 else 0
        print(f"\n--- Page Table Statistics ---")
        print(f"Frames: {self.frames}")
        print(f"Page Hits: {self.page_hits}")
        print(f"Page Faults: {self.page_faults}")
        print(f"Hit Rate: {hit_rate:.1f}%")

def demonstrate_memory_allocation():
    """Demonstrate memory allocation and fragmentation"""
    print("=== MEMORY ALLOCATION (First-Fit) ===")
    
    mm = MemoryManager(total_size=512)
    
    # Allocate memory
    mm.allocate_first_fit(1, 100)
    mm.allocate_first_fit(2, 50)
    mm.allocate_first_fit(3, 200)
    mm.display_memory()
    
    # Deallocate and show fragmentation
    print("\n--- Deallocating Process 2 ---")
    mm.deallocate(2)
    mm.display_memory()
    
    # Try to allocate larger block (shows fragmentation issue)
    print("\n--- Attempting to allocate 150KB ---")
    mm.allocate_first_fit(4, 150)
    mm.display_memory()

def demonstrate_best_fit():
    """Demonstrate best-fit allocation"""
    print("\n\n=== MEMORY ALLOCATION (Best-Fit) ===")
    
    mm = MemoryManager(total_size=512)
    mm.allocate_best_fit(1, 100)
    mm.allocate_best_fit(2, 50)
    mm.allocate_best_fit(3, 200)
    mm.deallocate(2)
    mm.allocate_best_fit(4, 40)  # Should fit in 50KB gap
    mm.display_memory()

def demonstrate_paging():
    """Demonstrate paging and page replacement"""
    print("\n\n=== PAGING (FIFO) ===")
    
    pt = PageTable(num_frames=3)
    pages = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    
    for page in pages:
        pt.access_page_fifo(page)
    
    pt.display_stats()
    
    # LRU demonstration
    pt_lru = PageTable(num_frames=3)
    pt_lru.access_page_lru(pages)

def demonstrate_memory_info():
    """Display actual Python memory info"""
    print("\n\n=== PYTHON MEMORY INFORMATION ===")
    
    import psutil
    import os
    
    try:
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        
        print(f"RSS (Resident Set Size): {mem_info.rss / 1024 / 1024:.2f} MB")
        print(f"VMS (Virtual Memory Size): {mem_info.vms / 1024 / 1024:.2f} MB")
        
        # System memory
        vm = psutil.virtual_memory()
        print(f"\nSystem Total Memory: {vm.total / 1024 / 1024 / 1024:.2f} GB")
        print(f"System Available Memory: {vm.available / 1024 / 1024 / 1024:.2f} GB")
        print(f"System Memory Usage: {vm.percent}%")
    except ImportError:
        print("Install 'psutil' for detailed memory info: pip install psutil")
        print(f"Basic Python object size: {sys.getsizeof([])} bytes (empty list)")

if __name__ == "__main__":
    print("OPERATING SYSTEMS - MEMORY MANAGEMENT SIMULATION")
    print("=" * 60 + "\n")
    
    demonstrate_memory_allocation()
    demonstrate_best_fit()
    demonstrate_paging()
    demonstrate_memory_info()
    
    print("\n" + "=" * 60)
    print("Memory Management Demonstration Completed!")