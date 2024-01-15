"use strict";(self.webpackChunk_datalayer_jupyter_iam=self.webpackChunk_datalayer_jupyter_iam||[]).push([[9943],{9943:(e,t,n)=>{n.r(t),n.d(t,{Bounce:()=>L,Flip:()=>R,Icons:()=>h,Slide:()=>O,ToastContainer:()=>w,Zoom:()=>N,collapseToast:()=>d,cssTransition:()=>p,toast:()=>F,useToast:()=>E,useToastContainer:()=>y});var o=n(56769);function s(e){var t,n,o="";if("string"==typeof e||"number"==typeof e)o+=e;else if("object"==typeof e)if(Array.isArray(e))for(t=0;t<e.length;t++)e[t]&&(n=s(e[t]))&&(o&&(o+=" "),o+=n);else for(t in e)e[t]&&(o&&(o+=" "),o+=t);return o}const a=function(){for(var e,t,n=0,o="";n<arguments.length;)(e=arguments[n++])&&(t=s(e))&&(o&&(o+=" "),o+=t);return o},r=e=>"number"==typeof e&&!isNaN(e),i=e=>"string"==typeof e,l=e=>"function"==typeof e,c=e=>i(e)||l(e)?e:null,u=e=>(0,o.isValidElement)(e)||i(e)||l(e)||r(e);function d(e,t,n){void 0===n&&(n=300);const{scrollHeight:o,style:s}=e;requestAnimationFrame((()=>{s.minHeight="initial",s.height=o+"px",s.transition=`all ${n}ms`,requestAnimationFrame((()=>{s.height="0",s.padding="0",s.margin="0",setTimeout(t,n)}))}))}function p(e){let{enter:t,exit:n,appendPosition:s=!1,collapse:a=!0,collapseDuration:r=300}=e;return function(e){let{children:i,position:l,preventExitTransition:c,done:u,nodeRef:p,isIn:f}=e;const m=s?`${t}--${l}`:t,g=s?`${n}--${l}`:n,h=(0,o.useRef)(0);return(0,o.useLayoutEffect)((()=>{const e=p.current,t=m.split(" "),n=o=>{o.target===p.current&&(e.dispatchEvent(new Event("d")),e.removeEventListener("animationend",n),e.removeEventListener("animationcancel",n),0===h.current&&"animationcancel"!==o.type&&e.classList.remove(...t))};e.classList.add(...t),e.addEventListener("animationend",n),e.addEventListener("animationcancel",n)}),[]),(0,o.useEffect)((()=>{const e=p.current,t=()=>{e.removeEventListener("animationend",t),a?d(e,u,r):u()};f||(c?t():(h.current=1,e.className+=` ${g}`,e.addEventListener("animationend",t)))}),[f]),o.createElement(o.Fragment,null,i)}}function f(e,t){return null!=e?{content:e.content,containerId:e.props.containerId,id:e.props.toastId,theme:e.props.theme,type:e.props.type,data:e.props.data||{},isLoading:e.props.isLoading,icon:e.props.icon,status:t}:{}}const m={list:new Map,emitQueue:new Map,on(e,t){return this.list.has(e)||this.list.set(e,[]),this.list.get(e).push(t),this},off(e,t){if(t){const n=this.list.get(e).filter((e=>e!==t));return this.list.set(e,n),this}return this.list.delete(e),this},cancelEmit(e){const t=this.emitQueue.get(e);return t&&(t.forEach(clearTimeout),this.emitQueue.delete(e)),this},emit(e){this.list.has(e)&&this.list.get(e).forEach((t=>{const n=setTimeout((()=>{t(...[].slice.call(arguments,1))}),0);this.emitQueue.has(e)||this.emitQueue.set(e,[]),this.emitQueue.get(e).push(n)}))}},g=e=>{let{theme:t,type:n,...s}=e;return o.createElement("svg",{viewBox:"0 0 24 24",width:"100%",height:"100%",fill:"colored"===t?"currentColor":`var(--toastify-icon-color-${n})`,...s})},h={info:function(e){return o.createElement(g,{...e},o.createElement("path",{d:"M12 0a12 12 0 1012 12A12.013 12.013 0 0012 0zm.25 5a1.5 1.5 0 11-1.5 1.5 1.5 1.5 0 011.5-1.5zm2.25 13.5h-4a1 1 0 010-2h.75a.25.25 0 00.25-.25v-4.5a.25.25 0 00-.25-.25h-.75a1 1 0 010-2h1a2 2 0 012 2v4.75a.25.25 0 00.25.25h.75a1 1 0 110 2z"}))},warning:function(e){return o.createElement(g,{...e},o.createElement("path",{d:"M23.32 17.191L15.438 2.184C14.728.833 13.416 0 11.996 0c-1.42 0-2.733.833-3.443 2.184L.533 17.448a4.744 4.744 0 000 4.368C1.243 23.167 2.555 24 3.975 24h16.05C22.22 24 24 22.044 24 19.632c0-.904-.251-1.746-.68-2.44zm-9.622 1.46c0 1.033-.724 1.823-1.698 1.823s-1.698-.79-1.698-1.822v-.043c0-1.028.724-1.822 1.698-1.822s1.698.79 1.698 1.822v.043zm.039-12.285l-.84 8.06c-.057.581-.408.943-.897.943-.49 0-.84-.367-.896-.942l-.84-8.065c-.057-.624.25-1.095.779-1.095h1.91c.528.005.84.476.784 1.1z"}))},success:function(e){return o.createElement(g,{...e},o.createElement("path",{d:"M12 0a12 12 0 1012 12A12.014 12.014 0 0012 0zm6.927 8.2l-6.845 9.289a1.011 1.011 0 01-1.43.188l-4.888-3.908a1 1 0 111.25-1.562l4.076 3.261 6.227-8.451a1 1 0 111.61 1.183z"}))},error:function(e){return o.createElement(g,{...e},o.createElement("path",{d:"M11.983 0a12.206 12.206 0 00-8.51 3.653A11.8 11.8 0 000 12.207 11.779 11.779 0 0011.8 24h.214A12.111 12.111 0 0024 11.791 11.766 11.766 0 0011.983 0zM10.5 16.542a1.476 1.476 0 011.449-1.53h.027a1.527 1.527 0 011.523 1.47 1.475 1.475 0 01-1.449 1.53h-.027a1.529 1.529 0 01-1.523-1.47zM11 12.5v-6a1 1 0 012 0v6a1 1 0 11-2 0z"}))},spinner:function(){return o.createElement("div",{className:"Toastify__spinner"})}};function y(e){const[,t]=(0,o.useReducer)((e=>e+1),0),[n,s]=(0,o.useState)([]),a=(0,o.useRef)(null),d=(0,o.useRef)(new Map).current,p=e=>-1!==n.indexOf(e),g=(0,o.useRef)({toastKey:1,displayedToast:0,count:0,queue:[],props:e,containerId:null,isToastActive:p,getToast:e=>d.get(e)}).current;function y(e){let{containerId:t}=e;const{limit:n}=g.props;!n||t&&g.containerId!==t||(g.count-=g.queue.length,g.queue=[])}function v(e){s((t=>null==e?[]:t.filter((t=>t!==e))))}function T(){const{toastContent:e,toastProps:t,staleId:n}=g.queue.shift();C(e,t,n)}function E(e,n){let{delay:s,staleId:p,...y}=n;if(!u(e)||function(e){return!a.current||g.props.enableMultiContainer&&e.containerId!==g.props.containerId||d.has(e.toastId)&&null==e.updateId}(y))return;const{toastId:E,updateId:b,data:_}=y,{props:I}=g,L=()=>v(E),O=null==b;O&&g.count++;const N={...I,style:I.toastStyle,key:g.toastKey++,...Object.fromEntries(Object.entries(y).filter((e=>{let[t,n]=e;return null!=n}))),toastId:E,updateId:b,data:_,closeToast:L,isIn:!1,className:c(y.className||I.toastClassName),bodyClassName:c(y.bodyClassName||I.bodyClassName),progressClassName:c(y.progressClassName||I.progressClassName),autoClose:!y.isLoading&&(R=y.autoClose,w=I.autoClose,!1===R||r(R)&&R>0?R:w),deleteToast(){const e=f(d.get(E),"removed");d.delete(E),m.emit(4,e);const n=g.queue.length;if(g.count=null==E?g.count-g.displayedToast:g.count-1,g.count<0&&(g.count=0),n>0){const e=null==E?g.props.limit:1;if(1===n||1===e)g.displayedToast++,T();else{const t=e>n?n:e;g.displayedToast=t;for(let e=0;e<t;e++)T()}}else t()}};var R,w;N.iconOut=function(e){let{theme:t,type:n,isLoading:s,icon:a}=e,c=null;const u={theme:t,type:n};return!1===a||(l(a)?c=a(u):(0,o.isValidElement)(a)?c=(0,o.cloneElement)(a,u):i(a)||r(a)?c=a:s?c=h.spinner():(e=>e in h)(n)&&(c=h[n](u))),c}(N),l(y.onOpen)&&(N.onOpen=y.onOpen),l(y.onClose)&&(N.onClose=y.onClose),N.closeButton=I.closeButton,!1===y.closeButton||u(y.closeButton)?N.closeButton=y.closeButton:!0===y.closeButton&&(N.closeButton=!u(I.closeButton)||I.closeButton);let k=e;(0,o.isValidElement)(e)&&!i(e.type)?k=(0,o.cloneElement)(e,{closeToast:L,toastProps:N,data:_}):l(e)&&(k=e({closeToast:L,toastProps:N,data:_})),I.limit&&I.limit>0&&g.count>I.limit&&O?g.queue.push({toastContent:k,toastProps:N,staleId:p}):r(s)?setTimeout((()=>{C(k,N,p)}),s):C(k,N,p)}function C(e,t,n){const{toastId:o}=t;n&&d.delete(n);const a={content:e,props:t};d.set(o,a),s((e=>[...e,o].filter((e=>e!==n)))),m.emit(4,f(a,null==a.props.updateId?"added":"updated"))}return(0,o.useEffect)((()=>(g.containerId=e.containerId,m.cancelEmit(3).on(0,E).on(1,(e=>a.current&&v(e))).on(5,y).emit(2,g),()=>{d.clear(),m.emit(3,g)})),[]),(0,o.useEffect)((()=>{g.props=e,g.isToastActive=p,g.displayedToast=n.length})),{getToastToRender:function(t){const n=new Map,o=Array.from(d.values());return e.newestOnTop&&o.reverse(),o.forEach((e=>{const{position:t}=e.props;n.has(t)||n.set(t,[]),n.get(t).push(e)})),Array.from(n,(e=>t(e[0],e[1])))},containerRef:a,isToastActive:p}}function v(e){return e.targetTouches&&e.targetTouches.length>=1?e.targetTouches[0].clientX:e.clientX}function T(e){return e.targetTouches&&e.targetTouches.length>=1?e.targetTouches[0].clientY:e.clientY}function E(e){const[t,n]=(0,o.useState)(!1),[s,a]=(0,o.useState)(!1),r=(0,o.useRef)(null),i=(0,o.useRef)({start:0,x:0,y:0,delta:0,removalDistance:0,canCloseOnClick:!0,canDrag:!1,boundingRect:null,didMove:!1}).current,c=(0,o.useRef)(e),{autoClose:u,pauseOnHover:d,closeToast:p,onClick:f,closeOnClick:m}=e;function g(t){if(e.draggable){"touchstart"===t.nativeEvent.type&&t.nativeEvent.preventDefault(),i.didMove=!1,document.addEventListener("mousemove",C),document.addEventListener("mouseup",b),document.addEventListener("touchmove",C),document.addEventListener("touchend",b);const n=r.current;i.canCloseOnClick=!0,i.canDrag=!0,i.boundingRect=n.getBoundingClientRect(),n.style.transition="",i.x=v(t.nativeEvent),i.y=T(t.nativeEvent),"x"===e.draggableDirection?(i.start=i.x,i.removalDistance=n.offsetWidth*(e.draggablePercent/100)):(i.start=i.y,i.removalDistance=n.offsetHeight*(80===e.draggablePercent?1.5*e.draggablePercent:e.draggablePercent/100))}}function h(t){if(i.boundingRect){const{top:n,bottom:o,left:s,right:a}=i.boundingRect;"touchend"!==t.nativeEvent.type&&e.pauseOnHover&&i.x>=s&&i.x<=a&&i.y>=n&&i.y<=o?E():y()}}function y(){n(!0)}function E(){n(!1)}function C(n){const o=r.current;i.canDrag&&o&&(i.didMove=!0,t&&E(),i.x=v(n),i.y=T(n),i.delta="x"===e.draggableDirection?i.x-i.start:i.y-i.start,i.start!==i.x&&(i.canCloseOnClick=!1),o.style.transform=`translate${e.draggableDirection}(${i.delta}px)`,o.style.opacity=""+(1-Math.abs(i.delta/i.removalDistance)))}function b(){document.removeEventListener("mousemove",C),document.removeEventListener("mouseup",b),document.removeEventListener("touchmove",C),document.removeEventListener("touchend",b);const t=r.current;if(i.canDrag&&i.didMove&&t){if(i.canDrag=!1,Math.abs(i.delta)>i.removalDistance)return a(!0),void e.closeToast();t.style.transition="transform 0.2s, opacity 0.2s",t.style.transform=`translate${e.draggableDirection}(0)`,t.style.opacity="1"}}(0,o.useEffect)((()=>{c.current=e})),(0,o.useEffect)((()=>(r.current&&r.current.addEventListener("d",y,{once:!0}),l(e.onOpen)&&e.onOpen((0,o.isValidElement)(e.children)&&e.children.props),()=>{const e=c.current;l(e.onClose)&&e.onClose((0,o.isValidElement)(e.children)&&e.children.props)})),[]),(0,o.useEffect)((()=>(e.pauseOnFocusLoss&&(document.hasFocus()||E(),window.addEventListener("focus",y),window.addEventListener("blur",E)),()=>{e.pauseOnFocusLoss&&(window.removeEventListener("focus",y),window.removeEventListener("blur",E))})),[e.pauseOnFocusLoss]);const _={onMouseDown:g,onTouchStart:g,onMouseUp:h,onTouchEnd:h};return u&&d&&(_.onMouseEnter=E,_.onMouseLeave=y),m&&(_.onClick=e=>{f&&f(e),i.canCloseOnClick&&p()}),{playToast:y,pauseToast:E,isRunning:t,preventExitTransition:s,toastRef:r,eventHandlers:_}}function C(e){let{closeToast:t,theme:n,ariaLabel:s="close"}=e;return o.createElement("button",{className:`Toastify__close-button Toastify__close-button--${n}`,type:"button",onClick:e=>{e.stopPropagation(),t(e)},"aria-label":s},o.createElement("svg",{"aria-hidden":"true",viewBox:"0 0 14 16"},o.createElement("path",{fillRule:"evenodd",d:"M7.71 8.23l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75L1 11.98l3.75-3.75L1 4.48 2.48 3l3.75 3.75L9.98 3l1.48 1.48-3.75 3.75z"})))}function b(e){let{delay:t,isRunning:n,closeToast:s,type:r="default",hide:i,className:c,style:u,controlledProgress:d,progress:p,rtl:f,isIn:m,theme:g}=e;const h=i||d&&0===p,y={...u,animationDuration:`${t}ms`,animationPlayState:n?"running":"paused",opacity:h?0:1};d&&(y.transform=`scaleX(${p})`);const v=a("Toastify__progress-bar",d?"Toastify__progress-bar--controlled":"Toastify__progress-bar--animated",`Toastify__progress-bar-theme--${g}`,`Toastify__progress-bar--${r}`,{"Toastify__progress-bar--rtl":f}),T=l(c)?c({rtl:f,type:r,defaultClassName:v}):a(v,c);return o.createElement("div",{role:"progressbar","aria-hidden":h?"true":"false","aria-label":"notification timer",className:T,style:y,[d&&p>=1?"onTransitionEnd":"onAnimationEnd"]:d&&p<1?null:()=>{m&&s()}})}const _=e=>{const{isRunning:t,preventExitTransition:n,toastRef:s,eventHandlers:r}=E(e),{closeButton:i,children:c,autoClose:u,onClick:d,type:p,hideProgressBar:f,closeToast:m,transition:g,position:h,className:y,style:v,bodyClassName:T,bodyStyle:_,progressClassName:I,progressStyle:L,updateId:O,role:N,progress:R,rtl:w,toastId:k,deleteToast:M,isIn:x,isLoading:$,iconOut:B,closeOnClick:P,theme:A}=e,D=a("Toastify__toast",`Toastify__toast-theme--${A}`,`Toastify__toast--${p}`,{"Toastify__toast--rtl":w},{"Toastify__toast--close-on-click":P}),z=l(y)?y({rtl:w,position:h,type:p,defaultClassName:D}):a(D,y),F=!!R||!u,S={closeToast:m,type:p,theme:A};let H=null;return!1===i||(H=l(i)?i(S):(0,o.isValidElement)(i)?(0,o.cloneElement)(i,S):C(S)),o.createElement(g,{isIn:x,done:M,position:h,preventExitTransition:n,nodeRef:s},o.createElement("div",{id:k,onClick:d,className:z,...r,style:v,ref:s},o.createElement("div",{...x&&{role:N},className:l(T)?T({type:p}):a("Toastify__toast-body",T),style:_},null!=B&&o.createElement("div",{className:a("Toastify__toast-icon",{"Toastify--animate-icon Toastify__zoom-enter":!$})},B),o.createElement("div",null,c)),H,o.createElement(b,{...O&&!F?{key:`pb-${O}`}:{},rtl:w,theme:A,delay:u,isRunning:t,isIn:x,closeToast:m,hide:f,type:p,style:L,className:I,controlledProgress:F,progress:R||0})))},I=function(e,t){return void 0===t&&(t=!1),{enter:`Toastify--animate Toastify__${e}-enter`,exit:`Toastify--animate Toastify__${e}-exit`,appendPosition:t}},L=p(I("bounce",!0)),O=p(I("slide",!0)),N=p(I("zoom")),R=p(I("flip")),w=(0,o.forwardRef)(((e,t)=>{const{getToastToRender:n,containerRef:s,isToastActive:r}=y(e),{className:i,style:u,rtl:d,containerId:p}=e;function f(e){const t=a("Toastify__toast-container",`Toastify__toast-container--${e}`,{"Toastify__toast-container--rtl":d});return l(i)?i({position:e,rtl:d,defaultClassName:t}):a(t,c(i))}return(0,o.useEffect)((()=>{t&&(t.current=s.current)}),[]),o.createElement("div",{ref:s,className:"Toastify",id:p},n(((e,t)=>{const n=t.length?{...u}:{...u,pointerEvents:"none"};return o.createElement("div",{className:f(e),style:n,key:`container-${e}`},t.map(((e,n)=>{let{content:s,props:a}=e;return o.createElement(_,{...a,isIn:r(a.toastId),style:{...a.style,"--nth":n+1,"--len":t.length},key:`toast-${a.key}`},s)})))})))}));w.displayName="ToastContainer",w.defaultProps={position:"top-right",transition:L,autoClose:5e3,closeButton:C,pauseOnHover:!0,pauseOnFocusLoss:!0,closeOnClick:!0,draggable:!0,draggablePercent:80,draggableDirection:"x",role:"alert",theme:"light"};let k,M=new Map,x=[],$=1;function B(){return""+$++}function P(e){return e&&(i(e.toastId)||r(e.toastId))?e.toastId:B()}function A(e,t){return M.size>0?m.emit(0,e,t):x.push({content:e,options:t}),t.toastId}function D(e,t){return{...t,type:t&&t.type||e,toastId:P(t)}}function z(e){return(t,n)=>A(t,D(e,n))}function F(e,t){return A(e,D("default",t))}F.loading=(e,t)=>A(e,D("default",{isLoading:!0,autoClose:!1,closeOnClick:!1,closeButton:!1,draggable:!1,...t})),F.promise=function(e,t,n){let o,{pending:s,error:a,success:r}=t;s&&(o=i(s)?F.loading(s,n):F.loading(s.render,{...n,...s}));const c={isLoading:null,autoClose:null,closeOnClick:null,closeButton:null,draggable:null},u=(e,t,s)=>{if(null==t)return void F.dismiss(o);const a={type:e,...c,...n,data:s},r=i(t)?{render:t}:t;return o?F.update(o,{...a,...r}):F(r.render,{...a,...r}),s},d=l(e)?e():e;return d.then((e=>u("success",r,e))).catch((e=>u("error",a,e))),d},F.success=z("success"),F.info=z("info"),F.error=z("error"),F.warning=z("warning"),F.warn=F.warning,F.dark=(e,t)=>A(e,D("default",{theme:"dark",...t})),F.dismiss=e=>{M.size>0?m.emit(1,e):x=x.filter((t=>null!=e&&t.options.toastId!==e))},F.clearWaitingQueue=function(e){return void 0===e&&(e={}),m.emit(5,e)},F.isActive=e=>{let t=!1;return M.forEach((n=>{n.isToastActive&&n.isToastActive(e)&&(t=!0)})),t},F.update=function(e,t){void 0===t&&(t={}),setTimeout((()=>{const n=function(e,t){let{containerId:n}=t;const o=M.get(n||k);return o&&o.getToast(e)}(e,t);if(n){const{props:o,content:s}=n,a={delay:100,...o,...t,toastId:t.toastId||e,updateId:B()};a.toastId!==e&&(a.staleId=e);const r=a.render||s;delete a.render,A(r,a)}}),0)},F.done=e=>{F.update(e,{progress:1})},F.onChange=e=>(m.on(4,e),()=>{m.off(4,e)}),F.POSITION={TOP_LEFT:"top-left",TOP_RIGHT:"top-right",TOP_CENTER:"top-center",BOTTOM_LEFT:"bottom-left",BOTTOM_RIGHT:"bottom-right",BOTTOM_CENTER:"bottom-center"},F.TYPE={INFO:"info",SUCCESS:"success",WARNING:"warning",ERROR:"error",DEFAULT:"default"},m.on(2,(e=>{k=e.containerId||e,M.set(k,e),x.forEach((e=>{m.emit(0,e.content,e.options)})),x=[]})).on(3,(e=>{M.delete(e.containerId||e),0===M.size&&m.off(0).off(1).off(5)}))}}]);