#!/usr/bin/python
import cgi, cgitb
from collections import OrderedDict;

cgitb.enable()
conv = cgi.FieldStorage();
ipAddress = conv.getvalue('ipaddress');  #get IP address as string
netMask = int(conv.getvalue('netmask')); #store netmask as int

TEAM = 6;
SUBNETS = 4;

#process and store IP address as a list of bytes
ipAddrList = ipAddress.split('.');
ipBytes = [int(octet) for octet in ipAddrList];

#convert IP address and mask bytes into bit string
ipBits = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*ipBytes);
maskBits = (netMask * '1') + (32-netMask)*'0';

#convert subnet mask bytes into bit string
subnetMaskBits = ((netMask+2) * '1') + (32-(netMask+2))*'0';

def validIp(ipBytes):
    #validate IP address format
    if len(ipBytes) == 4:
        for octet in ipBytes:
            if (octet <0) or (octet > 255):
             return False;
        return True;
    return False;

def validMask(mask):
    #validate netmaks
    if (int(mask) >= 0 and int(mask) <= 28):
        return True;
    return False;

def getWildcardBits(maskBits):
    #generate host mask by invertig subnet mask bits
    wildcardBits = "";
    for b in maskBits:
        wildcardBits += str(1-(int(b)));
    return wildcardBits;

def getIpNetworkOctets(ipBits, maskBits):
    #get IP addres network byts
    ipNetworkBits = "";
    for x in range(32):
        ipNetworkBits += str(int(ipBits[x]) and (maskBits[x]));
        groupedIpNetworkBits = [ipNetworkBits[i:i+8] for i in range(0, len(ipNetworkBits), 8)]  
        ipNetworkOctets = [int(octet, 2) for octet in groupedIpNetworkBits];
    return ipNetworkOctets;

def getHostOctets(ipBits, maskBits):
    #extract host bytes
    hostBits = "";
    wildcardBits = getWildcardBits(maskBits);
    for x in range(32):
        hostBits += str(int(ipBits[x]) and (wildcardBits[x]));
        groupedHostBits = [hostBits[i:i+8] for i in range(0, len(hostBits), 8)]  
        hostOctets = [int(octet, 2) for octet in groupedHostBits];
    return hostOctets;
    
def getOctets(bits):
    #helper function to extracting bytes list
    groupedBits = [bits[i:i+8] for i in range(0, len(bits), 8)]
    octets = [int(octet, 2) for octet in groupedBits];
    return octets;

def getSubnets(ipBits, maskBits):
    #generate subnets and store as sorted dict
    #the key is the subnet. the values are the minimum host, maximum host and broadcast addresses
    subnetDict = OrderedDict();
    subnetStartIndex = maskBits.index('0');
    
    sn0 = ipBits[:subnetStartIndex] + '00' + (32-subnetStartIndex-2)*'0';
    sn1 = ipBits[:subnetStartIndex] + '01' + (32-subnetStartIndex-2)*'0';
    sn2 = ipBits[:subnetStartIndex] + '10' + (32-subnetStartIndex-2)*'0';
    sn3 = ipBits[:subnetStartIndex] + '11' + (32-subnetStartIndex-2)*'0';

    sn0hMin = ipBits[:subnetStartIndex] + '00' + (32-subnetStartIndex-2-1)*'0' + '1';
    sn0hMax = ipBits[:subnetStartIndex] + '00' + (32-subnetStartIndex-2-1)*'1' + '0';
    sn0bCast = ipBits[:subnetStartIndex] + '00' + (32-subnetStartIndex-2-1)*'1' + '1';

    sn1hMin = ipBits[:subnetStartIndex] + '01' + (32-subnetStartIndex-2-1)*'0' + '1';
    sn1hMax = ipBits[:subnetStartIndex] + '01' + (32-subnetStartIndex-2-1)*'1' + '0';
    sn1bCast = ipBits[:subnetStartIndex] + '01' + (32-subnetStartIndex-2-1)*'1' + '1';

    sn2hMin = ipBits[:subnetStartIndex] + '10' + (32-subnetStartIndex-2-1)*'0' + '1';
    sn2hMax = ipBits[:subnetStartIndex] + '10' + (32-subnetStartIndex-2-1)*'1' + '0';
    sn2bCast = ipBits[:subnetStartIndex] + '10' + (32-subnetStartIndex-2-1)*'1' + '1';

    sn3hMin = ipBits[:subnetStartIndex] + '11' + (32-subnetStartIndex-2-1)*'0' + '1';
    sn3hMax = ipBits[:subnetStartIndex] + '11' + (32-subnetStartIndex-2-1)*'1' + '0';
    sn3bCast = ipBits[:subnetStartIndex] + '11' + (32-subnetStartIndex-2-1)*'1' + '1';
    
    subnetDict =  {sn0: [sn0hMin,sn0hMax,sn0bCast],
                   sn1: [sn1hMin,sn1hMax,sn1bCast],
                   sn2: [sn2hMin,sn2hMax,sn2bCast],
                   sn3: [sn3hMin,sn3hMax,sn3bCast]};
    return subnetDict;

if validIp(ipBytes) and validMask(netMask):
    #run app (generate subnets) if inputs are valid
    #generate IP address bytes list
    networkOctets = getIpNetworkOctets(ipBits, maskBits);
    
    #store network byte for display in the htm page
    networkOctetsStr = '.'.join([str(x) for x in networkOctets]);
    
    #generate subnet bytes list
    subnetMask = getOctets(subnetMaskBits);  
    
    #generate and store the subnets and relevant info
    subnetDict = getSubnets(ipBits, maskBits);
    hostOctetsTemp = getHostOctets(ipBits, maskBits);
    hostOctets = [str(octet) for octet in hostOctetsTemp if octet != 0];
    
    #store separately the host byte for display on htm page
    hostOctetsStr = '.'.join(hostOctets);
    
    #boilerplate code for displaying response on htm page
    print ("Content-Type: text/html\n")
    print ("<html><body>")
    print ("<h3>Input data:</h3>");
    print ("<p>IP = {}, N={}, team {} -> {} subnets</p>".format(ipAddress, netMask, TEAM, SUBNETS));
    print ("<p>Network = {}/{}, ignore last {} bits (host .{})</p>".format(networkOctetsStr, netMask, 32-netMask, hostOctetsStr));
    print ("<h3>Generated subnets:</h3>");
    
    #display lines for each subnet in a table
    print ("<table>");
    print("<tr style='text-align:left'><th style='width:150px'>Subnet</th><th style='width:150px'>Subnet mask</th><th style='width:100px'>Min host</th><th> </th><th style='width:120px'>Max host</th><th style='width:190px'>Broadcast address</th></tr>");
    
    #go through each subnet
    for k,v in sorted(subnetDict.items()):
        #concat octets 
        subNetIpStr = '.'.join([str(x) for x in getOctets(k)]);
        subNetMaskStr = '.'.join([str(x) for x in subnetMask]);
        hostMinNet = '.'.join([str(x) for x in getOctets(v[0])[:-1]]);
        hostMinHost = getOctets(v[0])[-1:][0];
        hostMaxNet = '.'.join([str(x) for x in getOctets(v[1])[:-1]]);
        hostMaxHost = getOctets(v[1])[-1:][0];
        broadCastNet = '.'.join([str(x) for x in getOctets(v[2])[:-1]]);
        broadCastHost = getOctets(v[2])[-1:][0];
        print("<tr><td style='width:150px'>{} / {},</td><td style='width:150px'>{},</td><td style='width:100px'>{}.<span style='color:blue'>{}</span></td><td> - </td><td style='width:10px'>{}.<span style='color:blue'>{}</span>,</td><td style='width:100px'>{}.<span style='color:red'>{}</span></td></tr>".format(subNetIpStr, int(netMask)+2, subNetMaskStr, hostMinNet, hostMinHost, hostMaxNet, hostMaxHost, broadCastNet, broadCastHost));
    print ("</table>");
    print ("</br>");
    print ("<a href='front.htm'>Go back</a>");
    print ("</body></html>");

elif not validIp(ipBytes):
    #invalid IP htm response
    print ("Content-Type: text/html\n")
    print ("<html><body>")
    print ("<p>IP address invalid");
    print ("</br>");
    print ("<a href='front.htm'>Go back</a>");
    print ("</body></html>");

elif not validMask(netMask):
    #invalid netmask htm response
    print ("Content-Type: text/html\n")
    print ("<html><body>")
    print ("<p>Netmask is invalid");
    print ("</br>");
    print ("<a href='front.htm'>Go back</a>");
    print ("</body></html>");
