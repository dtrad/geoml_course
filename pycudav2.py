import pycuda
import pycuda.driver as drv
drv.init()
print('CUDA device query (PyCUDA version) \n')
print('Detected {} CUDA Capable device(s) \n'.format(drv.Device.count()))

for i in range(drv.Device.count()):
    gpu_device = drv.Device(i)
    print(gpu_device)
    print( 'Device {}: {}'.format( i, gpu_device.name() ) )
    compute_capability = float( '%d.%d' % gpu_device.compute_capability() )
    print( '\t Compute Capability: {}'.format(compute_capability))
    print( '\t Total Memory: {} megabytes'.format(gpu_device.total_memory()//(1024**2)))

import pycuda.autoinit
from pycuda import gpuarray
from time import time
import numpy as np  

host_data = np.float32( np.random.random(5000000) )


def speedcomparison():
    t1 = time()
    host_data_2x =  host_data * np.float32(2)
    t2 = time()
    print('total time to compute on CPU: %f' % (t2 - t1))
    device_data = gpuarray.to_gpu(host_data)
    # allocate memory for output
    t1 = time()
    device_data_2x = device_data * np.float32(2)
    t2 = time()
    from_device = device_data_2x.get()
    print('total time to compute on GPU: %f' % (t2 - t1))
    print('Is the host computation the same as the GPU computation? : {}'.format(np.allclose(from_device, host_data_2x) ))

print("First time GPU is slow because it needs to compile the code.")

speedcomparison()
speedcomparison()
