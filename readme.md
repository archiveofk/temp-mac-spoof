# MAC Address Spoofer

A Python tool to temporarily spoof your MAC address on Linux. Automatically restores your original MAC address when you exit.

## Requirements

- Linux
- Python 3
- Root privileges (sudo) for spoofing

## Usage

### View MAC Address

View MAC for a specific interface:
```bash
python3 spoof.py --get -i wlan0
```

View MAC for all interfaces:
```bash
python3 spoof.py --get
```

### List Interfaces

```bash
python3 spoof.py --list
```

### List Vendors

```bash
python3 spoof.py --list-vendors
```

### Spoof MAC Address

Random MAC:
```bash
sudo python3 spoof.py -i wlan0
```

Specific MAC:
```bash
sudo python3 spoof.py -i wlan0 -m 00:11:22:33:44:55
```

Spoof as vendor:
```bash
sudo python3 spoof.py -i wlan0 -v apple
```

Available vendors: apple, samsung, intel, microsoft, dell, hp, lenovo, cisco, huawei, sony, asus, tp-link, netgear, linksys, google, amazon, xiaomi, oneplus

## Options

- `-i, --interface` - Network interface (wlan0, eth0, etc.)
- `-m, --mac` - Specific MAC address
- `-v, --vendor` - Vendor to spoof as
- `-l, --list` - List available interfaces
- `--list-vendors` - List available vendors
- `-g, --get` - Get current MAC address

## Notes

- Requires sudo for spoofing
- You will briefly lose connection when changing MAC (1-2 seconds)
- MAC change only lasts while script is running
- Press Ctrl+C to restore original MAC and exit
- Common interfaces: wlan0 (WiFi), eth0 (Ethernet)
