# Forza_Horizon_4_Telemetry_Extraction
How to extract telemetry data from Forza Horizon 4 using a python script, and store it into a CSV file

# Algorithm for Telemetry data extraction
The algorithm used is for receiving and parsing telemetry data from a racing game (specifically Forza Horizon 4) using UDP sockets and storing it in a CSV file.


1. Import Necessary Modules: The code begins by importing required modules such as socket, struct, time, and csv.

2. DataPacket Class: Defines a class DataPacket which will hold the decoded telemetry data. However, it's currently an empty class.


3. Decoding Functions: These functions (get_single, get_uint16, get_uint32, get_uint8, get_int8) are responsible for extracting specific data types from the byte stream received over UDP. They utilize the struct module to unpack binary data.


4. BufferOffset: Defines a constant BufferOffset with a value of 12. This is used to calculate the index for accessing specific fields in the packet.


5. Packet Parsing Function (parse_packet): This function takes the raw packet received from the game, extracts various telemetry data using the decoding functions defined earlier, and populates an instance of the DataPacket class with the decoded data. If any error occurs during parsing, it catches the IndexError exception and prints an error message.


6. Configure UDP Socket: Sets up a UDP socket to receive telemetry data from Forza Horizon 4. It binds the socket to a specific IP address (127.0.0.1) and port (5300).


7. CSV File Handling: Creates a CSV file (telemetry_data.csv) and writes the header with field names for telemetry data.

    
8. Main Loop: Enters an infinite loop to continuously receive and process telemetry data packets from the game. Inside the loop:

a. It receives a packet from the UDP socket.

b. It parses the received packet using the parse_packet function.

c. If parsing is successful, it writes the parsed data to the CSV file using the DictWriter object and flushes the file.

d. It prints some telemetry data to the console for debugging or monitoring purposes.

e. Catches socket.error exceptions and prints an error message if any socket-related errors occur.


9. Socket Cleanup: Finally, when the loop exits (which can happen when the script is
terminated), it closes the UDP socket.

![FC](https://github.com/user-attachments/assets/06fcd695-5d62-4ce2-b331-ad44be02762f)


# Telemetry data in CSV File
![telemetry](https://github.com/user-attachments/assets/950e3faa-70fe-4be6-9212-83cb69614561)



