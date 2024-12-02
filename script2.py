import yaml
import argparse

def bin_to_str(binary_file):
    with open(binary_file, 'rb') as f:
        binary_data = f.read()
    return ' '.join(f'{byte:08b}' for byte in binary_data).split(' ')


def interpret(binary_file, output_file, memory_range):
    memory = [0] * 1024
    registers = [0] * 32

    all_bin = bin_to_str(binary_file)

    while all_bin != []:
        bin_code = ""

        if int(all_bin[0],2) == 97: n = 5
        elif int(all_bin[0],2) == 10: n = 5
        elif int(all_bin[0], 2) == 101: n = 7
        elif int(all_bin[0], 2) == 121: n = 9

        for i in range(n):
            bin_code += all_bin[i]
        all_bin = all_bin[n:]

        A = int(bin_code[:8], 2)
        if A == 97:  # LOAD
            B = int(bin_code[8:24], 2)
            C = int(bin_code[24:35], 2)
            registers[B] = C
        elif A == 10:  # READ
            B = int(bin_code[8:24], 2)
            C = int(bin_code[24:40], 2)
            registers[B] = memory[C]
        elif A == 101:  # WRITE
            B = int(bin_code[8:21], 2)
            C = int(bin_code[21:37], 2)
            D = int(bin_code[37:53], 2)
            memory[B+D] = registers[C]
        elif A == 121:  # SUB
            B = int(bin_code[8:24], 2)
            C = int(bin_code[24:37], 2)
            D = int(bin_code[37:53], 2)
            E = int(bin_code[53:69], 2)
            memory[B+C] = memory[D] - memory[E]
        else:
            raise ValueError(f"Unknown instruction with A={int(A, 2)}")

    start, end = memory_range
    with open(output_file, 'w') as f:
        yaml.dump({'memory': memory[start:end]}, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter")
    parser.add_argument('--bin')
    parser.add_argument('--out')
    parser.add_argument('--range', nargs=2, type=int)
    args = parser.parse_args()

    interpret(args.bin, args.out, tuple(args.range))