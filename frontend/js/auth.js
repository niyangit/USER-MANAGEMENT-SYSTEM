const API='https://user-management-system-36zz.onrender.com';
async function login(){
 const r=await fetch(API+'/api/v1/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:email.value,password:password.value})});
 const d=await r.json();
 if(d.status==='success'){localStorage.setItem('token',d.data.access_token);location.href='dashboard.html';}
 else alert(d.error.message);
}
function logout(){localStorage.removeItem('token');location.href='login.html';}
