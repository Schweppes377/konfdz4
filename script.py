import argparse
import yaml

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        instructions = f.readlines()

    binary_file = bytearray()
    log_data = []

    for line in instructions:
        if not line:
            continue

        parts = line.split()
        command = parts[0].upper()

        if command == "LOAD":
            A, B, C = 97, int(parts[1]), int(parts[2])
            instr = (A << 32) | (B << 16) | (C << 5)
            binary_file.extend(instr.to_bytes(5, byteorder='big'))
            log_data.append({'cmd_line': line.strip(), 'binary': bin(instr)[2:].zfill(40), 'hex': hex(instr)[2:].zfill(12)})
        elif command == "READ":
            A, B, C = 10, int(parts[1]), int(parts[2])
            instr = (A << 32) | (B << 16) | (C << 0)
            binary_file.extend(instr.to_bytes(5, byteorder='big'))
            log_data.append({'cmd_line': line.strip(), 'binary': bin(instr)[2:].zfill(40), 'hex': hex(instr)[2:].zfill(12)})
        elif command == "WRITE":
            A, B, C, D = 101, int(parts[1]), int(parts[2]), int(parts[3])
            instr = (A << 48) | (B << 35) | (C << 19) | (D << 3)
            binary_file.extend(instr.to_bytes(7, byteorder='big'))
            log_data.append({'cmd_line': line.strip(), 'binary': bin(instr)[2:].zfill(56), 'hex': hex(instr)[2:].zfill(12)})
        elif command == "SUB":
            A, B, C, D, E = 121, int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4])
            instr = (A << 64) | (B << 48) | (C << 35) | (D << 19) | (E << 3)
            binary_file.extend(instr.to_bytes(9, byteorder='big'))
            log_data.append({'cmd_line': line.strip(), 'binary': bin(instr)[2:].zfill(72), 'hex': hex(instr)[2:].zfill(12)})
        else:
            raise ValueError(f"Unknown command: {command}")

    with open(output_file, 'wb') as f:
        f.write(binary_file)
    with open(log_file, 'w') as f:
        yaml.dump(log_data, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler")
    parser.add_argument('--input')
    parser.add_argument('--bin')
    parser.add_argument('--log')
    args = parser.parse_args()
    assemble(args.input, args.bin, args.log)