import json
import numpy as np

m = np.load('./matrix_72.npy')

size = len(m)
m_stat = {}
m_stat['sum'] = 0
m_stat['avr'] = 0
m_stat['sumMD'] = 0
m_stat['avrMD'] = 0
m_stat['sumSD'] = 0
m_stat['avrSD'] = 0
m_stat['max'] = m[0][0]
m_stat['min'] = m[0][0]

for i in range(0, size):
    for j in range(0, size):
        m_stat['sum'] += m[i][j]
        if i == j:
            m_stat['sumMD'] += m[i][j]
        if i + j == (size - 1):
            m_stat['sumSD'] += m[i][j]
        m_stat['min'] = min(m_stat['min'], m[i][j])
        m_stat['max'] = max(m_stat['max'], m[i][j])

m_stat['avr'] = m_stat['sum'] / (size*size)
m_stat['avrMD'] = m_stat['sumMD'] / size
m_stat['avrSD'] = m_stat['sumSD'] / size

for key in m_stat.keys():
    m_stat[key] = float(m_stat[key])

with open("matrix_stat.json", 'w') as result:
    result.write(json.dumps(m_stat))

norm_matrix = np.ndarray((size, size), dtype=float)

for i in range(0, size):
    for j in range(0, size):
        norm_matrix[i][j] = m[i][j] / m_stat['sum']

np.save('norm_matrix', norm_matrix)