import json
import sys

def parse_Identifier(js):
    print("In Identifier: name=" + js['name'])

def parse_MemberAccess(js):
    print("In MemberAccess: memberName=" + js['memberName'])
    parse(js['expression'])

def parse_IndexAccess(js):
    print("In IndexAccess")
    parse(js['baseExpression'])
    parse(js['indexExpression'])

def parse_Assignment(js):
    print("In Assignment: operator:" + js['operator'])
    parse(js['leftHandSide'])
    parse(js['rightHandSide'])

def parse_ExpressionStatement(js):
    print("In ExpressionStatement")
    parse(js['expression'])

def parse_Block(js):
    print("In Block")
    for js_expression in js['statements']:
        parse(js_expression)

def parse_FunctionDefinition(js):
    print("In FunctionDefinition: name=" + js['name'] + " payable=" + str(js['payable']))
    parse(js['body'])

def parse_VariableDeclaration(js):
    print("In VariableDeclaration: name=" + js['name'])

def parse_ContractDefinition(js):
    print("In ContractDefinition: name=" + js['name'])
    for js_node in js['nodes']:
        parse(js_node)

def parse_PragmaDirective(js):
    print("In PragmaDirective")

def parse_SourceUnit(js):
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
    elif js['nodeType'] == 'FunctionDefinition':
        parse_FunctionDefinition(js)
    elif js['nodeType'] == 'Block':
        parse_Block(js)
    elif js['nodeType'] == 'ExpressionStatement':
        parse_ExpressionStatement(js)
    elif js['nodeType'] == 'Assignment':
        parse_Assignment(js)
    elif js['nodeType'] == 'IndexAccess':
        parse_IndexAccess(js)
    elif js['nodeType'] == 'MemberAccess':
        parse_MemberAccess(js)
    elif js['nodeType'] == 'Identifier':
        parse_Identifier(js)
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
