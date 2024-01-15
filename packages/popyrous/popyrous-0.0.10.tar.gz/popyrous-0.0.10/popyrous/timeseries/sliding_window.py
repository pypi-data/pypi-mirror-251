

import numpy as np

def sliding_window(input_matrix, sequence_length:int, downsampling:int=1, squeezed:bool=True, forward_facing:bool=True, 
        include_current_step:bool=True, stacked:bool=True, includes_future_data:bool=False, dtype=np.float32,
        powers_of_two:bool=False):
        """Generate tabulated data out of a multivariate timeseries sequence. 
        The tabulated data will be the result of a sliding window passing through the sequence.
        The output of the function is typically used for generating input variables 
        for machine learning algorithms such as deep learning.

        ### Args:
        
            :param `input_matrix` (numpy matrix): Matrix of input data
            :param `sequence_length` (int): Sequence length of the sliding window
            :param `downsampling` (int): Downsampling rate of the input data. Sequence length is divided by this number.
            :param `squeezed` (bool, optional): Squeezed outputs have size (batch, seqlen*features) 
            useful for, e.g., ANN models, whereas unsqueezed outputs have shape (batch, seqlen, features) useful for LSTM, etc. 
            Default is True.
            :param `forward_facing` (bool, optional): Whether the tabulated sequences will be forward-facing
                like t - K to t, or vise versa, like t to t - K. Defaults to True.
            :param `include_current_step` (bool, optional): Whether the current time step is a part of the 
                sequence being processed or not. Defaults to True.
            :param `stacked`: If True (default), Output columns will be sequence of first feature, 
                then second feature, etc. Otherwise, output matrices will have a
                cascaded arrangement, i.e. features of first time step,
                features of second time step, etc. Only applies to squeezed data, not unsqueezed 3D tensors.
            :param `includes_future_data`: If True, the future data will be processed rather than past data.
                This is useful for forecasting.
            :param `dtype`: Data type of the output. Defaults to np.float32.
            :param `powers_of_two`: If True, the sequence length will be rounded to the nearest power of two.

        ### Returns:
        
            numpy matrix: Matrix of size (NumDataPoints, SeqLength, NumFeatures) for unsqueezed data, or 
                          (NumDataPoints, SeqLength*NumFeatures) for squeezed data.
        """
        # Processing direction
        if includes_future_data:
            input_matrix = np.flipud(input_matrix).astype(dtype)
            if forward_facing:
                forward_facing = False


        # Calculate Sequence Lengths
        if sequence_length > 1:
            seq_len_ds = int(np.ceil(sequence_length/downsampling))
            if powers_of_two:
                seq_len_ds = int(2**(np.round(np.log2(seq_len_ds))))
            sequence_length = (seq_len_ds-1) * downsampling + 1
        else:
            sequence_length = 1
            downsampling = 1
            seq_len_ds = 1
        
        # Processing inputs
        num_features = input_matrix.shape[-1]
        buffer = np.ones((sequence_length,num_features), dtype=dtype)*input_matrix[0,:].astype(dtype)
        buffer_ds = buffer[::downsampling,...]
        output = []
        for x in input_matrix:
            if include_current_step:
                buffer = np.append(buffer[1:,:],x.reshape(1,-1),axis=0) if forward_facing else \
                    np.append(x.reshape(1,-1),buffer[:-1,:],axis=0)
                buffer_ds = buffer[::downsampling,...]
            output.append(buffer_ds)
            if not include_current_step:
                buffer = np.append(buffer[1:,:],x.reshape(1,-1),axis=0) if forward_facing else \
                    np.append(x.reshape(1,-1),buffer[:-1,:],axis=0)
                buffer_ds = buffer[::downsampling,...]
        if squeezed:
            output = np.vstack(
                [buffer_ds.reshape((1, num_features*seq_len_ds), 
                order='F' if stacked else 'A') for buffer_ds in output])
        else:
            output = np.stack(output, axis=0)
        
        if includes_future_data:
            output = np.flipud(output)
            
        return {"table":output, "seq_len":sequence_length, "ds":downsampling, "seq_len_ds":seq_len_ds}


if __name__ == "__main__":
    seq = np.arange(0,100).reshape(-1,1)
    results = sliding_window(seq, sequence_length=32, downsampling=4, squeezed=True, forward_facing=True,
        include_current_step=True, stacked=True, includes_future_data=False, dtype=np.float32,
        powers_of_two=True)
    out = results["table"]
    print(out.shape)
    print(out)
                             