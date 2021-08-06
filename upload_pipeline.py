import generate_gen_pointcloud
from utils import upload_pipeline
import sys

resp = upload_pipeline(sys.argv[2], getattr(generate_gen_pointcloud, sys.argv[1]))
print(resp)
