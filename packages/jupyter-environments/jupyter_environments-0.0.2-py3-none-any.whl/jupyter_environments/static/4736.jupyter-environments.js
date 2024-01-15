/*! For license information please see 4736.jupyter-environments.js.LICENSE.txt */
(()=>{"use strict";const t=Symbol("Comlink.proxy"),e=Symbol("Comlink.endpoint"),s=Symbol("Comlink.releaseProxy"),i=Symbol("Comlink.finalizer"),a=Symbol("Comlink.thrown"),n=t=>"object"==typeof t&&null!==t||"function"==typeof t,r=new Map([["proxy",{canHandle:e=>n(e)&&e[t],serialize(t){const{port1:e,port2:s}=new MessageChannel;return o(t,e),[s,[s]]},deserialize:t=>(t.start(),d(t,[],undefined))}],["throw",{canHandle:t=>n(t)&&a in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function o(e,s=globalThis,n=["*"]){s.addEventListener("message",(function r(p){if(!p||!p.data)return;if(!function(t,e){for(const s of t){if(e===s||"*"===s)return!0;if(s instanceof RegExp&&s.test(e))return!0}return!1}(n,p.origin))return void console.warn(`Invalid origin '${p.origin}' for comlink proxy`);const{id:c,type:u,path:h}=Object.assign({path:[]},p.data),d=(p.data.argumentList||[]).map(f);let m;try{const s=h.slice(0,-1).reduce(((t,e)=>t[e]),e),i=h.reduce(((t,e)=>t[e]),e);switch(u){case"GET":m=i;break;case"SET":s[h.slice(-1)[0]]=f(p.data.value),m=!0;break;case"APPLY":m=i.apply(s,d);break;case"CONSTRUCT":m=function(e){return Object.assign(e,{[t]:!0})}(new i(...d));break;case"ENDPOINT":{const{port1:t,port2:s}=new MessageChannel;o(e,s),m=function(t,e){return _.set(t,e),t}(t,[t])}break;case"RELEASE":m=void 0;break;default:return}}catch(t){m={value:t,[a]:0}}Promise.resolve(m).catch((t=>({value:t,[a]:0}))).then((t=>{const[a,n]=y(t);s.postMessage(Object.assign(Object.assign({},a),{id:c}),n),"RELEASE"===u&&(s.removeEventListener("message",r),l(s),i in e&&"function"==typeof e[i]&&e[i]())})).catch((t=>{const[e,i]=y({value:new TypeError("Unserializable return value"),[a]:0});s.postMessage(Object.assign(Object.assign({},e),{id:c}),i)}))})),s.start&&s.start()}function l(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function p(t){if(t)throw new Error("Proxy has been released and is not useable")}function c(t){return g(t,{type:"RELEASE"}).then((()=>{l(t)}))}const u=new WeakMap,h="FinalizationRegistry"in globalThis&&new FinalizationRegistry((t=>{const e=(u.get(t)||0)-1;u.set(t,e),0===e&&c(t)}));function d(t,i=[],a=function(){}){let n=!1;const r=new Proxy(a,{get(e,a){if(p(n),a===s)return()=>{!function(t){h&&h.unregister(t)}(r),c(t),n=!0};if("then"===a){if(0===i.length)return{then:()=>r};const e=g(t,{type:"GET",path:i.map((t=>t.toString()))}).then(f);return e.then.bind(e)}return d(t,[...i,a])},set(e,s,a){p(n);const[r,o]=y(a);return g(t,{type:"SET",path:[...i,s].map((t=>t.toString())),value:r},o).then(f)},apply(s,a,r){p(n);const o=i[i.length-1];if(o===e)return g(t,{type:"ENDPOINT"}).then(f);if("bind"===o)return d(t,i.slice(0,-1));const[l,c]=m(r);return g(t,{type:"APPLY",path:i.map((t=>t.toString())),argumentList:l},c).then(f)},construct(e,s){p(n);const[a,r]=m(s);return g(t,{type:"CONSTRUCT",path:i.map((t=>t.toString())),argumentList:a},r).then(f)}});return function(t,e){const s=(u.get(e)||0)+1;u.set(e,s),h&&h.register(t,e,t)}(r,t),r}function m(t){const e=t.map(y);return[e.map((t=>t[0])),(s=e.map((t=>t[1])),Array.prototype.concat.apply([],s))];var s}const _=new WeakMap;function y(t){for(const[e,s]of r)if(s.canHandle(t)){const[i,a]=s.serialize(t);return[{type:"HANDLER",name:e,value:i},a]}return[{type:"RAW",value:t},_.get(t)||[]]}function f(t){switch(t.type){case"HANDLER":return r.get(t.name).deserialize(t.value);case"RAW":return t.value}}function g(t,e,s){return new Promise((i=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(s){s.data&&s.data.id&&s.data.id===a&&(t.removeEventListener("message",e),i(s.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:a},e),s)}))}o(new class{constructor(){this._options=null,this._initializer=null,this._localPath="",this._driveName="",this._initialized=new Promise(((t,e)=>{this._initializer={resolve:t,reject:e}}))}async initialize(t){var e;if(this._options=t,t.location.includes(":")){const e=t.location.split(":");this._driveName=e[0],this._localPath=e[1]}else this._driveName="",this._localPath=t.location;await this.initRuntime(t),await this.initPackageManager(t),await this.initKernel(t),await this.initGlobals(t),null===(e=this._initializer)||void 0===e||e.resolve()}async initRuntime(t){const{pyodideUrl:e,indexUrl:s}=t;if(e.endsWith(".mjs")){const t=await import(e);this._pyodide=await t.loadPyodide({indexURL:s})}else importScripts(e),this._pyodide=await self.loadPyodide({indexURL:s})}async initPackageManager(t){if(!this._options)throw new Error("Uninitialized");const{pipliteWheelUrl:e,disablePyPIFallback:s,pipliteUrls:i}=this._options;await this._pyodide.loadPackage(["micropip"]),await this._pyodide.runPythonAsync(`\n      import micropip\n      await micropip.install('${e}', keep_going=True)\n      import piplite.piplite\n      piplite.piplite._PIPLITE_DISABLE_PYPI = ${s?"True":"False"}\n      piplite.piplite._PIPLITE_URLS = ${JSON.stringify(i)}\n    `)}async initKernel(t){await this._pyodide.runPythonAsync("\n      await piplite.install(['matplotlib', 'ipykernel'], keep_going=True);\n      await piplite.install(['pyolite'], keep_going=True);\n      await piplite.install(['ipython'], keep_going=True);\n      import pyolite\n    "),t.mountDrive&&this._localPath&&await this._pyodide.runPythonAsync(`\n        import os;\n        os.chdir("${this._localPath}");\n      `)}async initGlobals(t){const{globals:e}=this._pyodide;this._kernel=e.get("pyolite").kernel_instance.copy(),this._stdout_stream=e.get("pyolite").stdout_stream.copy(),this._stderr_stream=e.get("pyolite").stderr_stream.copy(),this._interpreter=this._kernel.interpreter.copy(),this._interpreter.send_comm=this.sendComm.bind(this)}mapToObject(t){const e=t instanceof Array?[]:{};return t.forEach(((t,s)=>{e[s]=t instanceof Map||t instanceof Array?this.mapToObject(t):t})),e}formatResult(t){if(!this._pyodide.isPyProxy(t))return t;const e=t.toJs();return this.mapToObject(e)}async setup(t){await this._initialized,this._kernel._parent_header=this._pyodide.toPy(t)}async execute(t,e){await this.setup(e);const s=(t,e)=>{const s={name:this.formatResult(t),text:this.formatResult(e)};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:s,type:"stream"})};this._stdout_stream.publish_stream_callback=s,this._stderr_stream.publish_stream_callback=s,this._interpreter.display_pub.clear_output_callback=t=>{const e={wait:this.formatResult(t)};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:e,type:"clear_output"})},this._interpreter.display_pub.display_data_callback=(t,e,s)=>{const i={data:this.formatResult(t),metadata:this.formatResult(e),transient:this.formatResult(s)};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:i,type:"display_data"})},this._interpreter.display_pub.update_display_data_callback=(t,e,s)=>{const i={data:this.formatResult(t),metadata:this.formatResult(e),transient:this.formatResult(s)};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:i,type:"update_display_data"})},this._interpreter.displayhook.publish_execution_result=(t,e,s)=>{const i={execution_count:t,data:this.formatResult(e),metadata:this.formatResult(s)};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:i,type:"execute_result"})},this._interpreter.input=this.input.bind(this),this._interpreter.getpass=this.getpass.bind(this);const i=await this._kernel.run(t.code),a=this.formatResult(i);return"error"===a.status&&((t,e,s)=>{const i={ename:t,evalue:e,traceback:s};postMessage({parentHeader:this.formatResult(this._kernel._parent_header).header,bundle:i,type:"execute_error"})})(a.ename,a.evalue,a.traceback),a}async complete(t,e){await this.setup(e);const s=this._kernel.complete(t.code,t.cursor_pos);return this.formatResult(s)}async inspect(t,e){await this.setup(e);const s=this._kernel.inspect(t.code,t.cursor_pos,t.detail_level);return this.formatResult(s)}async isComplete(t,e){await this.setup(e);const s=this._kernel.is_complete(t.code);return this.formatResult(s)}async commInfo(t,e){await this.setup(e);const s=this._kernel.comm_info(t.target_name);return{comms:this.formatResult(s),status:"ok"}}async commOpen(t,e){await this.setup(e);const s=this._kernel.comm_manager.comm_open(this._pyodide.toPy(t));return this.formatResult(s)}async commMsg(t,e){await this.setup(e);const s=this._kernel.comm_manager.comm_msg(this._pyodide.toPy(t));return this.formatResult(s)}async commClose(t,e){await this.setup(e);const s=this._kernel.comm_manager.comm_close(this._pyodide.toPy(t));return this.formatResult(s)}async inputReply(t,e){await this.setup(e),this._resolveInputReply(t)}async sendInputRequest(t,e){const s={prompt:t,password:e};postMessage({type:"input_request",parentHeader:this.formatResult(this._kernel._parent_header).header,content:s})}async getpass(t){t=void 0===t?"":t,await this.sendInputRequest(t,!0);const e=new Promise((t=>{this._resolveInputReply=t}));return(await e).value}async input(t){t=void 0===t?"":t,await this.sendInputRequest(t,!1);const e=new Promise((t=>{this._resolveInputReply=t}));return(await e).value}async sendComm(t,e,s,i,a){postMessage({type:t,content:this.formatResult(e),metadata:this.formatResult(s),ident:this.formatResult(i),buffers:this.formatResult(a),parentHeader:this.formatResult(this._kernel._parent_header).header})}})})();