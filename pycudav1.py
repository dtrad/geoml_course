import pycuda
import pycuda.autoinit
from pycuda import gpuarray
import numpy as np
import pycuda.driver as drv
drv.init()

x_host = np.array([1,2,3], dtype=np.float32)
y_host = np.array([1,1,1], dtype=np.float32)
print(x_host + y_host)
x_device = gpuarray.to_gpu(x_host)
y_device = gpuarray.to_gpu(y_host)
print((x_device + y_device).get())
