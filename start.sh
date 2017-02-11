#!/bin/bash
APPLICATION1="/Applications/blender-2.*/blender.app/Contents/MacOS/blender"
APPLICATION2="/Applications/blender.app/Contents/MacOS/blender"

if [ -f $APPLICATION1 ]; then
    # Start Visual SceneMaker
    java -classpath "./VisualSceneMaker/bld/VisualSceneMaker3.jar" de.dfki.vsm.SceneMaker3 >> /dev/null &
    # Start Blender with Anna file
    open $APPLICATION1 "./Anna/Anna-v04.blend"
elif [ -f $APPLICATION2 ]; then
    # Start Visual SceneMaker
    java -classpath "./VisualSceneMaker/bld/VisualSceneMaker3.jar" de.dfki.vsm.SceneMaker3 >> /dev/null &
    # Start Blender with Anna file
    open $APPLICATION2 "./Anna/Anna-v04.blend"
else
    echo "Blender path not found. Expected Blender installation path in $APPLICATION1 or $APPLICATION2"
fi