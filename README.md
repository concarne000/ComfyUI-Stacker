# ComfyUI-Stacker
Simple stack push/pop for images, strings and integers.

The main use of this is to reduce unloading and loading of models when there are multiple steps in a workflow.
E.g. using an SDXL model with ControlNet to create images to later feed into an Image to Video model.

The Push nodes will save a file in the specified folder, default being a 'Stack' folder under the 'ComfyUI' folder. It will save a PNG for images, and text files for strings and numbers.

The Pop will take the last file that was saved in the stack, and then delete it.
The Pop nodes allow the option to override the pop, e.g. if you want to change the prompt for a generation without repushing another prompt. The stack will remain unchanged with the override enabled.
The Pop nodes also allow a fallback when the stack is empty, without the fallback enabled the node with throw an exception stopping the generation. Note that any pops done before the exception in a generation will remain popped from the stacks.

The 'Key' can be considered the variable name of the stack. For example, you could have two StackPushInt nodes, one with the key of 'width' and the other 'height', then be able to pull the right number in the next workflow for each variable.

A generic object stack has also been implemented, but by default it is disabled.

# Todo

~~Clean the key text~~

~~Allow the stack to pop a default value if it is empty~~

~~Add an override option~~

Allow a 'peek' and 'sneak from bottom' option

Fix a 'no-change' prompt still having to be re-encoded
