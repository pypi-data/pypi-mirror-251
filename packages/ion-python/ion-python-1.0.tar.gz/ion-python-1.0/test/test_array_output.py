import ctypes

from ionpy import Node, Builder, Buffer, PortMap, Port, Param, Type, TypeCode
import numpy as np


def test_binding():
    input_port = Port(name='input', type=Type.from_dtype(np.dtype(np.int32)), dim=2)
    len_param = Param(key='len', val=4)
    builder = Builder()
    builder.set_target(target='host')
    builder.with_bb_module(path='ion-bb-test')

    node = builder.add('test_array_output').set_iport([input_port]).set_param(params=[len_param, ])

    idata = np.array([[42, 42]], dtype=np.int32)
    ibuf = Buffer(array=idata)
    input_port.bind(ibuf)
    obufs = []
    odatas = []
    for i in range(4):
        odatas.append(np.array([[0, 0]], dtype=np.int32))
        obufs.append(Buffer(array=odatas[i]))

    output_port = node.get_port(name='array_output')
    output_port.bind(obufs)

    # First run
    builder.run()
    for i in range(4):
        print(odatas[i])


test_binding()
