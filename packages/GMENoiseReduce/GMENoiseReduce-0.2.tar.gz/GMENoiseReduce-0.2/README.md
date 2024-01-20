# GMENoiseReduce

Python implementation of the Generalized Maximum Entropy white noise elimination technique discussed in https://pubs.aip.org/aip/jap/article/132/7/074903/2837401/Eliminating-white-noise-in-spectra-A-generalized

## Installation

    !pip install GMENoiseReduce

## Usage

    from GMENoiseReduce import GME
    x,y = data
    smoothed-yvals = GME.smooth(x,y)
  ## Advanced Usage
The full function takes in additional arguments if the curve is not ideal 

    smoothed-yvals = GME.smooth(x,y, int order, int noise_threshold)

 Despite the method needing zero information about the original system,  the solutions provided are currently not always stable, the current values for "order" (referred to as M in the original paper code) and "noise_threshold" are 44, and 100 respectfully. These returned the most stable results. However, if you wish for there to be lesser detail in the returned curve, change the res value to some thing lower. 