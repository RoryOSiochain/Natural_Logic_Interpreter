import re


class Expression:
    """
    Expression class takes a logical expression in form of string and creates
    an object with useful methods to manipulate the expression or to get useful
    information from it.
    
    Attributes
    ----------
    expression: str
            A logical argument using OR, AND, and NOT operations
    keywords:   ["OR", "AND", "IF", "THEN"]
            List of keywords used in this program
    and_regex:  str
            Regular expression used to identify conjunctive arguments
    or_regex:   str
            Regular expression used to identify disjunctive arguments
    conditional_regex:  str
            Regular expression used to identify conditional arguments
    
    Methods
    -------
    get()
    set(new_expression)
    recognizer()
    valid_parentheses_checker()
    expression_parser()
    is_pure_proposition()
    negative_inverter()
    temp_negative_inverter() 
    """

    def __init__(self, expression):
        self.expression = expression
        self.keywords = ["OR", "AND", "IF", "THEN"]
        self.and_regex = r"(\(+.*?\)+) AND (\(+.*\)+)( AND \(+.*\)+)*$"
        self.or_regex = r"(\(+.*?\)+) OR (\(+.*\)+)( OR \(+.*\)+)*$"
        self.conditional_regex = r"IF (\(.*\)) THEN (\(.*\))$"

    def __eq__(self, other):
        return self.get() == other.get()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.expression)

    def __str__(self):
        return self.expression

    def get(self):
        """
        Returns the expression of the object in string.

        :return: self.expression
        :rtype: str
        """
        return self.expression

    def set(self, new_expression):
        """
        Sets the self.expression to a new string
        
        :param new_expression
        :type new_expression: str
        :return: -
        """
        self.expression = new_expression

    def recognizer(self):
        """
        Recognizes the main type of a logical argument.

        :return: 
        "AND", "OR", "Conditional", "Pure", "Broken":   str
        """
        if re.match(self.or_regex, self.expression):
            p = re.compile(self.or_regex)
            m = re.match(p, self.expression)
            for i in m.groups()[:-1]:
                if "))" in i and "((" not in i or "((" in i and "))" not in i:
                    return "AND"
            return "OR"
        elif re.match(self.and_regex, self.expression):
            p = re.compile(self.and_regex)
            m = re.match(p, self.expression)
            for i in m.groups()[:-1]:
                if "))" in i and "((" not in i or "((" in i and "))" not in i:
                    return "OR"
            return "AND"
        elif re.match(self.conditional_regex, self.expression):
            return "Conditional"
        else:

            # Here we check whether the argument contains any keywords or it
            # is just stating a pure expression as truth.

            flag = True
            for i in self.keywords:
                if i in self.expression:
                    flag = False
                    break
            if flag:
                return "Pure"
            else:
                # If none was applied it means the expression is broken
                return "Broken"

    def valid_parentheses_checker(self):
        """
        Checks whether expression of an object is using valid from parentheses

        :return: True | False
        :rtype: bool
        """
        if "(" not in self.expression and ")" not in self.expression:
            return False
        if "(" not in self.expression or ")" not in self.expression:
            return False
        else:
            return True

    def expression_parser(self):
        """
        Parses the expression of an Expression object to its main parts and
        creates new objects with the sub-parts and places them in a list.
        
        :return: parsed_expression_list
        :rtype: list
        """
        if self.recognizer() == "AND":
            parsed_expression = []
            match = re.match(self.and_regex, self.expression)
            groups = match.groups()[:-1]
            for expression in groups:
                parsed_expression.append(expression)

            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("((")
                    i = i[:double_paren_index] + i[double_paren_index + 1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    double_paren_index = i.index("))")
                    i = i[:double_paren_index + 1] + i[double_paren_index + 2:]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Definer(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.recognizer() == "OR":
            parsed_expression = []
            match = re.match(self.or_regex, self.expression)
            groups = match.groups()[:-1]
            for expression in groups:
                parsed_expression.append(expression)
            for i in parsed_expression:
                if "))" in i and "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:-1]
                    parsed_expression[list_index] = i
                elif "((" in i:
                    list_index = parsed_expression.index(i)
                    i = i[1:]
                    parsed_expression[list_index] = i
                elif "))" in i:
                    list_index = parsed_expression.index(i)
                    i = i[:-1]
                    parsed_expression[list_index] = i
            parsed_expression_list = []
            for i in parsed_expression:
                new_expression_object = Definer(i)
                parsed_expression_list.append(new_expression_object)
            return parsed_expression_list

        elif self.recognizer() == "Conditional":
            condt_matched = re.match(self.conditional_regex, self.expression)
            condt_object1 = Definer(condt_matched.group(1))
            condt_object2 = Definer(condt_matched.group(2))
            parsed_expression = {"IF": condt_object1,
                                 "THEN": condt_object2}
            return parsed_expression

    def is_pure_proposition(self):
        """
        Checks whether a proposition is pure, meaning it is just stating the 
        truth of an expression without any keywords.
        
        :return: True | False
         :rtype: bool
        """
        if self.recognizer() == "Conditional":
            parsed_expression = self.expression_parser()
            for expression in parsed_expression:
                if parsed_expression[expression].recognizer() != "Pure":
                    return False
            return True

        else:
            for i in self.expression_parser():
                if i.recognizer() != "Pure":
                    return False
            return True

    def negative_inverter(self):
        """
        Removes NOT from the expression of an Expression object and sets it.
        
        :return: -
        """
        expression = self.expression
        expression = expression[0] + expression[5:]
        self.expression = expression

    def temp_negative_inverter(self):
        """
        Returns a string that has the NOT in the expression of an Expression
        object removed.
        
        :return: temp_inverted_object
        :rtype: str
        """
        expression = self.expression
        expression = expression[0] + expression[5:]
        temp_inverted_object = Expression(expression)
        return temp_inverted_object


# ------------------------------------------------------------------------------


class Definer(Expression):
    """
    Definer class is a subclass of Expression that provides methods useful for
    defining logical expressions into our knowledge dictionary.

    Attributes
    ----------
    expression: str
            A logical argument using OR, AND, and NOT operations

    Methods
    -------
    and_definer()
    or_definer()
    conditional_definer()
    definer()
    and_in_or_checker(or_expression)
    and_temp_transformer()
    """

    def __init__(self, expression):
        Expression.__init__(self, expression)

    def and_definer(self):
        """
        Defines an conjunctive expression into the knowledge dictionary and set
        the expression as True.

        :return: True
        :rtype: bool
        """
        for expression in self.expression_parser():
            if "NOT" not in expression.expression:
                knowledge_dict[expression] = True
            else:
                # If NOT is in the expression we invert it and set it to False.
                expression.negative_inverter()
                knowledge_dict[expression] = False
        return True

    def or_definer(self):
        """
        Defines a disjunctive expression into the knowledge dictionary and set
        the expression to True or False based on evaluation of previously
        entered expressions.
        
        :return: True | False | None
        :rtype: bool
        """
        expression_in_dict = False

        for expression in self.expression_parser():
            if "NOT" in expression.get():
                reversed_temp = expression.temp_negative_inverter()
                if reversed_temp in knowledge_dict:
                    expression_in_dict = True
                    break
                continue
            if expression in knowledge_dict:
                expression_in_dict = True
                break

        if expression_in_dict is True:
            for expression in self.expression_parser():
                if "NOT" in expression.get():
                    reversed_temp = expression.temp_negative_inverter()
                    if reversed_temp not in knowledge_dict:
                        knowledge_dict[reversed_temp] = None
                else:
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None

            # count to check if all elements are false
            count = 0
            for expression in self.expression_parser():
                if "NOT" in expression.get():
                    expression.negative_inverter()
                    if knowledge_dict[expression] is False:
                        return True
                    elif knowledge_dict[expression] is True:
                        count += 1
                else:
                    if knowledge_dict[expression] is True:
                        return True
                    elif knowledge_dict[expression] is False:
                        count += 1

            if count == len(self.expression_parser()):
                return False
            else:
                return None

        else:
            for expression in self.expression_parser():
                if "NOT" in expression.get():
                    reversed_temp = expression.temp_negative_inverter()
                    if reversed_temp not in knowledge_dict:
                        knowledge_dict[reversed_temp] = None
                else:
                    if expression not in knowledge_dict:
                        knowledge_dict[expression] = None
            return True

    def conditional_definer(self):
        """
        Defines a conditional expression into the knowledge dictionary and set
        the expression to True or False based on evaluation of previously
        entered expressions.

        :return: True | False | None
        :rtype: bool
        """
        for expression in self.expression_parser():
            if "NOT" in self.expression_parser()[expression].expression:
                continue
            if self.expression_parser()[expression] not in knowledge_dict:
                knowledge_dict[self.expression_parser()[expression]] = None

        if "NOT" in self.expression_parser()["IF"].expression:
            if_proposition = self.expression_parser()["IF"]
            if_proposition.negative_inverter()

            if if_proposition not in knowledge_dict:
                return None

            if knowledge_dict[if_proposition] is False:
                if "NOT" in self.expression_parser()["THEN"].expression:
                    then_proposition = self.expression_parser()["THEN"]
                    then_proposition.negative_inverter()
                    knowledge_dict[then_proposition] = False
                else:
                    knowledge_dict[self.expression_parser()["THEN"]] = True
                return True
            elif knowledge_dict[if_proposition] is True:
                return True
            else:
                return None
        else:
            if knowledge_dict[self.expression_parser()["IF"]] is True:
                if "NOT" in self.expression_parser()["THEN"].expression:
                    then_proposition = self.expression_parser()["THEN"]
                    then_proposition.negative_inverter()
                    knowledge_dict[then_proposition] = False
                else:
                    knowledge_dict[self.expression_parser()["THEN"]] = True
                return True
            elif knowledge_dict[self.expression_parser()["IF"]] is False:
                return True
            else:
                return None

    def definer(self):
        """
        Used as a general definer to be used in interpreter function. For the
        sake of simplicity, definer checks the type of the expression in its
        body and uses the right definer accordingly.
        
        :return: True | False | None
        :rtype: bool
        """
        if self.recognizer() == "AND":
            return self.and_definer()

        elif self.recognizer() == "OR":
            return self.or_definer()

        elif self.recognizer() == "Conditional":
            return self.conditional_definer()

    def special_definer(self):
        """
        Special definer is used for defining the AND expressions that have been
        previously been in an OR expression. It is special since we don't want
        to set them to True.

        :return: True | False | None
        :rtype: bool
        """
        for expression in self.expression_parser():
            if expression not in knowledge_dict:
                knowledge_dict[expression] = None

        true_count = 0
        for expression in self.expression_parser():
            if knowledge_dict[expression] is None:
                return None
            if knowledge_dict[expression] is False:
                return False
            if knowledge_dict[expression] is True:
                true_count += 1
        if true_count == len(self.expression_parser()):
            return True

    def and_in_or_checker(self, main_expression):
        """
        Checks whether the expression we are looking is an AND expression that
        is part of an OR expression.
        
        :param main_expression: 
        :type main_expression: Expression
        :return: True | False
        :rtype: bool
        """
        if self.recognizer() == "AND" and main_expression.recognizer() == "OR":
            return True
        else:
            return None

    def and_temp_transformer(self):
        """
        Sets a mark in the expression so we can recognize it's different later.
        
        :return: -
        """
        self.expression = self.expression + "@"
# ------------------------------------------------------------------------------


class Resolver(Expression):
    """
    Resolver class is a subclass of Expression that provides methods useful for
    resolving logical expressions in our knowledge dictionary into proof_dict.

    Attributes
    ----------
    expression: str
            A logical argument using OR, AND, and NOT operations

    Methods
    -------
    and_resolver()
    or_resolver()
    conditional_resolver()
    general_resolver()
    """
    def __init__(self, expression):
        Expression.__init__(self, expression)

    def and_resolver(self):
        """
        Resolves an AND expression based on other expressions stored in
        proof_dict.
        
        :return: True | False | None
        :rtype: bool
        """
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                continue
            if expression not in proof_dict or expression is None:
                proof_dict[expression] = None
                return None  # Can't be determined

        true_count = 0
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                expression.negative_inverter()
                if proof_dict[expression] is True:
                    return False
                if proof_dict[expression] is False:
                    true_count += 1
            else:
                if proof_dict[expression] is False:
                    return False
                if proof_dict[expression] is True:
                    true_count += 1
        if true_count == len(self.expression_parser()):
            return True

    def or_resolver(self):
        """
        Resolves an OR expression based on other expressions stored in
        proof_dict.

        :return: True | False | None
        :rtype: bool
        """
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                continue
            if expression not in proof_dict or proof_dict[expression] is None:
                proof_dict[expression] = None

        # count to check if all elements are false
        count = 0
        for expression in self.expression_parser():
            if "NOT" in expression.get():
                expression.negative_inverter()
                if expression not in proof_dict:
                    proof_dict[expression] = None
                if proof_dict[expression] is False:
                    return True
                if proof_dict[expression] is True:
                    count += 1
            else:
                if proof_dict[expression] is True:
                    return True
                if proof_dict[expression] is False:
                    count += 1

        if count == len(self.expression_parser()):
            return False
        else:
            return None

    def conditional_resolver(self):
        """
        Resolves a conditional expression based on other expressions stored in
        proof_dict.

        :return: True | False | None
        :rtype: bool
        """
        if_statement = self.expression_parser()["IF"]
        then_statement = self.expression_parser()["THEN"]

        if then_statement not in proof_dict:
            proof_dict[then_statement] = None

        if "NOT" in if_statement.get() and "NOT" not in then_statement.get():
            if_statement.negative_inverter()
            if if_statement not in proof_dict:
                proof_dict[if_statement] = None
                return None
            if proof_dict[if_statement] is False and proof_dict[
                    then_statement] is False:
                return False
            elif proof_dict[if_statement] is True:
                return True
            elif proof_dict[if_statement] is False and proof_dict[
                    then_statement] is True:
                return True
            else:
                return None

        elif "NOT" in if_statement.get() and "NOT" in then_statement.get():
            if_statement.negative_inverter()
            then_statement.negative_inverter()
            if if_statement not in proof_dict:
                proof_dict[if_statement] = None
                return None
            if proof_dict[if_statement] is False and proof_dict[
                    then_statement] is True:
                return False
            elif proof_dict[if_statement] is True:
                return True
            elif proof_dict[if_statement] is False and proof_dict[
                    then_statement] is False:
                return True
            else:
                return None

        elif "NOT" not in if_statement.get() and "NOT" in then_statement.get():
            then_statement.negative_inverter()
            if if_statement not in proof_dict:
                proof_dict[if_statement] = None
                return None
            if proof_dict[if_statement] is True and proof_dict[
                    then_statement] is True:
                return False
            elif proof_dict[if_statement] is False:
                return True
            elif proof_dict[if_statement] is True and proof_dict[
                    then_statement] is False:
                return True
            else:
                return None

        else:
            if if_statement not in proof_dict:
                proof_dict[if_statement] = None
                return None
            if proof_dict[if_statement] is True and proof_dict[
                    then_statement] is False:
                return False
            elif proof_dict[if_statement] is False:
                return True
            elif proof_dict[if_statement] is True and proof_dict[
                    then_statement] is True:
                return True
            else:
                return None

    def general_resolver(self):
        """
        Used as a general resolver to be used in validator function. For the
        sake of simplicity, general_resolver checks the type of the expression
        in its body and uses the right resolver accordingly.

        :return: True | False | None
        :rtype: bool
        """
        if self.recognizer() == "AND":
            return self.and_resolver()
        elif self.recognizer() == "OR":
            return self.or_resolver()
        elif self.recognizer() == "Conditional":
            return self.conditional_resolver()
# ------------------------------------------------------------------------------


def interpreter(expression):
    """
    interpreter function is a recursive function that uses divide and conquer
    to go through nested arguments of the input expression and defines them
    accordingly.
    
    :param expression:
    :type expression: str
    :return: -
    """
    # Let's check to see if we have an AND operator that was part of an AND
    flag = False
    if expression[-1] == "@":
        # When it was delete the mark but set the flag to True so we will treat
        # it differently in the future.
        flag = True
        # Flag has become True and we can normalize the expression again
        expression = expression[0:-1]

    # Create an expression class with the expression string.
    expression_object = Definer(expression)

    # First base case
    if expression_object.recognizer() == "Pure":
        if "NOT" not in expression_object.get():
            knowledge_dict[expression_object] = True
        else:
            expression_object.negative_inverter()
            knowledge_dict[expression_object] = False

    # Second base case
    elif expression_object.is_pure_proposition():
        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer()
        else:
            knowledge_dict[expression_object] = expression_object.definer()

    # Third base case
    else:
        parsed_expression = expression_object.expression_parser()

        if flag:
            knowledge_dict[expression_object] = expression_object.special_definer()
        else:
            knowledge_dict[expression_object] = expression_object.definer()

        # Check to see if it is conditional so we can mark its IF proposition
        if expression_object.recognizer() == "Conditional":
            for expression in parsed_expression.values():

                expression_type = expression.recognizer()

                if expression_type == "AND":
                    parsed_expression["IF"].and_temp_transformer()

                # Recursive step
                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(expression.get())

        else:
            for expression in parsed_expression:
                expression_type = expression.recognizer()

                # Check to see if any AND  was part of an OR proposition
                if expression.and_in_or_checker(expression_object) is True:
                    expression.and_temp_transformer()

                # Recursive step
                if expression_type != "Pure" and expression_type != "Broken":
                    interpreter(expression.get())
# ------------------------------------------------------------------------------


def validator(expression):
    """
    validator function is a recursive function that uses divide and conquer
    to go through nested arguments of the input expression and validates them
    accordingly. (Uses arguments previously defined in knowledge dictionary that
    was later on copied into proof_dict. validator stores the result in
    proof_dict.

    :param expression:
    :type expression: str
    :return: -
    """
    # Create an object with the expression string.
    expression_object = Resolver(expression)

    expression_object_type = expression_object.recognizer()
    parsed_expression = expression_object.expression_parser()

    # First base case
    if expression_object_type == "Pure":
        if "NOT" in expression_object.get():
            temp_inverted = expression_object.temp_negative_inverter()
            if temp_inverted not in knowledge_dict:
                proof_dict[expression_object] = None
                return None
            elif knowledge_dict[temp_inverted] is True:
                proof_dict[expression_object] = False
                return False
            else:
                proof_dict[expression_object] = True
                return True
        else:
            if expression_object not in knowledge_dict:
                proof_dict[expression_object] = None
                return None
            else:
                proof_dict[expression_object] = knowledge_dict[
                    expression_object]
                return proof_dict[expression_object]

    # Second base case
    elif expression_object.is_pure_proposition() is True:
        proof_dict[expression_object] = expression_object.general_resolver()

    else:
        proof_dict[expression_object] = expression_object.general_resolver()

        if expression_object.recognizer() == "Conditional":
            for expression in parsed_expression.values():

                expression_type = expression.recognizer()

                # Recursive step
                if expression_type != "Pure" and expression_type != "Broken":
                    validator(expression.get())

        else:
            for expression in parsed_expression:
                expression_type = expression.recognizer()
                # Recursive step
                if expression_type != "Pure" and expression_type != "Broken":
                    validator(expression.get())

# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # Knowledge dict is where we store all the definitions defined by definer
    # function.
    knowledge_dict = dict()

    user_input = ""

    print("Please keep entering the logical arguments you would like to" +
          " define.\nTo see the results and further validate new arguments" +
          " based on your arguments enter -1.")

    input_list = list()

    while user_input != "-1":
        user_input = input("\nNew argument:\t")
        if user_input != "-1":
            expression_object = Expression(user_input)
            if expression_object.recognizer() == "Broken":
                print("Incorrect Syntax. Please try again: ")
                continue
            elif expression_object.recognizer() == "Pure":
                if expression_object.valid_parentheses_checker() is False:
                    print("Parentheses do not exist or aren't in a valid form.")
                    continue
            input_list.append(user_input)

    for count in range(2):
        # We repeat the procedure of defining to make sure all the elements get
        # updated.
        for expression in input_list:
            interpreter(expression)

    print(40 * "-" + "\nExpressions and arguments you defined: ")

    for expression in knowledge_dict:
        print(expression.get(), "--->", knowledge_dict[expression])

    print(40 * "-" + "\nEnter the new argument you would like to validate: " +
          "\nEnter 'view' at any time to see the full list of arguments and" +
          " their results\nEnter 'exit' to quit.")

    # proof_dict is where we store all the validation results we resolved.
    # At the beelining we copy all the elements of knowledge_dict so resolver
    # can use previously defined arguments.
    proof_dict = knowledge_dict.copy()

    while user_input != "exit":
        user_input = input("\nValidate:\t")
        if user_input != "exit":
            if user_input == "view":
                for expression in proof_dict:
                    print(expression.get(), "--->", proof_dict[expression])
            else:
                for i in range(2):
                    # We repeat the procedure of defining to make sure all the
                    # elements get validated.
                    validator(user_input)
                for expression in proof_dict:
                    if expression.get() == user_input:
                        print(user_input, "----->", proof_dict[expression])
