"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[8464],{8464:(e,t,l)=>{l.r(t),l.d(t,{default:()=>g});var a=l(5872),n=l.n(a),u=l(78580),s=l.n(u),o=l(55786),r=l(10581),i=l(55867),h=l(67294),c=l(4715),d=l(74448),v=l(11965);function g(e){var t;const{data:l,formData:a,height:u,width:g,setDataMask:m,setHoveredFilter:p,unsetHoveredFilter:f,setFocusedFilter:b,unsetFocusedFilter:w,setFilterActive:F,filterState:S,inputRef:Z}=e,{defaultValue:k,multiSelect:C}=a,[M,x]=(0,h.useState)(null!=k?k:[]),y=e=>{const t=(0,o.Z)(e);x(t);const l={};t.length&&(l.interactive_groupby=t),m({filterState:{value:t.length?t:null},extraFormData:l})};(0,h.useEffect)((()=>{y(S.value)}),[JSON.stringify(S.value),C]),(0,h.useEffect)((()=>{y(null!=k?k:null)}),[JSON.stringify(k),C]);const D=(0,o.Z)(a.groupby).map(r.Z),$=null!=(t=D[0])&&t.length?D[0]:null,_=$?l.filter((e=>s()($).call($,e.column_name))):l,A=l?_:[],E=0===A.length?(0,i.t)("No columns"):(0,i.tn)("%s option","%s options",A.length,A.length),K={};S.validateMessage&&(K.extra=(0,v.tZ)(d.Am,{status:S.validateStatus},S.validateMessage));const N=A.map((e=>{const{column_name:t,verbose_name:l}=e;return{label:null!=l?l:t,value:t}}));return(0,v.tZ)(d.un,{height:u,width:g},(0,v.tZ)(d.jp,n()({validateStatus:S.validateStatus},K),(0,v.tZ)(c.Ph,{allowClear:!0,value:M,placeholder:E,mode:C?"multiple":void 0,onChange:y,onBlur:w,onFocus:b,onMouseEnter:p,onMouseLeave:f,ref:Z,options:N,onDropdownVisibleChange:F})))}},74448:(e,t,l)=>{l.d(t,{Am:()=>r,h2:()=>u,jp:()=>o,un:()=>s});var a=l(51995),n=l(4591);const u=0,s=a.iK.div`
  min-height: ${e=>{let{height:t}=e;return t}}px;
  width: ${e=>{let{width:t}=e;return t===u?"100%":`${t}px`}};
`,o=(0,a.iK)(n.Z)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,r=a.iK.div`
  color: ${e=>{var t;let{theme:l,status:a="error"}=e;return null==(t=l.colors[a])?void 0:t.base}};
`}}]);
//# sourceMappingURL=db7f84692be7d95f464c.chunk.js.map