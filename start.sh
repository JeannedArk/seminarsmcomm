#!/bin/bash
DIRECTORY="/Applications/blender-2.*/blender.app/Contents/MacOS/blender"

# Start Visual SceneMaker
java -classpath "./VisualSceneMaker/bld/VisualSceneMaker3.jar" de.dfki.vsm.SceneMaker3 >> /dev/null
if [ -f $DIRECTORY ]; then
    # Start Blender with Anna file
    open $DIRECTORY "./Anna/Anna-v04.blend"
else
    echo "Blender path not found. Expected Blender installation path in $DIRECTORY"
fi