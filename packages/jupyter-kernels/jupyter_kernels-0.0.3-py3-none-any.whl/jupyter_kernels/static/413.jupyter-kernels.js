"use strict";(self.webpackChunk_datalayer_jupyter_kernels=self.webpackChunk_datalayer_jupyter_kernels||[]).push([[413],{80413:(e,t,n)=>{n.r(t),n.d(t,{smalltalk:()=>x});var a=/[+\-\/\\*~<>=@%|&?!.,:;^]/,i=/true|false|nil|self|super|thisContext/,r=function(e,t){this.next=e,this.parent=t},s=function(e,t,n){this.name=e,this.context=t,this.eos=n},l=function(){this.context=new r(o,null),this.expectVariable=!0,this.indentation=0,this.userIndentationDelta=0};l.prototype.userIndent=function(e,t){this.userIndentationDelta=e>0?e/t-this.indentation:0};var o=function(e,t,n){var l=new s(null,t,!1),o=e.next();return'"'===o?l=u(e,new r(u,t)):"'"===o?l=c(e,new r(c,t)):"#"===o?"'"===e.peek()?(e.next(),l=h(e,new r(h,t))):e.eatWhile(/[^\s.{}\[\]()]/)?l.name="string.special":l.name="meta":"$"===o?("<"===e.next()&&(e.eatWhile(/[^\s>]/),e.next()),l.name="string.special"):"|"===o&&n.expectVariable?l.context=new r(p,t):/[\[\]{}()]/.test(o)?(l.name="bracket",l.eos=/[\[{(]/.test(o),"["===o?n.indentation++:"]"===o&&(n.indentation=Math.max(0,n.indentation-1))):a.test(o)?(e.eatWhile(a),l.name="operator",l.eos=";"!==o):/\d/.test(o)?(e.eatWhile(/[\w\d]/),l.name="number"):/[\w_]/.test(o)?(e.eatWhile(/[\w\d_]/),l.name=n.expectVariable?i.test(e.current())?"keyword":"variable":null):l.eos=n.expectVariable,l},u=function(e,t){return e.eatWhile(/[^"]/),new s("comment",e.eat('"')?t.parent:t,!0)},c=function(e,t){return e.eatWhile(/[^']/),new s("string",e.eat("'")?t.parent:t,!1)},h=function(e,t){return e.eatWhile(/[^']/),new s("string.special",e.eat("'")?t.parent:t,!1)},p=function(e,t){var n=new s(null,t,!1);return"|"===e.next()?(n.context=t.parent,n.eos=!0):(e.eatWhile(/[^|]/),n.name="variable"),n};const x={name:"smalltalk",startState:function(){return new l},token:function(e,t){if(t.userIndent(e.indentation(),e.indentUnit),e.eatSpace())return null;var n=t.context.next(e,t.context,t);return t.context=n.context,t.expectVariable=n.eos,n.name},blankLine:function(e,t){e.userIndent(0,t)},indent:function(e,t,n){var a=e.context.next===o&&t&&"]"===t.charAt(0)?-1:e.userIndentationDelta;return(e.indentation+a)*n.unit},languageData:{indentOnInput:/^\s*\]$/}}}}]);