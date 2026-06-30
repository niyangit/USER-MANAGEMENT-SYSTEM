const token=localStorage.getItem('token');
document.getElementById('profile').textContent=JSON.stringify(JSON.parse(atob(token.split('.')[1])),null,2);