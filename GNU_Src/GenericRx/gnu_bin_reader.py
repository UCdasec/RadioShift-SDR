import numpy as np
import matplotlib.pyplot as plt
import argparse
################################Spectrogram###########################
def hann_window(N):
    n = np.arange(N)
    return 0.5 * (1 - np.cos(2 * np.pi * n / (N - 1)))    
  
#expect in shape [samples,channel] ~ [1024,2]
#return [samples, channel] ~ [32, 64] 
def spectrogram_vDFT(frame, n_fft=64, n_time_samples=32, use_db=True):
    L = len(frame)
    
    # Calculate hop_length to achieve exactly n_time_samples
    if n_time_samples > 1:
        hop_length = (L - n_fft) // (n_time_samples - 1)
    else:
        hop_length = 0 # Only one window possible if n_time_samples is 1
        
    hop_length = max(1, hop_length)
    
    spectral_sum = []
    window = hann_window(n_fft) 
    
    # Iterate exactly n_time_samples times
    for t in range(n_time_samples):
        start = t * hop_length
        end = start + n_fft
        
        if end > L:
            break
            
        segment = frame[start:end]
        
        if segment.ndim == 2:
            inphase = segment[:, 0]
            quadrature = segment[:, 1]
        else:
            inphase = segment
            quadrature = np.zeros_like(segment)
            
        full_segment = (inphase + 1j * quadrature) * window
        
        # Compute FFT and Shift
        X_k = np.fft.fft(full_segment)
        X_k_shifted = np.fft.fftshift(X_k)
        
        mag = np.abs(X_k_shifted)
        spectral_sum.append(mag)

    spectrogram = np.array(spectral_sum)

    if use_db:
        eps = 1e-12
        spectrogram = 20 * np.log10(spectrogram + eps)

    # spectrogram=spectrogram.transpose()
    return spectrogram
###########################################################
def show_plot(file_path:str, offset:int=0, length:int=1024):
    data=np.fromfile(file_path, dtype=np.complex64)
    iq=np.array([np.real(data[:]),np.imag(data[:])]).T
    print(data.shape)
    print(iq.shape)
    
    frame=iq[offset:offset+length]

    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    (ax1, ax2), (ax3, ax4) = axes

    # Plot 1: I and Q vs sample index
    ax1.plot(frame[:, 0], label="I")
    ax1.plot(frame[:, 1], label="Q")
    ax1.set_title("Time")
    ax1.set_xlabel("Sample")
    ax1.set_ylabel("Amplitude")
    ax1.legend()

    # Plot 2: I vs Q (constellation)
    ax2.plot(frame[:, 0], frame[:, 1], linewidth=0.25,marker='o', markersize=3)
    ax2.set_title("Constellation")
    ax2.set_xlabel("I")
    ax2.set_ylabel("Q")
    ax2.set_aspect("equal")

    # Plot 3: Spectrogram
    spec = spectrogram_vDFT(frame,64,32)
    ax3.imshow(spec, aspect="auto", origin="lower", cmap="inferno")
    ax3.set_title("Spectrogram")
    ax3.set_ylabel("Time")
    ax3.set_xlabel("Frequency bin")

    # Plot 4: empty or reuse — add whatever you need here
    ax4.axis("off")


    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Plot IQ data from a complex float binary file")
    parser.add_argument("file", help="Path to .complex_float binary file")
    parser.add_argument("--offset", type=int, default=0, help="Sample offset (default: 0)")
    parser.add_argument("--length", type=int, default=1024, help="Number of samples to plot (default: 1024)")
    args = parser.parse_args()

    show_plot(args.file,args.offset,args.length)
    
main()
