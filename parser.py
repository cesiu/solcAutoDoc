# Parses solc --ast-compact-json output. Produces code->English translations. Places translations into tree.
# Eric LaBouve (elabouve@calpoly.edu)
# CSC 570, Winter '18

import json
import sys
import re

from functools import reduce
import magic_nlp

binary_op_to_english = {"*":" multiplied by ", "/":" divided by ", "%":" remainder of ", "+":" added to ", "-":" subtracted by ", "&&":" and ", "||":" or ", ">":" is greater than ", "<":" is less than ", ">=":" is greater than or equal to ", "<=":" is less than or equal to ", "==":" is equal to ", "!=":" is not equal to "}
unary_op_to_english = {"++":" add one to ", "--":" remove one from ", "!":" not ", "-":" negative of "}
assignment_op_to_english = {"=":" is ", "+=":" gains ", "-=":" loses ", "*=":" multiplied by ", "/=":" divided by ", "%=":" moded by "}
msg_members_to_english = {"data":" the complete calldata ", "gas":" the remaining money in this function ", "sender":" the money sender ", "sig":" the function the sender activated ", "value":" the money sent by the sender "}

msg_found = False
found_first_function = False # Dont comment code above the first function
                             # Code above first function are variable and struct definitions
in_for_loop_header = False

def parse_var_names(_str):
    """Separate any snake_case or CamelCase words before adding to description"""
    global found_first_function
    if found_first_function:
        space_sep_str = re.sub('([A-Z]+)', r' \1', _str).lower()
        # space_sep_str = re.sub('_', r' \1', space_sep_str).lower()
        space_sep_str = re.sub('_', ' ', space_sep_str).lower()
        return " " + space_sep_str + " "
    else:
        return ""

def dedupe_spaces(description):
    """Remove any extra spaces between words
       Called from ExpressionStatement nodes"""
    # Remove any extra spaces
    single_space_sep_desc = re.sub(' +', ' ', description)
    # Smoosh together apostrophes and commas
    single_space_sep_desc = re.sub(' \'', '\'', single_space_sep_desc)
    single_space_sep_desc = re.sub(' ,', ',', single_space_sep_desc)
    return single_space_sep_desc

def parse_Literal(js):
    """A literal value, ex 42"""
    #print("In Literal: kind=" + js['kind'] + " value=" + js['value'])
    return parse_var_names(js['value'])

def parse_Continue(js):
    """Continue key word"""
    #print("In Continue")
    return "do nothing"

def parse_PlaceholderStatement(js):
    #print("In PlaceholderStatement")
    return ""

def parse_ElementaryTypeNameExpression(js):
    """Contains type descriptions"""
    #print("In ElementaryTypeNameExpression")
    return ""

def parse_Identifier(js):
    """Name for a variable. Can be found inside a MemberAccess"""
    #print("In Identifier: name=" + js['name'])
    global msg_found
    if js['name'] == 'msg':
        msg_found = True
        return ""
    else:
        return parse_var_names(js['name'])

def parse_MemberAccess(js):
    """Index into a structure to extract a value"""
    #print("In MemberAccess: memberName=" + js['memberName'])
    global msg_found
    ret_str = parse(js['expression'])
    if msg_found:
        ret_str += parse_var_names(msg_members_to_english[js['memberName']])
        msg_found = False
    else:
        ret_str += parse_var_names('\'s ' + js['memberName'] + ' ')
    return ret_str

def parse_IndexAccess(js):
    """Index into an array, ex: arr[3]"""
    #print("In IndexAccess")
    return parse(js['baseExpression']) \
           + parse_var_names(" list at ") \
           + parse(js['indexExpression'])

def parse_BinaryOperation(js):
    """An operator that acts on two values"""
    #print("In BinaryOperation: operator:" + js['operator'])
    return parse(js['leftExpression']) \
           + parse_var_names(binary_op_to_english[js['operator']]) \
           + parse(js['rightExpression'])

def parse_UnaryOperation(js):
    """An operator that acts on one value"""
    #print("In UnaryOperation: operator: " + js['operator'])
    return parse_var_names(unary_op_to_english[js['operator']]) \
           + parse(js['subExpression'])

def parse_Assignment(js):
    """Contains nodes to the left and right of the operator"""
    #print("In Assignment: operator:" + js['operator'])
    return parse(js['leftHandSide']) \
           + parse_var_names(assignment_op_to_english[js['operator']]) \
           + parse(js['rightHandSide'])

def parse_ExpressionStatement(js):
    """Node that indicates the line is an expression, such as an Assignment"""
    #print("In ExpressionStatement")
    return dedupe_spaces(parse(js['expression']))

def parse_IfStatement(js):
    """Declaration and parameters for an if statement
        May or may not have an else statement"""
    #print("In IfStatement")
    cond_str = parse(js['condition'])

    ret_str = "\nIf " + cond_str + " then do "
    ret_str += parse(js['trueBody'])
    ret_str += "\nThis only happens if " + cond_str

    if js['falseBody'] != None:
        ret_str += "\nIf it is not the case that " + cond_str
        ret_str += parse(js['falseBody'])
        ret_str += "\nThis only happens if it is not the case that " + cond_str

    return dedupe_spaces(ret_str)

def parse_WhileStatement(js):
    """Declaration and parameters for a while statement"""
    #print("In WhileStatement")
    return "\nAs long as " \
           + parse(js['condition']) \
           + " do\n" \
           + parse(js['body']) \
           + " and this continues as long as " \
           + parse(js['condition']) + "\n"

def parse_ForStatement(js):
    """Declaration and parameters for a for statement"""
    #print("In ForStatement")
    global in_for_loop_header

    in_for_loop_header = True
    ret_str = "\nSet "
    ret_str += parse(js['initializationExpression'])
    ret_str += "\nThen as long as "
    ret_str += parse(js['condition'])
    ret_str += " do\n"

    in_for_loop_header = False
    ret_str += parse(js['body'])
    ret_str += "\nEach time that happens "

    in_for_loop_header = True
    ret_str += parse(js['loopExpression'])
    ret_str += " and this continues as long as "
    ret_str += parse(js['condition'])

    return dedupe_spaces(ret_str) + "\n"

def parse_Block(js):
    """Contains a list of statements and is widely used to organize
        other nodes such as FunctionDefinitions"""
    #print("In Block")
    ret_str = ""
    ret_strs = []
    for js_expr in js['statements']:
        if js_expr['nodeType'] != 'IfStatement' \
           and js_expr['nodeType'] != 'ForStatement' \
           and js_expr['nodeType'] != 'WhileStatement':
            ret_strs.append(dedupe_spaces(parse(js_expr).strip()))
        else:
            ret_strs = magic_nlp.preproc(ret_strs)
            ret_str += reduce(magic_nlp.concat, ret_strs, "")
            ret_strs = []
            ret_str += parse(js_expr)

    if ret_strs:
        ret_strs = magic_nlp.preproc(ret_strs)
        ret_str += reduce(magic_nlp.concat, ret_strs, "")
    return ret_str

def parse_TupleExpression(js):
    """Indicates use of a tuple"""
    #print("In TupleExpression")
    ret_str = ""
    for component in js['components']:
        ret_str += parse(component)
    return ret_str

def parse_ArrayTypeName(js):
    """The type for an array, ex int[]"""
    #print("In ArrayTypeName")
    return parse(js['baseType'])

def parse_UserDefinedTypeName(js):
    """Indicates declaring a new user defined enumeration type"""
    #print("In UserDefinedTypeName: name=" + js['name'])
    return ""

def parse_EnumDefinition(js):
    #print("In EnumDefinition: name=" + js['name'])
    ret_str = ""
    for member in js['members']:
        ret_str += parse(member)
    return ret_str

def parse_EnumValue(js):
    """Usage of an Enumeration Value"""
    #print("In EnumValue: name=" + js['name'])
    return ""

def parse_StructDefinition(js):
    """Definition for a new structure datatype"""
    #print("In StructDefinition: name=" + js['name'])
    ret_str = ""
    for member in js['members']:
        ret_str += parse(member)
    return ret_str

def parse_ParameterList(js):
    """A list of parameters that may be passed to a function, constructor, etc"""
    #print("In ParameterList")
    ret_str = ""
    for param in js['parameters']:
        ret_str += parse(param)
    return ret_str

def parse_Return(js):
    """Return statement from a function"""
    #print("In Return")
    if js['expression'] != None:
        return parse(js['expression'])
    else:
        return ""

def parse_FunctionCall(js):
    """Contains all function calling params and values"""
    #print("In FunctionCall")
    ret_str = parse(js['expression'])
    for arg in js['arguments']:
        ret_str += parse(arg)
    return ret_str

def parse_FunctionDefinition(js):
    """Indicates the top of a function definition"""
    #print("In FunctionDefinition: name=" + js['name'] + " payable=" + str(js['payable']))
    global found_first_function
    found_first_function = True
    return parse(js['body']) + "\n\n"

def parse_ModifierDefinition(js):
    """Definition for a modifier, like a wrapper function"""
    #print("In ModifierDefinition: name=" + js['name'])
    return parse(js['parameters']) + parse(js['body'])

def parse_EventDefinition(js):
    """Indicates the top of an event definition (like a wrapper function)"""
    #print("In EventDefinition name=" + js['name'])
    return parse(js['parameters'])

def parse_ElementaryTypeName(js):
    """Gives the type of an elementary type, ex byte32"""
    #print("In ElementaryTypeName")
    return ""

def parse_Mapping(js):
    """Indicates that we are declaring a mapping variable"""
    #print("In Mapping")
    return parse(js['keyType']) + parse(js['valueType'])

def parse_VariableDeclarationStatement(js):
    """Declare a list of variables. ex: i, j, k = 0;"""
    #print("In VariableDeclarationStatement")
    ret_str = ""
    declarations_size = len(js['declarations'])
    for declaration in js['declarations']:
        ret_str += parse(declaration)
        if declarations_size > 1:
            ret_str += parse_var_names(' and ')
        declarations_size -= 1
    ret_str += parse_var_names(' is ')
    if js['initialValue'] != None:
        ret_str += parse(js['initialValue'])
    else:
        ret_str += parse_var_names(' default value ')
    if not in_for_loop_header:
        ret_str = dedupe_spaces(ret_str)
    return ret_str

def parse_VariableDeclaration(js):
    """Contains one contract-wide variable declaration"""
    #print("In VariableDeclaration: name=" + js['name'])
    return parse_var_names(js['name'])

def parse_ContractDefinition(js):
    """Top of a contract"""
    #print("In ContractDefinition: name=" + js['name'])
    ret_str = ""
    for js_node in js['nodes']:
        ret_str += parse(js_node)
    return ret_str

def parse_PragmaDirective(js):
    """Indicates the solidity type we are compiling with"""
    #print("In PragmaDirective")
    return ""

def parse_SourceUnit(js):
    """Top level node that holds all nodes"""
    #print("In SourceUnit")
    ret_str = ""
    for js_node in js['nodes']:
        ret_str += parse(js_node)
    return ret_str

def parse(js):
    """ Parses the input json tree to discover variable names """
    # Determine the node type and execute node specific code
    if js['nodeType'] == 'SourceUnit':
        return parse_SourceUnit(js)
    elif js['nodeType'] == 'PragmaDirective':
        return parse_PragmaDirective(js)
    elif js['nodeType'] == 'ContractDefinition':
        return parse_ContractDefinition(js)
    elif js['nodeType'] == 'VariableDeclaration':
        return parse_VariableDeclaration(js)
    elif js['nodeType'] == 'VariableDeclarationStatement':
        return parse_VariableDeclarationStatement(js)
    elif js['nodeType'] == 'Mapping':
        return parse_Mapping(js)
    elif js['nodeType'] == 'ElementaryTypeName':
        return parse_ElementaryTypeName(js)
    elif js['nodeType'] == 'EventDefinition':
        return parse_EventDefinition(js)
    elif js['nodeType'] == 'ModifierDefinition':
        return parse_ModifierDefinition(js)
    elif js['nodeType'] == 'FunctionDefinition':
        return parse_FunctionDefinition(js)
    elif js['nodeType'] == 'FunctionCall':
        return parse_FunctionCall(js)
    elif js['nodeType'] == 'Return':
        return parse_Return(js)
    elif js['nodeType'] == 'ParameterList':
        return parse_ParameterList(js)
    elif js['nodeType'] == 'StructDefinition':
        return parse_StructDefinition(js)
    elif js['nodeType'] == 'EnumDefinition':
        return parse_EnumDefinition(js)
    elif js['nodeType'] == 'EnumValue':
        return parse_EnumValue(js)
    elif js['nodeType'] == 'UserDefinedTypeName':
        return parse_UserDefinedTypeName(js)
    elif js['nodeType'] == 'ArrayTypeName':
        return parse_ArrayTypeName(js)
    elif js['nodeType'] == 'TupleExpression':
        return parse_TupleExpression(js)
    elif js['nodeType'] == 'Block':
        return parse_Block(js)
    elif js['nodeType'] == 'IfStatement':
        return parse_IfStatement(js)
    elif js['nodeType'] == 'ForStatement':
        return parse_ForStatement(js)
    elif js['nodeType'] == 'WhileStatement':
        return parse_WhileStatement(js)
    elif js['nodeType'] == 'ExpressionStatement':
        return parse_ExpressionStatement(js)
    elif js['nodeType'] == 'Assignment':
        return parse_Assignment(js)
    elif js['nodeType'] == 'UnaryOperation':
        return parse_UnaryOperation(js)
    elif js['nodeType'] == 'BinaryOperation':
        return parse_BinaryOperation(js)
    elif js['nodeType'] == 'IndexAccess':
        return parse_IndexAccess(js)
    elif js['nodeType'] == 'MemberAccess':
        return parse_MemberAccess(js)
    elif js['nodeType'] == 'Identifier':
        return parse_Identifier(js)
    elif js['nodeType'] == 'ElementaryTypeNameExpression':
        return parse_ElementaryTypeNameExpression(js)
    elif js['nodeType'] == 'PlaceholderStatement':
        return parse_PlaceholderStatement(js)
    elif js['nodeType'] == 'Continue':
        return parse_Continue(js)
    elif js['nodeType'] == 'Literal':
        return parse_Literal(js)
    else:
        print("Node type not recognized: " + str(js['nodeType']))
        return ""

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
    print("\n\n" + re.sub("[\n]{2,}", "\n\n", parse(solc_json)))
