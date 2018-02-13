import json
import sys

def parse_Literal(js):
    """A literal value, ex 42"""
    print("In Literal: kind=" + js['kind'] + " value=" + js['value'])

def parse_Continue(js):
    """Continue key word"""
    print("In Continue")

def parse_PlaceholderStatement(js):
    print("In PlaceholderStatement")

def parse_ElementaryTypeNameExpression(js):
    """Contains type descriptions"""
    print("In ElementaryTypeNameExpression")

def parse_Identifier(js):
    """Name for a variable. Can be found inside a MemberAccess"""
    print("In Identifier: name=" + js['name'])

def parse_MemberAccess(js):
    """Index into a structure to extract a value"""
    print("In MemberAccess: memberName=" + js['memberName'])
    parse(js['expression'])

def parse_IndexAccess(js):
    """Index into an array, ex: arr[3]"""
    print("In IndexAccess")
    parse(js['baseExpression'])
    parse(js['indexExpression'])

def parse_BinaryOperation(js):
    """An operator that acts on two values"""
    print("In BinaryOperation: operator:" + js['operator'])
    parse(js['leftExpression'])
    parse(js['rightExpression'])

def parse_UnaryOperation(js):
    """An operator that acts on one value"""
    print("In UnaryOperation: operator: " + js['operator'])
    parse(js['subExpression'])

def parse_Assignment(js):
    """Contains nodes to the left and right of the operator"""
    print("In Assignment: operator:" + js['operator'])
    parse(js['leftHandSide'])
    parse(js['rightHandSide'])

def parse_ExpressionStatement(js):
    """Node that indicates the line is an expression, such as an Assignment"""
    print("In ExpressionStatement")
    parse(js['expression'])

def parse_IfStatement(js):
    """Declaration and parameters for an if statement
        May or may not have an else statement"""
    print("In IfStatement")
    parse(js['condition'])
    parse(js['trueBody'])
    if js['falseBody'] != None:
        parse(js['falseBody'])

def parse_WhileStatement(js):
    """Declaration and parameters for a while statement"""
    print("In WhileStatement")
    parse(js['condition'])
    parse(js['body'])

def parse_ForStatement(js):
    """Declaration and parameters for a for statement"""
    print("In ForStatement")
    parse(js['initializationExpression'])
    parse(js['condition'])
    parse(js['loopExpression'])
    parse(js['body'])

def parse_Block(js):
    """Contains a list of statements and is widely used to organize 
        other nodes such as FunctionDefinitions"""
    print("In Block")
    for js_expression in js['statements']:
        parse(js_expression)

def parse_TupleExpression(js):
    """Indicates use of a tuple"""
    print("In TupleExpression")
    for component in js['components']:
        parse(component)

def parse_ArrayTypeName(js):
    """The type for an array, ex int[]"""
    print("In ArrayTypeName")
    parse(js['baseType'])

def parse_UserDefinedTypeName(js):
    """Indicates declaring a new user defined enumeration type"""
    print("In UserDefinedTypeName: name=" + js['name'])

def parse_EnumDefinition(js):
    print("In EnumDefinition: name=" + js['name'])
    for member in js['members']:
        parse(member)

def parse_EnumValue(js):
    """Usage of an Enumeration Value"""
    print("In EnumValue: name=" + js['name'])

def parse_StructDefinition(js):
    """Definition for a new structure datatype"""
    print("In StructDefinition: name=" + js['name'])
    for member in js['members']:
        parse(member)

def parse_ParameterList(js):
    """A list of parameters that may be passed to a function, constructor, etc"""
    print("In ParameterList")
    for param in js['parameters']:
        parse(param)

def parse_Return(js):
    """Return statement from a function"""
    print("In Return")
    parse(js['expression'])

def parse_FunctionCall(js):
    """Contains all function calling params and values"""
    print("In FunctionCall")
    parse(js['expression'])
    for arg in js['arguments']:
        parse(arg)

def parse_FunctionDefinition(js):
    """Indicates the top of a function definition"""
    print("In FunctionDefinition: name=" + js['name'] + " payable=" + str(js['payable']))
    parse(js['body'])

def parse_ModifierDefinition(js):
    """Definition for a modifier, like a wrapper function"""
    print("In ModifierDefinition: name=" + js['name'])
    parse(js['parameters'])
    parse(js['body'])

def parse_EventDefinition(js):
    """Indicates the top of an event definition (like a wrapper function)"""
    print("In EventDefinition name=" + js['name'])
    parse(js['parameters'])

def parse_ElementaryTypeName(js):
    """Gives the type of an elementary type, ex byte32"""
    print("In ElementaryTypeName")

def parse_Mapping(js):
    """Indicates that we are declaring a mapping variable"""
    print("In Mapping")
    parse(js['keyType'])
    parse(js['valueType'])

def parse_VariableDeclarationStatement(js):
    print("In VariableDeclarationStatement")
    if js['initialValue'] != None:
        parse(js['initialValue'])
    for declaration in js['declarations']:
        parse(declaration)

def parse_VariableDeclaration(js):
    """Contains one contract-wide variable declaration"""
    print("In VariableDeclaration: name=" + js['name'])

def parse_ContractDefinition(js):
    """Top of a contract"""
    print("In ContractDefinition: name=" + js['name'])
    for js_node in js['nodes']:
        parse(js_node)

def parse_PragmaDirective(js):
    """Indicates the solidity type we are compiling with"""
    print("In PragmaDirective")

def parse_SourceUnit(js):
    """Top level node that holds all nodes"""
    print("In SourceUnit")
    for js_node in js['nodes']:
        parse(js_node)

def parse(js):
    """ Parses the input json tree to discover variable names """
    # Determine the node type and execute node specific code
    if js['nodeType'] == 'SourceUnit':
        parse_SourceUnit(js)
    elif js['nodeType'] == 'PragmaDirective':
        parse_PragmaDirective(js)
    elif js['nodeType'] == 'ContractDefinition':
        parse_ContractDefinition(js)
    elif js['nodeType'] == 'VariableDeclaration':
        parse_VariableDeclaration(js)
    elif js['nodeType'] == 'VariableDeclarationStatement':
        parse_VariableDeclarationStatement(js)
    elif js['nodeType'] == 'Mapping':
        parse_Mapping(js)
    elif js['nodeType'] == 'ElementaryTypeName':
        parse_ElementaryTypeName(js)
    elif js['nodeType'] == 'EventDefinition':
        parse_EventDefinition(js)
    elif js['nodeType'] == 'ModifierDefinition':
        parse_ModifierDefinition(js)
    elif js['nodeType'] == 'FunctionDefinition':
        parse_FunctionDefinition(js)
    elif js['nodeType'] == 'FunctionCall':
        parse_FunctionCall(js)
    elif js['nodeType'] == 'Return':
        parse_Return(js)
    elif js['nodeType'] == 'ParameterList':
        parse_ParameterList(js)
    elif js['nodeType'] == 'StructDefinition':
        parse_StructDefinition(js)
    elif js['nodeType'] == 'EnumDefinition':
        parse_EnumDefinition(js)
    elif js['nodeType'] == 'EnumValue':
        parse_EnumValue(js)
    elif js['nodeType'] == 'UserDefinedTypeName':
        parse_UserDefinedTypeName(js)
    elif js['nodeType'] == 'ArrayTypeName':
        parse_ArrayTypeName(js)
    elif js['nodeType'] == 'TupleExpression':
        parse_TupleExpression(js)
    elif js['nodeType'] == 'Block':
        parse_Block(js)
    elif js['nodeType'] == 'IfStatement':
        parse_IfStatement(js)
    elif js['nodeType'] == 'ForStatement':
        parse_ForStatement(js)
    elif js['nodeType'] == 'WhileStatement':
        parse_WhileStatement(js)
    elif js['nodeType'] == 'ExpressionStatement':
        parse_ExpressionStatement(js)
    elif js['nodeType'] == 'Assignment':
        parse_Assignment(js)
    elif js['nodeType'] == 'UnaryOperation':
        parse_UnaryOperation(js)
    elif js['nodeType'] == 'BinaryOperation':
        parse_BinaryOperation(js)
    elif js['nodeType'] == 'IndexAccess':
        parse_IndexAccess(js)
    elif js['nodeType'] == 'MemberAccess':
        parse_MemberAccess(js)
    elif js['nodeType'] == 'Identifier':
        parse_Identifier(js)
    elif js['nodeType'] == 'ElementaryTypeNameExpression':
        parse_ElementaryTypeNameExpression(js)
    elif js['nodeType'] == 'PlaceholderStatement':
        parse_PlaceholderStatement(js)
    elif js['nodeType'] == 'Continue':
        parse_Continue(js)
    elif js['nodeType'] == 'Literal':
        parse_Literal(js)
    else:
        print("Node type not recognized: " + str(js['nodeType']))

if __name__ == "__main__":
    # Get path to solc json output
    file_path = sys.argv[1]
    file_contents = ''
    with open(file_path, 'r') as file:
        line_num = 0
        for line in file:
            # Skip first 4 lines
            if line_num >= 4:
                file_contents += line;
            line_num += 1
    solc_json = json.loads(file_contents)
    parse(solc_json)
