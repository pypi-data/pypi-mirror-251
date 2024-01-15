"use strict";(self.webpackChunk_datalayer_jupyter_kernels=self.webpackChunk_datalayer_jupyter_kernels||[]).push([[1292],{87366:(o,e,n)=>{n.d(e,{Z:()=>p});var r=n(64481),a=n.n(r),t=n(9103),l=a()((function(o){return o[1]}));l.i(t.Z),l.push([o.id,"/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n/* Set the default typography for monospace elements */\ntt,\ncode,\nkbd,\nsamp,\npre {\n  font-family: var(--jp-code-font-family);\n  font-size: var(--jp-code-font-size);\n  line-height: var(--jp-code-line-height);\n}\n\n/* fix illegible yellow backround in exception stacktrace */\n:where(\n    .jp-RenderedText[data-mime-type='application/vnd.jupyter.stderr']\n      pre\n      .ansi-yellow-bg\n  ) {\n  color: black;\n}\n",""]);const p=l},9103:(o,e,n)=>{n.d(e,{Z:()=>t});var r=n(64481),a=n.n(r)()((function(o){return o[1]}));a.push([o.id,"/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n/*\nThe following CSS variables define the main, public API for styling JupyterLab.\nThese variables should be used by all plugins wherever possible. In other\nwords, plugins should not define custom colors, sizes, etc unless absolutely\nnecessary. This enables users to change the visual theme of JupyterLab\nby changing these variables.\n\nMany variables appear in an ordered sequence (0,1,2,3). These sequences\nare designed to work well together, so for example, `--jp-border-color1` should\nbe used with `--jp-layout-color1`. The numbers have the following meanings:\n\n* 0: super-primary, reserved for special emphasis\n* 1: primary, most important under normal situations\n* 2: secondary, next most important under normal situations\n* 3: tertiary, next most important under normal situations\n\nThroughout JupyterLab, we are mostly following principles from Google's\nMaterial Design when selecting colors. We are not, however, following\nall of MD as it is not optimized for dense, information rich UIs.\n*/\n\n:root {\n  /* Elevation\n   *\n   * We style box-shadows using Material Design's idea of elevation. These particular numbers are taken from here:\n   *\n   * https://github.com/material-components/material-components-web\n   * https://material-components-web.appspot.com/elevation.html\n   */\n\n  /* The dark theme shadows need a bit of work, but this will probably also require work on the core layout\n   * colors used in the theme as well. */\n  --jp-shadow-base-lightness: 32;\n  --jp-shadow-umbra-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.2\n  );\n  --jp-shadow-penumbra-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.14\n  );\n  --jp-shadow-ambient-color: rgba(\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    var(--jp-shadow-base-lightness),\n    0.12\n  );\n  --jp-elevation-z0: none;\n  --jp-elevation-z1: 0 2px 1px -1px var(--jp-shadow-umbra-color),\n    0 1px 1px 0 var(--jp-shadow-penumbra-color),\n    0 1px 3px 0 var(--jp-shadow-ambient-color);\n  --jp-elevation-z2: 0 3px 1px -2px var(--jp-shadow-umbra-color),\n    0 2px 2px 0 var(--jp-shadow-penumbra-color),\n    0 1px 5px 0 var(--jp-shadow-ambient-color);\n  --jp-elevation-z4: 0 2px 4px -1px var(--jp-shadow-umbra-color),\n    0 4px 5px 0 var(--jp-shadow-penumbra-color),\n    0 1px 10px 0 var(--jp-shadow-ambient-color);\n  --jp-elevation-z6: 0 3px 5px -1px var(--jp-shadow-umbra-color),\n    0 6px 10px 0 var(--jp-shadow-penumbra-color),\n    0 1px 18px 0 var(--jp-shadow-ambient-color);\n  --jp-elevation-z8: 0 5px 5px -3px var(--jp-shadow-umbra-color),\n    0 8px 10px 1px var(--jp-shadow-penumbra-color),\n    0 3px 14px 2px var(--jp-shadow-ambient-color);\n  --jp-elevation-z12: 0 7px 8px -4px var(--jp-shadow-umbra-color),\n    0 12px 17px 2px var(--jp-shadow-penumbra-color),\n    0 5px 22px 4px var(--jp-shadow-ambient-color);\n  --jp-elevation-z16: 0 8px 10px -5px var(--jp-shadow-umbra-color),\n    0 16px 24px 2px var(--jp-shadow-penumbra-color),\n    0 6px 30px 5px var(--jp-shadow-ambient-color);\n  --jp-elevation-z20: 0 10px 13px -6px var(--jp-shadow-umbra-color),\n    0 20px 31px 3px var(--jp-shadow-penumbra-color),\n    0 8px 38px 7px var(--jp-shadow-ambient-color);\n  --jp-elevation-z24: 0 11px 15px -7px var(--jp-shadow-umbra-color),\n    0 24px 38px 3px var(--jp-shadow-penumbra-color),\n    0 9px 46px 8px var(--jp-shadow-ambient-color);\n\n  /* Borders\n   *\n   * The following variables, specify the visual styling of borders in JupyterLab.\n   */\n\n  --jp-border-width: 1px;\n  --jp-border-color0: var(--md-grey-700);\n  --jp-border-color1: var(--md-grey-700);\n  --jp-border-color2: var(--md-grey-800);\n  --jp-border-color3: var(--md-grey-900);\n  --jp-inverse-border-color: var(--md-grey-600);\n  --jp-border-radius: 2px;\n\n  /* UI Fonts\n   *\n   * The UI font CSS variables are used for the typography all of the JupyterLab\n   * user interface elements that are not directly user generated content.\n   *\n   * The font sizing here is done assuming that the body font size of --jp-ui-font-size1\n   * is applied to a parent element. When children elements, such as headings, are sized\n   * in em all things will be computed relative to that body size.\n   */\n\n  --jp-ui-font-scale-factor: 1.2;\n  --jp-ui-font-size0: 0.83333em;\n  --jp-ui-font-size1: 13px; /* Base font size */\n  --jp-ui-font-size2: 1.2em;\n  --jp-ui-font-size3: 1.44em;\n  --jp-ui-font-family: system-ui, -apple-system, blinkmacsystemfont, 'Segoe UI',\n    helvetica, arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji',\n    'Segoe UI Symbol';\n\n  /*\n   * Use these font colors against the corresponding main layout colors.\n   * In a light theme, these go from dark to light.\n   */\n\n  /* Defaults use Material Design specification */\n  --jp-ui-font-color0: rgba(255, 255, 255, 1);\n  --jp-ui-font-color1: rgba(255, 255, 255, 0.87);\n  --jp-ui-font-color2: rgba(255, 255, 255, 0.54);\n  --jp-ui-font-color3: rgba(255, 255, 255, 0.38);\n\n  /*\n   * Use these against the brand/accent/warn/error colors.\n   * These will typically go from light to darker, in both a dark and light theme.\n   */\n\n  --jp-ui-inverse-font-color0: rgba(0, 0, 0, 1);\n  --jp-ui-inverse-font-color1: rgba(0, 0, 0, 0.8);\n  --jp-ui-inverse-font-color2: rgba(0, 0, 0, 0.5);\n  --jp-ui-inverse-font-color3: rgba(0, 0, 0, 0.3);\n\n  /* Content Fonts\n   *\n   * Content font variables are used for typography of user generated content.\n   *\n   * The font sizing here is done assuming that the body font size of --jp-content-font-size1\n   * is applied to a parent element. When children elements, such as headings, are sized\n   * in em all things will be computed relative to that body size.\n   */\n\n  --jp-content-line-height: 1.6;\n  --jp-content-font-scale-factor: 1.2;\n  --jp-content-font-size0: 0.83333em;\n  --jp-content-font-size1: 14px; /* Base font size */\n  --jp-content-font-size2: 1.2em;\n  --jp-content-font-size3: 1.44em;\n  --jp-content-font-size4: 1.728em;\n  --jp-content-font-size5: 2.0736em;\n\n  /* This gives a magnification of about 125% in presentation mode over normal. */\n  --jp-content-presentation-font-size1: 17px;\n  --jp-content-heading-line-height: 1;\n  --jp-content-heading-margin-top: 1.2em;\n  --jp-content-heading-margin-bottom: 0.8em;\n  --jp-content-heading-font-weight: 500;\n\n  /* Defaults use Material Design specification */\n  --jp-content-font-color0: rgba(255, 255, 255, 1);\n  --jp-content-font-color1: rgba(255, 255, 255, 1);\n  --jp-content-font-color2: rgba(255, 255, 255, 0.7);\n  --jp-content-font-color3: rgba(255, 255, 255, 0.5);\n  --jp-content-link-color: var(--md-blue-300);\n  --jp-content-font-family: system-ui, -apple-system, blinkmacsystemfont,\n    'Segoe UI', helvetica, arial, sans-serif, 'Apple Color Emoji',\n    'Segoe UI Emoji', 'Segoe UI Symbol';\n\n  /*\n   * Code Fonts\n   *\n   * Code font variables are used for typography of code and other monospaces content.\n   */\n\n  --jp-code-font-size: 13px;\n  --jp-code-line-height: 1.3077; /* 17px for 13px base */\n  --jp-code-padding: 5px; /* 5px for 13px base, codemirror highlighting needs integer px value */\n  --jp-code-font-family-default: menlo, consolas, 'DejaVu Sans Mono', monospace;\n  --jp-code-font-family: var(--jp-code-font-family-default);\n\n  /* This gives a magnification of about 125% in presentation mode over normal. */\n  --jp-code-presentation-font-size: 16px;\n\n  /* may need to tweak cursor width if you change font size */\n  --jp-code-cursor-width0: 1.4px;\n  --jp-code-cursor-width1: 2px;\n  --jp-code-cursor-width2: 4px;\n\n  /* Layout\n   *\n   * The following are the main layout colors use in JupyterLab. In a light\n   * theme these would go from light to dark.\n   */\n\n  --jp-layout-color0: #111;\n  --jp-layout-color1: var(--md-grey-900);\n  --jp-layout-color2: var(--md-grey-800);\n  --jp-layout-color3: var(--md-grey-700);\n  --jp-layout-color4: var(--md-grey-600);\n\n  /* Inverse Layout\n   *\n   * The following are the inverse layout colors use in JupyterLab. In a light\n   * theme these would go from dark to light.\n   */\n\n  --jp-inverse-layout-color0: white;\n  --jp-inverse-layout-color1: white;\n  --jp-inverse-layout-color2: var(--md-grey-200);\n  --jp-inverse-layout-color3: var(--md-grey-400);\n  --jp-inverse-layout-color4: var(--md-grey-600);\n\n  /* Brand/accent */\n\n  --jp-brand-color0: var(--md-blue-700);\n  --jp-brand-color1: var(--md-blue-500);\n  --jp-brand-color2: var(--md-blue-300);\n  --jp-brand-color3: var(--md-blue-100);\n  --jp-brand-color4: var(--md-blue-50);\n  --jp-accent-color0: var(--md-green-700);\n  --jp-accent-color1: var(--md-green-500);\n  --jp-accent-color2: var(--md-green-300);\n  --jp-accent-color3: var(--md-green-100);\n\n  /* State colors (warn, error, success, info) */\n\n  --jp-warn-color0: var(--md-orange-700);\n  --jp-warn-color1: var(--md-orange-500);\n  --jp-warn-color2: var(--md-orange-300);\n  --jp-warn-color3: var(--md-orange-100);\n  --jp-error-color0: var(--md-red-700);\n  --jp-error-color1: var(--md-red-500);\n  --jp-error-color2: var(--md-red-300);\n  --jp-error-color3: var(--md-red-100);\n  --jp-success-color0: var(--md-green-700);\n  --jp-success-color1: var(--md-green-500);\n  --jp-success-color2: var(--md-green-300);\n  --jp-success-color3: var(--md-green-100);\n  --jp-info-color0: var(--md-cyan-700);\n  --jp-info-color1: var(--md-cyan-500);\n  --jp-info-color2: var(--md-cyan-300);\n  --jp-info-color3: var(--md-cyan-100);\n\n  /* Cell specific styles */\n\n  --jp-cell-padding: 5px;\n  --jp-cell-collapser-width: 8px;\n  --jp-cell-collapser-min-height: 20px;\n  --jp-cell-collapser-not-active-hover-opacity: 0.6;\n  --jp-cell-editor-background: var(--jp-layout-color1);\n  --jp-cell-editor-border-color: var(--md-grey-700);\n  --jp-cell-editor-box-shadow: inset 0 0 2px var(--md-blue-300);\n  --jp-cell-editor-active-background: var(--jp-layout-color0);\n  --jp-cell-editor-active-border-color: var(--jp-brand-color1);\n  --jp-cell-prompt-width: 64px;\n  --jp-cell-prompt-font-family: var(--jp-code-font-family-default);\n  --jp-cell-prompt-letter-spacing: 0;\n  --jp-cell-prompt-opacity: 1;\n  --jp-cell-prompt-not-active-opacity: 1;\n  --jp-cell-prompt-not-active-font-color: var(--md-grey-300);\n\n  /* A custom blend of MD grey and blue 600\n   * See https://meyerweb.com/eric/tools/color-blend/#546E7A:1E88E5:5:hex */\n  --jp-cell-inprompt-font-color: #307fc1;\n\n  /* A custom blend of MD grey and orange 600\n   * https://meyerweb.com/eric/tools/color-blend/#546E7A:F4511E:5:hex */\n  --jp-cell-outprompt-font-color: #bf5b3d;\n\n  /* Notebook specific styles */\n\n  --jp-notebook-padding: 10px;\n  --jp-notebook-select-background: var(--jp-layout-color1);\n  --jp-notebook-multiselected-color: rgba(33, 150, 243, 0.24);\n\n  /* The scroll padding is calculated to fill enough space at the bottom of the\n  notebook to show one single-line cell (with appropriate padding) at the top\n  when the notebook is scrolled all the way to the bottom. We also subtract one\n  pixel so that no scrollbar appears if we have just one single-line cell in the\n  notebook. This padding is to enable a 'scroll past end' feature in a notebook.\n  */\n  --jp-notebook-scroll-padding: calc(\n    100% - var(--jp-code-font-size) * var(--jp-code-line-height) -\n      var(--jp-code-padding) - var(--jp-cell-padding) - 1px\n  );\n\n  /* Rendermime styles */\n\n  --jp-rendermime-error-background: rgba(244, 67, 54, 0.28);\n  --jp-rendermime-table-row-background: var(--md-grey-900);\n  --jp-rendermime-table-row-hover-background: rgba(3, 169, 244, 0.2);\n\n  /* Dialog specific styles */\n\n  --jp-dialog-background: rgba(0, 0, 0, 0.6);\n\n  /* Console specific styles */\n\n  --jp-console-padding: 10px;\n\n  /* Toolbar specific styles */\n\n  --jp-toolbar-border-color: var(--jp-border-color2);\n  --jp-toolbar-micro-height: 8px;\n  --jp-toolbar-background: var(--jp-layout-color1);\n  --jp-toolbar-box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.8);\n  --jp-toolbar-header-margin: 4px 4px 0 4px;\n  --jp-toolbar-active-background: var(--jp-layout-color0);\n\n  /* Statusbar specific styles */\n\n  --jp-statusbar-height: 24px;\n\n  /* Input field styles */\n\n  --jp-input-box-shadow: inset 0 0 2px var(--md-blue-300);\n  --jp-input-active-background: var(--jp-layout-color0);\n  --jp-input-hover-background: var(--jp-layout-color2);\n  --jp-input-background: var(--md-grey-800);\n  --jp-input-border-color: var(--jp-inverse-border-color);\n  --jp-input-active-border-color: var(--jp-brand-color1);\n  --jp-input-active-box-shadow-color: rgba(19, 124, 189, 0.3);\n\n  /* General editor styles */\n\n  --jp-editor-selected-background: var(--jp-layout-color2);\n  --jp-editor-selected-focused-background: rgba(33, 150, 243, 0.24);\n  --jp-editor-cursor-color: var(--jp-ui-font-color0);\n\n  /* Code mirror specific styles */\n\n  --jp-mirror-editor-keyword-color: var(--md-green-500);\n  --jp-mirror-editor-atom-color: var(--md-blue-300);\n  --jp-mirror-editor-number-color: var(--md-green-400);\n  --jp-mirror-editor-def-color: var(--md-blue-600);\n  --jp-mirror-editor-variable-color: var(--md-grey-300);\n  --jp-mirror-editor-variable-2-color: var(--md-blue-500);\n  --jp-mirror-editor-variable-3-color: var(--md-green-600);\n  --jp-mirror-editor-punctuation-color: var(--md-blue-400);\n  --jp-mirror-editor-property-color: var(--md-blue-400);\n  --jp-mirror-editor-operator-color: #a2f;\n  --jp-mirror-editor-comment-color: #408080;\n  --jp-mirror-editor-string-color: #ff7070;\n  --jp-mirror-editor-string-2-color: var(--md-purple-300);\n  --jp-mirror-editor-meta-color: #a2f;\n  --jp-mirror-editor-qualifier-color: #555;\n  --jp-mirror-editor-builtin-color: var(--md-green-600);\n  --jp-mirror-editor-bracket-color: #997;\n  --jp-mirror-editor-tag-color: var(--md-green-700);\n  --jp-mirror-editor-attribute-color: var(--md-blue-700);\n  --jp-mirror-editor-header-color: var(--md-blue-500);\n  --jp-mirror-editor-quote-color: var(--md-green-300);\n  --jp-mirror-editor-link-color: var(--md-blue-700);\n  --jp-mirror-editor-error-color: #f00;\n  --jp-mirror-editor-hr-color: #999;\n\n  /*\n    RTC user specific colors.\n    These colors are used for the cursor, username in the editor,\n    and the icon of the user.\n  */\n\n  --jp-collaborator-color1: #ad4a00;\n  --jp-collaborator-color2: #7b6a00;\n  --jp-collaborator-color3: #007e00;\n  --jp-collaborator-color4: #008772;\n  --jp-collaborator-color5: #0079b9;\n  --jp-collaborator-color6: #8b45c6;\n  --jp-collaborator-color7: #be208b;\n\n  /* Vega extension styles */\n\n  --jp-vega-background: var(--md-grey-400);\n\n  /* Sidebar-related styles */\n\n  --jp-sidebar-min-width: 250px;\n\n  /* Search-related styles */\n\n  --jp-search-toggle-off-opacity: 0.6;\n  --jp-search-toggle-hover-opacity: 0.8;\n  --jp-search-toggle-on-opacity: 1;\n  --jp-search-selected-match-background-color: rgb(255, 225, 0);\n  --jp-search-selected-match-color: black;\n  --jp-search-unselected-match-background-color: var(\n    --jp-inverse-layout-color0\n  );\n  --jp-search-unselected-match-color: var(--jp-ui-inverse-font-color0);\n\n  /* scrollbar related styles. Supports every browser except Edge. */\n\n  /* colors based on JetBrain's Darcula theme */\n\n  --jp-scrollbar-background-color: #3f4244;\n  --jp-scrollbar-thumb-color: 88, 96, 97; /* need to specify thumb color as an RGB triplet */\n  --jp-scrollbar-endpad: 3px; /* the minimum gap between the thumb and the ends of a scrollbar */\n\n  /* hacks for setting the thumb shape. These do nothing in Firefox */\n\n  --jp-scrollbar-thumb-margin: 3.5px; /* the space in between the sides of the thumb and the track */\n  --jp-scrollbar-thumb-radius: 9px; /* set to a large-ish value for rounded endcaps on the thumb */\n\n  /* Icon colors that work well with light or dark backgrounds */\n  --jp-icon-contrast-color0: var(--md-purple-600);\n  --jp-icon-contrast-color1: var(--md-green-600);\n  --jp-icon-contrast-color2: var(--md-pink-600);\n  --jp-icon-contrast-color3: var(--md-blue-600);\n\n  /* Button colors */\n  --jp-accept-color-normal: var(--md-blue-700);\n  --jp-accept-color-hover: var(--md-blue-800);\n  --jp-accept-color-active: var(--md-blue-900);\n  --jp-warn-color-normal: var(--md-red-700);\n  --jp-warn-color-hover: var(--md-red-800);\n  --jp-warn-color-active: var(--md-red-900);\n  --jp-reject-color-normal: var(--md-grey-600);\n  --jp-reject-color-hover: var(--md-grey-700);\n  --jp-reject-color-active: var(--md-grey-800);\n\n  /* File or activity icons and switch semantic variables */\n  --jp-jupyter-icon-color: #f37626;\n  --jp-notebook-icon-color: #f37626;\n  --jp-json-icon-color: var(--md-orange-500);\n  --jp-console-icon-background-color: var(--md-blue-500);\n  --jp-console-icon-color: white;\n  --jp-terminal-icon-background-color: var(--md-grey-200);\n  --jp-terminal-icon-color: var(--md-grey-800);\n  --jp-text-editor-icon-color: var(--md-grey-200);\n  --jp-inspector-icon-color: var(--md-grey-200);\n  --jp-switch-color: var(--md-grey-400);\n  --jp-switch-true-position-color: var(--md-orange-700);\n}\n",""]);const t=a},81292:(o,e,n)=>{n.r(e),n.d(e,{default:()=>l});var r=n(93379),a=n.n(r),t=n(87366);a()(t.Z,{insert:"head",singleton:!1});const l=t.Z.locals||{}}}]);