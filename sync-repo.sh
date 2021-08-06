# update with github
set -ex

pushd /arhome/virtualhome
MODEL_HEAD=`git rev-parse HEAD`
if [ -n "${SCRIPT_VERSION}" ] && [ "${SCRIPT_VERSION}" != "${MODEL_HEAD}" ]; then
  git fetch
  git checkout ${SCRIPT_VERSION}
  python3 -m pip install -r requirements.txt
fi
popd