# Q1 Answer: 765
# Q2 Answer: 24
# Q3 Answer: 2017-04-05

import datetime

# Temperature lookup table
temp_lookup = {}
for i in range(0xA0, 0xE0):  # Range between 0xA0 to 0xDF
    temp_lookup[i] = 30.0 + (i - 0xA0) * 0.1  # 0xA0 - 30.0°C, each next value increases by 0.1°C


# Open the binary input file (read)
input_file = open(r"C:\Users\anspe\Downloads\binaryFileC_84.bin", "rb")

# Open the CSV output file (write)
output_file = open("14320246.csv", "w")

# Decoder State Variables
frame_buffer = []  # Temporarily holds the bytes for a single frame.
sync_state = 0  # Tracks the presence of the two '~' header bytes.
frame_count = 0  # Total count of complete frames detected.
corrupt_count = 0  # Number of frames with invalid checksums.
first_timestamp = None  # Used to calculate the calendar date.

# Checksum Calculation Function
def calculate_checksum(frame_bytes):
    """
    1. Sum all bytes except the checksum byte.
    2. Compute the modulo 256 of the sum.
    3. Subtract the result from 255.
    """
    return 255 - (sum(frame_bytes[:-1]) % 256)


# Byte-by-byte decoding loop
# Read file one byte at a time (i.e. simulates serial communication)
byte = input_file.read(1)

while byte:

    # Convert raw byte into integer (0–255)
    value = int.from_bytes(byte, "big")  # "big" is a byte order parameter; it is ignored for a single byte.

    # Frame Synchronisation 
    # Each valid frame begins with two '~' characters.
    # 'sync_state' is used to track the presence of these two characters.
    if sync_state == 0:
        # Searching for the first '~'. 
        if value == ord("~"):
            sync_state = 1  # First '~' detected.
        byte = input_file.read(1)
        continue

    elif sync_state == 1:
        # Searching for the second '~'.
        if value == ord("~"):
            # Both '~' detected; begin a new frame.
            frame_buffer = [ord("~"), ord("~")]
            sync_state = 2  # Now start collecting frame data.
        else:
            # If second character is not '~', reset and search again.
            sync_state = 0
        byte = input_file.read(1)
        continue

    # Frame Assembly
    # Once synchronised, bytes are appended to frame_buffer, until 26 bytes are collected (complete frame length).

    frame_buffer.append(value)

    if len(frame_buffer) == 26:

        frame_count += 1  # Count this complete frame.

        # Decode single-byte fields
        sys_id  = frame_buffer[2]
        dest_id = frame_buffer[3]
        comp_id = frame_buffer[4]
        seq     = frame_buffer[5]
        msg_id  = frame_buffer[6]

        # Decode multi-byte numerical values
        # RPM: unsigned 16-bit, MSB first (big-endian)
        rpm = int.from_bytes(frame_buffer[8:10], "big", signed=False)

        # Voltage: unsigned 16-bit, MSB first (big-endian)    
        volt = int.from_bytes(frame_buffer[10:12], "big", signed=False)

        # Current: signed 16-bit, LSB first (little-endian)   
        curr = int.from_bytes(frame_buffer[12:14], "little", signed=True)

        # Temperature conversion
        # If temperature byte is outside lookup table, 0.0 is written.
        mos_temp = temp_lookup.get(frame_buffer[14], 0.0)
        cap_temp = temp_lookup.get(frame_buffer[15], 0.0)

        # Reconstruct timestamp
        # Unsigned 64-bit integer, big-endian (in microseconds since Unix epoch).
        timestamp = int.from_bytes(frame_buffer[17:25], "big", signed=False)

        if first_timestamp is None:
            first_timestamp = timestamp

        # Checksum Verification
        # Read checksum value stored in the frame (byte 26)
        checksum_received = frame_buffer[25]

        # Calculate expected checksum
        checksum_calculated = calculate_checksum(frame_buffer)

        # If values do not match, the frame is considered corrupted.
        if checksum_received != checksum_calculated:
            corrupt_count += 1

        # Write Frame to CSV File
        # All frames are written, including corrupt ones.
        output_file.write(
            "~~,{},{},{},{},{},P,{},{},{},{:.1f},{:.1f},T,{},{},".format(
                sys_id, dest_id, comp_id, seq, msg_id,
                rpm, volt, curr,
                mos_temp, cap_temp,
                timestamp, checksum_received
            )
        )
        output_file.write("\n") 

        # Reset buffer and state for next frame
        frame_buffer = []
        sync_state = 0

    byte = input_file.read(1)

# Final Results
print("End of file reached")
input_file.close()
output_file.close()

# Convert first timestamp to timezone-aware UTC date
calendar_date = datetime.datetime.fromtimestamp(
    first_timestamp / 1e6,
    datetime.timezone.utc
).date()

print("Decoding complete")
print("Q1 – Total complete frames:", frame_count)
print("Q2 – Corrupt frames:", corrupt_count)
print("Q3 – Calendar date:", calendar_date)
