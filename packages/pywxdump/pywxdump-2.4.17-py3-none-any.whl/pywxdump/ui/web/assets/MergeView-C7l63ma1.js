import{h}from"./axios-jGQk5ZQo.js";import{d as m,r,e as i,o as y,c as f,a as e,f as o,g as v,h as b}from"./index-FGVSFSnI.js";const g={style:{"background-color":"#d2d2fa",height:"100vh",display:"grid","place-items":"center"}},w={style:{"background-color":"#fff",width:"70%",height:"70%","border-radius":"10px",padding:"20px",overflow:"auto"}},V=e("div",{style:{display:"flex","justify-content":"space-between","align-items":"center"}},[e("div",{style:{"font-size":"20px","font-weight":"bold"}},"解密-微信数据库"),e("div",{style:{display:"flex","justify-content":"space-between","align-items":"center"}})],-1),x={style:{"margin-top":"20px"}},k=e("label",null,"密钥（key）: ",-1),C=e("br",null,null,-1),P=e("label",null,"微信数据库路径: ",-1),B=e("br",null,null,-1),E=m({__name:"MergeView",setup(N){const n=r(""),a=r(""),s=r(""),c=async()=>{try{s.value=await h.post("/api/merge",{dbPath:n.value,outPath:a.value})}catch(u){return console.error("Error fetching data:",u),[]}};return(u,t)=>{const d=i("el-input"),p=i("el-button"),_=i("el-divider");return y(),f("div",g,[e("div",w,[V,e("div",x,[k,o(d,{placeholder:"数据库路径（文件夹，并且确保文件夹下的db文件已经解密）：",modelValue:n.value,"onUpdate:modelValue":t[0]||(t[0]=l=>n.value=l),style:{width:"50%"}},null,8,["modelValue"]),C,P,o(d,{placeholder:"输出文件夹",modelValue:a.value,"onUpdate:modelValue":t[1]||(t[1]=l=>a.value=l),style:{width:"50%"}},null,8,["modelValue"]),B,o(p,{style:{"margin-top":"10px",width:"50%"},type:"success",onClick:c},{default:v(()=>[b("合并")]),_:1}),o(_),o(d,{type:"textarea",rows:10,readonly:"",placeholder:"解密后数据库路径",modelValue:s.value,"onUpdate:modelValue":t[2]||(t[2]=l=>s.value=l),style:{width:"100%"}},null,8,["modelValue"])])])])}}});export{E as default};
