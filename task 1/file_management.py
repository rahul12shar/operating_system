import os
import shutil
from datetime import datetime

class FileManager:
    """Demonstrates OS file management operations"""
    
    def __init__(self, base_dir="demo_files"):
        self.base_dir = base_dir
        self._setup()
    
    def _setup(self):
        """Create demo directory structure"""
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
        os.makedirs(self.base_dir)
        print(f"Created base directory: {self.base_dir}")
    
    def create_file(self, filename, content):
        """Create a new file with content"""
        filepath = os.path.join(self.base_dir, filename)
        
        # Open file with exclusive creation (fails if exists)
        try:
            with open(filepath, 'x') as f:
                f.write(content)
            print(f"✓ Created file: {filename}")
            return filepath
        except FileExistsError:
            print(f"✗ File already exists: {filename}")
            return None
    
    def read_file(self, filename):
        """Read file content"""
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            print(f"✓ Read {len(content)} bytes from {filename}")
            return content
        except FileNotFoundError:
            print(f"✗ File not found: {filename}")
            return None
    
    def write_file(self, filename, content, mode='w'):
        """Write to existing file"""
        filepath = os.path.join(self.base_dir, filename)
        
        with open(filepath, mode) as f:
            bytes_written = f.write(content)
        
        mode_desc = "Overwrote" if mode == 'w' else "Appended to"
        print(f"✓ {mode_desc} file: {filename} ({bytes_written} bytes)")
    
    def delete_file(self, filename):
        """Delete a file"""
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            os.remove(filepath)
            print(f"✓ Deleted file: {filename}")
            return True
        except FileNotFoundError:
            print(f"✗ Cannot delete - file not found: {filename}")
            return False
    
    def get_file_info(self, filename):
        """Get file metadata"""
        filepath = os.path.join(self.base_dir, filename)
        
        try:
            stat_info = os.stat(filepath)
            
            print(f"\n--- File Information: {filename} ---")
            print(f"  Size: {stat_info.st_size} bytes")
            print(f"  Created: {datetime.fromtimestamp(stat_info.st_ctime)}")
            print(f"  Modified: {datetime.fromtimestamp(stat_info.st_mtime)}")
            print(f"  Accessed: {datetime.fromtimestamp(stat_info.st_atime)}")
            print(f"  Permissions: {oct(stat_info.st_mode)}")
            print(f"  Inode: {stat_info.st_ino}")
            
            return stat_info
        except FileNotFoundError:
            print(f"✗ File not found: {filename}")
            return None
    
    def list_directory(self):
        """List all files in directory"""
        print(f"\n--- Directory Listing: {self.base_dir} ---")
        
        files = os.listdir(self.base_dir)
        if not files:
            print("  (empty)")
        else:
            for f in sorted(files):
                filepath = os.path.join(self.base_dir, f)
                size = os.path.getsize(filepath)
                print(f"  {f} ({size} bytes)")
        
        return files
    
    def copy_file(self, source, destination):
        """Copy a file"""
        src_path = os.path.join(self.base_dir, source)
        dst_path = os.path.join(self.base_dir, destination)
        
        try:
            shutil.copy2(src_path, dst_path)
            print(f"✓ Copied {source} → {destination}")
            return True
        except FileNotFoundError:
            print(f"✗ Source file not found: {source}")
            return False
    
    def rename_file(self, old_name, new_name):
        """Rename a file"""
        old_path = os.path.join(self.base_dir, old_name)
        new_path = os.path.join(self.base_dir, new_name)
        
        try:
            os.rename(old_path, new_path)
            print(f"✓ Renamed {old_name} → {new_name}")
            return True
        except FileNotFoundError:
            print(f"✗ File not found: {old_name}")
            return False

def demonstrate_file_operations():
    """Demonstrate comprehensive file management"""
    print("=== FILE MANAGEMENT DEMONSTRATION ===\n")
    
    fm = FileManager()
    
    # Create files
    print("1. Creating Files:")
    fm.create_file("report.txt", "Annual Report 2024\nRevenue: $1M\n")
    fm.create_file("data.csv", "Name,Age,City\nAlice,30,NYC\nBob,25,LA\n")
    fm.create_file("config.ini", "[Settings]\ntheme=dark\nlanguage=en\n")
    
    # List directory
    print("\n2. Directory Contents:")
    fm.list_directory()
    
    # Read file
    print("\n3. Reading File:")
    content = fm.read_file("report.txt")
    print(f"   Content: {content[:50]}...")
    
    # Append to file
    print("\n4. Appending to File:")
    fm.write_file("report.txt", "Profit: $200K\n", mode='a')
    
    # Get file info
    print("\n5. File Metadata:")
    fm.get_file_info("report.txt")
    
    # Copy file
    print("\n6. Copying File:")
    fm.copy_file("report.txt", "report_backup.txt")
    
    # Rename file
    print("\n7. Renaming File:")
    fm.rename_file("config.ini", "settings.ini")
    
    # Final directory listing
    print("\n8. Final Directory Contents:")
    fm.list_directory()
    
    # Delete files
    print("\n9. Deleting Files:")
    fm.delete_file("data.csv")
    fm.delete_file("report_backup.txt")
    
    # Cleanup
    print("\n10. Cleanup:")
    shutil.rmtree(fm.base_dir)
    print(f"Removed directory: {fm.base_dir}")

if __name__ == "__main__":
    demonstrate_file_operations()
    print("\n" + "=" * 60)
    print("File Management Demonstration Completed!")