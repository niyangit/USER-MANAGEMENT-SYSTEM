const API='http://127.0.0.1:8000';
async function registerUser(){
 const r=await fetch(API+'/api/v1/users',{method:'POST',headers:{'Content-Type':'application/json'},
body: JSON.stringify({
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value
})});
 const d=await r.json();
 if(d.status==='success'){alert('Registered');location.href='login.html';}
 else alert(d.error.message);
}

