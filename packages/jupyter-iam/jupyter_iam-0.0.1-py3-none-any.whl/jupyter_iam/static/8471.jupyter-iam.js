"use strict";(self.webpackChunk_datalayer_jupyter_iam=self.webpackChunk_datalayer_jupyter_iam||[]).push([[8471],{68471:(e,t,s)=>{s.d(t,{MN:()=>n,WQ:()=>v,ko:()=>l,_3:()=>m,A_:()=>f,Jy:()=>c,U:()=>r});var i=s(56769);function n(e){const{spacing:t,children:s,className:n,...a}=e,o=i.Children.count(s);return i.createElement("div",{className:`jp-StatusBar-GroupItem ${n||""}`,...a},i.Children.map(s,((e,s)=>0===s?i.createElement("div",{style:{marginRight:`${t}px`}},e):s===o-1?i.createElement("div",{style:{marginLeft:`${t}px`}},e):i.createElement("div",{style:{margin:`0px ${t}px`}},e))))}var a=s(59965),o=s(92279);function r(e){const t=new d(e);return e.startHidden||t.launch(),t}class d extends o.$L{constructor(e){super(),this._body=e.body,this._body.addClass("jp-StatusBar-HoverItem"),this._anchor=e.anchor,this._align=e.align,e.hasDynamicSize&&(this._observer=new ResizeObserver((()=>{this.update()}))),(this.layout=new o.LN).addWidget(e.body),this._body.node.addEventListener("resize",(()=>{this.update()}))}launch(){this._setGeometry(),o.$L.attach(this,document.body),this.update(),this._anchor.addClass("jp-mod-clicked"),this._anchor.removeClass("jp-mod-highlight")}onUpdateRequest(e){this._setGeometry(),super.onUpdateRequest(e)}onAfterAttach(e){var t;document.addEventListener("click",this,!1),this.node.addEventListener("keydown",this,!1),window.addEventListener("resize",this,!1),null===(t=this._observer)||void 0===t||t.observe(this._body.node)}onBeforeDetach(e){var t;null===(t=this._observer)||void 0===t||t.disconnect(),document.removeEventListener("click",this,!1),this.node.removeEventListener("keydown",this,!1),window.removeEventListener("resize",this,!1)}onResize(){this.update()}dispose(){var e;null===(e=this._observer)||void 0===e||e.disconnect(),super.dispose(),this._anchor.removeClass("jp-mod-clicked"),this._anchor.addClass("jp-mod-highlight")}handleEvent(e){switch(e.type){case"keydown":this._evtKeydown(e);break;case"click":this._evtClick(e);break;case"resize":this.onResize()}}_evtClick(e){!e.target||this._body.node.contains(e.target)||this._anchor.node.contains(e.target)||this.dispose()}_evtKeydown(e){27===e.keyCode&&(e.stopPropagation(),e.preventDefault(),this.dispose())}_setGeometry(){let e=0;const t=this._anchor.node.getBoundingClientRect(),s=this._body.node.getBoundingClientRect();"right"===this._align&&(e=-(s.width-t.width));const i=window.getComputedStyle(this._body.node);a.Y.setGeometry({anchor:t,host:document.body,maxHeight:500,minHeight:20,node:this._body.node,offset:{horizontal:e},privilege:"forceAbove",style:i})}}function l(e){const{width:t,percentage:s,...n}=e;return i.createElement("div",{className:"jp-Statusbar-ProgressBar-progress-bar",role:"progressbar","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":s},i.createElement(h,{...{percentage:s,...n},contentWidth:t}))}function h(e){return i.createElement("div",{style:{width:`${e.percentage}%`}},i.createElement("p",null,e.content))}function c(e){const{title:t,source:s,className:n,...a}=e;return i.createElement("span",{className:`jp-StatusBar-TextItem ${n}`,title:t,...a},s)}function m(e){return i.createElement("div",{className:"jp-Statusbar-ProgressCircle",role:"progressbar","aria-label":e.label||"Unlabelled progress circle","aria-valuemin":0,"aria-valuemax":100,"aria-valuenow":e.progress},i.createElement("svg",{viewBox:"0 0 250 250"},i.createElement("circle",{cx:"125",cy:"125",r:"104",stroke:"var(--jp-inverse-layout-color3)",strokeWidth:"20",fill:"none"}),i.createElement("path",{transform:"translate(125,125) scale(.9)",d:(e=>{const t=Math.max(3.6*e,.1),s=t*Math.PI/180,i=104*Math.sin(s),n=-104*Math.cos(s);return"M 0 0 v -104 A 104 104 1 "+(t<180?1:0)+" 0 "+i.toFixed(4)+" "+n.toFixed(4)+" z"})(e.progress),fill:"var(--jp-inverse-layout-color3)"})))}var u,p=s(46931),g=s(16781);class f extends o.$L{constructor(){super(),this._leftRankItems=[],this._rightRankItems=[],this._statusItems={},this._disposables=new g.DisposableSet,this.addClass("jp-StatusBar-Widget");const e=this.layout=new o.LN,t=this._leftSide=new o.s_,s=this._middlePanel=new o.s_,i=this._rightSide=new o.s_;t.addClass("jp-StatusBar-Left"),s.addClass("jp-StatusBar-Middle"),i.addClass("jp-StatusBar-Right"),e.addWidget(t),e.addWidget(s),e.addWidget(i)}registerStatusItem(e,t){if(e in this._statusItems)throw new Error(`Status item ${e} already registered.`);const s={...u.statusItemDefaults,...t},{align:i,item:n,rank:a}=s,o=()=>{this._refreshItem(e)};s.activeStateChanged&&s.activeStateChanged.connect(o);const r={id:e,rank:a};if(s.item.addClass("jp-StatusBar-Item"),this._statusItems[e]=s,"left"===i){const e=this._findInsertIndex(this._leftRankItems,r);-1===e?(this._leftSide.addWidget(n),this._leftRankItems.push(r)):(p.RO.insert(this._leftRankItems,e,r),this._leftSide.insertWidget(e,n))}else if("right"===i){const e=this._findInsertIndex(this._rightRankItems,r);-1===e?(this._rightSide.addWidget(n),this._rightRankItems.push(r)):(p.RO.insert(this._rightRankItems,e,r),this._rightSide.insertWidget(e,n))}else this._middlePanel.addWidget(n);this._refreshItem(e);const d=new g.DisposableDelegate((()=>{delete this._statusItems[e],s.activeStateChanged&&s.activeStateChanged.disconnect(o),n.parent=null,n.dispose()}));return this._disposables.add(d),d}dispose(){this._leftRankItems.length=0,this._rightRankItems.length=0,this._disposables.dispose(),super.dispose()}onUpdateRequest(e){this._refreshAll(),super.onUpdateRequest(e)}_findInsertIndex(e,t){return p.RO.findFirstIndex(e,(e=>e.rank>t.rank))}_refreshItem(e){const t=this._statusItems[e];t.isActive()?(t.item.show(),t.item.update()):t.item.hide()}_refreshAll(){Object.keys(this._statusItems).forEach((e=>{this._refreshItem(e)}))}}!function(e){e.statusItemDefaults={align:"left",rank:0,isActive:()=>!0,activeStateChanged:void 0}}(u||(u={}));const v=new(s(47963).Token)("@jupyterlab/statusbar:IStatusBar","A service for the status bar on the application. Use this if you want to add new status bar items.")},59965:(e,t,s)=>{s.d(t,{Y:()=>a});const i="jp-HoverBox",n="-1000";var a;!function(e){e.setGeometry=function(e){const{anchor:t,host:s,node:a,privilege:o,outOfViewDisplay:r}=e,d=s.getBoundingClientRect();a.classList.contains(i)||a.classList.add(i),a.style.visibility&&(a.style.visibility=""),""===a.style.zIndex&&(a.style.zIndex=""),a.style.maxHeight="",a.style.marginTop="";const l=e.style||window.getComputedStyle(a),h=t.top-d.top,c=d.bottom-t.bottom,m=parseInt(l.marginTop,10)||0,u=parseInt(l.marginLeft,10)||0,p=parseInt(l.minHeight,10)||e.minHeight;let g=parseInt(l.maxHeight,10)||e.maxHeight;const f="forceAbove"!==o&&("forceBelow"===o||("above"===o?h<g&&h<c:c>=g||c>=h));if(f?g=Math.min(c-m,g):(g=Math.min(h,g),a.style.marginTop="0px"),a.style.maxHeight=`${g}px`,!(g>=p&&(c>=p||h>=p)))return a.style.zIndex=n,void(a.style.visibility="hidden");e.size?(a.style.width=`${e.size.width}px`,a.style.height=`${e.size.height}px`,a.style.contain="strict"):(a.style.contain="",a.style.width="auto",a.style.height="");const v=e.size?e.size.height:a.getBoundingClientRect().height,y=e.offset&&e.offset.vertical&&e.offset.vertical.above||0,_=e.offset&&e.offset.vertical&&e.offset.vertical.below||0;let b=f?d.bottom-c+_:d.top+h-v+y;a.style.top=`${Math.floor(b)}px`;const k=e.offset&&e.offset.horizontal||0;let w=t.left+k;a.style.left=`${Math.ceil(w)}px`;let I=a.getBoundingClientRect(),x=I.right;x>window.innerWidth&&(w-=x-window.innerWidth,x=window.innerWidth,a.style.left=`${Math.ceil(w)}px`),w<k-u&&(w=k-u,a.style.left=`${Math.ceil(w)}px`),a.style.zIndex="-1000";const C=I.bottom,S=s.contains(document.elementFromPoint(w,b)),R=s.contains(document.elementFromPoint(x,b)),E=s.contains(document.elementFromPoint(x,C)),z=s.contains(document.elementFromPoint(w,C));a.style.zIndex="";const j=S||R,B=z||E,$=S||z,L=E||R,W=C-b,M=x-w,A=b<d.top,H=C>d.bottom,P=w+u<d.left,D=x>d.right;let N=!1,F=!1,U=!1;if(A)switch((null==r?void 0:r.top)||"hidden-inside"){case"hidden-inside":j||(N=!0);break;case"hidden-outside":B||(N=!0);break;case"stick-inside":d.top>b&&(b=d.top,U=!0);break;case"stick-outside":d.top>C&&(b=d.top-W,U=!0)}if(H)switch((null==r?void 0:r.bottom)||"hidden-outside"){case"hidden-inside":B||(N=!0);break;case"hidden-outside":j||(N=!0);break;case"stick-inside":d.bottom<C&&(b=d.bottom-W,U=!0);break;case"stick-outside":d.bottom<b&&(b=d.bottom,U=!0)}if(P)switch((null==r?void 0:r.left)||"hidden-inside"){case"hidden-inside":$||(N=!0);break;case"hidden-outside":L||(N=!0);break;case"stick-inside":d.left>w+u&&(w=d.left-u,F=!0);break;case"stick-outside":d.left>x&&(w=d.left-u-M,F=!0)}if(D)switch((null==r?void 0:r.right)||"hidden-outside"){case"hidden-inside":L||(N=!0);break;case"hidden-outside":$||(N=!0);break;case"stick-inside":d.right<x&&(w=d.right-M,F=!0);break;case"stick-outside":d.right<w&&(w=d.right,F=!0)}N&&(a.style.zIndex=n,a.style.visibility="hidden"),F&&(a.style.left=`${Math.ceil(w)}px`),U&&(a.style.top=`${Math.ceil(b)}px`)}}(a||(a={}))}}]);