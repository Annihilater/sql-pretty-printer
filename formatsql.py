import ctypes
import json
import sys

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "File not found."
    except IOError:
        return "Error reading the file."
    
# Check if two filenames are provided as command-line arguments
if len(sys.argv) != 3:
    print("Please provide SQL file and format option file as command-line arguments.")
    sys.exit(1)
  
filename_input_sqlfile = sys.argv[1]
filename_input_format_option_file = sys.argv[2]
  
# Change the path of input sql file, "c:\\prg\\gsp_vcl\\sampleFiles\\demo.sql"
inputSql = read_file(filename_input_sqlfile).encode()

# Change the path of format option file, "c:\\prg\\gsp_vcl\\sampleFiles\\format_options.json"
inputOption = read_file(filename_input_format_option_file).encode()
  
# Load the DLL
dll = ctypes.WinDLL('.\gspsf32.dll')

# Define the function prototype
formatsql = dll.formatsql
formatsql.argtypes = [
    ctypes.c_char_p,   # inputSql
    ctypes.c_uint,     # inputSqlLength
    ctypes.c_char_p,   # inputOption
    ctypes.c_uint,     # inputOptionLength
    ctypes.c_char_p,   # outputSql
    ctypes.c_uint,     # outputSqlLength
    ctypes.c_char_p,   # outMessage
    ctypes.c_uint      # outMessageLength
]
formatsql.restype = ctypes.c_int

# Call the formatsql function

PRE_ALLOCATE_OUTPUT_SQL_LEN = 1024 * 8
PRE_ALLOCATE_OUTPUT_MSG_LEN = 1024 * 8

outputSql = ctypes.create_string_buffer(PRE_ALLOCATE_OUTPUT_SQL_LEN)
outMessage = ctypes.create_string_buffer(PRE_ALLOCATE_OUTPUT_MSG_LEN)

result = formatsql(
    inputSql,
    len(inputSql),
    inputOption,
    len(inputOption),
    outputSql,
    PRE_ALLOCATE_OUTPUT_SQL_LEN,
    outMessage,
    PRE_ALLOCATE_OUTPUT_MSG_LEN
)

if result > PRE_ALLOCATE_OUTPUT_SQL_LEN:
    PRE_ALLOCATE_OUTPUT_SQL_LEN = result
    outputSql = ctypes.create_string_buffer(PRE_ALLOCATE_OUTPUT_SQL_LEN)
    result = formatsql(
        inputSql,
        len(inputSql),
        inputOption,
        len(inputOption),
        outputSql,
        PRE_ALLOCATE_OUTPUT_SQL_LEN,
        outMessage,
        PRE_ALLOCATE_OUTPUT_MSG_LEN
    )    

# print(outMessage.value.decode('utf-8'))
outMessageJson = json.loads(outMessage.value.decode('utf-8'))
retval_value = outMessageJson["retval"]
retval_msg = outMessageJson["retMessage"]

# Check the result
if retval_value == 0:
    print("Success!")
else:
    print("Error:", retval_value)
    print("Error message:", retval_msg)
    
print(outputSql.value.decode('utf-8'))

    