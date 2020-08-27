from math import log
import sys

class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. 
  islead (boolean): whether this is a leaf. False.
  """
  
  def __init__(self,attr):
    self.children = {}
    self.attr = attr
    self.isleaf = False

class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.
    
    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """
    def __init__(self,value):
        self.value = value
        self.isleaf = True
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print str(self)
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.isleaf:
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.isleaf:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)
  
  def classify(self, classificationData):
    """
    Uses the classification tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with this tree.
    """
    #YOUR CODE HERE
    node = self.root

    if not node.isleaf:

        createTemp1 = classificationData[node.attr]
        createTemp2 = node.children[createTemp1]

        createPartial = Tree(createTemp2)
        return createPartial.classify(classificationData)

    else:
        return node.value


def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE

    for place in examples:

        if attrName in place:
            if place[attrName] == attrValue:
                newExamples.append(place)
        else:
            continue

    return newExamples


def getClassCounts(examples,className):
    """
    Helper function to get a dictionary of counts of different class values
    in a set of examples. That is, this returns a dictionary where each key 
    in the list corresponds to a possible value of the class and the value
    at that key corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """
    classCounts = {}
    #YOUR CODE HERE

    for place in examples:

        holdTemp = place[className]

        if holdTemp not in classCounts.keys():
            classCounts[holdTemp] = 1
        else:
            classCounts[holdTemp] = 1 + classCounts[holdTemp]

    return classCounts


def getMostCommonClass(examples,className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples,className)
    return max(counts, key=counts.get) if len(examples)>0 else None

def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a dictionary of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
	  That is, this returns a dictionary of dictionaries, where each key  
	  corresponds to a possible value of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for the attribute
        className (str): the name of the class
    Returns:
        dictionary<str,dictionary<str,int>>
        This is a dictionary that for each value of the attribute has a
        dictionary from class values to class counts, as in getClassCounts
    """
    attributeCounts = {}
    #YOUR CODE HERE

    for place in attrValues:

        requiredCases = getPertinentExamples(examples, attrName, place)
        calculateNum = getClassCounts(requiredCases, className)

        attributeCounts[place] = calculateNum

    return attributeCounts


def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE

    averageNum = sum(classCounts)
    calculateNum = 0

    for place in classCounts:

        float1 = float(place) / averageNum
        temp1 = log(float1, 2)
        temp2 = float1 * temp1

        negateTemp = (-1) * temp2
        calculateNum = calculateNum + negateTemp

    return calculateNum


def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.




    """
    #YOUR CODE HERE

    calculateNum = 0
    size = len(examples)

    for part in attrValues:
        place = getAttributeCounts(examples, attrName, attrValues, className)[part].values()

        sum1 = sum(place)
        float1 = float(sum1)
        temp1 = float1 / size

        temp2 = temp1 * setEntropy(place)
        calculateNum = calculateNum + temp2

    return calculateNum


def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE

    keepNum = getClassCounts(examples, className)
    holdNum = keepNum.values()
    numRange = list(holdNum)

    tempVar1 = setEntropy(numRange)
    tempVar2 = remainder(examples, attrName, attrValues, className)
    subtractMath = tempVar1 - tempVar2

    return subtractMath



  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE

    calculateNum = 1
    averageNum = sum(classCounts)
    #count = 0

    for place in classCounts:

        float1 = float(place)
        temp1 = float1 / averageNum
        temp2 = temp1 ** 2
        negateTemp = (-1) * temp2

        calculateNum = calculateNum + negateTemp

    return calculateNum



def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE

    calculateNum = 0
    size = len(examples)

    for part in attrValues:
        place = getAttributeCounts(examples, attrName, attrValues, className)[part].values()

        averageNum = sum(place)
        float1 = float(averageNum)

        temp1 = giniIndex(place)
        temp2 = float1 / size
        temp3 = temp1 * temp2

        calculateNum = calculateNum + temp3

    if not (calculateNum == 0):
        return 1.0 / calculateNum
    else:
        return sys.maxint


def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE

    size1 = len(examples)
    size2 = len(remainingAttributes)
    keepNum1 = getClassCounts(examples, className).keys()
    size3 = len(keepNum1)
    keepNum2 = getMostCommonClass(examples, className)

    temp1 = LeafNode(defaultLabel)
    temp2 = LeafNode(examples[0][className])
    temp3 = LeafNode(keepNum2)

    if (not(size1 == 0)) and (not(size3 == 1)) and (not(size2 == 0)):
        tempVar1 = remainingAttributes[0]
        tempVar2 = attributeValues[tempVar1]
        tempVar3 = infoGain(examples, tempVar1, tempVar2, className)

        for place in remainingAttributes:

            holdNum = infoGain(examples, place, attributeValues[place], className)

            if not (holdNum > tempVar3):
                continue

            else:
                tempVar3 = holdNum
                tempVar1 = place

        createPartial = Node(tempVar1)
        # leftOver = list(remainingAttributes)

        for part in attributeValues[tempVar1]:

            holdProp = getPertinentExamples(examples, tempVar1, part)
            propSize = len(holdProp)

            if not (propSize == 0):
                tempArr = []
                for piece in remainingAttributes:
                    tempArr.append(piece)

                newProp = tempArr
                newProp.remove(tempVar1)

                newNum = getMostCommonClass(holdProp, className)
                createPartial.children[part] = makeSubtrees(newProp, holdProp,
                                                            attributeValues, className, newNum,
                                                            setScoreFunc, gainFunc)

            else:
                createPartial.children[part] = temp1

        return createPartial

    else:
        if size1 == 0:
            return temp1
        elif size3 == 1:
            return temp2
        elif size2 == 0:
            return temp3



def makePrunedTree(examples, attrValues,className,setScoreFunc,gainFunc,q):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makePrunedSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc,q))
    
def makePrunedSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc,q):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE (Extra Credit)
