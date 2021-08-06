from kfp import components
from kfp import dsl
from kubernetes.client import V1Toleration
from kubernetes.client.models import (
    V1VolumeMount,
    V1Volume,
    V1PersistentVolumeClaimVolumeSource,
    V1EmptyDirVolumeSource
)

from utils import add_env


def add_ssh_volume(op):
    op.container.add_volume_mount(V1VolumeMount(name='ssh-v', mount_path='/root/.ssh'))
    return op


@dsl.pipeline(
    name='Generate point cloud for augmented home assistant',
    description='Generate point cloud for augmented home assistant'
)
def gen_pointcloud(
        image,
        git_rev,
        actions,
        s3_pointcloud_dir
):
    train_env = {}

    train_num_gpus = 1
    train_op = components.load_component_from_file('components/train.yaml')(
        image=image,
        git_rev=git_rev,
        actions=actions,
        s3_pointcloud_dir=s3_pointcloud_dir)
    (train_op.container
     .set_memory_request('29Gi')
     .set_memory_limit('29Gi')
     .set_cpu_request('3.5')
     .set_cpu_limit('3.5')
     .set_gpu_limit(str(train_num_gpus))
     .add_volume_mount(V1VolumeMount(name='tensorboard', mount_path='/shared/tensorboard'))
     .add_volume_mount(V1VolumeMount(name='shm', mount_path='/dev/shm'))
     )
    (add_env(add_ssh_volume(train_op), train_env)
     .add_toleration(V1Toleration(key='nvidia.com/gpu', operator='Exists', effect='NoSchedule'))
     .add_node_selector_constraint('beta.kubernetes.io/instance-type', f'g3s.xlarge')
     .add_volume(V1Volume(name='tensorboard',
                          persistent_volume_claim=V1PersistentVolumeClaimVolumeSource('tensorboard-research-kf')))
     .add_volume(V1Volume(name='shm', empty_dir=V1EmptyDirVolumeSource(medium='Memory')))
     )
