with open("protein sequences.fasta", "r") as input_file:
    sequence = ""
    seq_dict={}
    for line in input_file:
        if line.startswith(">"):
            if sequence:
                seq_dict[names]=sequence
                names = line.strip()
                sequence = ""
            else:
                names = line.strip()
            #    output_file.write(line)                 
        else:
            sequence += line.strip()
seq_dict[names]=sequence
input_file.close()
with open("protein sequences_rm.fa", "w") as output_file:
    for key,valueL in seq_dict.items():
        if len(valueL)>=50 adn "B" not in valueL and "J" not in valueL and "O" not in valueL and "U" not in valueL and "X" not in valueL and "Z" not in valueL:
output_file.close()
