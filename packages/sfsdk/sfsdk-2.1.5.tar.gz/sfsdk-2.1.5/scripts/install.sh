cd "$(dirname "$0")"/..

echo y | pip3 uninstall sfsdk; \
  rm -rf dist build; \
  pip3 install --user .
