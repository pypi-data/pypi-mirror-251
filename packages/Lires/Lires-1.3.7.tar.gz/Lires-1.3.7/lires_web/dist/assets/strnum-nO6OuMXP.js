const o=/^[-+]?0x[a-fA-F0-9]+$/,c=/^([\-\+])?(0*)(\.[0-9]+([eE]\-?[0-9]+)?|[0-9]+(\.[0-9]+([eE]\-?[0-9]+)?)?)$/;!Number.parseInt&&window.parseInt&&(Number.parseInt=window.parseInt);!Number.parseFloat&&window.parseFloat&&(Number.parseFloat=window.parseFloat);const d={hex:!0,leadingZeros:!0,decimalPoint:".",eNotation:!0};function g(e,n={}){if(n=Object.assign({},d,n),!e||typeof e!="string")return e;let r=e.trim();if(n.skipLike!==void 0&&n.skipLike.test(r))return e;if(n.hex&&o.test(r))return Number.parseInt(r,16);{const s=c.exec(r);if(s){const l=s[1],a=s[2];let f=N(s[3]);const u=s[4]||s[6];if(!n.leadingZeros&&a.length>0&&l&&r[2]!==".")return e;if(!n.leadingZeros&&a.length>0&&!l&&r[1]!==".")return e;{const i=Number(r),t=""+i;return t.search(/[eE]/)!==-1||u?n.eNotation?i:e:r.indexOf(".")!==-1?t==="0"&&f===""||t===f||l&&t==="-"+f?i:e:a?f===t||l+f===t?i:e:r===t||r===l+t?i:e}}else return e}}function N(e){return e&&e.indexOf(".")!==-1&&(e=e.replace(/0+$/,""),e==="."?e="0":e[0]==="."?e="0"+e:e[e.length-1]==="."&&(e=e.substr(0,e.length-1))),e}var x=g;export{x as s};
