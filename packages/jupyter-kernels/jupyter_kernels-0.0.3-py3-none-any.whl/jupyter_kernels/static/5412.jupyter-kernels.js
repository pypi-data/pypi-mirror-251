"use strict";(self.webpackChunk_datalayer_jupyter_kernels=self.webpackChunk_datalayer_jupyter_kernels||[]).push([[5412],{25412:(e,r,t)=>{t.r(r),t.d(r,{default:()=>i});var n=t(56276);class s{constructor(){this._renderers={}}addRenderer(e,r){if(this._renderers[e])throw new Error(`A renderer with id '${e}' is already registered.`);if(!r.fieldRenderer&&!r.widgetRenderer)throw new Error(`The component for '${e}' cannot be registered as it does not define 'fieldRenderer' nor 'widgetRenderer'.`);const t=e.lastIndexOf("."),n=e.substring(0,t),s=e.substring(t+1);if(0==n.length||0==s.length)throw new Error(`Form renderer id must follows the structure '<ISettingRegistry.IPlugin.id>.<propertyName>'; got ${e}.`);this._renderers[e]=r}get renderers(){return this._renderers}getRenderer(e){return this._renderers[e]}}const i=[{id:"@jupyterlab/ui-components-extension:labicon-manager",description:"Provides the icon manager.",provides:n.E,autoStart:!0,activate:e=>Object.create(null)},{id:"@jupyterlab/ui-components-extension:form-renderer-registry",description:"Provides the settings form renderer registry.",provides:n.C,autoStart:!0,activate:e=>new s}]},56276:(e,r,t)=>{t.d(r,{C:()=>s,E:()=>i});var n=t(47963);const s=new n.Token("@jupyterlab/ui-components:IFormRendererRegistry","A service for settings form renderer registration."),i=new n.Token("@jupyterlab/ui-components:ILabIconManager","A service to register and request icons.")}}]);