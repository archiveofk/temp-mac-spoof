# MAC Address Spoofer

A Python tool to temporarily spoof your MAC address on Linux. Automatically restores your original MAC address when the program exits.

## Features

- 🔄 **Temporary MAC Spoofing** - Changes MAC address while running, restores original on exit
- 🎭 **Vendor Spoofing** - Spoof as popular device manufacturers (Apple, Samsung, Intel, etc.)
- 🔍 **MAC Address Viewer** - View current MAC addresses without root privileges
- 🛡️ **Automatic Restoration** - Original MAC is automatically restored when you exit (Ctrl+C)
- 📋 **Interface Management** - List and manage network interfaces

## Requirements

- Linux (tested on Arch Linux, should work on most distributions)
- Python 3
- Root privileges (sudo) for spoofing operations
- `ip` command (usually pre-installed on Linux)

## Installation

1. Clone or download the script:ash
# Make the script executable
chmod +x spoof.py
## Usage

### View Current MAC Addresses

View MAC address for a specific interface (no root needed):
python3 spoof.py --get -i wlan0View MAC addresses for all interfaces:
python3 spoof.py --get### List Available Interfaces
h
python3 spoof.py --list### List Available Vendors
h
python3 spoof.py --list-vendors### Spoof MAC Address

**Random MAC address:**ash
sudo python3 spoof.py -i wlan0**Specific MAC address:**
sudo python3 spoof.py -i wlan0 -m 00:11:22:33:44:55**Spoof as a specific vendor:**
# Spoof as Apple device
sudo python3 spoof.py -i wlan0 -v apple

# Spoof as Samsung device
sudo python3 spoof.py -i wlan0 -v samsung

# Spoof as Intel device
sudo python3 spoof.py -i wlan0 -v intel### Available Vendors

- apple
- samsung
- intel
- microsoft
- dell
- hp
- lenovo
- cisco
- huawei
- sony
- asus
- tp-link
- netgear
- linksys
- google
- amazon
- xiaomi
- oneplus

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--interface` | `-i` | Network interface to spoof (e.g., wlan0, eth0) |
| `--mac` | `-m` | Specific MAC address to use (default: random) |
| `--vendor` | `-v` | Vendor to spoof as (use --list-vendors to see options) |
| `--list` | `-l` | List available network interfaces |
| `--list-vendors` | | List available vendor IDs |
| `--get` | `-g` | Get current MAC address(es) |

## How It Works

1. **Saves Original MAC** - The script reads and stores your current MAC address
2. **Brings Interface Down** - Temporarily disables the network interface (required to change MAC)
3. **Changes MAC Address** - Sets the new MAC address using `ip link set`
4. **Brings Interface Up** - Re-enables the interface with the new MAC
5. **Keeps Running** - Maintains the spoofed MAC while the script is active
6. **Auto-Restore** - When you press Ctrl+C, it automatically restores your original MAC

## Important Notes

⚠️ **Root Privileges Required**: Spoofing requires root/sudo access because it modifies network interface settings.

⚠️ **Brief Disconnection**: When changing the MAC address, your network interface will be briefly disabled (usually 1-2 seconds). Your network manager should automatically reconnect.

⚠️ **Temporary Only**: The MAC address change only lasts while the script is running. Once you exit (Ctrl+C), your original MAC is restored.

⚠️ **Interface Names**: Common interface names:
- `wlan0`, `wlan1` - WiFi interfaces
- `eth0`, `eth1` - Ethernet interfaces
- `enp3s0`, `enp4s0` - Modern Linux Ethernet naming

## Example Workflow
h
# 1. Check your current MAC address
python3 spoof.py --get -i wlan0

# 2. Start spoofing as Apple device
sudo python3 spoof.py -i wlan0 -v apple

# 3. In another terminal, verify the change (no root needed)
python3 spoof.py --get -i wlan0

# 4. When done, press Ctrl+C in the spoofing terminal to restore original MAC## Troubleshooting

**Error: "Interface may not exist"**
- Use `python3 spoof.py --list` to see available interfaces
- Make sure you're using the correct interface name (case-sensitive)

**Error: "requires root privileges"**
- Use `sudo` when running spoofing commands
- The `--get` option doesn't require root

**Interface doesn't reconnect after spoofing**
- Check if your network manager is running
- Try manually bringing the interface up: `sudo ip link set <interface> up`

## Technical Details

- Uses Linux `ip` command for interface management
- MAC addresses are changed at Layer 2 (Data Link Layer)
- Vendor IDs use the first 3 octets (OUI - Organizationally Unique Identifier)
- Last 3 octets are randomized when using vendor spoofing

## Disclaimer

This tool is for educational and privacy purposes. Ensure you have permission to modify network settings on the system you're using. MAC address spoofing may violate terms of service on some networks.

## License

Free to use and modify.