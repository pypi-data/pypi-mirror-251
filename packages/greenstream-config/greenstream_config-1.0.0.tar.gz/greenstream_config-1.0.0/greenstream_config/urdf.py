from urchin import Link, Joint
from typing import List, Tuple
from greenstream_config.types import Camera, CameraOverride, GreenstreamConfig

def get_camera_urdf(camera: Camera) -> Tuple[Link, Joint]:
    # This is the camera urdf from the gama/lookout greenstream.launch.py
    # We need to generate this from the camera config
    return Link(), Joint()
 
def get_cameras_urdf(cameras: List[Camera]) -> Tuple[List[Link], List[Joint]]:
    # This is the cameras urdf from the gama/lookout greenstream.launch.py
    # We need to generate this from the camera config
    #
    links: List[Link] = []
    joints: List[Joint] = []
    for camera in cameras:
        link, join = get_camera_urdf(camera)
        links.append(link)
        joints.append(join)
        
    return links, joints