# subroutines-------------------------------------------------------------------

def extract_data():
    with open('OUTCAR', 'r') as file:
        lines = file.readlines()
        
    frames = []
    frame_id = 1
    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        if "TOTAL-FORCE (eV/Angst)" in line:
            start_line = i + 2  # Skip two lines to get to the numerical content
        elif "total drift:" in line:
            end_line = i-1
            frame_data = lines[start_line:end_line]
            frames.append((frame_id, frame_data))
            frame_id += 1

    with open('reduced_OUTCAR.dat', 'w') as file:
        for frame_id, frame_data in frames:
            file.write(f"Frame_ID {frame_id}\n")
            file.writelines(frame_data)
            
# -------------------------------------------
def count_entries_per_frame():
    with open('reduced_OUTCAR.dat', 'r') as file:
        count = 0
        next(file)
        for line in file:
            if line.startswith('Frame_ID'):
                break
            else:
                count += 1
    return count
          
# -------------------------------------------
def calculate_sum_and_average(start_frame, end_frame, parameter, atom_index):

    dataset = atom_index
    dataset = dataset.strip("''")
    elements = dataset.split()
    comma_separated = ", ".join(elements)
    atom_index = list(map(int, elements))

    selected_entry = len(atom_index)
    target_frame_flag = 0
    current_frame_end_flag = 0
    frame_ID = 0
    current_entry = -1
    summation = 0.0
    with open('reduced_OUTCAR.dat', 'r') as file, open("output.dat", 'w') as outputfile:
        for line in file:
            if line.startswith('Frame_ID'):
                frame_infor = line.split()
                frame_ID = int(frame_infor[1])
                if frame_ID >= start_frame and frame_ID <= end_frame:
                    current_entry = -1
                    summation = 0.0
                    target_frame_flag = 1
                    current_frame_end_flag = 0
                    index_copy = atom_index.copy()
                    continue
                elif frame_ID < start_frame:
                    target_frame_flag = 0
                    continue
                elif frame_ID > start_frame:
                    break
            else:
                if target_frame_flag == 0:
                    continue
                elif target_frame_flag == 1 and current_frame_end_flag == 0:
                    current_entry += 1
                    first_number = list(index_copy)[0]
                    if current_entry == first_number:
                        frame_line = line.split()
                        summation += float(frame_line[parameter - 1])
                        index_copy.remove(first_number)
                        index_copy_length = len(index_copy)
                        if index_copy_length == 0:
                            averaged = summation / selected_entry
                            print(frame_ID, summation, averaged)
                            result = [frame_ID, summation, averaged]
                            outputfile.write(f"{result[0]} {result[1]} {result[2]}\n")
                            current_frame_end_flag = 1
                            continue
                    else:
                        continue

# -------------------------------------------
def plot():
    import matplotlib.pyplot as plt
    # Read data from the file
    #data_plot = 'output.dat'
    data = []
    with open('output.dat', 'r') as file:
        for line in file:
            values = line.split()
            data.append([float(values[0]), float(values[1])])

    # Extract X and Y values from the data
    x = [entry[0] for entry in data]
    y = [entry[1] for entry in data]

    # Plot the figure
    plt.plot(x, y)
    plt.xlabel('Step')
    plt.ylabel('Total-Force (eV/Angst)')
    plt.title('Force vs Step')

    # Save the figure
    output_file = 'output.png'
    plt.savefig(output_file)

    # Show the figure
    plt.show()
