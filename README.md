# RadioShift-SDR: A Tutorial on How to Use USRPs for Wireless Communications

## Overview 

This repo contains code and tutorial documents for setting up two USRPs (one for transmitter and one for reciever) for basic wireless communications (e.g., FM and BPSK). 

Details regarding how to run our code and setup the USRPs can be found in our tutorial document ./Tutorial_USRP_Setup_Instructions.pdf

This can be used as a part of our end-to-end framework, named RadioShift, which can (a) automatically generate simulated I/Q frames with various domain shifts, (b) capture real-world I/Q frames, (c) train lightweight neural networks, and (c) test them on FPGAs given the RF signals we collect. The source code of our framework are divided into three separate repositories (as each of them can be used independently).

https://github.com/UCdasec/RadioShift (Simulated RF Signal Generation)

https://github.com/UCdasec/RadioShift-SDR (Real-world RF Signal Generation)

https://github.com/UCdasec/RadioFINN (Train and Test Neural Networks on FPGAs)

## Reference
We use the source code and documents of this repository to collect real-world RF signals, which are used in the following paper.  

Anagh Mishra, Phu Le, Ryan Evans, Nirnimesh Ghose, Boyang Wang, "RadioShift: A Framework Measuing the Robustness of Lightweight Neural Networks over RF Signals," the IEEE National Aerospace and Electronics Conference (IEEE NAECON 2026), Cincinnati, OH, August 9-12, 2026, USA.

To completely reproduce research results in the above paper, one will need to use all the three repos mentioned above.
