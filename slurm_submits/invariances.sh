#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --output=/vol/bitbucket/g21mscprj03/SSL/out/invariances/%j.out


export PATH=/vol/bitbucket/g21mscprj03/sslvenv/bin/:$PATH
source activate
source /vol/cuda/11.0.3-cudnn8.0.5.39/setup.sh
TERM=vt100  # TERM=xterm
/usr/bin/nvidia-smi
uptime

cd /vol/bitbucket/g21mscprj03/SSL

model=byol
dset=cifar10
python invariances.py --dataset $dset --model $model --transform rotation