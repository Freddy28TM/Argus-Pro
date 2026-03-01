#!/usr/bin/env python3
import subprocess
import os
from bitstring import BitArray
from rich.console import Console

console = Console()

class BinaryEngine:
    """
    The bridge between Python logic and Clang-compiled high-performance 
    binary manipulation tools.
    """
    
    def __init__(self):
        # Path to the compiled Clang binary
        self.binary_path = os.path.abspath("./modules/reversing/reverser")

    def _execute_native(self, mode, data, key=""):
        """Internal method to call the Clang-compiled reverser."""
        if not os.path.exists(self.binary_path):
            return f"[bold red]Error:[/bold red] Native binary not found at {self.binary_path}. Please recompile src/native/reverser.c"
        
        try:
            # Prepare command: ./reverser <mode> <data> [key]
            cmd = [self.binary_path, mode, data]
            if key:
                cmd.append(key)
            
            # Execute and capture output
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        
        except subprocess.CalledProcessError as e:
            return f"[bold red]Execution Error:[/bold red] {e.stderr}"
        except Exception as e:
            return f"[bold red]Unexpected Error:[/bold red] {str(e)}"

    def hex_decode(self, hex_string):
        """Decodes Hex to ASCII via Clang."""
        return self._execute_native("hex", hex_string)

    def xor_decrypt(self, data, key):
        """XORs data against a single-byte key via Clang."""
        return self._execute_native("xor", data, key)

    def bit_analyze(self, hex_string):
        """
        Performs bit-level analysis. 
        Useful for identifying patterns in binary headers.
        """
        try:
            b = BitArray(hex=hex_string)
            return {
                "binary": b.bin,
                "length": len(b.bin),
                "byte_count": len(b.bytes)
            }
        except Exception as e:
            return {"error": str(e)}

    def check_magic_bytes(self, filepath):
        """Identifies file types based on hex signatures."""
        signatures = {
            b'\x7fELF': "Linux Executable (ELF)",
            b'MZ': "Windows Executable (PE)",
            b'\xff\xd8\xff': "JPEG Image",
            b'\x89PNG': "PNG Image",
            b'%PDF': "PDF Document"
        }
        
        try:
            with open(filepath, 'rb') as f:
                header = f.read(4)
                for sig, file_type in signatures.items():
                    if header.startswith(sig):
                        return file_type
            return "Unknown Binary/Data"
        except Exception as e:
            return f"File Error: {e}"

# --- Self-Test Block ---
if __name__ == "__main__":
    engine = BinaryEngine()
    console.print("[bold yellow]Running Handler Self-Test...[/bold yellow]")
    
    # Test Hex
    test_hex = "4172677573" # "Argus"
    console.print(f"Hex Test ({test_hex}): [green]{engine.hex_decode(test_hex)}[/green]")
    
    # Test Bits
    bits = engine.bit_analyze(test_hex)
    console.print(f"Bit Analysis: [cyan]{bits['binary']}[/cyan] ({bits['length']} bits)")
