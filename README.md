# Serial Message Decoder (Autonomous Mobile Robots)

## 📌 Overview

This project implements a Python-based serial message decoder that reads a binary data stream and converts it into human-readable values.

It was developed as part of an Autonomous Mobile Robots coursework, focusing on understanding how structured data is transmitted, interpreted, and validated in real-world robotic systems.

The decoder processes incoming bytes sequentially (simulating real serial communication), reconstructs data frames, validates them using a checksum, and exports the decoded values to a CSV file.

---

## ⚙️ Key Features

* Byte-by-byte decoding (simulating real-time serial communication)
* Frame synchronization using header detection (`~~`)
* Multi-byte data parsing with correct endianness
* Temperature conversion using lookup table
* 64-bit timestamp reconstruction (Unix time in microseconds)
* Checksum validation for detecting corrupted frames
* CSV output generation for further analysis

---

## 🧠 Protocol Structure

Each data frame consists of 26 bytes:

| Section  | Description                                                     |
| -------- | --------------------------------------------------------------- |
| Header   | `~~` indicates start of a frame                                 |
| Metadata | System ID, Destination ID, Component ID, Sequence, Message Type |
| Payload  | RPM, Voltage, Current, Temperature values                       |
| Timing   | 64-bit timestamp (Unix time in microseconds)                    |
| Checksum | Used to detect corrupted frames                                 |

---

## 📂 Project Structure

```
Serial-Message-Decoder/
│
├── src/
│   └── decoder.py          # Main decoding script
│
├── data/
│   └── sample_output.csv   # Example decoded output
│
├── docs/
│   └── coursework.pdf      # Coursework description (optional)
│
└── README.md
```

---

## ▶️ How to Run the Project

### 1. Clone the repository

```
git clone https://github.com/yourusername/serial-message-decoder.git
cd serial-message-decoder
```

---

### 2. Add your binary input file

Place your `.bin` file inside the project directory.

Example:

```
data/binary_input.bin
```

---

### 3. Update file path in the script

Open `src/decoder.py` and update:

```python
input_file = open("data/binary_input.bin", "rb")
output_file = open("data/output.csv", "w")
```

---

### 4. Run the script

```
python src/decoder.py
```

---

### 5. View the output

After execution, a CSV file will be generated:

```
data/output.csv
```

Each row represents one decoded data frame.

---

## 📊 Example Output Format

```
~~,219,247,7,27,25,P,2532,9136,-66,30.9,31.0,T,970479533016225,209
```

---

## 🔍 How to Verify the Output

* Check that each row starts with `~~` (valid frame)
* Verify:

  * RPM, Voltage, Current values are reasonable
  * Temperature values match lookup table
* Compare checksum values to identify corrupted frames
* Ensure timestamps convert correctly to real dates

---

## 📚 Learning Outcomes

This project demonstrates:

* Understanding of serial communication protocols
* Binary data decoding and parsing
* Handling byte streams and frame synchronization
* Endianness in multi-byte data interpretation
* Error detection using checksum validation
* Data transformation into structured formats (CSV)

---

## 🏫 Academic Context

Developed as part of:
**AERO60492 – Autonomous Mobile Robots**

The task involved decoding a structured binary message stream into meaningful engineering data.

---

## 🚀 Possible Improvements

* Add real-time serial port input (e.g., using `pyserial`)
* Visualize decoded data (plots/graphs)
* Modularize code into classes
* Add unit tests for checksum and parsing
* Build a GUI for live monitoring

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👤 Author

Ansper Miranda
