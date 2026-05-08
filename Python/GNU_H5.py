import h5py
import numpy as np
import matplotlib.pyplot as plt

class GNU_To_H5:
    def __init__(self, datasets = None):
        self.datasets = datasets

    def save_to_h5(file_path, dataset_samples, labels):
        # Create H5 File using Samples and Labels
        with h5py.File(file_path, "w") as hf:
            hf.create_dataset("all_IQ", data=dataset_samples)
            hf.create_dataset("all_labels", data=labels)

    def raw_iq_to_samples(raw_iq_data, num_frames, num_IQ_samples):
        # Reshape the raw IQ data into frames
        initial_sample_len = len(raw_iq_data)
        start_idx = initial_sample_len - (num_frames * num_IQ_samples)
        iq_samples_sliced = raw_iq_data[start_idx:]
        reshaped_data = np.zeros((num_frames, num_IQ_samples, 2))

        for i in range(num_frames):
            start = i * num_IQ_samples
            end = start + num_IQ_samples
            samples_frame = iq_samples_sliced[start:end]
            inphase_samples = np.real(samples_frame)
            quadrature_samples = np.imag(samples_frame)
            IQ_frame = np.stack((inphase_samples, quadrature_samples), axis=-1)
            reshaped_data[i] = IQ_frame
        return reshaped_data
            
    # Creating a function to output the min and max range of each dataset from the h5py file

    def dataset_range(dataset, dataset_mods, frames_per_mod):
        total_max = -np.inf
        total_min = np.inf
        num_mods = len(dataset_mods)
        for i in range(num_mods):
            mod_data = dataset[i*frames_per_mod:(i+1)*frames_per_mod]
            mod_max = np.max(mod_data)
            mod_min = np.min(mod_data)
            print(f"Modulation {dataset_mods[i]} - Min: {mod_min}, Max: {mod_max}")
            total_max = max(total_max, mod_max)
            total_min = min(total_min, mod_min)
        print(f"Overall - Min: {total_min}, Max: {total_max}")

    
    def print_time_IQ(indices, samples):
        for x in indices:
            # iq_samples_lb = (x)*1024
            # iq_samples_ub = iq_samples_lb+1024

            plt.figure(figsize=(6, 6))
            plt.scatter((samples[x, :, 0]), (samples[x, :, 1]), alpha=0.5, s=1)
            plt.title(f"Constellation Plot (Frame: {x})")
            plt.xlabel("Real (I)")
            plt.ylabel("Imaginary (Q)")
            plt.grid(True)
            plt.show()

            # Plot Time Series (Real and Imaginary parts over time)
            plt.figure(figsize=(10, 4))
            plt.plot(samples[x, :, 0], label='Real (I)')
            plt.plot((samples[x, :, 1]), label='Imag (Q)', alpha=0.7)
            plt.title(f"Time Domain Signal (Frame: {x})")
            plt.legend()
            plt.show()
    
    def compile_and_label_datasets(datasets_dict, custom_labels = None):
        """
        Takes a dictionary of datasets, stacks them vertically, 
        and generates a corresponding 1D array of integer labels.
        """
        samples_list = []
        labels_list = []
        label_map = {}
                
        # Iterate through each modulation scheme in the dataset
        for class_index, (key, dataset) in enumerate(datasets_dict.items()):
            # Map the integer label to the dataset name
            label_map[class_index] = key
            
            # Extract the data into a numpy array 
            # (Using [:] ensures we pull it into memory if it's an h5py object)
            data_chunk = dataset[:] 
            samples_list.append(data_chunk)
            
            # Generate an array of labels for this specific chunk
            num_samples_in_chunk = data_chunk.shape[0]
            if custom_labels is not None:
                label_chunk = np.full((num_samples_in_chunk,), custom_labels[class_index], dtype=int)

            else:
                label_chunk = np.full((num_samples_in_chunk,), class_index, dtype=int)
            labels_list.append(label_chunk)
            
        # Stack all the collected lists into final numpy arrays
        final_samples = np.vstack(samples_list)
        final_labels = np.concatenate(labels_list)
        
        return final_samples, final_labels, label_map