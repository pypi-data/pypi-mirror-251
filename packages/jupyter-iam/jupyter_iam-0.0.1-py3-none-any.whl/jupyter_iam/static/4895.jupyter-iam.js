"use strict";(self.webpackChunk_datalayer_jupyter_iam=self.webpackChunk_datalayer_jupyter_iam||[]).push([[4895],{24895:(e,t,r)=>{function i(e){var t,r;e?(t=/^(exx?|(ld|cp)([di]r?)?|[lp]ea|pop|push|ad[cd]|cpl|daa|dec|inc|neg|sbc|sub|and|bit|[cs]cf|x?or|res|set|r[lr]c?a?|r[lr]d|s[lr]a|srl|djnz|nop|[de]i|halt|im|in([di]mr?|ir?|irx|2r?)|ot(dmr?|[id]rx|imr?)|out(0?|[di]r?|[di]2r?)|tst(io)?|slp)(\.([sl]?i)?[sl])?\b/i,r=/^(((call|j[pr]|rst|ret[in]?)(\.([sl]?i)?[sl])?)|(rs|st)mix)\b/i):(t=/^(exx?|(ld|cp|in)([di]r?)?|pop|push|ad[cd]|cpl|daa|dec|inc|neg|sbc|sub|and|bit|[cs]cf|x?or|res|set|r[lr]c?a?|r[lr]d|s[lr]a|srl|djnz|nop|rst|[de]i|halt|im|ot[di]r|out[di]?)\b/i,r=/^(call|j[pr]|ret[in]?|b_?(call|jump))\b/i);var i=/^(af?|bc?|c|de?|e|hl?|l|i[xy]?|r|sp)\b/i,n=/^(n?[zc]|p[oe]?|m)\b/i,a=/^([hl][xy]|i[xy][hl]|slia|sll)\b/i,l=/^([\da-f]+h|[0-7]+o|[01]+b|\d+d?)\b/i;return{name:"z80",startState:function(){return{context:0}},token:function(s,c){if(s.column()||(c.context=0),s.eatSpace())return null;var u;if(s.eatWhile(/\w/)){if(e&&s.eat(".")&&s.eatWhile(/\w/),u=s.current(),!s.indentation())return s.match(l)?"number":null;if((1==c.context||4==c.context)&&i.test(u))return c.context=4,"variable";if(2==c.context&&n.test(u))return c.context=4,"variableName.special";if(t.test(u))return c.context=1,"keyword";if(r.test(u))return c.context=2,"keyword";if(4==c.context&&l.test(u))return"number";if(a.test(u))return"error"}else{if(s.eat(";"))return s.skipToEnd(),"comment";if(s.eat('"')){for(;(u=s.next())&&'"'!=u;)"\\"==u&&s.next();return"string"}if(s.eat("'")){if(s.match(/\\?.'/))return"number"}else if(s.eat(".")||s.sol()&&s.eat("#")){if(c.context=5,s.eatWhile(/\w/))return"def"}else if(s.eat("$")){if(s.eatWhile(/[\da-f]/i))return"number"}else if(s.eat("%")){if(s.eatWhile(/[01]/))return"number"}else s.next()}return null}}}r.r(t),r.d(t,{ez80:()=>a,z80:()=>n});const n=i(!1),a=i(!0)}}]);