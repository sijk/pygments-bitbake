#
#
# Pygments lexer for BitBake files.
#
#
# Copyright (c) 2011, Simon Knopp <simon.knopp@pg.canterbury.ac.nz>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# - Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from pygments.lexer import RegexLexer, bygroups, using, include
from pygments.lexers import PythonLexer, BashLexer
from pygments.token import *

class BitbakeLexer(RegexLexer):
    name = 'Bitbake'
    aliases = ['bitbake']
    filenames = ['*.bb', '*.bbclass', '*.inc', '*.conf']

    tokens = {
        'root': [
            include('comment'),
            include('include'),
            include('variable-definition'),
            include('python-function'),
            include('shell-function'),
            include('python-def'),
            include('add-task'),
            (r'\s+', Text)
        ],

        'variable-definition': [
            (r'^(export)?(\s*)'                         # export
             r'([\w\d.+/_-]+(?:_[${}\w\d.+/_-]+)?)'     # FILES_${PN}-dev
             r'(?:(\[)([\w\d.+/_-]+)(\]))*(\s*)'        # [md5sum]
             r'([:+.]=|=[+.]|\?\??=|=)(\s*)',           # += 
                bygroups(Keyword.Type, Text, 
                         Name.Variable, 
                         Punctuation, Name.Attribute, Punctuation, Text, 
                         Operator, Text),
                'string'),
        ],

        'string': [
            (r'"', String, 'string-body'),
        ],
        'string-body': [
            include('comment'),
            include('variable-expansion'),
            include('python-expansion'),
            (r'\\\n', String.Escape),
            (r'"', String, '#pop'),
            (r'[^"\$\\]*', String),
        ],

        'comment': [
            (r'^\s*#\s*', Comment, 'comment-body'),
        ],
        'comment-body': [
            (r'TODO|FIXME|XXX', Generic.Emph),
            (r'.*\n', Comment, '#pop'),
        ],

        'variable-expansion': [
            (r'\$\{[\w\d.+/_-]+\}', Comment.PreProc),
        ],

        'python-expansion': [
            (r'(\$\{@)([^}]+)(\})', 
                bygroups(Comment.PreProc, using(PythonLexer), Comment.PreProc)),
        ],

        'shell-function': [
            (r'^(fakeroot)?(\s*)([\w\d_-]+)(\s*)(\(\))(\s*)(\{)',
                bygroups(Keyword.Type, Text, Name.Function, Text,
                         Punctuation, Text, Punctuation),
                'shell-function-body'),
        ],
        'shell-function-body': [
            (r'^(\s*)(\})(\s*\n)', bygroups(Text, Punctuation, Text), '#pop'),
            (r'.*\n', using(BashLexer)),
        ],

        'python-function': [
            (r'^(python)(\s+)([\w\d_-]+)(\s*)(\(\))(\s*)(\{)',
                bygroups(Keyword.Type, Text, Name.Function, Text,
                         Punctuation, Text, Punctuation),
                'python-function-body'),
        ],
        'python-function-body': [
            (r'^(\s*)(\})(\s*\n)', bygroups(Text, Punctuation, Text), '#pop'),
            (r'.*\n', using(PythonLexer)),
        ],

        'python-def': [
            (r'^(?=def\s).*\n', using(PythonLexer), 'python-def-body'),
        ],
        'python-def-body': [
            (r'^(?!\s)', Text, '#pop'),
            (r'.*\n', using(PythonLexer)),
        ],

        'include': [
            (r'^(\s*)(include|require|inherit)(\s*)', 
                bygroups(Text, Keyword.Namespace, Text), 
                'include-body'),
        ],
        'include-body': [
            include('string'),
            include('variable-expansion'),
            (r'[\w\d.+_-]+', Name.Namespace),
            (r'\n', Text, '#pop'),
            (r'\s', Text),
        ],

        'add-task': [
            (r'addtask|addhandler|EXPORT_FUNCTIONS', Keyword, 'add-task-body'),
        ],
        'add-task-body': [
            (r'before|after', Keyword),
            (r'[\w\d_-]+', Name),
            (r'\n', Text, '#pop'),
            (r'\s+', Text),
        ],
    }

