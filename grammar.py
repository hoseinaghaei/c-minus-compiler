from utils import NonTerminal, Terminal, ActionSymbol


class Grammar(object):
    statr_non_terminal = NonTerminal.Program
    next = [
        ("Program", NonTerminal.Program, [[NonTerminal.Declarationlist]]),
        ("Declaration-list", NonTerminal.Declarationlist, [[NonTerminal.Declaration, NonTerminal.Declarationlist, ActionSymbol.INITZERO], [NonTerminal.EPSILON]]),
        ("Declaration", NonTerminal.Declaration, [[NonTerminal.Declarationinitial, NonTerminal.Declarationprime]]),
        ("Declaration-initial", NonTerminal.Declarationinitial, [[NonTerminal.Typespecifier, Terminal.ID, ActionSymbol.DECLAREID]]),
        ("Declaration-prime", NonTerminal.Declarationprime, [[NonTerminal.Fundeclarationprime], [NonTerminal.Vardeclarationprime]]),
        ("Var-declaration-prime", NonTerminal.Vardeclarationprime,
         [[Terminal.SEMICOLON],
          [Terminal.OPENBRACET, Terminal.NUM, ActionSymbol.PNUM, Terminal.CLOSEBRACET, ActionSymbol.DECLARE_ARRAY, Terminal.SEMICOLON]]),
        ("Fun-declaration-prime", NonTerminal.Fundeclarationprime,
         [[ActionSymbol.DECLAREFUNCTION, Terminal.OPENPARENTHESIS, ActionSymbol.OPENSCOPE, ActionSymbol.FUNCOPENSCOPEFLAG, NonTerminal.Params, Terminal.CLOSEPARENTHESIS, NonTerminal.Compoundstmt, ActionSymbol.RETURN]]),
        ("Type-specifier", NonTerminal.Typespecifier, [[Terminal.VOID], [Terminal.INT]]),
        ("Params", NonTerminal.Params,
         [[Terminal.VOID], [Terminal.INT, Terminal.ID, ActionSymbol.DECLAREID, ActionSymbol.PID, NonTerminal.Paramprime, ActionSymbol.POPPARAM, NonTerminal.Paramlist]]),
        ("Param-list", NonTerminal.Paramlist, [[NonTerminal.EPSILON], [Terminal.COMMA, NonTerminal.Param, NonTerminal.Paramlist]]),
        ("Param", NonTerminal.Param, [[NonTerminal.Declarationinitial, ActionSymbol.PID, NonTerminal.Paramprime, ActionSymbol.POPPARAM]]),
        ("Param-prime", NonTerminal.Paramprime, [[NonTerminal.EPSILON], [Terminal.OPENBRACET, Terminal.CLOSEBRACET, ActionSymbol.ARRAY_PARAM]]),
        ("Compound-stmt", NonTerminal.Compoundstmt,
         [[Terminal.OPENACOLAD, ActionSymbol.OPENSCOPE, NonTerminal.Declarationlist, NonTerminal.Statementlist, ActionSymbol.CLOSESCOP, Terminal.CLOSEACOLAD]]),
        ("Statement-list", NonTerminal.Statementlist, [[NonTerminal.EPSILON], [NonTerminal.Statement, NonTerminal.Statementlist]]),
        ("Statement", NonTerminal.Statement, [[NonTerminal.Expressionstmt], [NonTerminal.Compoundstmt], [NonTerminal.Selectionstmt],
                                 [NonTerminal.Iterationstmt], [NonTerminal.Returnstmt]]),
        ("Expression-stmt", NonTerminal.Expressionstmt,
         [[Terminal.SEMICOLON], [Terminal.BREAK, ActionSymbol.BREAK, Terminal.SEMICOLON], [NonTerminal.Expression, ActionSymbol.POP, Terminal.SEMICOLON]]),
        ("Selection-stmt", NonTerminal.Selectionstmt, [
            [Terminal.IF, Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS, ActionSymbol.IFSAVE,
             NonTerminal.Statement, NonTerminal.Elsestmt]]),
        ("Else-stmt", NonTerminal.Elsestmt, [[Terminal.ENDIF, ActionSymbol.ENDIF], [Terminal.ELSE, ActionSymbol.STARTELSE, NonTerminal.Statement, ActionSymbol.ENDIFAFTERELSE, Terminal.ENDIF]]),
        ("Iteration-stmt", NonTerminal.Iterationstmt, [
            [Terminal.FOR, ActionSymbol.DEBUG, Terminal.OPENPARENTHESIS, NonTerminal.Expression, ActionSymbol.FORCHECKCONDITION, Terminal.SEMICOLON, NonTerminal.Expression, ActionSymbol.IFSAVE, ActionSymbol.IFSAVE,
             Terminal.SEMICOLON, NonTerminal.Expression, ActionSymbol.FORJUMPCHECKCONDITION, Terminal.CLOSEPARENTHESIS, ActionSymbol.BREAKSCOPE, NonTerminal.Statement, ActionSymbol.FORSAVE, ActionSymbol.BREAKSAVE]]),
        ("Return-stmt", NonTerminal.Returnstmt, [[Terminal.RETURN, NonTerminal.Returnstmtprime, ActionSymbol.RETURN]]),
        ("Return-stmt-prime", NonTerminal.Returnstmtprime, [[Terminal.SEMICOLON], [NonTerminal.Expression, ActionSymbol.RETURNVALUE, Terminal.SEMICOLON]]),
        ("Expression", NonTerminal.Expression, [[NonTerminal.Simpleexpressionzegond], [Terminal.ID, ActionSymbol.PID, NonTerminal.B]]),
        ("B", NonTerminal.B, [[Terminal.EQUAL, NonTerminal.Expression, ActionSymbol.ASSIGN],
                         [Terminal.OPENBRACET, NonTerminal.Expression, ActionSymbol.ARRAYINDEX, Terminal.CLOSEBRACET, NonTerminal.H],
                         [NonTerminal.Simpleexpressionprime]]),
        ("H", NonTerminal.H,
         [[Terminal.EQUAL, NonTerminal.Expression, ActionSymbol.ASSIGN], [NonTerminal.G, NonTerminal.D, NonTerminal.C]]),
        ("Simple-expression-zegond", NonTerminal.Simpleexpressionzegond, [[NonTerminal.Additiveexpressionzegond, NonTerminal.C]]),
        ("Simple-expression-prime", NonTerminal.Simpleexpressionprime, [[NonTerminal.Additiveexpressionprime, NonTerminal.C]]),
        ("C", NonTerminal.C, [[NonTerminal.Relop, NonTerminal.Additiveexpression, ActionSymbol.EVALOPERATION], [NonTerminal.EPSILON]]),
        ("Relop", NonTerminal.Relop, [[Terminal.LESS, ActionSymbol.POPERAND], [Terminal.DOUBLEEQUAL, ActionSymbol.POPERAND]]),
        ("Additive-expression", NonTerminal.Additiveexpression, [[NonTerminal.Term, NonTerminal.D]]),
        ("Additive-expression-prime", NonTerminal.Additiveexpressionprime, [[NonTerminal.Termprime, NonTerminal.D]]),
        ("Additive-expression-zegond", NonTerminal.Additiveexpressionzegond, [[NonTerminal.Termzegond, NonTerminal.D]]),
        ("D", NonTerminal.D, [[NonTerminal.Addop, NonTerminal.Term, ActionSymbol.EVALOPERATION, NonTerminal.D], [NonTerminal.EPSILON]]),
        ("Addop", NonTerminal.Addop, [[Terminal.ADD, ActionSymbol.POPERAND], [Terminal.SUB, ActionSymbol.POPERAND]]),
        ("Term", NonTerminal.Term, [[NonTerminal.Signedfactor, NonTerminal.G]]),
        ("Term-prime", NonTerminal.Termprime, [[NonTerminal.Signedfactorprime, NonTerminal.G]]),
        ("Term-zegond", NonTerminal.Termzegond, [[NonTerminal.Signedfactorzegond, NonTerminal.G]]),
        ("G", NonTerminal.G, [[Terminal.STAR, ActionSymbol.POPERAND, NonTerminal.Signedfactor, ActionSymbol.EVALOPERATION, NonTerminal.G], [NonTerminal.EPSILON]]),
        ("Signed-factor", NonTerminal.Signedfactor,
         [[Terminal.ADD, ActionSymbol.POPERAND, NonTerminal.Factor], [Terminal.SUB, ActionSymbol.POPERAND, NonTerminal.Factor], [NonTerminal.Factor]]),
        ("Signed-factor-prime", NonTerminal.Signedfactorprime, [[NonTerminal.Factorprime]]),
        ("Signed-factor-zegond", NonTerminal.Signedfactorzegond,
         [[Terminal.ADD, ActionSymbol.POPERAND, NonTerminal.Factor, ActionSymbol.EVALOPERATION], [Terminal.SUB, ActionSymbol.POPERAND, NonTerminal.Factor, ActionSymbol.EVALOPERATION], [NonTerminal.Factorzegond]]),
        ("Factor", NonTerminal.Factor, [[Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS],
                              [Terminal.ID, ActionSymbol.PID, NonTerminal.Varcallprime], [Terminal.NUM, ActionSymbol.PNUM]]),
        ("Var-call-prime", NonTerminal.Varcallprime,
         [[NonTerminal.Varprime], [Terminal.OPENPARENTHESIS, ActionSymbol.START_ARGUMENT, NonTerminal.Args, ActionSymbol.END_ARGUMENT, Terminal.CLOSEPARENTHESIS, ActionSymbol.CALL]]),
        ("Var-prime", NonTerminal.Varprime,
         [[Terminal.OPENBRACET, NonTerminal.Expression, ActionSymbol.ARRAYINDEX, Terminal.CLOSEBRACET], [NonTerminal.EPSILON]]),
        ("Factor-prime", NonTerminal.Factorprime,
         [[Terminal.OPENPARENTHESIS, ActionSymbol.START_ARGUMENT, NonTerminal.Args, ActionSymbol.END_ARGUMENT, Terminal.CLOSEPARENTHESIS, ActionSymbol.CALL], [NonTerminal.EPSILON]]),
        ("Factor-zegond", NonTerminal.Factorzegond,
         [[Terminal.OPENPARENTHESIS, NonTerminal.Expression, Terminal.CLOSEPARENTHESIS], [Terminal.NUM, ActionSymbol.PNUM]]),
        ("Args", NonTerminal.Args, [[NonTerminal.Arglist], [NonTerminal.EPSILON]]),
        ("Arg-list", NonTerminal.Arglist, [[NonTerminal.Expression, ActionSymbol.ADD_ARGUMENT, NonTerminal.Arglistprime]]),
        ("Arg-list-prime", NonTerminal.Arglistprime,
         [[Terminal.COMMA, NonTerminal.Expression, ActionSymbol.ADD_ARGUMENT, NonTerminal.Arglistprime], [NonTerminal.EPSILON]])
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
        NonTerminal.Statementlist: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                    Terminal.OPENACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR,
                                    Terminal.RETURN, Terminal.ADD, Terminal.SUB, NonTerminal.EPSILON],
        NonTerminal.Statement: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                Terminal.OPENACOLAD, Terminal.BREAK, Terminal.IF, Terminal.FOR,
                                Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Expressionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                     Terminal.BREAK, Terminal.ADD, Terminal.SUB],
        NonTerminal.Selectionstmt: [Terminal.IF],
        NonTerminal.Elsestmt: [Terminal.ENDIF, Terminal.ELSE],
        NonTerminal.Iterationstmt: [Terminal.FOR],
        NonTerminal.Returnstmt: [Terminal.RETURN],
        NonTerminal.Returnstmtprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                      Terminal.ADD, Terminal.SUB],
        NonTerminal.Expression: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                                 Terminal.SUB],
        NonTerminal.B: [Terminal.OPENBRACET, Terminal.OPENPARENTHESIS, Terminal.EQUAL, Terminal.LESS,
                        Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.H: [Terminal.EQUAL, Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB,
                        Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Simpleexpressionzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                                             Terminal.SUB],
        NonTerminal.Simpleexpressionprime: [Terminal.OPENPARENTHESIS, Terminal.LESS, Terminal.DOUBLEEQUAL,
                                            Terminal.ADD, Terminal.SUB, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.C: [Terminal.LESS, Terminal.DOUBLEEQUAL, NonTerminal.EPSILON],
        NonTerminal.Relop: [Terminal.LESS, Terminal.DOUBLEEQUAL],
        NonTerminal.Additiveexpression: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                                         Terminal.SUB],
        NonTerminal.Additiveexpressionprime: [Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB,
                                              Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Additiveexpressionzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                                               Terminal.SUB],
        NonTerminal.D: [Terminal.ADD, Terminal.SUB, NonTerminal.EPSILON],
        NonTerminal.Addop: [Terminal.ADD, Terminal.SUB],
        NonTerminal.Term: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termprime: [Terminal.OPENPARENTHESIS, Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Termzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.G: [Terminal.STAR, NonTerminal.EPSILON],
        NonTerminal.Signedfactor: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                                   Terminal.SUB],
        NonTerminal.Signedfactorprime: [Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Signedfactorzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Factor: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS],
        NonTerminal.Varcallprime: [Terminal.OPENBRACET, Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Varprime: [Terminal.OPENBRACET, NonTerminal.EPSILON],
        NonTerminal.Factorprime: [Terminal.OPENPARENTHESIS, NonTerminal.EPSILON],
        NonTerminal.Factorzegond: [Terminal.NUM, Terminal.OPENPARENTHESIS],
        NonTerminal.Args: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB,
                           NonTerminal.EPSILON],
        NonTerminal.Arglist: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD,
                              Terminal.SUB],
        NonTerminal.Arglistprime: [Terminal.COMMA, NonTerminal.EPSILON]
    }

    follows = {
        NonTerminal.Program: [Terminal.DOLLAR],
        NonTerminal.Declarationlist: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                      Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF,
                                      Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Declaration: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                  Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD,
                                  Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                  Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Declarationinitial: [Terminal.SEMICOLON, Terminal.OPENBRACET, Terminal.OPENPARENTHESIS,
                                         Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Declarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                       Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD,
                                       Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                       Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Vardeclarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                          Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD,
                                          Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                          Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Fundeclarationprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                          Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD,
                                          Terminal.BREAK, Terminal.IF, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                          Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Typespecifier: [Terminal.ID],
        NonTerminal.Params: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Paramlist: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Param: [Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Paramprime: [Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Compoundstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                   Terminal.VOID, Terminal.INT, Terminal.OPENACOLAD, Terminal.CLOSEACOLAD,
                                   Terminal.BREAK, Terminal.IF, Terminal.ENDIF, Terminal.ELSE, Terminal.FOR,
                                   Terminal.RETURN, Terminal.ADD, Terminal.SUB, Terminal.DOLLAR],
        NonTerminal.Statementlist: [Terminal.CLOSEACOLAD],
        NonTerminal.Statement: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF,
                                Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Expressionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                     Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF,
                                     Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                     Terminal.SUB],
        NonTerminal.Selectionstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                    Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF,
                                    Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                    Terminal.SUB],
        NonTerminal.Elsestmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                               Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF,
                               Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Iterationstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                    Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF,
                                    Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                    Terminal.SUB],
        NonTerminal.Returnstmt: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                 Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF, Terminal.ENDIF,
                                 Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD, Terminal.SUB],
        NonTerminal.Returnstmtprime: [Terminal.ID, Terminal.SEMICOLON, Terminal.NUM, Terminal.OPENPARENTHESIS,
                                      Terminal.OPENACOLAD, Terminal.CLOSEACOLAD, Terminal.BREAK, Terminal.IF,
                                      Terminal.ENDIF, Terminal.ELSE, Terminal.FOR, Terminal.RETURN, Terminal.ADD,
                                      Terminal.SUB],
        NonTerminal.Expression: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.B: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.H: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Simpleexpressionprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.C: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA],
        NonTerminal.Relop: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Additiveexpression: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS,
                                         Terminal.COMMA],
        NonTerminal.Additiveexpressionprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS,
                                              Terminal.COMMA, Terminal.LESS, Terminal.DOUBLEEQUAL],
        NonTerminal.Additiveexpressionzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS,
                                               Terminal.COMMA, Terminal.LESS, Terminal.DOUBLEEQUAL],
        NonTerminal.D: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                        Terminal.LESS, Terminal.DOUBLEEQUAL],
        NonTerminal.Addop: [Terminal.ID, Terminal.NUM, Terminal.OPENPARENTHESIS, Terminal.ADD, Terminal.SUB],
        NonTerminal.Term: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                           Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Termzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                 Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.G: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                        Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB],
        NonTerminal.Signedfactor: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                   Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Signedfactorprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS,
                                        Terminal.COMMA, Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB,
                                        Terminal.STAR],
        NonTerminal.Signedfactorzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS,
                                         Terminal.COMMA, Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD,
                                         Terminal.SUB, Terminal.STAR],
        NonTerminal.Factor: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                             Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Varcallprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                   Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Varprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                               Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Factorprime: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                  Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Factorzegond: [Terminal.SEMICOLON, Terminal.CLOSEBRACET, Terminal.CLOSEPARENTHESIS, Terminal.COMMA,
                                   Terminal.LESS, Terminal.DOUBLEEQUAL, Terminal.ADD, Terminal.SUB, Terminal.STAR],
        NonTerminal.Args: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Arglist: [Terminal.CLOSEPARENTHESIS],
        NonTerminal.Arglistprime: [Terminal.CLOSEPARENTHESIS]
    }


    def get_non_terminal_display_name(self, non_terminal: NonTerminal) -> str:
        return [i[0] for i in self.next if i[1] == non_terminal][0]

    def is_look_ahead_in_follow(self, non_terminal: NonTerminal, look_ahead: str) -> bool:
        follows = [i.value for i in self.follows[non_terminal]]
        return look_ahead in follows

    def is_epsilon_in_first(self, non_terminal: NonTerminal) -> bool:
        return NonTerminal.EPSILON in self.firsts[non_terminal]

    def _get_first(self, name) -> set:
        if isinstance(name, NonTerminal) and name != NonTerminal.EPSILON:
            return set([i.value for i in self.firsts[name]])
        else:
            return {name.value}

    def get_rhs_first(self, rules: list) -> set:
        firsts = set()
        for rule in rules:
            firsts.update(self._get_first(rule))
            if rule == NonTerminal.EPSILON or isinstance(rule, ActionSymbol):
                continue
            if isinstance(rule, Terminal) or NonTerminal.EPSILON not in self.firsts[rule]:
                if NonTerminal.EPSILON in firsts:
                    firsts.remove({NonTerminal.EPSILON})
                break

        return firsts
