import re

class ExpressionEvaluator:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'sin': lambda x: __import__('math').sin(x),
            'cos': lambda x: __import__('math').cos(x),
            'sqrt': lambda x: __import__('math').sqrt(x)
        }
    
    def precedence(self, op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0
    
    def infix_to_postfix(self, expression):
        output = []
        stack = []
        tokens = re.findall(r'\d+\.?\d*|\w+|[+\-*/^()]', expression.replace(' ', ''))
        
        for token in tokens:
            if re.match(r'\d+\.?\d*', token):
                output.append(float(token))
            elif token in self.variables:
                output.append(self.variables[token])
            elif token in self.functions:
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())
            elif token in '+-*/^':
                while stack and stack[-1] != '(' and self.precedence(stack[-1]) >= self.precedence(token):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def evaluate_postfix(self, postfix):
        stack = []
        
        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(token)
            elif token in self.functions:
                arg = stack.pop()
                stack.append(self.functions[token](arg))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        
        return stack[0]
    
    def evaluate(self, expression):
        postfix = self.infix_to_postfix(expression)
        return self.evaluate_postfix(postfix)
    
    def set_variable(self, name, value):
        self.variables[name] = value

if __name__ == "__main__":
    print("\n=== EXPRESSION EVALUATOR ===")
    print("Supported: +, -, *, /, ^, (), variables, sin, cos, sqrt")
    evaluator = ExpressionEvaluator()
    
    while True:
        print("\n" + "="*40)
        print("1. Evaluate Expression")
        print("2. Set Variable")
        print("3. View Variables")
        print("4. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            expr = input("Enter expression: ")
            try:
                result = evaluator.evaluate(expr)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == '2':
            var = input("Enter variable name: ")
            value = float(input("Enter value: "))
            evaluator.set_variable(var, value)
            print(f"✓ {var} = {value}")
        elif choice == '3':
            if evaluator.variables:
                print("Variables:")
                for var, val in evaluator.variables.items():
                    print(f"  {var} = {val}")
            else:
                print("No variables set")
        elif choice == '4':
            break