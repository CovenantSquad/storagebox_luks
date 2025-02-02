import datetime, os, socket, subprocess, sys

# StorageBox information
box_dnsname = "u436509.your-storagebox.de"
box_port = 445
box_sharepath = "/backup"
box_mountpoint = "/mnt/storagebox"
luks_filename = "luks.img"

# Shell commands
cmd_mountbox  = "mount -t cifs " + "//" + box_dnsname + box_sharepath + " " + box_mountpoint + " -o credentials=/home/mirko/.smbcredentials,x-systemd.idle-timeout=0"
cmd_openluks  = "/sbin/cryptsetup --verbose luksOpen "  + box_mountpoint + "/" + luks_filename + " storagebox-luks -d /root/keyfile"
cmd_mountluks = "mount /dev/mapper/storagebox-luks /mnt/luks"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Test a connection to the Storagebox (SMB port)
print("=====" + str(datetime.now()) + "====\nTrying telnet to " + box_dnsname + ":" + str(box_port))
sock.settimeout(10)
is_reachable = sock.connect_ex((box_dnsname, box_port))
if is_reachable != 0:
    print("Cannot open a connection to " + box_dnsname + ":" + str(box_port) + "Quitting..."); sys.exit()
    exit
else:
    print("Connection test to " + box_dnsname + ":" + str(box_port) + " successful")

# Mount the Storagebox
# process_boxmnt = subprocess.run(cmd_mountbox.split(" "), stdout=subprocess.PIPE)

# Find the luks.img file
is_luksfile = os.path.isfile(box_mountpoint + "/" + luks_filename)
if is_luksfile == False:
    print("Cannot find " + luks_filename + " in " + box_mountpoint + "." + "\nPlease check if the Storagebox has been  mounted correctly.\nQuitting..."); sys.exit()
    exit
else:
    print("Found " + luks_filename + " in " + box_mountpoint)

# Open and mount the luks file
subprocess.run(cmd_openluks.split(" "))
subprocess.run(cmd_mountluks.split(" "))