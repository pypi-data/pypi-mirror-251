"use strict";(self.webpackChunk_datalayer_jupyter_content=self.webpackChunk_datalayer_jupyter_content||[]).push([[4049],{44049:(t,e,n)=>{n.r(e),n.d(e,{solr:()=>i});var r=/[^\s\|\!\+\-\*\?\~\^\&\:\(\)\[\]\{\}\"\\]/,o=/[\|\!\+\-\*\?\~\^\&]/,u=/^(OR|AND|NOT|TO)$/i;function a(t,e){var n,i,k=t.next();return'"'==k?e.tokenize=(i=k,function(t,e){for(var n,r=!1;null!=(n=t.next())&&(n!=i||r);)r=!r&&"\\"==n;return r||(e.tokenize=a),"string"}):o.test(k)?e.tokenize=(n=k,function(t,e){return"|"==n?t.eat(/\|/):"&"==n&&t.eat(/\&/),e.tokenize=a,"operator"}):r.test(k)&&(e.tokenize=function(t){return function(e,n){for(var o=t;(t=e.peek())&&null!=t.match(r);)o+=e.next();return n.tokenize=a,u.test(o)?"operator":function(t){return parseFloat(t).toString()===t}(o)?"number":":"==e.peek()?"propertyName":"string"}}(k)),e.tokenize!=a?e.tokenize(t,e):null}const i={name:"solr",startState:function(){return{tokenize:a}},token:function(t,e){return t.eatSpace()?null:e.tokenize(t,e)}}}}]);