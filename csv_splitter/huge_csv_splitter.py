print("Importing necessary libraries...")
import pandas as pd
import os
file_to_cut = [f for f in os.listdir('.') if f.endswith(".txt")] #have it in .txt format not to struggle with csv formatting
master = pd.read_csv(file_to_cut[0], engine='python')

print("In how many files do you want to split the master?")
number_of_files = input()


#prepare number of files as variables. This will be the name of the output csv files.
num = int(number_of_files)
file_names = ["file_chunk_{}".format(i) for i in range(0,num)]


#check if the dataframe size allows for a division with no remainders
master_length = master.shape[0]
remainder = master_length % num
size_of_csv_chunks = int(round((master_length / num), 0)) #size of chunk


def generate_indexes():
    if remainder == 0:
        idx = [i for i in range(-1, master_length, size_of_csv_chunks)]
    else:
        idx = [i for i in range(-(remainder), master_length,size_of_csv_chunks)]
    idx[0] = 0 #resets first iteration of indexing to 0
    return idx

indexes = generate_indexes()
indexes_start = indexes[:-1]
indexes_end = indexes[1:]


#create a dictionary of dataframes chunks
storage = {}
iter_count = 0

for file, i_start, i_end in zip(file_names, indexes_start, indexes_end):
    remainder = 1 if remainder == 0 else remainder #adjust remainder for indexing purposes. In case of % num == 0, it would cut the final chunk
    iter_count += 1
    
    if iter_count == num: #at last iter count, adjust last chunk with the remainder
        chunk = master.iloc[i_start:i_end+remainder]
    else:
        chunk = master.iloc[i_start:i_end]
    storage["{}".format(file)] = chunk


#write dataframes
print("Starting to write csvs...")
for key in storage.keys():
    storage[key].to_csv("{}.csv".format(key), index = False, chunksize = 10000)


#rejoice!
print("Script completed successfully")