"use strict";(self.webpackChunk_datalayer_jupyter_kernels=self.webpackChunk_datalayer_jupyter_kernels||[]).push([[1626],{51626:(e,t,n)=>{function r(e,t){return new RegExp((t?"":"^")+"(?:"+e.join("|")+")"+(t?"$":"\\b"))}function a(e,t,n){return n.tokenize.push(e),e(t,n)}n.r(t),n.d(t,{crystal:()=>S});var u=/^(?:[-+/%|&^]|\*\*?|[<>]{2})/,i=/^(?:[=!]~|===|<=>|[<>=!]=?|[|&]{2}|~)/,c=/^(?:\[\][?=]?)/,o=/^(?:\.(?:\.{2})?|->|[?:])/,s=/^[a-z_\u009F-\uFFFF][a-zA-Z0-9_\u009F-\uFFFF]*/,l=/^[A-Z_\u009F-\uFFFF][a-zA-Z0-9_\u009F-\uFFFF]*/,f=r(["abstract","alias","as","asm","begin","break","case","class","def","do","else","elsif","end","ensure","enum","extend","for","fun","if","include","instance_sizeof","lib","macro","module","next","of","out","pointerof","private","protected","rescue","return","require","select","sizeof","struct","super","then","type","typeof","uninitialized","union","unless","until","when","while","with","yield","__DIR__","__END_LINE__","__FILE__","__LINE__"]),m=r(["true","false","nil","self"]),h=r(["def","fun","macro","class","module","struct","lib","enum","union","do","for"]),p=r(["if","unless","case","while","until","begin","then"]),k=["end","else","elsif","rescue","ensure"],d=r(k),F=["\\)","\\}","\\]"],_=new RegExp("^(?:"+F.join("|")+")$"),z={def:x,fun:x,macro:function(e,t){if(e.eatSpace())return null;var n;if(n=e.match(s)){if("def"==n)return"keyword";e.eat(/[?!]/)}return t.tokenize.pop(),"def"},class:I,module:I,struct:I,lib:I,enum:I,union:I},b={"[":"]","{":"}","(":")","<":">"};function g(e,t){if(e.eatSpace())return null;if("\\"!=t.lastToken&&e.match("{%",!1))return a(w("%","%"),e,t);if("\\"!=t.lastToken&&e.match("{{",!1))return a(w("{","}"),e,t);if("#"==e.peek())return e.skipToEnd(),"comment";var n;if(e.match(s))return e.eat(/[?!]/),n=e.current(),e.eat(":")?"atom":"."==t.lastToken?"property":f.test(n)?(h.test(n)?"fun"==n&&t.blocks.indexOf("lib")>=0||"def"==n&&"abstract"==t.lastToken||(t.blocks.push(n),t.currentIndent+=1):"operator"!=t.lastStyle&&t.lastStyle||!p.test(n)?"end"==n&&(t.blocks.pop(),t.currentIndent-=1):(t.blocks.push(n),t.currentIndent+=1),z.hasOwnProperty(n)&&t.tokenize.push(z[n]),"keyword"):m.test(n)?"atom":"variable";if(e.eat("@"))return"["==e.peek()?a(y("[","]","meta"),e,t):(e.eat("@"),e.match(s)||e.match(l),"propertyName");if(e.match(l))return"tag";if(e.eat(":"))return e.eat('"')?a(v('"',"atom",!1),e,t):e.match(s)||e.match(l)||e.match(u)||e.match(i)||e.match(c)?"atom":(e.eat(":"),"operator");if(e.eat('"'))return a(v('"',"string",!0),e,t);if("%"==e.peek()){var r,k="string",d=!0;if(e.match("%r"))k="string.special",r=e.next();else if(e.match("%w"))d=!1,r=e.next();else if(e.match("%q"))d=!1,r=e.next();else if(r=e.match(/^%([^\w\s=])/))r=r[1];else{if(e.match(/^%[a-zA-Z_\u009F-\uFFFF][\w\u009F-\uFFFF]*/))return"meta";if(e.eat("%"))return"operator"}return b.hasOwnProperty(r)&&(r=b[r]),a(v(r,k,d),e,t)}return(n=e.match(/^<<-('?)([A-Z]\w*)\1/))?a(function(e,t){return function(n,r){if(n.sol()&&(n.eatSpace(),n.match(e)))return r.tokenize.pop(),"string";for(var a=!1;n.peek();)if(a)n.next(),a=!1;else{if(n.match("{%",!1))return r.tokenize.push(w("%","%")),"string";if(n.match("{{",!1))return r.tokenize.push(w("{","}")),"string";if(t&&n.match("#{",!1))return r.tokenize.push(y("#{","}","meta")),"string";a=t&&"\\"==n.next()}return"string"}}(n[2],!n[1]),e,t):e.eat("'")?(e.match(/^(?:[^']|\\(?:[befnrtv0'"]|[0-7]{3}|u(?:[0-9a-fA-F]{4}|\{[0-9a-fA-F]{1,6}\})))/),e.eat("'"),"atom"):e.eat("0")?(e.eat("x")?e.match(/^[0-9a-fA-F_]+/):e.eat("o")?e.match(/^[0-7_]+/):e.eat("b")&&e.match(/^[01_]+/),"number"):e.eat(/^\d/)?(e.match(/^[\d_]*(?:\.[\d_]+)?(?:[eE][+-]?\d+)?/),"number"):e.match(u)?(e.eat("="),"operator"):e.match(i)||e.match(o)?"operator":(n=e.match(/[({[]/,!1))?a(y(n=n[0],b[n],null),e,t):e.eat("\\")?(e.next(),"meta"):(e.next(),null)}function y(e,t,n,r){return function(a,u){if(!r&&a.match(e))return u.tokenize[u.tokenize.length-1]=y(e,t,n,!0),u.currentIndent+=1,n;var i=g(a,u);return a.current()===t&&(u.tokenize.pop(),u.currentIndent-=1,i=n),i}}function w(e,t,n){return function(r,a){return!n&&r.match("{"+e)?(a.currentIndent+=1,a.tokenize[a.tokenize.length-1]=w(e,t,!0),"meta"):r.match(t+"}")?(a.currentIndent-=1,a.tokenize.pop(),"meta"):g(r,a)}}function x(e,t){return e.eatSpace()?null:(e.match(s)?e.eat(/[!?]/):e.match(u)||e.match(i)||e.match(c),t.tokenize.pop(),"def")}function I(e,t){return e.eatSpace()?null:(e.match(l),t.tokenize.pop(),"def")}function v(e,t,n){return function(r,a){for(var u=!1;r.peek();)if(u)r.next(),u=!1;else{if(r.match("{%",!1))return a.tokenize.push(w("%","%")),t;if(r.match("{{",!1))return a.tokenize.push(w("{","}")),t;if(n&&r.match("#{",!1))return a.tokenize.push(y("#{","}","meta")),t;var i=r.next();if(i==e)return a.tokenize.pop(),t;u=n&&"\\"==i}return t}}const S={name:"crystal",startState:function(){return{tokenize:[g],currentIndent:0,lastToken:null,lastStyle:null,blocks:[]}},token:function(e,t){var n=t.tokenize[t.tokenize.length-1](e,t),r=e.current();return n&&"comment"!=n&&(t.lastToken=r,t.lastStyle=n),n},indent:function(e,t,n){return t=t.replace(/^\s*(?:\{%)?\s*|\s*(?:%\})?\s*$/g,""),d.test(t)||_.test(t)?n.unit*(e.currentIndent-1):n.unit*e.currentIndent},languageData:{indentOnInput:r(F.concat(k),!0),commentTokens:{line:"#"}}}}}]);