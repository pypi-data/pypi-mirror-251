"use strict";(self.webpackChunk_datalayer_jupyter_kernels=self.webpackChunk_datalayer_jupyter_kernels||[]).push([[4196],{53695:(e,t,s)=>{s.d(t,{Ll:()=>n,qP:()=>a,vM:()=>i});var r=s(47963);const n=new r.Token("@datalayer/jupyterlite-kernel:IKernels"),i="javascript",a=new r.Token("@datalayer/jupyterlite-kernel:IKernelSpecs")},54196:(e,t,s)=>{s.r(t),s.d(t,{default:()=>C});var r=s(48425),n=s(53695),i=s(6041),a=s(3283),o=s(47963),l=s(71676),c=s(29643);class u{constructor(e){this._kernels=new i.v,this._clients=new i.v,this._kernelClients=new i.v;const{kernelspecs:t}=e;this._kernelspecs=t}async startNew(e){const{id:t,name:s,location:r}=e,n=this._kernelspecs.factories.get(s);if(!n)return{id:t,name:s};const i=new c.WU,d=(e,t,s)=>{var r;const n=this._kernels.get(e);if(!n)throw Error(`No kernel ${e}`);this._clients.set(t,s),null===(r=this._kernelClients.get(e))||void 0===r||r.add(t),s.on("message",(async e=>{let t;if(e instanceof ArrayBuffer)e=new Uint8Array(e).buffer,t=(0,a.deserialize)(e,"v1.kernel.websocket.jupyter.org");else{if("string"!=typeof e)return;{const s=(new TextEncoder).encode(e);t=(0,a.deserialize)(s,"v1.kernel.websocket.jupyter.org")}}"input_reply"===t.header.msg_type?n.handleMessage(t):(async e=>{await i.runExclusive((async()=>{await n.handleMessage(e)}))})(t)}));const o=()=>{var s;this._clients.delete(t),null===(s=this._kernelClients.get(e))||void 0===s||s.delete(t)};n.disposed.connect(o),s.onclose=o},g=null!=t?t:o.UUID.uuid4(),h=`${u.WS_BASE_URL}api/kernels/${g}/channels`,p=this._kernels.get(g);if(p)return{id:p.id,name:p.name};const v=await n({id:g,sendMessage:e=>{const t=e.header.session,s=this._clients.get(t);if(!s)return void console.warn(`Trying to send message on removed socket for kernel ${g}`);const r=(0,a.serialize)(e,"v1.kernel.websocket.jupyter.org");if("iopub"!==e.channel)s.send(r);else{const e=this._kernelClients.get(g);null==e||e.forEach((e=>{var t;null===(t=this._clients.get(e))||void 0===t||t.send(r)}))}},name:s,location:r});await v.ready,this._kernels.set(g,v),this._kernelClients.set(g,new Set);const y=new l.Server(h);return y.on("connection",(e=>{var t;const s=null!==(t=new URL(e.url).searchParams.get("session_id"))&&void 0!==t?t:"";d(g,s,e)})),y.on("close",(()=>{this._clients.keys().forEach((e=>{var t;const s=this._clients.get(e);(null==s?void 0:s.readyState)===WebSocket.CLOSED&&(this._clients.delete(e),null===(t=this._kernelClients.get(g))||void 0===t||t.delete(e))}))})),v.disposed.connect((()=>{y.close(),this._kernels.delete(g),this._kernelClients.delete(g)})),{id:v.id,name:v.name}}async restart(e){const t=this._kernels.get(e);if(!t)throw Error(`Kernel ${e} does not exist`);const{id:s,name:r,location:n}=t;return t.dispose(),this.startNew({id:s,name:r,location:n})}async shutdown(e){var t;null===(t=this._kernels.delete(e))||void 0===t||t.dispose()}}!function(e){e.WS_BASE_URL=r.PageConfig.getBaseUrl().replace(/^http/,"ws")}(u||(u={}));class d{constructor(){this._specs=new Map,this._factories=new Map}get specs(){return 0===this._specs.size?null:{default:this.defaultKernelName,kernelspecs:Object.fromEntries(this._specs)}}get defaultKernelName(){let e=r.PageConfig.getOption("defaultKernelName");if(!e&&this._specs.size){const t=Array.from(this._specs.keys());t.sort(),e=t[0]}return e||n.vM}get factories(){return this._factories}register(e){const{spec:t,create:s}=e;this._specs.set(t.name,t),this._factories.set(t.name,s)}}var g=s(16519),h=s(98209);class p{constructor(){this._registration=null,this._registrationChanged=new h.Signal(this),this.initialize()}get registrationChanged(){return this._registrationChanged}get enabled(){return null!==this._registration}async initialize(){if("serviceWorker"in navigator||(console.error("ServiceWorker registration failed: Service Workers not supported in this browser"),this.setRegistration(null)),navigator.serviceWorker.controller){const e=await navigator.serviceWorker.getRegistration(navigator.serviceWorker.controller.scriptURL);e&&this.setRegistration(e)}return await navigator.serviceWorker.register(r.URLExt.join(r.PageConfig.getBaseUrl(),"services.js")).then((e=>{this.setRegistration(e)}),(e=>{console.error(`ServiceWorker registration failed: ${e}`),this.setRegistration(null)}))}setRegistration(e){this._registration=e,this._registrationChanged.emit(this._registration)}}const v=new o.Token("@datalayer/jupyterlite-session:ISessions");var y=s(46931);class f{constructor(e){this._sessions=[],this._kernels=e.kernels}async get(e){const t=this._sessions.find((t=>t.id===e));if(!t)throw Error(`Session ${e} not found`);return t}async list(){return this._sessions}async patch(e){const{id:t,path:s,name:r}=e,n=this._sessions.findIndex((e=>e.id===t)),i=this._sessions[n];if(!i)throw Error(`Session ${t} not found`);const a={...i,path:null!=s?s:i.path,name:null!=r?r:i.name};return this._sessions[n]=a,a}async startNew(e){var t,s,n;const{path:i,name:a}=e,l=this._sessions.find((e=>e.name===a));if(l)return l;const c=null!==(s=null===(t=e.kernel)||void 0===t?void 0:t.name)&&void 0!==s?s:"",u=null!==(n=e.id)&&void 0!==n?n:o.UUID.uuid4(),d=await this._kernels.startNew({id:u,name:c,location:r.PathExt.dirname(e.path)}),g={id:u,path:i,name:null!=a?a:i,type:"notebook",kernel:{id:d.id,name:d.name}};return this._sessions.push(g),g}async shutdown(e){var t;const s=this._sessions.find((t=>t.id===e));if(!s)throw Error(`Session ${e} not found`);const r=null===(t=s.kernel)||void 0===t?void 0:t.id;r&&await this._kernels.shutdown(r),y.RO.removeFirstOf(this._sessions,s)}}const w=new o.Token("@datalayer/jupyterlite-settings:ISettings");var _=s(42824);const k="JupyterLite Storage";class m{constructor(e){this._storageName=k,this._storageDrivers=null,this._localforage=e.localforage,this._storageName=e.storageName||k,this._storageDrivers=e.storageDrivers||null,this._ready=new o.PromiseDelegate}get ready(){return this._ready.promise}get storage(){return this.ready.then((()=>this._storage))}async initialize(){await this.initStorage(),this._ready.resolve(void 0)}async initStorage(){this._storage=this.defaultSettingsStorage()}get defaultStorageOptions(){var e;const t=(null===(e=this._storageDrivers)||void 0===e?void 0:e.length)?this._storageDrivers:null;return{version:1,name:this._storageName,...t?{driver:t}:{}}}defaultSettingsStorage(){return this._localforage.createInstance({description:"Offline Storage for Settings",storeName:"settings",...this.defaultStorageOptions})}async get(e){let t=(await this.getAll()).settings.find((t=>t.id===e));return t||(t=await this._getFederated(e)),t}async getAll(){var e;const t=null!==(e=r.PageConfig.getOption("settingsUrl"))&&void 0!==e?e:"/",s=await this.storage,n=await(await fetch(r.URLExt.join(t,"all.json"))).json(),i=await Promise.all(n.map((async e=>{var t;const{id:r}=e,n=null!==(t=await s.getItem(r))&&void 0!==t?t:e.raw;return{...S.override(e),raw:n,settings:_.parse(n)}})));return{settings:i}}async save(e,t){await(await this.storage).setItem(e,t)}async _getFederated(e){var t;const[s,n]=e.split(":");if(!S.isFederated(s))return;const i=r.PageConfig.getOption("fullLabextensionsUrl"),a=r.URLExt.join(i,s,"schemas",s,`${n}.json`),o=r.URLExt.join(i,s,"package.json"),l=await(await fetch(a)).json(),c=await(await fetch(o)).json(),u=null!==(t=await(await this.storage).getItem(e))&&void 0!==t?t:"{}",d=_.parse(u)||{};return S.override({id:e,raw:u,schema:l,settings:d,version:c.version||"3.0.8"})}}var S;!function(e){const t=JSON.parse(r.PageConfig.getOption("settingsOverrides")||"{}");e.isFederated=function(e){let t;try{t=JSON.parse(r.PageConfig.getOption("federated_extensions"))}catch{return!1}for(const{name:s}of t)if(s===e)return!0;return!1},e.override=function(e){if(t[e.id]){e.schema.properties||(e.schema.properties={});for(const[s,r]of Object.entries(t[e.id]||{}))e.schema.properties[s].default=r}return e}}(S||(S={}));var j=s(62243),O=s.n(j);const N={id:"@datalayer/jupyterlite-server-extension:service-worker",autoStart:!0,provides:g.g,activate:e=>new p},R={id:"@datalayer/jupyterlite-server-extension:settings-routes",autoStart:!0,requires:[w],activate:(e,t)=>{const s="/api/settings/((?:@([^/]+?)[/])?([^/]+?):([^:]+))$";e.router.get(s,(async(e,s)=>{const r=await t.get(s);return new Response(JSON.stringify(r))})),e.router.put(s,(async(e,s)=>{const r=e.body,{raw:n}=r;return await t.save(s,n),new Response(null,{status:204})})),e.router.get("/api/settings",(async e=>{const s=await t.getAll();return new Response(JSON.stringify(s))}))}},C=[{id:"@datalayer/jupyterlite-server-extension:kernels",autoStart:!0,provides:n.Ll,requires:[n.qP],activate:(e,t)=>new u({kernelspecs:t})},{id:"@datalayer/jupyterlite-server-extension:kernels-routes",autoStart:!0,requires:[n.Ll],activate:(e,t)=>{e.router.post("/api/kernels/(.*)/restart",(async(e,s)=>{const r=await t.restart(s);return new Response(JSON.stringify(r))})),e.router.delete("/api/kernels/(.*)",(async(e,s)=>{const r=await t.shutdown(s);return new Response(JSON.stringify(r),{status:204})}))}},{id:"@datalayer/jupyterlite-server-extension:kernelspec",autoStart:!0,provides:n.qP,activate:e=>new d},{id:"@datalayer/jupyterlite-server-extension:kernelspec-routes",autoStart:!0,requires:[n.qP],activate:(e,t)=>{e.router.get("/api/kernelspecs",(async e=>{const{specs:s}=t;if(!s)return new Response(null);const r={},n=s.kernelspecs;Object.keys(n).forEach((e=>{const t=n[e],{resources:s}=null!=t?t:{};r[e]={name:e,spec:t,resources:s}}));const i={default:s.default,kernelspecs:r};return new Response(JSON.stringify(i))}))}},{id:"@datalayer/jupyterlite-server-extension:nbconvert-routes",autoStart:!0,activate:e=>{e.router.get("/api/nbconvert",(async e=>new Response(JSON.stringify({}))))}},N,{id:"@datalayer/jupyterlite-server-extension:sessions",autoStart:!0,provides:v,requires:[n.Ll],activate:(e,t)=>new f({kernels:t})},{id:"@datalayer/jupyterlite-server-extension:sessions-routes",autoStart:!0,requires:[v],activate:(e,t)=>{e.router.get("/api/sessions/(.+)",(async(e,s)=>{const r=await t.get(s);return new Response(JSON.stringify(r),{status:200})})),e.router.get("/api/sessions",(async e=>{const s=await t.list();return new Response(JSON.stringify(s),{status:200})})),e.router.patch("/api/sessions(.*)",(async(e,s)=>{const r=e.body,n=await t.patch(r);return new Response(JSON.stringify(n),{status:200})})),e.router.delete("/api/sessions/(.+)",(async(e,s)=>(await t.shutdown(s),new Response(null,{status:204})))),e.router.post("/api/sessions",(async e=>{const s=e.body,r=await t.startNew(s);return new Response(JSON.stringify(r),{status:201})}))}},{id:"@datalayer/jupyterlite-server-extension:settings",autoStart:!0,requires:[],provides:w,activate:e=>{const t=r.PageConfig.getOption("settingsStorageName"),s=JSON.parse(r.PageConfig.getOption("settingsStorageDrivers")||"null"),n=new m({storageName:t,storageDrivers:s,localforage:O()});return e.started.then((()=>n.initialize().catch(console.warn))),n}},R]},16519:(e,t,s)=>{s.d(t,{g:()=>r});const r=new(s(47963).Token)("@datalayer/jupyterlite-server-extension:IServiceWorkerRegistrationWrapper")}}]);