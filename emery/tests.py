#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest import TestCase

from page import Page

class TableTests(TestCase):
    def test_parse_html_table(self):
        self.maxDiff = None
        FIXTURE = '''
<TABLE  CELLSPACING=1>
<THEAD>
<TR>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Date / Time</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>City</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>State</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Shape</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Duration</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Summary</TH>
<TH BGCOLOR=#c0c0c0 BORDERCOLOR=#000000 ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Posted</TH>
</TR>
</THEAD>
<TBODY>
<TR VALIGN=TOP>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><A HREF=089/S89728.html>6/20/12 13:53</A></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Pevek (Russia)</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><BR></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Other</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><BR></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>I saw it and it blew seven people's minds!</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>6/20/12</TD>
</TR>
<tr valign="TOP">
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt"><a href="089/S89724.html">6/20/12 09:15</a></font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt">Redmond</font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt"><br></font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt">Oval</font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt">1 minute</font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt">Sighted 4 unknown craft flying at slow speed</font></td>
<td bgcolor="#FFFFCC"><font face="Calibri" color="#000000" style="FONT-SIZE:11pt">6/20/12</font></td>
</tr>
'''
        EXPECTS = [(
            '6/20/12 13:53', 'Pevek (Russia)', '', 'Other', '', "I saw it and it blew seven people's minds!", '6/20/12')
            , (
                '6/20/12 09:15', 'Redmond', '', 'Oval', '1 minute', 'Sighted 4 unknown craft flying at slow speed',
                '6/20/12')]
        self.assertEquals(EXPECTS, list(Page.parse_table(FIXTURE)))

    def test_get_links(self):
        FIXTURE = '''
<p><a href="http://www.lolcatbible.com/">LOLCat Bible</a></p>
'''
        p = Page(html=FIXTURE)
        self.assertEquals([('LOLCat Bible', 'http://www.lolcatbible.com/')], p.links)

    def test_get_imgs(self):
        FIXTURE = '''
<p><img width="275" height="346" class="thumbimage" src="/images/thumb/8/8d/Gtfo.jpg/275px-Gtfo.jpg" alt="Ceiling Cat banishiz Boi an Gurl frum teh gardn of Eden."></p>
'''
        p = Page(html=FIXTURE)
        self.assertEquals(
            [('Ceiling Cat banishiz Boi an Gurl frum teh gardn of Eden.', '/images/thumb/8/8d/Gtfo.jpg/275px-Gtfo.jpg')]
            , p.images)

    def test_get_tables(self):
        FIXTURE = '''
<table>
<TR VALIGN=TOP>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><A HREF=089/S89728.html>6/20/12 13:53</A></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Pevek (Russia)</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><BR></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>Other</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000><BR></TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>I saw it and it blew seven people's minds!</TD>
<TD bgcolor="#FFFFCC" ><FONT style=FONT-SIZE:11pt FACE="Calibri" COLOR=#000000>6/20/12</TD>
</TR>
</table>
'''
        EXPECTS = [('6/20/12 13:53', 'Pevek (Russia)', '', 'Other', '',
                    "I saw it and it blew seven people's minds!", '6/20/12')]
        p = Page(html=FIXTURE, fix_html=True)
        self.assertEquals(EXPECTS, list(p.tables[0]))
