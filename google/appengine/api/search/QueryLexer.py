#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import sys
from google.appengine._internal.antlr3 import *
from google.appengine._internal.antlr3.compat import set, frozenset



HIDDEN = BaseRecognizer.HIDDEN


FUNCTION=8
FIX=30
ESC=36
OCTAL_ESC=35
FUZZY=9
NOT=28
AND=26
ESCAPED_CHAR=44
EOF=-1
LPAREN=24
HAS=23
QUOTE=33
RPAREN=25
START_CHAR=39
COMMA=29
ARGS=4
DIGIT=43
EQ=22
NE=21
LESSTHAN=18
GE=19
TEXT_ESC=41
CONJUNCTION=5
UNICODE_ESC=34
HEX_DIGIT=45
LITERAL=11
VALUE=15
TEXT=32
MINUS=38
NUMBER_PREFIX=40
REWRITE=31
EMPTY=7
SEQUENCE=14
DISJUNCTION=6
WS=16
NEGATION=12
OR=27
GT=20
GLOBAL=10
LE=17
MID_CHAR=42
STRING=13
BACKSLASH=37


class QueryLexer(Lexer):

    grammarFileName = ""
    antlr_version = version_str_to_tuple("3.1.1")
    antlr_version_str = "3.1.1"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        Lexer.__init__(self, input, state)

        self.dfa7 = self.DFA7(
            self, 7,
            eot = self.DFA7_eot,
            eof = self.DFA7_eof,
            min = self.DFA7_min,
            max = self.DFA7_max,
            accept = self.DFA7_accept,
            special = self.DFA7_special,
            transition = self.DFA7_transition
            )

        self.dfa8 = self.DFA8(
            self, 8,
            eot = self.DFA8_eot,
            eof = self.DFA8_eof,
            min = self.DFA8_min,
            max = self.DFA8_max,
            accept = self.DFA8_accept,
            special = self.DFA8_special,
            transition = self.DFA8_transition
            )







    def mHAS(self, ):

        try:
            _type = HAS
            _channel = DEFAULT_CHANNEL



            pass
            self.match(58)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mOR(self, ):

        try:
            _type = OR
            _channel = DEFAULT_CHANNEL



            pass
            self.match("OR")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mAND(self, ):

        try:
            _type = AND
            _channel = DEFAULT_CHANNEL



            pass
            self.match("AND")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mNOT(self, ):

        try:
            _type = NOT
            _channel = DEFAULT_CHANNEL



            pass
            self.match("NOT")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mREWRITE(self, ):

        try:
            _type = REWRITE
            _channel = DEFAULT_CHANNEL



            pass
            self.match(126)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mFIX(self, ):

        try:
            _type = FIX
            _channel = DEFAULT_CHANNEL



            pass
            self.match(43)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mESC(self, ):

        try:
            _type = ESC
            _channel = DEFAULT_CHANNEL


            alt1 = 3
            LA1_0 = self.input.LA(1)

            if (LA1_0 == 92) :
                LA1 = self.input.LA(2)
                if LA1 == 34 or LA1 == 92:
                    alt1 = 1
                elif LA1 == 117:
                    alt1 = 2
                elif LA1 == 48 or LA1 == 49 or LA1 == 50 or LA1 == 51 or LA1 == 52 or LA1 == 53 or LA1 == 54 or LA1 == 55:
                    alt1 = 3
                else:
                    nvae = NoViableAltException("", 1, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("", 1, 0, self.input)

                raise nvae

            if alt1 == 1:

                pass
                self.match(92)
                if self.input.LA(1) == 34 or self.input.LA(1) == 92:
                    self.input.consume()
                else:
                    mse = MismatchedSetException(None, self.input)
                    self.recover(mse)
                    raise mse



            elif alt1 == 2:

                pass
                self.mUNICODE_ESC()


            elif alt1 == 3:

                pass
                self.mOCTAL_ESC()


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL



            pass
            if (9 <= self.input.LA(1) <= 10) or (12 <= self.input.LA(1) <= 13) or self.input.LA(1) == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse




            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mLPAREN(self, ):

        try:
            _type = LPAREN
            _channel = DEFAULT_CHANNEL



            pass
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mRPAREN(self, ):

        try:
            _type = RPAREN
            _channel = DEFAULT_CHANNEL



            pass
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mCOMMA(self, ):

        try:
            _type = COMMA
            _channel = DEFAULT_CHANNEL



            pass
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mBACKSLASH(self, ):

        try:
            _type = BACKSLASH
            _channel = DEFAULT_CHANNEL



            pass
            self.match(92)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mLESSTHAN(self, ):

        try:
            _type = LESSTHAN
            _channel = DEFAULT_CHANNEL



            pass
            self.match(60)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mGT(self, ):

        try:
            _type = GT
            _channel = DEFAULT_CHANNEL



            pass
            self.match(62)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mGE(self, ):

        try:
            _type = GE
            _channel = DEFAULT_CHANNEL



            pass
            self.match(">=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mLE(self, ):

        try:
            _type = LE
            _channel = DEFAULT_CHANNEL



            pass
            self.match("<=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mNE(self, ):

        try:
            _type = NE
            _channel = DEFAULT_CHANNEL



            pass
            self.match("!=")



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mEQ(self, ):

        try:
            _type = EQ
            _channel = DEFAULT_CHANNEL



            pass
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mMINUS(self, ):

        try:
            _type = MINUS
            _channel = DEFAULT_CHANNEL



            pass
            self.match(45)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mQUOTE(self, ):

        try:
            _type = QUOTE
            _channel = DEFAULT_CHANNEL



            pass
            self.match(34)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mTEXT(self, ):

        try:
            _type = TEXT
            _channel = DEFAULT_CHANNEL



            pass

            alt2 = 3
            LA2_0 = self.input.LA(1)

            if (LA2_0 == 33 or (35 <= LA2_0 <= 39) or LA2_0 == 42 or (46 <= LA2_0 <= 47) or LA2_0 == 59 or (63 <= LA2_0 <= 91) or (93 <= LA2_0 <= 125) or (161 <= LA2_0 <= 65518)) :
                alt2 = 1
            elif (LA2_0 == 45 or (48 <= LA2_0 <= 57)) :
                alt2 = 2
            elif (LA2_0 == 92) :
                alt2 = 3
            else:
                nvae = NoViableAltException("", 2, 0, self.input)

                raise nvae

            if alt2 == 1:

                pass
                self.mSTART_CHAR()


            elif alt2 == 2:

                pass
                self.mNUMBER_PREFIX()


            elif alt2 == 3:

                pass
                self.mTEXT_ESC()




            while True:
                alt3 = 3
                LA3_0 = self.input.LA(1)

                if (LA3_0 == 33 or (35 <= LA3_0 <= 39) or (42 <= LA3_0 <= 43) or (45 <= LA3_0 <= 57) or LA3_0 == 59 or (63 <= LA3_0 <= 91) or (93 <= LA3_0 <= 125) or (161 <= LA3_0 <= 65518)) :
                    alt3 = 1
                elif (LA3_0 == 92) :
                    alt3 = 2


                if alt3 == 1:

                    pass
                    self.mMID_CHAR()


                elif alt3 == 2:

                    pass
                    self.mTEXT_ESC()


                else:
                    break





            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass






    def mNUMBER_PREFIX(self, ):

        try:


            pass

            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == 45) :
                alt4 = 1
            if alt4 == 1:

                pass
                self.mMINUS()



            self.mDIGIT()




        finally:

            pass






    def mTEXT_ESC(self, ):

        try:

            alt5 = 3
            LA5_0 = self.input.LA(1)

            if (LA5_0 == 92) :
                LA5 = self.input.LA(2)
                if LA5 == 34 or LA5 == 43 or LA5 == 44 or LA5 == 58 or LA5 == 60 or LA5 == 61 or LA5 == 62 or LA5 == 92 or LA5 == 126:
                    alt5 = 1
                elif LA5 == 117:
                    alt5 = 2
                elif LA5 == 48 or LA5 == 49 or LA5 == 50 or LA5 == 51 or LA5 == 52 or LA5 == 53 or LA5 == 54 or LA5 == 55:
                    alt5 = 3
                else:
                    nvae = NoViableAltException("", 5, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("", 5, 0, self.input)

                raise nvae

            if alt5 == 1:

                pass
                self.mESCAPED_CHAR()


            elif alt5 == 2:

                pass
                self.mUNICODE_ESC()


            elif alt5 == 3:

                pass
                self.mOCTAL_ESC()



        finally:

            pass






    def mUNICODE_ESC(self, ):

        try:


            pass
            self.match(92)
            self.match(117)
            self.mHEX_DIGIT()
            self.mHEX_DIGIT()
            self.mHEX_DIGIT()
            self.mHEX_DIGIT()




        finally:

            pass






    def mOCTAL_ESC(self, ):

        try:

            alt6 = 3
            LA6_0 = self.input.LA(1)

            if (LA6_0 == 92) :
                LA6_1 = self.input.LA(2)

                if ((48 <= LA6_1 <= 51)) :
                    LA6_2 = self.input.LA(3)

                    if ((48 <= LA6_2 <= 55)) :
                        LA6_4 = self.input.LA(4)

                        if ((48 <= LA6_4 <= 55)) :
                            alt6 = 1
                        else:
                            alt6 = 2
                    else:
                        alt6 = 3
                elif ((52 <= LA6_1 <= 55)) :
                    LA6_3 = self.input.LA(3)

                    if ((48 <= LA6_3 <= 55)) :
                        alt6 = 2
                    else:
                        alt6 = 3
                else:
                    nvae = NoViableAltException("", 6, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("", 6, 0, self.input)

                raise nvae

            if alt6 == 1:

                pass
                self.match(92)


                pass
                self.matchRange(48, 51)





                pass
                self.matchRange(48, 55)





                pass
                self.matchRange(48, 55)





            elif alt6 == 2:

                pass
                self.match(92)


                pass
                self.matchRange(48, 55)





                pass
                self.matchRange(48, 55)





            elif alt6 == 3:

                pass
                self.match(92)


                pass
                self.matchRange(48, 55)






        finally:

            pass






    def mDIGIT(self, ):

        try:


            pass
            self.matchRange(48, 57)




        finally:

            pass






    def mHEX_DIGIT(self, ):

        try:


            pass
            if (48 <= self.input.LA(1) <= 57) or (65 <= self.input.LA(1) <= 70) or (97 <= self.input.LA(1) <= 102):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass






    def mSTART_CHAR(self, ):

        try:


            pass
            if self.input.LA(1) == 33 or (35 <= self.input.LA(1) <= 39) or self.input.LA(1) == 42 or (46 <= self.input.LA(1) <= 47) or self.input.LA(1) == 59 or (63 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 125) or (161 <= self.input.LA(1) <= 65518):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass






    def mMID_CHAR(self, ):

        try:


            pass
            if self.input.LA(1) == 33 or (35 <= self.input.LA(1) <= 39) or (42 <= self.input.LA(1) <= 43) or (45 <= self.input.LA(1) <= 57) or self.input.LA(1) == 59 or (63 <= self.input.LA(1) <= 91) or (93 <= self.input.LA(1) <= 125) or (161 <= self.input.LA(1) <= 65518):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass






    def mESCAPED_CHAR(self, ):

        try:

            alt7 = 9
            alt7 = self.dfa7.predict(self.input)
            if alt7 == 1:

                pass
                self.match("\\,")


            elif alt7 == 2:

                pass
                self.match("\\:")


            elif alt7 == 3:

                pass
                self.match("\\=")


            elif alt7 == 4:

                pass
                self.match("\\<")


            elif alt7 == 5:

                pass
                self.match("\\>")


            elif alt7 == 6:

                pass
                self.match("\\+")


            elif alt7 == 7:

                pass
                self.match("\\~")


            elif alt7 == 8:

                pass
                self.match("\\\"")


            elif alt7 == 9:

                pass
                self.match("\\\\")



        finally:

            pass





    def mTokens(self):

        alt8 = 21
        alt8 = self.dfa8.predict(self.input)
        if alt8 == 1:

            pass
            self.mHAS()


        elif alt8 == 2:

            pass
            self.mOR()


        elif alt8 == 3:

            pass
            self.mAND()


        elif alt8 == 4:

            pass
            self.mNOT()


        elif alt8 == 5:

            pass
            self.mREWRITE()


        elif alt8 == 6:

            pass
            self.mFIX()


        elif alt8 == 7:

            pass
            self.mESC()


        elif alt8 == 8:

            pass
            self.mWS()


        elif alt8 == 9:

            pass
            self.mLPAREN()


        elif alt8 == 10:

            pass
            self.mRPAREN()


        elif alt8 == 11:

            pass
            self.mCOMMA()


        elif alt8 == 12:

            pass
            self.mBACKSLASH()


        elif alt8 == 13:

            pass
            self.mLESSTHAN()


        elif alt8 == 14:

            pass
            self.mGT()


        elif alt8 == 15:

            pass
            self.mGE()


        elif alt8 == 16:

            pass
            self.mLE()


        elif alt8 == 17:

            pass
            self.mNE()


        elif alt8 == 18:

            pass
            self.mEQ()


        elif alt8 == 19:

            pass
            self.mMINUS()


        elif alt8 == 20:

            pass
            self.mQUOTE()


        elif alt8 == 21:

            pass
            self.mTEXT()









    DFA7_eot = DFA.unpack(
        u"\13\uffff"
        )

    DFA7_eof = DFA.unpack(
        u"\13\uffff"
        )

    DFA7_min = DFA.unpack(
        u"\1\134\1\42\11\uffff"
        )

    DFA7_max = DFA.unpack(
        u"\1\134\1\176\11\uffff"
        )

    DFA7_accept = DFA.unpack(
        u"\2\uffff\1\1\1\2\1\3\1\4\1\5\1\6\1\7\1\10\1\11"
        )

    DFA7_special = DFA.unpack(
        u"\13\uffff"
        )


    DFA7_transition = [
        DFA.unpack(u"\1\1"),
        DFA.unpack(u"\1\11\10\uffff\1\7\1\2\15\uffff\1\3\1\uffff\1\5\1\4"
        u"\1\6\35\uffff\1\12\41\uffff\1\10"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"")
    ]



    DFA7 = DFA


    DFA8_eot = DFA.unpack(
        u"\2\uffff\3\22\2\uffff\1\32\4\uffff\1\35\1\37\1\22\1\uffff\1\41"
        u"\2\uffff\1\42\2\22\1\45\1\uffff\2\45\1\uffff\1\45\7\uffff\1\51"
        u"\1\52\2\uffff\2\45\3\uffff\1\45\1\uffff\1\45"
        )

    DFA8_eof = DFA.unpack(
        u"\57\uffff"
        )

    DFA8_min = DFA.unpack(
        u"\1\11\1\uffff\1\122\1\116\1\117\2\uffff\1\42\4\uffff\3\75\1\uffff"
        u"\1\60\2\uffff\1\41\1\104\1\124\1\41\1\60\2\41\1\uffff\1\41\7\uffff"
        u"\2\41\1\uffff\1\60\2\41\2\uffff\1\60\1\41\1\60\1\41"
        )

    DFA8_max = DFA.unpack(
        u"\1\uffee\1\uffff\1\122\1\116\1\117\2\uffff\1\176\4\uffff\3\75\1"
        u"\uffff\1\71\2\uffff\1\uffee\1\104\1\124\1\uffee\1\146\2\uffee\1"
        u"\uffff\1\uffee\7\uffff\2\uffee\1\uffff\1\146\2\uffee\2\uffff\1"
        u"\146\1\uffee\1\146\1\uffee"
        )

    DFA8_accept = DFA.unpack(
        u"\1\uffff\1\1\3\uffff\1\5\1\6\1\uffff\1\10\1\11\1\12\1\13\3\uffff"
        u"\1\22\1\uffff\1\24\1\25\7\uffff\1\14\1\uffff\1\20\1\15\1\17\1\16"
        u"\1\21\1\23\1\2\2\uffff\1\7\3\uffff\1\3\1\4\4\uffff"
        )

    DFA8_special = DFA.unpack(
        u"\57\uffff"
        )


    DFA8_transition = [
        DFA.unpack(u"\2\10\1\uffff\2\10\22\uffff\1\10\1\16\1\21\5\22\1\11"
        u"\1\12\1\22\1\6\1\13\1\20\14\22\1\1\1\22\1\14\1\17\1\15\2\22\1\3"
        u"\14\22\1\4\1\2\14\22\1\7\41\22\1\5\42\uffff\uff4e\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\23"),
        DFA.unpack(u"\1\24"),
        DFA.unpack(u"\1\25"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\26\10\uffff\2\22\3\uffff\4\31\4\33\2\uffff\1\22"
        u"\1\uffff\3\22\35\uffff\1\30\30\uffff\1\27\10\uffff\1\22"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\34"),
        DFA.unpack(u"\1\36"),
        DFA.unpack(u"\1\40"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\22"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\1\43"),
        DFA.unpack(u"\1\44"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\12\46\7\uffff\6\46\32\uffff\6\46"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\3\22\10\47"
        u"\2\22\1\uffff\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\3\22\10\50"
        u"\2\22\1\uffff\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u""),
        DFA.unpack(u"\12\53\7\uffff\6\53\32\uffff\6\53"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\3\22\10\54"
        u"\2\22\1\uffff\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\12\55\7\uffff\6\55\32\uffff\6\55"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22"),
        DFA.unpack(u"\12\56\7\uffff\6\56\32\uffff\6\56"),
        DFA.unpack(u"\1\22\1\uffff\5\22\2\uffff\2\22\1\uffff\15\22\1\uffff"
        u"\1\22\3\uffff\77\22\43\uffff\uff4e\22")
    ]



    DFA8 = DFA




def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from google.appengine._internal.antlr3.main import LexerMain
    main = LexerMain(QueryLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
