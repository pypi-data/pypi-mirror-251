"use strict";(self.webpackChunk_datalayer_jupyter_environments=self.webpackChunk_datalayer_jupyter_environments||[]).push([[3504],{3504:(r,n,t)=>{function e(r,n){return r.skipToEnd(),n.cur=s,"error"}function u(r,n){return r.match(/^HTTP\/\d\.\d/)?(n.cur=c,"keyword"):r.match(/^[A-Z]+/)&&/[ \t]/.test(r.peek())?(n.cur=a,"keyword"):e(r,n)}function c(r,n){var t=r.match(/^\d+/);if(!t)return e(r,n);n.cur=o;var u=Number(t[0]);return u>=100&&u<400?"atom":"error"}function o(r,n){return r.skipToEnd(),n.cur=s,null}function a(r,n){return r.eatWhile(/\S/),n.cur=i,"string.special"}function i(r,n){return r.match(/^HTTP\/\d\.\d$/)?(n.cur=s,"keyword"):e(r,n)}function s(r){return r.sol()&&!r.eat(/[ \t]/)?r.match(/^.*?:/)?"atom":(r.skipToEnd(),"error"):(r.skipToEnd(),"string")}function d(r){return r.skipToEnd(),null}t.r(n),t.d(n,{http:()=>k});const k={name:"http",token:function(r,n){var t=n.cur;return t!=s&&t!=d&&r.eatSpace()?null:t(r,n)},blankLine:function(r){r.cur=d},startState:function(){return{cur:u}}}}}]);