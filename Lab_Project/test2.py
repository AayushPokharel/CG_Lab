import numpy as np

arr = np.array([1,2],dtype=np.float32)
arr2 = np.array([3,4],dtype=np.float32)

np.append(arr,arr2)

print(arr)