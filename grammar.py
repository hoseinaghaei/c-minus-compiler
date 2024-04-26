from utils import NonTerminal, Terminal


class Grammar(object):
    statr_non_terminal = NonTerminal.Program
    next = [
        (NonTerminal.Program, [[NonTerminal.Declarationlist]]),
        (NonTerminal.Declarationlist, [[NonTerminal.Declaration, NonTerminal.Declarationlist], [NonTerminal.EPSILON]]),
        (NonTerminal.Declaration, [[NonTerminal.Declarationinitial, NonTerminal.Declarationprime]]),
        (NonTerminal.Declarationinitial, [[NonTerminal.Typespecifier, Terminal.ID]]),
        (NonTerminal.Declarationprime, [[NonTerminal.Fundeclarationprime], [NonTerminal.Vardeclarationprime]]),
        (NonTerminal.Vardeclarationprime, [[Terminal.SEMICOLON], [Terminal.OPENBRACET, Terminal.NUM, Terminal.CLOSEBRACET, Terminal.SEMICOLON]]),
        (NonTerminal.Fundeclarationprime, [[Terminal.OPENPARENTHESIS, NonTerminal.Params, Terminal.CLOSEPARENTHESIS, NonTerminal.Compoundstmt]]),
        (NonTerminal.Typespecifier, [[Terminal.VOID], [Terminal.INT]]),
        (NonTerminal.Params, [[Terminal.VOID], [Terminal.INT, Terminal.ID, NonTerminal.Paramprime, NonTerminal.Paramlist]]),
        (NonTerminal.Paramlist, [[NonTerminal.EPSILON], [Terminal.COMMA, NonTerminal.Param, NonTerminal.Paramlist]]),
        (NonTerminal.Param, [[NonTerminal.Declarationinitial, NonTerminal.Paramprime]]),
        (NonTerminal.Paramprime, [[NonTerminal.EPSILON], [Terminal.OPENBRACET, Terminal.CLOSEBRACET]]),
        (NonTerminal.Compoundstmt, [[Terminal.OPENACOLAD, NonTerminal.Declarationlist, NonTerminal.Statementlist, Terminal.CLOSEACOLAD]]),
        (NonTerminal.Statementlist, [[NonTerminal.EPSILON], [NonTerminal.Statement, NonTerminal.Statementlist]]),
        (NonTerminal.Statement, [[NonTerminal.Expressionstmt], [NonTerminal.Compoundstmt], [NonTerminal.Selectionstmt], [NonTerminal.Iterationstmt], [NonTerminal.Returnstmt]]),
        (NonTerminal.Expressionstmt, [[Terminal.SEMICOLON], [Terminal.BREAK, Terminal.SEMICOLON], [NonTerminal.Expression, Terminal.SEMICOLON]]),
        (NonTerminal.Selectionstmt, [[Terminal.IF, Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS, NonTerminal.Statement, NonTerminal.Elsestmt]]),
        (NonTerminal.Elsestmt, [[Terminal.ENDIF], [Terminal.ELSE, NonTerminal.Statement, Terminal.ENDIF]]),
        (NonTerminal.Iterationstmt, [[Terminal.FOR, Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.SEMICOLON,  NonTerminal.Expression, Terminal.SEMICOLON,  NonTerminal.Expression, Terminal.CLOSEPARENTHESIS, NonTerminal.Statement]]),
        (NonTerminal.Returnstmt, [[Terminal.RETURN, NonTerminal.Returnstmtprime]]),
        (NonTerminal.Returnstmtprime, [[Terminal.SEMICOLON], [NonTerminal.Expression, Terminal.SEMICOLON]]),
        (NonTerminal.Expression, [[NonTerminal.Simpleexpressionzegond], [Terminal.ID, NonTerminal.B]]),
        (NonTerminal.B, [[Terminal.EQUAL, NonTerminal.Expression], [Terminal.EQUAL, Terminal.OPENBRACET, NonTerminal.Expression, Terminal.CLOSEBRACET, NonTerminal.H], [Terminal.EQUAL, NonTerminal.Simpleexpressionprime]]),
        (NonTerminal.H, [[Terminal.EQUAL, NonTerminal.Expression], [Terminal.EQUAL, NonTerminal.G, NonTerminal.D, NonTerminal.C]]),
        (NonTerminal.Simpleexpressionzegond, [[NonTerminal.Additiveexpressionzegond, NonTerminal.C]]),
        (NonTerminal.Simpleexpressionprime, [[NonTerminal.Additiveexpressionprime, NonTerminal.C]]),
        (NonTerminal.C, [[NonTerminal.Relop, NonTerminal.Additiveexpression], [NonTerminal.EPSILON]]),
        (NonTerminal.Relop, [[Terminal.LESS], [Terminal.DOUBLEEQUAL]]),
        (NonTerminal.Additiveexpression, [[NonTerminal.Term, NonTerminal.D]]),
        (NonTerminal.Additiveexpressionprime, [[NonTerminal.Termprime, NonTerminal.D]]),
        (NonTerminal.Additiveexpressionzegond, [[NonTerminal.Termzegond, NonTerminal.D]]),
        (NonTerminal.D, [[NonTerminal.Addop, NonTerminal.Term, NonTerminal.D], [NonTerminal.EPSILON]]),
        (NonTerminal.Addop, [[Terminal.ADD], [Terminal.SUB]]),
        (NonTerminal.Term, [[NonTerminal.Signedfactor, NonTerminal.G]]),
        (NonTerminal.Termprime, [[NonTerminal.Signedfactorprime, NonTerminal.G]]),
        (NonTerminal.Termzegond, [[NonTerminal.Signedfactorzegond, NonTerminal.G]]),
        (NonTerminal.G, [[Terminal.STAR, NonTerminal.Signedfactor, NonTerminal.G], [NonTerminal.EPSILON]]),
        (NonTerminal.Signedfactor, [[Terminal.ADD, NonTerminal.Factor], [Terminal.SUB, NonTerminal.Factor], [NonTerminal.Factor]]),
        (NonTerminal.Signedfactorprime, [[NonTerminal.Factorprime]]),
        (NonTerminal.Signedfactorzegond, [[Terminal.ADD, NonTerminal.Factor], [Terminal.SUB, NonTerminal.Factor], [NonTerminal.Factorzegond]]),
        (NonTerminal.Factor, [[Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS], [Terminal.ID, NonTerminal.Varcallprime], [Terminal.NUM]]),
        (NonTerminal.Varcallprime, [[NonTerminal.Varprime], [Terminal.OPENPARENTHESIS, NonTerminal.Args, Terminal.CLOSEPARENTHESIS]]),
        (NonTerminal.Varprime, [[Terminal.OPENBRACET, NonTerminal.Expression, Terminal.CLOSEBRACET], [NonTerminal.EPSILON]]),
        (NonTerminal.Factorprime, [[Terminal.OPENPARENTHESIS, NonTerminal.Args, Terminal.CLOSEPARENTHESIS], [NonTerminal.EPSILON]]),
        (NonTerminal.Factorzegond, [[Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS], [Terminal.NUM]]),
        (NonTerminal.Args, [[NonTerminal.Arglist], [NonTerminal.EPSILON]]),
        (NonTerminal.Arglist, [[NonTerminal.Expression, NonTerminal.Arglistprime]]),
        (NonTerminal.Arglistprime, [[Terminal.COMMA, NonTerminal.Expression, NonTerminal.Arglistprime], [NonTerminal.EPSILON]])
    ]

    firsts = {
        NonTerminal.Program: [Terminal.VOID, Terminal.INT, NonTerminal.EPSILON],
        NonTerminal.Declarationlist: [Terminal.VOID, Terminal.INT, NonTerminal.EPSILON],
        NonTerminal.Declaration: [Terminal.VOID, Terminal.INT],
        NonTerminal.Declarationinitial: [Terminal.VOID, Terminal.INT],
        NonTerminal.Declarationprime: [Terminal.SEMICOLON, Terminal.OPENBRACET, Terminal.OPENPARENTHESIS],
        NonTerminal.Vardeclarationprime: [Terminal.SEMICOLON, Terminal.OPENBRACET],
        NonTerminal.Fundeclarationprime: [Terminal.OPENPARENTHESIS],
        NonTerminal.Typespecifier: [Terminal.VOID, Terminal.INT],
        NonTerminal.Params: [Terminal.VOID, Terminal.INT],
        NonTerminal.Paramlist: [Terminal.COMMA, NonTerminal.EPSILON],
        NonTerminal.Param: [Terminal.VOID, Terminal.INT],
        NonTerminal.Paramprime: [Terminal.OPENBRACET, NonTerminal.EPSILON],
        NonTerminal.Compoundstmt: [Terminal.OPENACOLAD],
        NonTerminal.Statementlist: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, NonTerminal.EPSILON],
        NonTerminal.Statement: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Expressionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.BREAK, Terminal.ADD, Terminal.SUB],
        NonTerminal.Selectionstmt: [Terminal.IF],
        NonTerminal.Elsestmt: [Terminal.ENDIF, Terminal.ELSE],
        NonTerminal.Iterationstmt: [Terminal.FOR],
        NonTerminal.Returnstmt: [Terminal.RETURN],
        NonTerminal.Returnstmtprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Expression: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.B: [Terminal.EQUAL],
        NonTerminal.H: [Terminal.EQUAL],
        NonTerminal.Simpleexpressionzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Simpleexpressionprime: [Terminal.OPENPARENTHESIS, Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.C: [Terminal.LESS, Terminal.DOUBLEEQUAL, NonTerminal.EPSILON],
        NonTerminal.Relop: [Terminal.LESS, Terminal.DOUBLEEQUAL],
        NonTerminal.Additiveexpression: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Additiveexpressionprime: [Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Additiveexpressionzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.D: [Terminal.ADD, Terminal.SUB, NonTerminal.EPSILON],
        NonTerminal.Addop: [Terminal.ADD, Terminal.SUB],
        NonTerminal.Term: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termprime: [Terminal.OPENPARENTHESIS, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Termzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.G: [Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Signedfactor: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Signedfactorprime: [Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Signedfactorzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Factor: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS],
        NonTerminal.Varcallprime: [Terminal.OPENBRACET, Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Varprime: [Terminal.OPENBRACET, NonTerminal.EPSILON],
        NonTerminal.Factorprime: [Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Factorzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS],
        NonTerminal.Args: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB, NonTerminal.EPSILON],
        NonTerminal.Arglist: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Arglistprime: [Terminal.COMMA, NonTerminal.EPSILON]
    }

    follows = {
        NonTerminal.Program: [Terminal.DOLLAR],
        NonTerminal.Declarationlist: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Declaration: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Declarationinitial: [Terminal.SEMICOLON, Terminal.OPENBRACET, Terminal.OPENPARENTHESIS, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Declarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Vardeclarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Fundeclarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR,Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Typespecifier: [Terminal.ID],
        NonTerminal.Params: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Paramlist: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Param: [Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Paramprime: [Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Compoundstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Statementlist: [Terminal.CLOSEACOLAD],
        NonTerminal.Statement: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Expressionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN,Terminal.ADD, Terminal.SUB],
        NonTerminal.Selectionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN,Terminal.ADD, Terminal.SUB],
        NonTerminal.Elsestmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Iterationstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN,Terminal.ADD, Terminal.SUB],
        NonTerminal.Returnstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Returnstmtprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN,Terminal.ADD, Terminal.SUB],
        NonTerminal.Expression: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.B: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.H: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.C: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Relop: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Additiveexpression: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Additiveexpressionprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL],
        NonTerminal.Additiveexpressionzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL],
        NonTerminal.D: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL],
        NonTerminal.Addop: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Term: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.G: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Signedfactor: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Signedfactorprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Signedfactorzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Factor: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Varcallprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Varprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Factorprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Factorzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA, Terminal.LESS,Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Args: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Arglist: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Arglistprime: [Terminal.CLOSEPARENTHESIS]
    }

    def is_look_ahead_in_follow(self, non_terminal: NonTerminal, look_ahead: str) -> bool:
        follows = [i.value for i in self.follows[non_terminal]]
        return look_ahead in follows

    def is_epsilon_in_first(self, non_terminal: NonTerminal) -> bool:
        return NonTerminal.EPSILON in self.firsts[non_terminal]

    def _get_first(self, name) -> set:
        if isinstance(name, NonTerminal):
            return set([i.value for i in self.firsts[name]])
        else:
            return {name.value}

    def get_rhs_first(self, rules: list) -> set:
        firsts = set()
        for rule in rules:
            firsts.update(self._get_first(rule))
            if isinstance(rule, Terminal) or NonTerminal.EPSILON not in self.firsts[rule]:
                break

        return firsts
