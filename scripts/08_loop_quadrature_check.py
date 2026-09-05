#!/usr/bin/env python3
"""Independent exact-filament Neumann mutual-inductance and Biot-Savart check.

Run remotely on Jellyfin. NumPy quadrature uses complete coplanar loop geometry;
no import from the trade script. Doubled resolutions test quadrature convergence.
This verifies free-space quasistatic geometry only, not lunar material effects.
"""
import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


def mutual_neumann(a, b, separation, n):
    angle=(np.arange(n)+.5)*2*np.pi/n
    p=np.stack([a*np.cos(angle),a*np.sin(angle)],axis=1)
    q=np.stack([separation+b*np.cos(angle),b*np.sin(angle)],axis=1)
    dl1=np.stack([-a*np.sin(angle),a*np.cos(angle)],axis=1)*2*np.pi/n
    dl2=np.stack([-b*np.sin(angle),b*np.cos(angle)],axis=1)*2*np.pi/n
    total=0.
    for start in range(0,n,64):
        dist=np.linalg.norm(p[start:start+64,None,:]-q[None,:,:],axis=2)
        dot=dl1[start:start+64]@dl2.T
        total+=float(np.sum(dot/dist))
    return 1e-7*total


def center_b_per_amp(a, separation, n):
    phi=(np.arange(n)+.5)*2*np.pi/n
    # z component dl cross (receiver-source), integrated over filament.
    distance2=separation**2+a*a-2*separation*a*np.cos(phi)
    numerator=a*a-a*separation*np.cos(phi)
    return 1e-7*float(np.sum(numerator/distance2**1.5))*2*np.pi/n


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    rows=[]
    for a,b,d in [(100,100,1000),(100,10,1000),(100,100,10000),(100,100,500),(300,100,1500)]:
        # Negative sign from coplanar equal-normal winding orientation.
        md=-1e-7*(math.pi*a*a)*(math.pi*b*b)/d**3
        m256=mutual_neumann(a,b,d,256)
        m512=mutual_neumann(a,b,d,512)
        exact_b=center_b_per_amp(a,d,4096)
        r1=1.724e-8*(2*math.pi*a)/(2.5e-6)
        r2=1.724e-8*(2*math.pi*b)/(2.5e-6)
        w=2*math.pi*10
        load=r2*math.sqrt(1+(w*m512)**2/(r1*r2))
        # Solve complex two-port directly; adjust source amplitude to100W input.
        matrix=np.array([[r1,1j*w*m512],[1j*w*m512,r2+load]],complex)
        currents=np.linalg.solve(matrix,np.array([1,0],complex))
        input_per_v=float(currents[0].real)
        voltage=math.sqrt(100/input_per_v)
        output=abs(currents[1]*voltage)**2*load
        rows.append(dict(tx_radius_m=a,rx_radius_m=b,distance_m=d,
                         mutual_256_h=m256,mutual_512_h=m512,dipole_mutual_h=md,
                         quadrature_relative_change=abs(m512-m256)/abs(m512),
                         dipole_relative_error=abs(md-m512)/abs(m512),
                         exact_center_field_t_per_a=exact_b,
                         exact_circuit_load_w=output))
    result=dict(host=platform.node(),platform=platform.platform(),
                python=platform.python_version(),numpy=np.__version__,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                model='vacuum quasistatic exact circular filaments; tuned two-port;100W input,10Hz,2.5mm2 copper',
                rows=rows)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
