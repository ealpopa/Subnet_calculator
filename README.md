# Subnet_calculator
Subnet_calculator (this is hardcoded to generate 4 subnets)
IP subnet calculator.

The application contains two components: front.hmt and back.py.

front.hmt 
This is the access page of the application.
It consists of two paragraphs and a form.
The form uses the GET method and contains two fields: "ipaddress" (which accepts text strings) and "netmask" which
accept numbers. The submit button sends the form to the back.py.application

back.py.
The application takes over the two input variables (IP address and network mask) and generates 4 subnets, together with
the smallest and largest host address as well as the broadcast address.

It takes over and stores the two input variables, from the form, in the form of bytes.
The subnet mask is the network mask + 2 bits (to get 4 subnets);
The network mask and subnet are generated in bit string format.
 
Functions
validIP - ensures that the entered IP address consists of 4 bytes with values ​​0-255. Parameters: bytes of the entered IP address
validMask - ensures that the entered network mask has values ​​0-28 (to be able to generate 4 subnets). Parameters: network mask
getWildcardBits - generate the string of bits needed to extract the host address (reversing the bits of the network mask). Parameters: network mask in bit string format.
getIpNetworkOctets - retrieves the list of bytes related to the network address from the entered IP address. Parameters: bitmap IP address, bitmap network mask.
getHostOctets - retrieves the list of bytes related to the host address from the entered IP address. Parameters: bitmap IP address, bitmap network mask.
getOctets - helper function for grouping a string of bits in a list of bytes. Parameters: a string of bits.
getSubnets - generating subnets and storing them as an ordered dictionary (so that they are displayed in ascending order).
           - this is the most important function.
           - works with strings of bits.
           - identifies the position of the first zero bit in the network mask
           - calculate 4 subnets by replacing the first two zero bits with bits 00, 01, 10, 11
           - calculates the minimum host by setting the last bit (LSB) in 1.
           - calculates the maximum host by setting the host bits (so 32 - number of bits of the subnet), minus the last bit, in 1.
           - calculates the broadcast address by setting the host bits (so 32 - number of subnet bits) in 1.
           - stores data in the dictionary as follows {subnet1: [hostMin, hostMax, bCast], ...}
           - Parameters: the bit string of the entered IP address, the bit string of the network mask.

Running the application, once the form is submitted, first validates the IP address and network mask. If the IP address or netmask is invalid, a message is displayed.
The bytes of the network address and the subnet mask are generated.
Subnets are generated.
Browse the ordered dictionary and display the information in the form of an htm formatted string.
