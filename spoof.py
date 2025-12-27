import subprocess
import sys
import signal
import random
import argparse
import time
# ran on arch linux so may not work on other distros or windows


# Common vendor IDs (first 3 octets of MAC address)
# idk if these are real cause i got ai to generate them
VENDOR_IDS = {
    'apple': ['00:1e:c2', '00:23:df', '00:25:00', '00:26:08', '00:26:4a', '00:26:bb'],
    'samsung': ['00:16:6c', '00:23:39', '00:23:6c', '00:25:66', '00:26:37'],
    'intel': ['00:13:ce', '00:1b:21', '00:1e:67', '00:21:5c', '00:25:00'],
    'microsoft': ['00:15:5d', '00:1d:d8', '00:22:48', '00:50:f2'],
    'dell': ['00:14:22', '00:1b:21', '00:21:70', '00:24:e8'],
    'hp': ['00:1e:0b', '00:21:5e', '00:23:7d', '00:25:b3'],
    'lenovo': ['00:21:cc', '00:23:8b', '00:25:64', '00:26:18'],
    'cisco': ['00:1e:13', '00:1e:79', '00:21:55', '00:26:0b'],
    'huawei': ['00:e0:fc', '00:1e:10', '00:25:9e'],
    'sony': ['00:13:a9', '00:16:fe', '00:1f:a7'],
    'asus': ['00:1d:60', '00:22:15', '00:24:8c'],
    'tp-link': ['00:27:19', '00:27:22', '00:50:56'],
    'netgear': ['00:09:5b', '00:1f:33', '00:24:b2'],
    'linksys': ['00:18:f8', '00:1c:df', '00:25:9c'],
    'google': ['00:1a:11', '00:1e:c2', 'f4:f5:e8'],
    'amazon': ['00:fc:58', 'f0:27:2d', '68:37:e9'],
    'xiaomi': ['28:e3:1f', '64:09:80', 'ac:1f:74'],
    'oneplus': ['00:1a:11', '00:1e:c2', 'f4:f5:e8'],
}

class MACSpoofer:
    def __init__(self, interface, mac_address=None, vendor=None):
        self.interface = interface
        self.original_mac = None
        self.mac_address = mac_address or self.generate_mac_from_vendor(vendor)
        
    def generate_mac_from_vendor(self, vendor=None):
        """Generate MAC address, optionally using a vendor ID"""
        if vendor and vendor.lower() in VENDOR_IDS:
            vendor_key = vendor.lower()
            if vendor_key == 'random':
                # Generate completely random MAC
                first_byte = random.randint(0x02, 0xFE) & 0xFE
                mac = [first_byte]
                mac.extend([random.randint(0x00, 0xFF) for _ in range(5)])
                return ':'.join(f'{b:02x}' for b in mac)
            else:
                # Use vendor ID + random last 3 octets
                vendor_id = random.choice(VENDOR_IDS[vendor_key])
                vendor_bytes = [int(b, 16) for b in vendor_id.split(':')]
                # Generate random last 3 octets
                random_bytes = [random.randint(0x00, 0xFF) for _ in range(3)]
                mac = vendor_bytes + random_bytes
                return ':'.join(f'{b:02x}' for b in mac)
        else:
            # Original random MAC generation
            first_byte = random.randint(0x02, 0xFE) & 0xFE
            mac = [first_byte]
            mac.extend([random.randint(0x00, 0xFF) for _ in range(5)])
            return ':'.join(f'{b:02x}' for b in mac)
    
    def get_current_mac(self):
        """Get current MAC address of the interface"""
        try:
            result = subprocess.run(
                ['ip', 'link', 'show', self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            for line in result.stdout.split('\n'):
                if 'link/ether' in line:
                    return line.split('link/ether')[1].split()[0]
        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            pass
        

        
        return None
    
    def set_mac(self, mac_address):
        try:
            # interface is just a network conenction pretty much
            # interface needs to be down to change the MAC address
            subprocess.run(
                ['ip', 'link', 'set', self.interface, 'down'],
                check=True,
                capture_output=True
            )
            
            # Set new MAC address
            #link defines the network connection
            # set allows you to set a parameter of the network connection
            # address is the MAC address
            subprocess.run(
                ['ip', 'link', 'set', self.interface, 'address', mac_address],
                check=True,
                capture_output=True
            )
            
            # Bring interface back up with the changes saved
            subprocess.run(
                ['ip', 'link', 'set', self.interface, 'up'],
                check=True,
                capture_output=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error setting MAC address: {e}", file=sys.stderr)
            return False
    
    def restore_mac(self):
        if self.original_mac:
            print(f"\nRestoring original MAC address: {self.original_mac}")
            self.set_mac(self.original_mac)
    
    def start(self):
  
        self.original_mac = self.get_current_mac()
        if not self.original_mac:
            print(f"Error: Could not get current MAC address for {self.interface}", file=sys.stderr)
            return False
        
        print(f"Original MAC address: {self.original_mac}")
        print(f"Setting new MAC address: {self.mac_address}")
        
        if not self.set_mac(self.mac_address):
            return False
        
        new_mac = self.get_current_mac()
        if new_mac == self.mac_address:
            print(f"MAC address successfully changed to: {new_mac}")
            return True
        else:
            print(f"Warning: MAC address may not have changed correctly", file=sys.stderr)
            return False
    
    def run(self):
        """Run the spoofer and keep it running"""
        if not self.start():
            return
        
        def signal_handler(sig, frame):
            self.restore_mac()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        print(f"\nMAC spoofing active. Press Ctrl+C to restore original MAC and exit.")
        print(f"Interface: {self.interface}")
        print(f"Spoofed MAC: {self.mac_address}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)

def get_mac_address(interface):
    try:
        result = subprocess.run(
            ['ip', 'link', 'show', interface],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.split('\n'):
            if 'link/ether' in line:
                return line.split('link/ether')[1].split()[0]
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        pass
    
    return None


def get_all_mac_addresses():
    interfaces = list_interfaces()
    macs = {}
    for interface in interfaces:
        mac = get_mac_address(interface)
        if mac:
            macs[interface] = mac
    return macs


def show_mac_address(interface=None):
    if interface:
        mac = get_mac_address(interface)
        if mac:
            print(f"{interface}: {mac}")
        else:
            print(f"Error: Could not get MAC address for {interface}", file=sys.stderr)
            print(f"Interface may not exist or may be down. Use --list to see available interfaces.", file=sys.stderr)
            sys.exit(1)
    else:
        macs = get_all_mac_addresses()
        if macs:
            print("Current MAC addresses:")
            for iface, mac in macs.items():
                print(f"  {iface}: {mac}")
        else:
            print("Error: Could not retrieve any MAC addresses", file=sys.stderr)
            sys.exit(1)


def list_interfaces():
    try:
        result = subprocess.run(
            ['ip', 'link', 'show'],
            capture_output=True,
            text=True,
            check=True
        )
        interfaces = []
        for line in result.stdout.split('\n'):
            if ': ' in line and 'lo:' not in line:
                parts = line.split(':')
                if len(parts) > 1:
                    interface = parts[1].strip().split()[0]
                    interfaces.append(interface)
        return interfaces
    except:
        return []


def list_vendors():
    print("Available vendors:")
    for vendor in sorted(VENDOR_IDS.keys()):
        if vendor != 'random':
            print(f"  - {vendor.capitalize()}")
    print("  - random (completely random MAC)")


def main():
    parser = argparse.ArgumentParser(
        description='Temporarily spoof MAC address. Restores original on exit.'
    )
    parser.add_argument(
        '-i', '--interface',
        help='Network interface to spoof (e.g., wlan0, eth0)'
    )
    parser.add_argument(
        '-m', '--mac',
        help='MAC address to use (default: random)'
    )
    parser.add_argument(
        '-v', '--vendor',
        help='Vendor to spoof as (use --list-vendors to see options)'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List available network interfaces'
    )
    parser.add_argument(
        '--list-vendors',
        action='store_true',
        help='List available vendor IDs'
    )
    parser.add_argument(
        '-g', '--get',
        action='store_true',
        help='Get current MAC address(es). Use with -i to get specific interface, or without to get all.'
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Available network interfaces:")
        for iface in list_interfaces():
            print(f"  - {iface}")
        return
    
    if args.list_vendors:
        list_vendors()
        return
    
    if args.get:
        # Get MAC address(es) - doesn't require root
        show_mac_address(args.interface)
        return
    
    # For spoofing, interface is required to choose which one
    if not args.interface:
        parser.error("Interface (-i/--interface) is required for spoofing. Use --get to view MAC addresses or --list to list interfaces.")
    
    # Validate vendor if provided
    if args.vendor and args.vendor.lower() not in VENDOR_IDS:
        print(f"Error: Unknown vendor '{args.vendor}'", file=sys.stderr)
        print("Use --list-vendors to see available options", file=sys.stderr)
        sys.exit(1)
    
    # Check if running as root (only needed for spoofing)
    if subprocess.run(['id', '-u'], capture_output=True).stdout.decode().strip() != '0':
        print("Error: This script requires root privileges for spoofing (use sudo)", file=sys.stderr)
        sys.exit(1)
    
    spoofer = MACSpoofer(args.interface, args.mac, args.vendor)
    spoofer.run()


if __name__ == '__main__':
    main()