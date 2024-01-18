"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[4717],{79789:(e,t,i)=>{i.d(t,{Z:()=>c});var r=i(67294),l=i(51995),a=i(55867),n=i(70163),o=i(58593),s=i(11965);const c=function(e){let{certifiedBy:t,details:i,size:c="l"}=e;const d=(0,l.Fg)();return(0,s.tZ)(o.u,{id:"certified-details-tooltip",title:(0,s.tZ)(r.Fragment,null,t&&(0,s.tZ)("div",null,(0,s.tZ)("strong",null,(0,a.t)("Certified by %s",t))),(0,s.tZ)("div",null,i))},(0,s.tZ)(n.Z.Certified,{iconColor:d.colors.primary.base,iconSize:c}))}},17198:(e,t,i)=>{i.d(t,{Z:()=>p});var r=i(51995),l=i(55867),a=i(67294),n=i(9875),o=i(74069),s=i(49238),c=i(11965);const d=r.iK.div`
  padding-top: 8px;
  width: 50%;
  label {
    color: ${e=>{let{theme:t}=e;return t.colors.grayscale.base}};
    text-transform: uppercase;
  }
`,h=r.iK.div`
  line-height: ${e=>{let{theme:t}=e;return 4*t.gridUnit}}px;
  padding-top: 16px;
`;function p(e){let{description:t,onConfirm:i,onHide:r,open:p,title:u}=e;const[m,f]=(0,a.useState)(!0),[g,b]=(0,a.useState)(""),v=()=>{b(""),i()};return(0,c.tZ)(o.Z,{disablePrimaryButton:m,onHide:()=>{b(""),r()},onHandledPrimaryAction:v,primaryButtonName:(0,l.t)("delete"),primaryButtonType:"danger",show:p,title:u},(0,c.tZ)(h,null,t),(0,c.tZ)(d,null,(0,c.tZ)(s.lX,{htmlFor:"delete"},(0,l.t)('Type "%s" to confirm',(0,l.t)("DELETE"))),(0,c.tZ)(n.II,{type:"text",id:"delete",autoComplete:"off",value:g,onChange:e=>{var t;const i=null!=(t=e.target.value)?t:"";f(i.toUpperCase()!==(0,l.t)("DELETE")),b(i)},onPressEnter:()=>{m||v()}})))}},36674:(e,t,i)=>{i.d(t,{Z:()=>d});var r=i(67294),l=i(51995),a=i(11965),n=i(55867),o=i(58593),s=i(70163);const c=l.iK.a`
  ${e=>{let{theme:t}=e;return a.iv`
    font-size: ${t.typography.sizes.xl}px;
    display: flex;
    padding: 0 0 0 ${2*t.gridUnit}px;
  `}};
`,d=e=>{let{itemId:t,isStarred:i,showTooltip:l,saveFaveStar:d,fetchFaveStar:h}=e;(0,r.useEffect)((()=>{null==h||h(t)}),[h,t]);const p=(0,r.useCallback)((e=>{e.preventDefault(),d(t,!!i)}),[i,t,d]),u=(0,a.tZ)(c,{href:"#",onClick:p,className:"fave-unfave-icon",role:"button"},i?(0,a.tZ)(s.Z.FavoriteSelected,null):(0,a.tZ)(s.Z.FavoriteUnselected,null));return l?(0,a.tZ)(o.u,{id:"fave-unfave-tooltip",title:(0,n.t)("Click to favorite/unfavorite")},u):u}},4144:(e,t,i)=>{i.d(t,{Z:()=>d});var r=i(5872),l=i.n(r),a=i(67294),n=i(51995),o=i(68492),s=i(11965);const c=n.iK.div`
  background-image: url(${e=>{let{src:t}=e;return t}});
  background-size: cover;
  background-position: center ${e=>{let{position:t}=e;return t}};
  display: inline-block;
  height: calc(100% - 1px);
  width: calc(100% - 2px);
  margin: 1px 1px 0 1px;
`;function d(e){let{src:t,fallback:i,isLoading:r,position:n,...d}=e;const[h,p]=(0,a.useState)(i);return(0,a.useEffect)((()=>(t&&fetch(t).then((e=>e.blob())).then((e=>{if(/image/.test(e.type)){const t=URL.createObjectURL(e);p(t)}})).catch((e=>{o.Z.error(e),p(i)})),()=>{p(i)})),[t,i]),(0,s.tZ)(c,l()({src:r?i:h},d,{position:n}))}},60718:(e,t,i)=>{i.d(t,{m:()=>p});var r=i(31069),l=i(55867),a=i(15926),n=i.n(a),o=i(65108),s=i(98286);const c=new Map,d=(0,o.g)(r.Z.get,c,(e=>{let{endpoint:t}=e;return t||""})),h=e=>({value:e.name,label:e.name,key:e.name}),p=async(e,t,i)=>{const r="name",a=n().encode({filters:[{col:r,opr:"ct",value:e}],page:t,page_size:i,order_column:r,order_direction:"asc"});return d({endpoint:`/api/v1/tag/?q=${a}`}).then((e=>({data:e.json.result.filter((e=>1===e.type)).map(h),totalCount:e.json.count}))).catch((async e=>{const t=(e=>{let{error:t,message:i}=e,r=i||t||(0,l.t)("An error has occurred");return"Forbidden"===i&&(r=(0,l.t)("You do not have permission to read tags")),r})(await(0,s.O$)(e));throw new Error(t)}))}},20818:(e,t,i)=>{i.d(t,{Z:()=>J});var r=i(57557),l=i.n(r),a=i(78580),n=i.n(a),o=i(67294),s=i(9875),c=i(49238),d=i(51127),h=i.n(d),p=i(35932),u=i(4715),m=i(15926),f=i.n(m),g=i(51995),b=i(55867),v=i(81545),y=i(31069),F=i(55786),x=i(78161),Z=i(28062),C=i(93185),S=i(74069),k=i(94670),$=i(45697),w=i.n($),N=i(76787),T=i(11965);const I={onChange:w().func,labelMargin:w().number,colorScheme:w().string,hasCustomLabelColors:w().bool};class _ extends o.PureComponent{constructor(e){super(e),this.state={hovered:!1},this.categoricalSchemeRegistry=(0,v.Z)(),this.choices=this.categoricalSchemeRegistry.keys().map((e=>[e,e])),this.schemes=this.categoricalSchemeRegistry.getMap()}setHover(e){this.setState({hovered:e})}render(){const{colorScheme:e,labelMargin:t=0,hasCustomLabelColors:i}=this.props;return(0,T.tZ)(N.Z,{description:(0,b.t)("Any color palette selected here will override the colors applied to this dashboard's individual charts"),labelMargin:t,name:"color_scheme",onChange:this.props.onChange,value:e,choices:this.choices,clearable:!0,schemes:this.schemes,hovered:this.state.hovered,hasCustomLabelColors:i})}}_.propTypes=I,_.defaultProps={hasCustomLabelColors:!1,colorScheme:void 0,onChange:()=>{}};const j=_;var E=i(87999),O=i(98286),U=i(14114),M=i(48273),A=i(60718);const R=(0,g.iK)(c.xJ)`
  margin-bottom: 0;
`,q=(0,g.iK)(k.Ad)`
  border-radius: ${e=>{let{theme:t}=e;return t.borderRadius}}px;
  border: 1px solid ${e=>{let{theme:t}=e;return t.colors.secondary.light2}};
`;var D={name:"1blj7km",styles:"margin-top:1em"};const J=(0,U.ZP)((e=>{let{addSuccessToast:t,addDangerToast:i,colorScheme:r,dashboardId:a,dashboardInfo:d,dashboardTitle:m,onHide:g=(()=>{}),onlyApply:$=!1,onSubmit:w=(()=>{}),show:N=!1}=e;const[I]=u.qz.useForm(),[_,U]=(0,o.useState)(!1),[J,X]=(0,o.useState)(!1),[L,z]=(0,o.useState)(r),[B,K]=(0,o.useState)(""),[P,H]=(0,o.useState)(),[G,Y]=(0,o.useState)([]),[V,W]=(0,o.useState)([]),Q=$?(0,b.t)("Apply"):(0,b.t)("Save"),[ee,te]=(0,o.useState)([]),ie=(0,v.Z)(),re=(0,o.useMemo)((()=>ee.map((e=>({value:e.name,label:e.name,key:e.name})))),[ee.length]),le=async e=>{const{error:t,statusText:i,message:r}=await(0,O.O$)(e);let l=t||i||(0,b.t)("An error has occurred");"object"==typeof r&&"json_metadata"in r?l=r.json_metadata:"string"==typeof r&&(l=r,"Forbidden"===r&&(l=(0,b.t)("You do not have permission to edit this dashboard"))),S.Z.error({title:(0,b.t)("Error"),content:l,okButtonProps:{danger:!0,className:"btn-danger"}})},ae=(0,o.useCallback)((function(e,t,i,r){void 0===e&&(e="owners"),void 0===t&&(t="");const l=f().encode({filter:t,page:i,page_size:r});return y.Z.get({endpoint:`/api/v1/dashboard/related/${e}?q=${l}`}).then((e=>({data:e.json.result.filter((e=>void 0===e.extra.active||e.extra.active)).map((e=>({value:e.value,label:e.text}))),totalCount:e.json.count})))}),[]),ne=(0,o.useCallback)((e=>{const{id:t,dashboard_title:i,slug:r,certified_by:a,certification_details:n,owners:o,roles:s,metadata:c,is_managed_externally:d}=e,p={id:t,title:i,slug:r||"",certifiedBy:a||"",certificationDetails:n||"",isManagedExternally:d||!1};I.setFieldsValue(p),H(p),Y(o),W(s),z(c.color_scheme);const u=l()(c,["positions","shared_label_colors","color_scheme_domain"]);K(u?h()(u):"")}),[I]),oe=(0,o.useCallback)((()=>{U(!0),y.Z.get({endpoint:`/api/v1/dashboard/${a}`}).then((e=>{var t;const i=e.json.result,r=null!=(t=i.json_metadata)&&t.length?JSON.parse(i.json_metadata):{};ne({...i,metadata:r}),U(!1)}),le)}),[a,ne]),se=()=>{try{return null!=B&&B.length?JSON.parse(B):{}}catch(e){return{}}},ce=e=>{const t=(0,F.Z)(e).map((e=>({id:e.value,full_name:e.label})));Y(t)},de=e=>{const t=(0,F.Z)(e).map((e=>({id:e.value,name:e.label})));W(t)},he=()=>(G||[]).map((e=>({value:e.id,label:e.full_name||`${e.first_name} ${e.last_name}`}))),pe=function(e,t){void 0===e&&(e="");let{updateMetadata:i=!0}=void 0===t?{}:t;const r=ie.keys(),l=se();if(e&&!n()(r).call(r,e))throw S.Z.error({title:(0,b.t)("Error"),content:(0,b.t)("A valid color scheme is required"),okButtonProps:{danger:!0,className:"btn-danger"}}),new Error("A valid color scheme is required");i&&(l.color_scheme=e,l.label_colors=l.label_colors||{},K(h()(l))),z(e)};return(0,o.useEffect)((()=>{N&&(d?ne(d):oe()),k.Ad.preload()}),[d,oe,ne,N]),(0,o.useEffect)((()=>{m&&P&&P.title!==m&&I.setFieldsValue({...P,title:m})}),[P,m,I]),(0,o.useEffect)((()=>{if((0,C.cr)(C.TT.TAGGING_SYSTEM))try{(0,M.$3)({objectType:M.g.DASHBOARD,objectId:a,includeTypes:!1},(e=>te(e)),(e=>{i(`Error fetching tags: ${e.text}`)}))}catch(e){le(e)}}),[a]),(0,T.tZ)(S.Z,{show:N,onHide:g,title:(0,b.t)("Dashboard properties"),footer:(0,T.tZ)(o.Fragment,null,(0,T.tZ)(p.Z,{htmlType:"button",buttonSize:"small",onClick:g,cta:!0},(0,b.t)("Cancel")),(0,T.tZ)(p.Z,{onClick:I.submit,buttonSize:"small",buttonStyle:"primary",className:"m-r-5",cta:!0,disabled:null==P?void 0:P.isManagedExternally,tooltip:null!=P&&P.isManagedExternally?(0,b.t)("This dashboard is managed externally, and can't be edited in Superset"):""},Q)),responsive:!0},(0,T.tZ)(u.qz,{form:I,onFinish:()=>{var e,r,l,n;const{title:o,slug:s,certifiedBy:c,certificationDetails:d}=I.getFieldsValue();let p,u=L,m="",f=B;try{if(!f.startsWith("{")||!f.endsWith("}"))throw new Error;p=JSON.parse(f)}catch(e){return void i((0,b.t)("JSON metadata is invalid!"))}u=(null==(e=p)?void 0:e.color_scheme)||L,m=null==(r=p)?void 0:r.color_namespace,null!=(l=p)&&l.shared_label_colors&&delete p.shared_label_colors,null!=(n=p)&&n.color_scheme_domain&&delete p.color_scheme_domain;const v=(0,x.ZP)();var F;if(Z.getNamespace(m).resetColors(),u?(v.updateColorMap(m,u),p.shared_label_colors=Object.fromEntries(v.getColorMap()),p.color_scheme_domain=(null==(F=ie.get(L))?void 0:F.colors)||[]):(v.reset(),p.shared_label_colors={},p.color_scheme_domain=[]),f=h()(p),pe(u,{updateMetadata:!1}),(0,C.cr)(C.TT.TAGGING_SYSTEM))try{(0,M.$3)({objectType:M.g.DASHBOARD,objectId:a,includeTypes:!1},(e=>{return t=e,(i=ee).map((e=>{t.some((t=>t.name===e.name))||(0,M._U)({objectType:M.g.DASHBOARD,objectId:a,includeTypes:!1},e.name,(()=>{}),(()=>{}))})),void t.map((e=>{i.some((t=>t.name===e.name))||(0,M.OY)({objectType:M.g.DASHBOARD,objectId:a},e,(()=>{}),(()=>{}))}));var t,i}),(e=>{le(e)}))}catch(e){le(e)}const S={},k={};(0,C.cr)(C.TT.DASHBOARD_RBAC)&&(S.roles=V,k.roles=(V||[]).map((e=>e.id)));const N={id:a,title:o,slug:s,jsonMetadata:f,owners:G,colorScheme:u,colorNamespace:m,certifiedBy:c,certificationDetails:d,...S};$?(w(N),g(),t((0,b.t)("Dashboard properties updated"))):y.Z.put({endpoint:`/api/v1/dashboard/${a}`,headers:{"Content-Type":"application/json"},body:JSON.stringify({dashboard_title:o,slug:s||null,json_metadata:f||null,owners:(G||[]).map((e=>e.id)),certified_by:c||null,certification_details:c&&d?d:null,...k})}).then((()=>{w(N),g(),t((0,b.t)("The dashboard has been saved"))}),le)},layout:"vertical",initialValues:P},(0,T.tZ)(u.X2,null,(0,T.tZ)(u.JX,{xs:24,md:24},(0,T.tZ)("h3",null,(0,b.t)("Basic information")))),(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(c.xJ,{label:(0,b.t)("Title"),name:"title"},(0,T.tZ)(s.II,{type:"text",disabled:_}))),(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,{label:(0,b.t)("URL slug"),name:"slug"},(0,T.tZ)(s.II,{type:"text",disabled:_})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("A readable URL for your dashboard")))),(0,C.cr)(C.TT.DASHBOARD_RBAC)?(()=>{const e=se(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,T.tZ)(o.Fragment,null,(0,T.tZ)(u.X2,null,(0,T.tZ)(u.JX,{xs:24,md:24},(0,T.tZ)("h3",{style:{marginTop:"1em"}},(0,b.t)("Access")))),(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,{label:(0,b.t)("Owners")},(0,T.tZ)(u.qb,{allowClear:!0,allowNewOptions:!0,ariaLabel:(0,b.t)("Owners"),disabled:_,mode:"multiple",onChange:ce,options:(e,t,i)=>ae("owners",e,t,i),value:he()})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username."))),(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,{label:(0,b.t)("Roles")},(0,T.tZ)(u.qb,{allowClear:!0,ariaLabel:(0,b.t)("Roles"),disabled:_,mode:"multiple",onChange:de,options:(e,t,i)=>ae("roles",e,t,i),value:(V||[]).map((e=>({value:e.id,label:`${e.name}`})))})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("Roles is a list which defines access to the dashboard. Granting a role access to a dashboard will bypass dataset level checks. If no roles are defined, regular access permissions apply.")))),(0,T.tZ)(u.X2,null,(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(j,{hasCustomLabelColors:t,onChange:pe,colorScheme:L,labelMargin:4}))))})():(()=>{const e=se(),t=!!Object.keys((null==e?void 0:e.label_colors)||{}).length;return(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)("h3",{style:{marginTop:"1em"}},(0,b.t)("Access")),(0,T.tZ)(R,{label:(0,b.t)("Owners")},(0,T.tZ)(u.qb,{allowClear:!0,ariaLabel:(0,b.t)("Owners"),disabled:_,mode:"multiple",onChange:ce,options:(e,t,i)=>ae("owners",e,t,i),value:he()})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("Owners is a list of users who can alter the dashboard. Searchable by name or username."))),(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)("h3",{style:{marginTop:"1em"}},(0,b.t)("Colors")),(0,T.tZ)(j,{hasCustomLabelColors:t,onChange:pe,colorScheme:L,labelMargin:4})))})(),(0,T.tZ)(u.X2,null,(0,T.tZ)(u.JX,{xs:24,md:24},(0,T.tZ)("h3",null,(0,b.t)("Certification")))),(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,{label:(0,b.t)("Certified by"),name:"certifiedBy"},(0,T.tZ)(s.II,{type:"text",disabled:_})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("Person or group that has certified this dashboard."))),(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,{label:(0,b.t)("Certification details"),name:"certificationDetails"},(0,T.tZ)(s.II,{type:"text",disabled:_})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("Any additional detail to show in the certification tooltip.")))),(0,C.cr)(C.TT.TAGGING_SYSTEM)?(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)("h3",{css:D},(0,b.t)("Tags")))):null,(0,C.cr)(C.TT.TAGGING_SYSTEM)?(0,T.tZ)(u.X2,{gutter:16},(0,T.tZ)(u.JX,{xs:24,md:12},(0,T.tZ)(R,null,(0,T.tZ)(u.qb,{ariaLabel:"Tags",mode:"multiple",allowNewOptions:!0,value:re,options:A.m,onChange:e=>{const t=[...new Set(e.map((e=>e.label)))];te([...t.map((e=>({name:e})))])},allowClear:!0})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("A list of tags that have been applied to this chart.")))):null,(0,T.tZ)(u.X2,null,(0,T.tZ)(u.JX,{xs:24,md:24},(0,T.tZ)("h3",{style:{marginTop:"1em"}},(0,T.tZ)(p.Z,{buttonStyle:"link",onClick:()=>X(!J)},(0,T.tZ)("i",{className:"fa fa-angle-"+(J?"down":"right"),style:{minWidth:"1em"}}),(0,b.t)("Advanced"))),J&&(0,T.tZ)(o.Fragment,null,(0,T.tZ)(R,{label:(0,b.t)("JSON metadata")},(0,T.tZ)(q,{showLoadingForImport:!0,name:"json_metadata",value:B,onChange:K,tabSize:2,width:"100%",height:"200px",wrapEnabled:!0})),(0,T.tZ)("p",{className:"help-block"},(0,b.t)("This JSON object is generated dynamically when clicking the save or overwrite button in the dashboard view. It is exposed here for reference and for power users who may want to alter specific parameters."),$&&(0,T.tZ)(o.Fragment,null," ",(0,b.t)('Please DO NOT overwrite the "filter_scopes" key.')," ",(0,T.tZ)(E.Z,{triggerNode:(0,T.tZ)("span",{className:"alert-link"},(0,b.t)('Use "%(menuName)s" menu instead.',{menuName:(0,b.t)("Set filter mapping")}))}))))))))}))},87999:(e,t,i)=>{i.d(t,{Z:()=>be});var r=i(67294),l=i(51995),a=i(1304),n=i(28216),o=i(14890),s=i(81395),c=i(9467),d=i(78580),h=i.n(d),p=i(45697),u=i.n(p),m=i(94184),f=i.n(m),g=i(35932),b=i(11965),v=i(55867),y=i(41609),F=i.n(y),x=i(80621),Z=i(81255);const C=[Z.gn,Z.U0];function S(e){let{currentNode:t={},components:i={},filterFields:r=[],selectedChartId:l}=e;if(!t)return null;const{type:a}=t;if(Z.dW===a&&t&&t.meta&&t.meta.chartId){const e={value:t.meta.chartId,label:t.meta.sliceName||`${a} ${t.meta.chartId}`,type:a,showCheckbox:l!==t.meta.chartId};return{...e,children:r.map((i=>({value:`${t.meta.chartId}:${i}`,label:`${e.label}`,type:"filter_box",showCheckbox:!1})))}}let n=[];if(t.children&&t.children.length&&t.children.forEach((e=>{const t=S({currentNode:i[e],components:i,filterFields:r,selectedChartId:l}),a=i[e].type;h()(C).call(C,a)?n.push(t):n=n.concat(t)})),h()(C).call(C,a)){let e=null;return e=a===Z.U0?(0,v.t)("All charts"):t.meta&&t.meta.text?t.meta.text:`${a} ${t.id}`,{value:t.id,label:e,type:a,children:n}}return n}function k(e){let{components:t={},filterFields:i=[],selectedChartId:r}=e;return F()(t)?[]:[{...S({currentNode:t[x._4],components:t,filterFields:i,selectedChartId:r})}]}function $(e,t){void 0===e&&(e=[]),void 0===t&&(t=-1);const i=[],r=(e,l)=>{e&&e.children&&(-1===t||l<t)&&(i.push(e.value),e.children.forEach((e=>r(e,l+1))))};return e.length>0&&e.forEach((e=>{r(e,0)})),i}var w=i(9679);function N(e){let{activeFilterField:t,checkedFilterFields:i}=e;return(0,w.o)(t?[t]:i)}var T=i(20194);function I(e){let{activeFilterField:t,checkedFilterFields:i}=e;if(t)return(0,T._)(t).chartId;if(i.length){const{chartId:e}=(0,T._)(i[0]);return i.some((t=>(0,T._)(t).chartId!==e))?null:e}return null}function _(e){let{checkedFilterFields:t=[],activeFilterField:i,filterScopeMap:r={},layout:l={}}=e;const a=N({checkedFilterFields:t,activeFilterField:i}),n=i?[i]:t,o=k({components:l,filterFields:n,selectedChartId:I({checkedFilterFields:t,activeFilterField:i})}),s=new Set;n.forEach((e=>{(r[e].checked||[]).forEach((t=>{s.add(`${t}:${e}`)}))}));const c=[...s],d=r[a]?r[a].expanded:$(o,1);return{[a]:{nodes:o,nodesFiltered:[...o],checked:c,expanded:d}}}var j=i(94654),E=i.n(j),O=i(83927),U=i.n(O),M=i(58809),A=i.n(M),R=i(8816),q=i.n(R);function D(e){let{tabScopes:t,parentNodeValue:i,forceAggregate:r=!1,hasChartSiblings:l=!1,tabChildren:a=[],immuneChartSiblings:n=[]}=e;if(r||!l&&Object.entries(t).every((e=>{let[t,{scope:i}]=e;return i&&i.length&&t===i[0]}))){const e=function(e){let{tabs:t=[],tabsInScope:i=[]}=e;const r=[];return t.forEach((e=>{let{value:t,children:l}=e;l&&!h()(i).call(i,t)&&l.forEach((e=>{let{value:t,children:l}=e;l&&!h()(i).call(i,t)&&r.push(...l.filter((e=>{let{type:t}=e;return t===Z.dW})))}))})),r.map((e=>{let{value:t}=e;return t}))}({tabs:a,tabsInScope:E()(t,(e=>{let{scope:t}=e;return t}))}),r=E()(Object.values(t),(e=>{let{immune:t}=e;return t}));return{scope:[i],immune:[...new Set([...e,...r])]}}const o=Object.values(t).filter((e=>{let{scope:t}=e;return t&&t.length}));return{scope:E()(o,(e=>{let{scope:t}=e;return t})),immune:o.length?E()(o,(e=>{let{immune:t}=e;return t})):E()(Object.values(t),(e=>{let{immune:t}=e;return t})).concat(n)}}function J(e){let{currentNode:t={},filterId:i,checkedChartIds:r=[]}=e;if(!t)return{};const{value:l,children:a}=t,n=a.filter((e=>{let{type:t}=e;return t===Z.dW})),o=a.filter((e=>{let{type:t}=e;return t===Z.gn})),s=n.filter((e=>{let{value:t}=e;return i!==t&&!h()(r).call(r,t)})).map((e=>{let{value:t}=e;return t})),c=q()(A()((e=>e.value)),U()((e=>J({currentNode:e,filterId:i,checkedChartIds:r}))))(o);if(!F()(n)&&n.some((e=>{let{value:t}=e;return h()(r).call(r,t)}))){if(F()(o))return{scope:[l],immune:s};const{scope:e,immune:t}=D({tabScopes:c,parentNodeValue:l,forceAggregate:!0,tabChildren:o});return{scope:e,immune:s.concat(t)}}return o.length?D({tabScopes:c,parentNodeValue:l,hasChartSiblings:!F()(n),tabChildren:o,immuneChartSiblings:s}):{scope:[],immune:s}}function X(e){let{filterKey:t,nodes:i=[],checkedChartIds:r=[]}=e;if(i.length){const{chartId:e}=(0,T._)(t);return J({currentNode:i[0],filterId:e,checkedChartIds:r})}return{}}var L=i(43399),z=i(2275),B=i(28388),K=i.n(B),P=i(70163);const H=(0,l.iK)(P.Z.BarChartOutlined)`
  ${e=>{let{theme:t}=e;return`\n    position: relative;\n    top: ${t.gridUnit-1}px;\n    color: ${t.colors.primary.base};\n    margin-right: ${2*t.gridUnit}px;\n  `}}
`;function G(e){let{currentNode:t={},selectedChartId:i}=e;if(!t)return null;const{label:r,value:l,type:a,children:n}=t;if(n&&n.length){const e=n.map((e=>G({currentNode:e,selectedChartId:i})));return{...t,label:(0,b.tZ)("span",{className:f()(`filter-scope-type ${a.toLowerCase()}`,{"selected-filter":i===l})},a===Z.dW&&(0,b.tZ)(H,null),r),children:e}}return{...t,label:(0,b.tZ)("span",{className:f()(`filter-scope-type ${a.toLowerCase()}`,{"selected-filter":i===l})},r)}}function Y(e){let{nodes:t,selectedChartId:i}=e;return t?t.map((e=>G({currentNode:e,selectedChartId:i}))):[]}var V=i(13842);const W={check:(0,b.tZ)(V.lU,null),uncheck:(0,b.tZ)(V.zq,null),halfCheck:(0,b.tZ)(V.dc,null),expandClose:(0,b.tZ)("span",{className:"rct-icon rct-icon-expand-close"}),expandOpen:(0,b.tZ)("span",{className:"rct-icon rct-icon-expand-open"}),expandAll:(0,b.tZ)("span",{className:"rct-icon rct-icon-expand-all"},(0,v.t)("Expand all")),collapseAll:(0,b.tZ)("span",{className:"rct-icon rct-icon-collapse-all"},(0,v.t)("Collapse all")),parentClose:(0,b.tZ)("span",{className:"rct-icon rct-icon-parent-close"}),parentOpen:(0,b.tZ)("span",{className:"rct-icon rct-icon-parent-open"}),leaf:(0,b.tZ)("span",{className:"rct-icon rct-icon-leaf"})},Q={nodes:u().arrayOf(z.ck).isRequired,checked:u().arrayOf(u().oneOfType([u().number,u().string])).isRequired,expanded:u().arrayOf(u().oneOfType([u().number,u().string])).isRequired,onCheck:u().func.isRequired,onExpand:u().func.isRequired,selectedChartId:u().number},ee=()=>{};function te(e){let{nodes:t=[],checked:i=[],expanded:r=[],onCheck:l,onExpand:a,selectedChartId:n}=e;return(0,b.tZ)(K(),{showExpandAll:!0,expandOnClick:!0,showNodeIcon:!1,nodes:Y({nodes:t,selectedChartId:n}),checked:i,expanded:r,onCheck:l,onExpand:a,onClick:ee,icons:W})}te.propTypes=Q,te.defaultProps={selectedChartId:null};var ie=i(49238);const re={label:u().string.isRequired,isSelected:u().bool.isRequired};function le(e){let{label:t,isSelected:i}=e;return(0,b.tZ)("span",{className:f()("filter-field-item filter-container",{"is-selected":i})},(0,b.tZ)(ie.lX,{htmlFor:t},t))}function ae(e){let{nodes:t,activeKey:i}=e;if(!t)return[];const r=t[0],l=r.children.map((e=>({...e,children:e.children.map((e=>{const{label:t,value:r}=e;return{...e,label:(0,b.tZ)(le,{isSelected:r===i,label:t})}}))})));return[{...r,label:(0,b.tZ)("span",{className:"root"},r.label),children:l}]}le.propTypes=re;const ne={activeKey:u().string,nodes:u().arrayOf(z.ck).isRequired,checked:u().arrayOf(u().oneOfType([u().number,u().string])).isRequired,expanded:u().arrayOf(u().oneOfType([u().number,u().string])).isRequired,onCheck:u().func.isRequired,onExpand:u().func.isRequired,onClick:u().func.isRequired};function oe(e){let{activeKey:t,nodes:i=[],checked:r=[],expanded:l=[],onClick:a,onCheck:n,onExpand:o}=e;return(0,b.tZ)(K(),{showExpandAll:!0,showNodeIcon:!1,expandOnClick:!0,nodes:ae({nodes:i,activeKey:t}),checked:r,expanded:l,onClick:a,onCheck:n,onExpand:o,icons:W})}oe.propTypes=ne,oe.defaultProps={activeKey:null};const se={dashboardFilters:u().objectOf(z.Er).isRequired,layout:u().object.isRequired,updateDashboardFiltersScope:u().func.isRequired,setUnsavedChanges:u().func.isRequired,onCloseModal:u().func.isRequired},ce=l.iK.div`
  ${e=>{let{theme:t}=e;return b.iv`
    display: flex;
    flex-direction: column;
    height: 80%;
    margin-right: ${-6*t.gridUnit}px;
    font-size: ${t.typography.sizes.m}px;

    & .nav.nav-tabs {
      border: none;
    }

    & .filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*t.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }

    & .warning-message {
      padding: ${6*t.gridUnit}px;
    }
  `}}
`,de=l.iK.div`
  ${e=>{let{theme:t}=e;return b.iv`
    &.filter-scope-body {
      flex: 1;
      max-height: calc(100% - ${32*t.gridUnit}px);

      .filter-field-pane,
      .filter-scope-pane {
        overflow-y: auto;
      }
    }
  `}}
`,he=l.iK.div`
  ${e=>{let{theme:t}=e;return b.iv`
    height: ${16*t.gridUnit}px;
    border-bottom: 1px solid ${t.colors.grayscale.light2};
    padding-left: ${6*t.gridUnit}px;
    margin-left: ${-6*t.gridUnit}px;

    h4 {
      margin-top: 0;
    }

    .selected-fields {
      margin: ${3*t.gridUnit}px 0 ${4*t.gridUnit}px;
      visibility: hidden;

      &.multi-edit-mode {
        visibility: visible;
      }

      .selected-scopes {
        padding-left: ${t.gridUnit}px;
      }
    }
  `}}
`,pe=l.iK.div`
  ${e=>{let{theme:t}=e;return b.iv`
    &.filters-scope-selector {
      display: flex;
      flex-direction: row;
      position: relative;
      height: 100%;

      a,
      a:active,
      a:hover {
        color: inherit;
        text-decoration: none;
      }

      .react-checkbox-tree .rct-icon.rct-icon-expand-all,
      .react-checkbox-tree .rct-icon.rct-icon-collapse-all {
        font-family: ${t.typography.families.sansSerif};
        font-size: ${t.typography.sizes.m}px;
        color: ${t.colors.primary.base};

        &::before {
          content: '';
        }

        &:hover {
          text-decoration: underline;
        }

        &:focus {
          outline: none;
        }
      }

      .filter-field-pane {
        position: relative;
        width: 40%;
        padding: ${4*t.gridUnit}px;
        padding-left: 0;
        border-right: 1px solid ${t.colors.grayscale.light2};

        .filter-container label {
          font-weight: ${t.typography.weights.normal};
          margin: 0 0 0 ${4*t.gridUnit}px;
          word-break: break-all;
        }

        .filter-field-item {
          height: ${9*t.gridUnit}px;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 0 ${6*t.gridUnit}px;
          margin-left: ${-6*t.gridUnit}px;

          &.is-selected {
            border: 1px solid ${t.colors.text.label};
            border-radius: ${t.borderRadius}px;
            background-color: ${t.colors.grayscale.light4};
            margin-left: ${-6*t.gridUnit}px;
          }
        }

        .react-checkbox-tree {
          .rct-title .root {
            font-weight: ${t.typography.weights.bold};
          }

          .rct-text {
            height: ${10*t.gridUnit}px;
          }
        }
      }

      .filter-scope-pane {
        position: relative;
        flex: 1;
        padding: ${4*t.gridUnit}px;
        padding-right: ${6*t.gridUnit}px;
      }

      .react-checkbox-tree {
        flex-direction: column;
        color: ${t.colors.grayscale.dark1};
        font-size: ${t.typography.sizes.m}px;

        .filter-scope-type {
          padding: ${2*t.gridUnit}px 0;
          display: flex;
          align-items: center;

          &.chart {
            font-weight: ${t.typography.weights.normal};
          }

          &.selected-filter {
            padding-left: ${7*t.gridUnit}px;
            position: relative;
            color: ${t.colors.text.label};

            &::before {
              content: ' ';
              position: absolute;
              left: 0;
              top: 50%;
              width: ${4*t.gridUnit}px;
              height: ${4*t.gridUnit}px;
              border-radius: ${t.borderRadius}px;
              margin-top: ${-2*t.gridUnit}px;
              box-shadow: inset 0 0 0 2px ${t.colors.grayscale.light2};
              background: ${t.colors.grayscale.light3};
            }
          }

          &.root {
            font-weight: ${t.typography.weights.bold};
          }
        }

        .rct-checkbox {
          svg {
            position: relative;
            top: 3px;
            width: ${4.5*t.gridUnit}px;
          }
        }

        .rct-node-leaf {
          .rct-bare-label {
            &::before {
              padding-left: ${t.gridUnit}px;
            }
          }
        }

        .rct-options {
          text-align: left;
          margin-left: 0;
          margin-bottom: ${2*t.gridUnit}px;
        }

        .rct-text {
          margin: 0;
          display: flex;
        }

        .rct-title {
          display: block;
        }

        // disable style from react-checkbox-trees.css
        .rct-node-clickable:hover,
        .rct-node-clickable:focus,
        label:hover,
        label:active {
          background: none !important;
        }
      }

      .multi-edit-mode {
        &.filter-scope-pane {
          .rct-node.rct-node-leaf .filter-scope-type.filter_box {
            display: none;
          }
        }

        .filter-field-item {
          padding: 0 ${4*t.gridUnit}px 0 ${12*t.gridUnit}px;
          margin-left: ${-12*t.gridUnit}px;

          &.is-selected {
            margin-left: ${-13*t.gridUnit}px;
          }
        }
      }

      .scope-search {
        position: absolute;
        right: ${4*t.gridUnit}px;
        top: ${4*t.gridUnit}px;
        border-radius: ${t.borderRadius}px;
        border: 1px solid ${t.colors.grayscale.light2};
        padding: ${t.gridUnit}px ${2*t.gridUnit}px;
        font-size: ${t.typography.sizes.m}px;
        outline: none;

        &:focus {
          border: 1px solid ${t.colors.primary.base};
        }
      }
    }
  `}}
`,ue=l.iK.div`
  ${e=>{let{theme:t}=e;return`\n    height: ${16*t.gridUnit}px;\n\n    border-top: ${t.gridUnit/4}px solid ${t.colors.primary.light3};\n    padding: ${6*t.gridUnit}px;\n    margin: 0 0 0 ${6*-t.gridUnit}px;\n    text-align: right;\n\n    .btn {\n      margin-right: ${4*t.gridUnit}px;\n\n      &:last-child {\n        margin-right: 0;\n      }\n    }\n  `}}
`;class me extends r.PureComponent{constructor(e){super(e);const{dashboardFilters:t,layout:i}=e;if(Object.keys(t).length>0){const e=function(e){let{dashboardFilters:t={}}=e;const i=Object.values(t).map((e=>{const{chartId:t,filterName:i,columns:r,labels:l}=e,a=Object.keys(r).map((e=>({value:(0,T.w)({chartId:t,column:e}),label:l[e]||e})));return{value:t,label:i,children:a,showCheckbox:!0}}));return[{value:x.dU,type:Z.U0,label:(0,v.t)("All filters"),children:i}]}({dashboardFilters:t}),r=e[0].children;this.allfilterFields=[],r.forEach((e=>{let{children:t}=e;t.forEach((e=>{this.allfilterFields.push(e.value)}))})),this.defaultFilterKey=r[0].children[0].value;const l=Object.values(t).reduce(((e,r)=>{let{chartId:l,columns:a}=r;return{...e,...Object.keys(a).reduce(((e,r)=>{const a=(0,T.w)({chartId:l,column:r}),n=k({components:i,filterFields:[a],selectedChartId:l}),o=$(n,1),s=((0,L.up)({filterScope:t[l].scopes[r]})||[]).filter((e=>e!==l));return{...e,[a]:{nodes:n,nodesFiltered:[...n],checked:s,expanded:o}}}),{})}}),{}),{chartId:a}=(0,T._)(this.defaultFilterKey),n=[],o=this.defaultFilterKey,s=[x.dU].concat(a),c=_({checkedFilterFields:n,activeFilterField:o,filterScopeMap:l,layout:i});this.state={showSelector:!0,activeFilterField:o,searchText:"",filterScopeMap:{...l,...c},filterFieldNodes:e,checkedFilterFields:n,expandedFilterIds:s}}else this.state={showSelector:!1};this.filterNodes=this.filterNodes.bind(this),this.onChangeFilterField=this.onChangeFilterField.bind(this),this.onCheckFilterScope=this.onCheckFilterScope.bind(this),this.onExpandFilterScope=this.onExpandFilterScope.bind(this),this.onSearchInputChange=this.onSearchInputChange.bind(this),this.onCheckFilterField=this.onCheckFilterField.bind(this),this.onExpandFilterField=this.onExpandFilterField.bind(this),this.onClose=this.onClose.bind(this),this.onSave=this.onSave.bind(this)}onCheckFilterScope(e){void 0===e&&(e=[]);const{activeFilterField:t,filterScopeMap:i,checkedFilterFields:r}=this.state,l=N({activeFilterField:t,checkedFilterFields:r}),a=t?[t]:r,n={...i[l],checked:e},o=function(e){let{checked:t=[],filterFields:i=[],filterScopeMap:r={}}=e;const l=t.reduce(((e,t)=>{const[i,r]=t.split(":");return{...e,[r]:(e[r]||[]).concat(parseInt(i,10))}}),{});return i.reduce(((e,t)=>{const{chartId:i}=(0,T._)(t),a=(l[t]||[]).filter((e=>e!==i));return{...e,[t]:{...r[t],checked:a}}}),{})}({checked:e,filterFields:a,filterScopeMap:i});this.setState((()=>({filterScopeMap:{...i,...o,[l]:n}})))}onExpandFilterScope(e){void 0===e&&(e=[]);const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:r}=this.state,l=N({activeFilterField:t,checkedFilterFields:i}),a={...r[l],expanded:e};this.setState((()=>({filterScopeMap:{...r,[l]:a}})))}onCheckFilterField(e){void 0===e&&(e=[]);const{layout:t}=this.props,{filterScopeMap:i}=this.state,r=_({checkedFilterFields:e,activeFilterField:null,filterScopeMap:i,layout:t});this.setState((()=>({activeFilterField:null,checkedFilterFields:e,filterScopeMap:{...i,...r}})))}onExpandFilterField(e){void 0===e&&(e=[]),this.setState((()=>({expandedFilterIds:e})))}onChangeFilterField(e){var t;void 0===e&&(e={});const{layout:i}=this.props,r=e.value,{activeFilterField:l,checkedFilterFields:a,filterScopeMap:n}=this.state;if(r===l){const e=_({checkedFilterFields:a,activeFilterField:null,filterScopeMap:n,layout:i});this.setState({activeFilterField:null,filterScopeMap:{...n,...e}})}else if(h()(t=this.allfilterFields).call(t,r)){const e=_({checkedFilterFields:a,activeFilterField:r,filterScopeMap:n,layout:i});this.setState({activeFilterField:r,filterScopeMap:{...n,...e}})}}onSearchInputChange(e){this.setState({searchText:e.target.value},this.filterTree)}onClose(){this.props.onCloseModal()}onSave(){const{filterScopeMap:e}=this.state,t=this.allfilterFields.reduce(((t,i)=>{const{nodes:r}=e[i];return{...t,[i]:X({filterKey:i,nodes:r,checkedChartIds:e[i].checked})}}),{});this.props.updateDashboardFiltersScope(t),this.props.setUnsavedChanges(!0),this.props.onCloseModal()}filterTree(){if(this.state.searchText){const e=e=>{const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:r}=e,l=N({activeFilterField:t,checkedFilterFields:i}),a=r[l].nodes.reduce(this.filterNodes,[]),n=$([...a]),o={...r[l],nodesFiltered:a,expanded:n};return{filterScopeMap:{...r,[l]:o}}};this.setState(e)}else this.setState((e=>{const{activeFilterField:t,checkedFilterFields:i,filterScopeMap:r}=e,l=N({activeFilterField:t,checkedFilterFields:i}),a={...r[l],nodesFiltered:r[l].nodes};return{filterScopeMap:{...r,[l]:a}}}))}filterNodes(e,t){void 0===e&&(e=[]),void 0===t&&(t={});const{searchText:i}=this.state,r=(t.children||[]).reduce(this.filterNodes,[]);return(t.label.toLocaleLowerCase().indexOf(i.toLocaleLowerCase())>-1||r.length)&&e.push({...t,children:r}),e}renderFilterFieldList(){const{activeFilterField:e,filterFieldNodes:t,checkedFilterFields:i,expandedFilterIds:r}=this.state;return(0,b.tZ)(oe,{activeKey:e,nodes:t,checked:i,expanded:r,onClick:this.onChangeFilterField,onCheck:this.onCheckFilterField,onExpand:this.onExpandFilterField})}renderFilterScopeTree(){const{filterScopeMap:e,activeFilterField:t,checkedFilterFields:i,searchText:l}=this.state,a=N({activeFilterField:t,checkedFilterFields:i}),n=I({activeFilterField:t,checkedFilterFields:i});return(0,b.tZ)(r.Fragment,null,(0,b.tZ)("input",{className:"filter-text scope-search multi-edit-mode",placeholder:(0,v.t)("Search..."),type:"text",value:l,onChange:this.onSearchInputChange}),(0,b.tZ)(te,{nodes:e[a].nodesFiltered,checked:e[a].checked,expanded:e[a].expanded,onCheck:this.onCheckFilterScope,onExpand:this.onExpandFilterScope,selectedChartId:n}))}renderEditingFiltersName(){const{dashboardFilters:e}=this.props,{activeFilterField:t,checkedFilterFields:i}=this.state,r=[].concat(t||i).map((t=>{const{chartId:i,column:r}=(0,T._)(t);return e[i].labels[r]||r}));return(0,b.tZ)("div",{className:"selected-fields multi-edit-mode"},0===r.length&&(0,v.t)("No filter is selected."),1===r.length&&(0,v.t)("Editing 1 filter:"),r.length>1&&(0,v.t)("Batch editing %d filters:",r.length),(0,b.tZ)("span",{className:"selected-scopes"},r.join(", ")))}render(){const{showSelector:e}=this.state;return(0,b.tZ)(ce,null,(0,b.tZ)(he,null,(0,b.tZ)("h4",null,(0,v.t)("Configure filter scopes")),e&&this.renderEditingFiltersName()),(0,b.tZ)(de,{className:"filter-scope-body"},e?(0,b.tZ)(pe,{className:"filters-scope-selector"},(0,b.tZ)("div",{className:f()("filter-field-pane multi-edit-mode")},this.renderFilterFieldList()),(0,b.tZ)("div",{className:"filter-scope-pane multi-edit-mode"},this.renderFilterScopeTree())):(0,b.tZ)("div",{className:"warning-message"},(0,v.t)("There are no filters in this dashboard."))),(0,b.tZ)(ue,null,(0,b.tZ)(g.Z,{buttonSize:"small",onClick:this.onClose},(0,v.t)("Close")),e&&(0,b.tZ)(g.Z,{buttonSize:"small",buttonStyle:"primary",onClick:this.onSave},(0,v.t)("Save"))))}}me.propTypes=se;const fe=(0,n.$j)((function(e){let{dashboardLayout:t,dashboardFilters:i}=e;return{dashboardFilters:i,layout:t.present}}),(function(e){return(0,o.DE)({updateDashboardFiltersScope:s.l6,setUnsavedChanges:c.if},e)}))(me),ge=l.iK.div((e=>{let{theme:{gridUnit:t}}=e;return{padding:2*t,paddingBottom:3*t}}));class be extends r.PureComponent{constructor(e){super(e),this.modal=void 0,this.modal=r.createRef(),this.handleCloseModal=this.handleCloseModal.bind(this)}handleCloseModal(){var e,t;null==this||null==(e=this.modal)||null==(t=e.current)||null==t.close||t.close()}render(){const e={onCloseModal:this.handleCloseModal};return(0,b.tZ)(a.Z,{ref:this.modal,triggerNode:this.props.triggerNode,modalBody:(0,b.tZ)(ge,null,(0,b.tZ)(fe,e)),width:"80%"})}}},48273:(e,t,i)=>{i.d(t,{$3:()=>p,OY:()=>u,Qz:()=>m,Y4:()=>g,_U:()=>f,g:()=>c});var r=i(78580),l=i.n(r),a=i(31069),n=i(15926),o=i.n(n);const s=Object.freeze(["dashboard","chart","saved_query"]),c=Object.freeze({DASHBOARD:"dashboard",CHART:"chart",QUERY:"saved_query"}),d={saved_query:1,chart:2,dashboard:3},h=e=>{if(!l()(s).call(s,e))throw new Error(`objectType ${e} is invalid`);return d[e]};function p(e,t,i){let{objectType:r,objectId:n,includeTypes:o=!1}=e;if(void 0===r||void 0===n)throw new Error("Need to specify objectType and objectId");if(!l()(s).call(s,r))throw new Error(`objectType ${r} is invalid`);a.Z.get({endpoint:`/api/v1/${r}/${n}`}).then((e=>{let{json:i}=e;return t(i.result.tags.filter((e=>-1===e.name.indexOf(":")||o)))})).catch((e=>i(e)))}function u(e,t,i,r){let{objectType:n,objectId:o}=e;if(void 0===n||void 0===o)throw new Error("Need to specify objectType and objectId");if(!l()(s).call(s,n))throw new Error(`objectType ${n} is invalid`);a.Z.delete({endpoint:`/api/v1/tag/${h(n)}/${o}/${t.name}`}).then((e=>{let{json:t}=e;return i(t?JSON.stringify(t):"Successfully Deleted Tagged Objects")})).catch((e=>{const t=e.message;return r(t||"Error Deleting Tagged Objects")}))}function m(e,t,i){const r=e.map((e=>e.name));a.Z.delete({endpoint:`/api/v1/tag/?q=${o().encode(r)}`}).then((e=>{let{json:i}=e;return i.message?t(i.message):t("Successfully Deleted Tag")})).catch((e=>{const t=e.message;return i(t||"Error Deleting Tag")}))}function f(e,t,i,r){let{objectType:l,objectId:n,includeTypes:o=!1}=e;if(void 0===l||void 0===n)throw new Error("Need to specify objectType and objectId");if(-1!==t.indexOf(":")&&!o)return;const s=h(l);a.Z.post({endpoint:`/api/v1/tag/${s}/${n}/`,body:JSON.stringify({properties:{tags:[t]}}),parseMethod:"json",headers:{"Content-Type":"application/json"}}).then((e=>{let{json:t}=e;return i(JSON.stringify(t))})).catch((e=>r(e)))}function g(e,t,i){let{tags:r="",types:l}=e,n=`/api/v1/tag/get_objects/?tags=${r}`;l&&(n+=`&types=${l}`),a.Z.get({endpoint:n}).then((e=>{let{json:i}=e;return t(i.result)})).catch((e=>i(e)))}},65108:(e,t,i)=>{i.d(t,{g:()=>r});const r=function(e,t,i){return void 0===i&&(i=function(){for(var e=arguments.length,t=new Array(e),i=0;i<e;i++)t[i]=arguments[i];return JSON.stringify([...t])}),function(){const r=i(...arguments);if(t.has(r))return t.get(r);const l=e(...arguments);return t.set(r,l),l}}}}]);
//# sourceMappingURL=4717.863fa7b67bb50ee63f20.entry.js.map