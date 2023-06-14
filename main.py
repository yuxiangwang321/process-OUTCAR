#  main

import pos_force as pf

start_frame = 2   # calculation starts from this frame
end_frame = 10000     # calculation ends at this frame, total number of frames is [end_frame - start_frame + 1]
parameter = 6       # which parameter: from 1 to 6, position_X, position_Y, position_Z, force_X, force_Y, force_Z
atom_index = '40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76 78 80 82 84 86 88 90 92 94 96 98 100 102 104 106 108 110 112 114 116 118 120 122 124 126 128 130 132 134 136 138 140 142 144 146 148 150 152 154 156 158 160 162 164 166 168 170 172 174 176 178 180 182 184 186 188 190 192 194 196 198 200 202 204 206 208 210 212 214 216 218 220 222 224 226 228 230 232 234 236 238'  
                    # a list if atom index for concerned atoms, format '1 3 5 7 9 33 69'. 
                    # NOTE: The atom index starts from 0, so you can output a index list from VMD

pf.extract_data()
pf.calculate_sum_and_average(start_frame, end_frame, parameter, atom_index)
pf.plot()

num_entries_per_frame = pf.count_entries_per_frame()
print("Number of atoms in the system: ", num_entries_per_frame)




                