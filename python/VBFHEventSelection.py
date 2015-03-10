#very simple EventSelection class aimed at demonstrating the 
#typical implementation of an EventSelection class

#On purpose, the categories are not in any "logical" order, and there is some redundant check when testing the category.
#This is mostly for illustration.

# requirements:
#   event.muons
#   event.electrons
#   event.jets

# the list of category names
categoryNames = [ "Test" ]

def eventCategory(event):
  """Check analysis requirements for various steps
     and return a tuple of data used to decide 
     to what category an event belong """
  categoryData = [ ]
  # 0: everything
  categoryData.append(True)
  # DONE
  return categoryData

def isInCategory(category, categoryData):
  """Check if the event enters category X, given the tuple computed by eventCategory."""
  if category==0:
    return (categoryData[0] is True)
  else:
    return False

