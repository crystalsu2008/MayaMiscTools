# MayaMiscTools
MayaMiscTools is a collection of some miscellaneous tools and scripts for Autodesk Maya. It's written in Python or MEL.

__Procedure Name__ : MayaMiscTools<br>
__Update__ : July 26, 2016<br>
__Author__ : Chris Su<br>
__Contact__ : crystalsu2008@gmail.com<br>

## History:
* v0.0

## How to use:
Put all scripts in a folder. It's recommended to place this folder in your Maya scripts folder, but it can be anywhere. Once you have the MayaMiscTools folder where you want it to be, then just drag and drop the "install.mel" file into Maya (drop in any viewport). This will add MayaMiscTools tool to the current shelf.<br>

## Functions:
* Rigging Tools<br>
This is a collection of few little tools for Rigging and Animation.
    * -Quick set joint's size.<br>
    -Quick change joints color, remove joints color and random set joints color.
    * -Show or hide joint's label.<br>
    -Show or hide joint's Local Rotation Axis.
    * -Manager dagPoses in the scenes.<br>
    -Go to the pose or bindPose.<br>
    -Create a new pose with selected objects.<br>
    -Switch selected poses to bindPose or non-bindPose.<br>
    -Adding the selected items to the dagPose. ```It's still some problems```<br>
    -Remove the selected joints from the specified pose. ```It's still some problems```<br>
    -Reset the pose to current pose.<br>
    -Rebind selected skin geometry at current pose, and keep the skin weights.```Not Done```
    * -(Lock and Hide) or (Unlocked and Show) joint's transform attributes.
    * -Select joints at the root of hierarchy.<br>
    -Select joints at the end of hierarchy.
    * -Set joint orient attribute to zero.<br>
    -Convert Kinect1 Skeleton System to Kinect2.<br>
    -Remove the Invalid Intermediate nodes under the selected objects.<br>
    -Show the Intermediate nodes under the selected objects.<br>
    -Quick switch between the Final objects and the Origin Intermediate objects. It's very useful to do some modify before the Construction History.


* Unique Name Manager<br>
This function is used to find out all dag nodes in the scenes those have same name, and fix the problem.

* Batch Processing Files```(It's not done yet!!!)```<br>
This procedure is used to execute a paragraph of script in the selected files.

* Others<br>
This is a collection of some not commonly tools.
