from pathlib import *
import unicodedata, struct, json


def decode(path: Path) -> list:

    magic_header_length = 28
    header_length = 0
    command_offset = 0
    string_block_offset = 0
    string_offsets = []
    strings = []

    try:
        bindata = open(path.as_posix(), 'rb')
    except FileNotFoundError:
        print("File not found")
        return []
    
    bindata.seek(0, 2)
    file_end = bindata.tell()

    bindata.seek(0,0)
    magic = bindata.read(20)

    if magic != b'BurikoCompiledScript':
        print("Invalid file format")
        bindata.close()
        return []
    
    #get header length
    bindata.seek(magic_header_length,0)
    header_length = struct.unpack("L", bindata.read(4))[0]

    #get command offset
    while True:
        if bindata.read(4) == b"\x01\x00\x00\x00":
            command_offset = bindata.tell() - 4
            break

    #get first string offset
    bindata.seek(command_offset)
    while True:
        if bindata.read(4) == b"\x03\x00\x00\x00":
            of = struct.unpack("L", bindata.read(4))[0]
            string_block_offset = of + command_offset
            break


    #get all message offsets
    # bindata.seek(command_offset)
    # whi_blockle bindata.tell() <= string_offset:
    #     if bindata.read(4) == b"\x03\x00\x00\x00":
    #         of = struct.unpack("L", bindata.read(4))[0]
    #         message_offsets.append(of + magic_header_length + header_length)

    bindata.seek(string_block_offset - 1)
    while bindata.tell() < file_end:
        if bindata.read(1) == b"\x00":
            string_offsets.append(bindata.tell())



    #get strings
    for i in range(len(string_offsets)  - 1):
        bindata.seek(string_offsets[i])
        char = b""
        while True:
            t = bindata.read(1)
            if t == b"\x00":
                break
            char += t

        string = char.decode("shift-jis")
        strings.append(string)



    #output
    out = []
    for i in range(len(strings)):
        t = {}
        t["index"] = i
        t["offset"] = string_offsets[i] - command_offset
        t["string"] = strings[i]

        #check if command or message
        if unicodedata.east_asian_width(strings[i][0]) == "Na":
            t["type"] = "command"
        else:
            t["type"] = "message"
        
        out.append(t)


    bindata.close()
    return out




def encode(orgin_file: Path, json_file: Path, output_file: Path, encode_format = "UTF-8") -> bool:
    magic_header_length = 28
    header_length = 0
    command_offset = 0
    string_block_offset = 0
    new_string_offsets = []
    string_offsers = []



    try:
        orgin_data = open(orgin_file.as_posix(), 'rb')
    except FileNotFoundError:
        print("File not found")
        return False
    
    try:
        with open(json_file.as_posix(), 'r', encoding='utf-8') as file:
            json_data = json.loads(file.read())
    except FileNotFoundError:
        print("File not found")
        return False
    
    try:
        output_data = open(output_file.as_posix(), 'wb+')
    except :
        print("write error")
        return False
    
    orgin_data.seek(0)
    magic = orgin_data.read(20)
    if magic != b'BurikoCompiledScript':
        print("Invalid file format")
        return
    
    #get header length 
    orgin_data.seek(magic_header_length)
    header_length = struct.unpack("L", orgin_data.read(4))[0]

    #get command offset
    while True:
        if orgin_data.read(4) == b"\x01\x00\x00\x00":
            command_offset = orgin_data.tell() - 4
            break

    #get first string offset
    orgin_data.seek(command_offset)
    while True:
        if orgin_data.read(4) == b"\x03\x00\x00\x00":
            of = struct.unpack("L", orgin_data.read(4))[0]
            string_block_offset = of + command_offset
            break

    #copy 
    orgin_data.seek(0)
    output_data.write(orgin_data.read(string_block_offset))

    #write new string
    output_data.seek(string_block_offset)
    for i in range(len(json_data)):
        string = json_data[i]["string"]
        #strings.append(string)
        new_string_offsets.append(output_data.tell() - command_offset)

        if json_data[i]["type"] == "message":
            output_data.write(string.encode(encode_format))
        else:
            output_data.write(string.encode("shift-jis"))

        output_data.write(b"\x00")


    #covert old string offsets to DWORD
    for a in json_data:
        string_offsers.append(struct.pack("L", a["offset"]))

    #write new string offsets
    output_data.seek(command_offset)
    while output_data.tell() < string_block_offset:
        if output_data.read(4) == b"\x03\x00\x00\x00":
            t = output_data.read(4)
            if t in string_offsers:
                output_data.seek(-4, 1)
                p = string_offsers.index(t)
                print("found, postion:", output_data.tell(), "offset:", new_string_offsets[p])
                output_data.write(struct.pack("L", new_string_offsets[p]))

                #string_offsers.pop(p)
                #new_string_offsets.pop(p)
    



    #close all files session
    orgin_data.close()
    output_data.close()

    return True