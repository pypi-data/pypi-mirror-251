"use strict";(self.webpackChunk_datalayer_jupyter_environments=self.webpackChunk_datalayer_jupyter_environments||[]).push([[3647],{73647:(e,t,r)=>{r.r(t),r.d(t,{pascal:()=>u});var n=function(e){for(var t={},r="absolute and array asm begin case const constructor destructor div do downto else end file for function goto if implementation in inherited inline interface label mod nil not object of operator or packed procedure program record reintroduce repeat self set shl shr string then to type unit until uses var while with xor as class dispinterface except exports finalization finally initialization inline is library on out packed property raise resourcestring threadvar try absolute abstract alias assembler bitpacked break cdecl continue cppdecl cvar default deprecated dynamic enumerator experimental export external far far16 forward generic helper implements index interrupt iocheck local message name near nodefault noreturn nostackframe oldfpccall otherwise overload override pascal platform private protected public published read register reintroduce result safecall saveregisters softfloat specialize static stdcall stored strict unaligned unimplemented varargs virtual write".split(" "),n=0;n<r.length;++n)t[r[n]]=!0;return t}(),a={null:!0},i=/[+\-*&%=<>!?|\/]/;function o(e,t){var r,o=e.next();if("#"==o&&t.startOfLine)return e.skipToEnd(),"meta";if('"'==o||"'"==o)return t.tokenize=(r=o,function(e,t){for(var n,a=!1,i=!1;null!=(n=e.next());){if(n==r&&!a){i=!0;break}a=!a&&"\\"==n}return!i&&a||(t.tokenize=null),"string"}),t.tokenize(e,t);if("("==o&&e.eat("*"))return t.tokenize=l,l(e,t);if("{"==o)return t.tokenize=s,s(e,t);if(/[\[\]\(\),;\:\.]/.test(o))return null;if(/\d/.test(o))return e.eatWhile(/[\w\.]/),"number";if("/"==o&&e.eat("/"))return e.skipToEnd(),"comment";if(i.test(o))return e.eatWhile(i),"operator";e.eatWhile(/[\w\$_]/);var u=e.current();return n.propertyIsEnumerable(u)?"keyword":a.propertyIsEnumerable(u)?"atom":"variable"}function l(e,t){for(var r,n=!1;r=e.next();){if(")"==r&&n){t.tokenize=null;break}n="*"==r}return"comment"}function s(e,t){for(var r;r=e.next();)if("}"==r){t.tokenize=null;break}return"comment"}const u={name:"pascal",startState:function(){return{tokenize:null}},token:function(e,t){return e.eatSpace()?null:(t.tokenize||o)(e,t)},languageData:{indentOnInput:/^\s*[{}]$/,commentTokens:{block:{open:"(*",close:"*)"}}}}}}]);