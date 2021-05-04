# Import the Maya commands library
from maya import cmds

# Create a window using the cmds.window command
# give it a title, icon and dimensions
window = cmds.window( title="Long Name", iconName='Short Name', widthHeight=(200, 55) )

# As we add contents to the window, align them vertically
cmds.columnLayout( adjustableColumn=True )

# A button that does nothing
cmds.button( label='Do Nothing' )

# Close button with a command to delete the UI
cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )

# Set its parent to the Maya window (denoted by '..')
cmds.setParent( '..' )

# Show the window that we created (window)
cmds.showWindow( window )