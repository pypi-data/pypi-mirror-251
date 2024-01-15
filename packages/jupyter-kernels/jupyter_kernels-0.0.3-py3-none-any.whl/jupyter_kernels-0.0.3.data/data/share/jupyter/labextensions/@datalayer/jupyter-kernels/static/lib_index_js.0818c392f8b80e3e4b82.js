"use strict";
(self["webpackChunk_datalayer_jupyter_kernels"] = self["webpackChunk_datalayer_jupyter_kernels"] || []).push([["lib_index_js"],{

/***/ "./lib/KernelsJupyterLab.js":
/*!**********************************!*\
  !*** ./lib/KernelsJupyterLab.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelsJupyterLab": () => (/* binding */ KernelsJupyterLab),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @datalayer/jupyter-react */ "webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/theme-light-extension */ "webpack/sharing/consume/default/@jupyterlab/theme-light-extension");
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyter/collaboration-extension */ "../../../node_modules/@jupyter/collaboration-extension/lib/index.js");
/* harmony import */ var _jupyterlab_index__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./jupyterlab/index */ "./lib/jupyterlab/index.js");





const JupyterLabComponent = () => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__.JupyterLabApp, { extensions: [_jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__, _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_3__, _jupyterlab_index__WEBPACK_IMPORTED_MODULE_4__], disabledExtensions: [
    //      "@jupyterlab/apputils-extension:sessionDialogs"
    ], position: "absolute", height: "100vh" }));
const KernelsJupyterLab = () => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__.Jupyter, { jupyterServerHttpUrl: "https://dev1-io.datalayer.run/jupyter/server/eric/default", jupyterServerWsUrl: "wss://dev1-io.datalayer.run/jupyter/server/eric/default", jupyterToken: "test", startDefaultKernel: false, disableCssLoading: true, collaborative: true, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(JupyterLabComponent, {}) }));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KernelsJupyterLab);


/***/ }),

/***/ "./lib/KernelsJupyterLabHeadless.js":
/*!******************************************!*\
  !*** ./lib/KernelsJupyterLabHeadless.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelsJupyterLabHeadless": () => (/* binding */ KernelsJupyterLabHeadless),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! styled-components */ "webpack/sharing/consume/default/styled-components/styled-components?16a2");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Kernels__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./Kernels */ "./lib/Kernels.js");



const ThemeGlobalStyle = styled_components__WEBPACK_IMPORTED_MODULE_1__.createGlobalStyle `
  body {
    background-color: white !important;
    overflow: auto;
  }
`;
const KernelsJupyterLabHeadless = () => {
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(ThemeGlobalStyle, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_Kernels__WEBPACK_IMPORTED_MODULE_2__["default"], {})] }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KernelsJupyterLabHeadless);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelsJupyterLab": () => (/* reexport safe */ _KernelsJupyterLab__WEBPACK_IMPORTED_MODULE_0__.KernelsJupyterLab),
/* harmony export */   "KernelsJupyterLabHeadless": () => (/* reexport safe */ _KernelsJupyterLabHeadless__WEBPACK_IMPORTED_MODULE_1__.KernelsJupyterLabHeadless),
/* harmony export */   "KernelsRoutes": () => (/* reexport safe */ _KernelsRoutes__WEBPACK_IMPORTED_MODULE_2__.KernelsRoutes)
/* harmony export */ });
/* harmony import */ var _KernelsJupyterLab__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./KernelsJupyterLab */ "./lib/KernelsJupyterLab.js");
/* harmony import */ var _KernelsJupyterLabHeadless__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./KernelsJupyterLabHeadless */ "./lib/KernelsJupyterLabHeadless.js");
/* harmony import */ var _KernelsRoutes__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./KernelsRoutes */ "./lib/KernelsRoutes.js");





/***/ })

}]);
//# sourceMappingURL=lib_index_js.0818c392f8b80e3e4b82.js.map