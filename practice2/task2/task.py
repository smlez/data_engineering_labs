import numpy as np
import os

matrix = np.load('./matrix_72_2.npy')
size = len(matrix)
x = list()
y = list()
z = list()
limit = 572 #вариант

for i in range(0, size):
    for j in range(0, size):
        if matrix[i][j] > limit:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez("points", x=x, y=y, z=z)
np.savez_compressed("points_zip", x=x, y=y, z=z)

not_compressed = os.path.getsize('points.npz')
compressed = os.path.getsize('points_zip.npz')

if (compressed < not_compressed):
    print(f"Сжатый файл весит меньше не сжатого на {not_compressed - compressed}")
else:
    print(f"Не сжатый файл весит меньше сжатого на {compressed - not_compressed}")