"use strict";(self.webpackChunk_datalayer_jupyter_content=self.webpackChunk_datalayer_jupyter_content||[]).push([[5909],{65909:(t,a,e)=>{e.r(a),e.d(a,{troff:()=>h});var n={};function r(t){if(t.eatSpace())return null;var a=t.sol(),e=t.next();if("\\"===e)return t.match("fB")||t.match("fR")||t.match("fI")||t.match("u")||t.match("d")||t.match("%")||t.match("&")?"string":t.match("m[")?(t.skipTo("]"),t.next(),"string"):t.match("s+")||t.match("s-")?(t.eatWhile(/[\d-]/),"string"):t.match("(")||t.match("*(")?(t.eatWhile(/[\w-]/),"string"):"string";if(a&&("."===e||"'"===e)&&t.eat("\\")&&t.eat('"'))return t.skipToEnd(),"comment";if(a&&"."===e){if(t.match("B ")||t.match("I ")||t.match("R "))return"attribute";if(t.match("TH ")||t.match("SH ")||t.match("SS ")||t.match("HP "))return t.skipToEnd(),"quote";if(t.match(/[A-Z]/)&&t.match(/[A-Z]/)||t.match(/[a-z]/)&&t.match(/[a-z]/))return"attribute"}t.eatWhile(/[\w-]/);var r=t.current();return n.hasOwnProperty(r)?n[r]:null}function c(t,a){return(a.tokens[0]||r)(t,a)}const h={name:"troff",startState:function(){return{tokens:[]}},token:function(t,a){return c(t,a)}}}}]);