const API = 'https://user-management-system-36zz.onrender.com';

const token = localStorage.getItem('token');

async function validateToken() {

    if (!token) {

        window.location.href =
            'login.html';

        return false;
    }

    try {

        const response =
            await fetch(
                API +
                '/api/v1/auth/me',
                {
                    headers: {
                        Authorization:
                            'Bearer ' +
                            token
                    }
                }
            );

        const result =
            await response.json();

        if (
            result.status !==
            'success'
        ) {

            localStorage.removeItem(
                'token'
            );

            window.location.href =
                'login.html';

            return false;
        }

        return true;

    } catch {

        localStorage.removeItem(
            'token'
        );

        window.location.href =
            'login.html';

        return false;
    }
}

function showLoader() {

    const loader =
        document.getElementById("loader");

    if (loader) {
        loader.classList.remove("hidden");
    }
}

function hideLoader() {

    const loader =
        document.getElementById("loader");

    if (loader) {
        loader.classList.add("hidden");
    }
}

function parseJwt(token) {
    return JSON.parse(atob(token.split('.')[1]));
}

let payload = null;

if (token) {

    try {

        payload = parseJwt(token);

    } catch {

        localStorage.removeItem("token");

        window.location.href =
            "login.html";
    }
}

const roleBadge =
    document.getElementById(
        "roleBadge"
    );

if (roleBadge && payload) {

    roleBadge.innerHTML = `
    <span class="px-3 py-1 rounded bg-blue-600 text-white">
        ${payload.role}
    </span>
    `;
}
async function loadDashboard() {

    if (payload.role === 'admin') {
        await loadUsers();
    } else {
        await loadProfile();
    }
}

async function loadUsers() {

    showLoader();

    try {

        const response = await fetch(
            API + '/api/v1/users',
            {
                headers: {
                    Authorization: 'Bearer ' + token
                }
            }
        );

        const result = await response.json();

        if (result.status !== 'success') {
            alert(result.error.message);
            return;
        }

        let html = '';

        result.data.forEach(user => {

            html += `
            <tr>
                <td class="p-2">${user.id}</td>
                <td>${user.name}</td>
                <td>${user.email}</td>

                <td class="space-x-2">

                    <button
                        onclick="editUser(${user.id})"
                        class="bg-blue-500 text-white px-2 py-1 rounded"
                    >
                        Edit
                    </button>

                    <button
                        onclick="blockUser(${user.id})"
                        class="bg-yellow-500 text-white px-2 py-1 rounded"
                    >
                        Block
                    </button>

                    <button
                        onclick="deleteUser(${user.id})"
                        class="bg-red-500 text-white px-2 py-1 rounded"
                    >
                        Delete
                    </button>

                </td>
            </tr>
            `;
        });

        document.getElementById('users').innerHTML = html;

    } finally {

        hideLoader();
    }
}

async function loadProfile() {

    showLoader();

    try {

        const response = await fetch(
            API + `/api/v1/users/${payload.user_id}`,
            {
                headers: {
                    Authorization: 'Bearer ' + token
                }
            }
        );

        const result = await response.json();

        if (result.status !== 'success') {
            alert(result.error.message);
            return;
        }

        const user = result.data;

        document.body.innerHTML = `
        <div class="min-h-screen bg-slate-100 flex items-center justify-center">

            <div class="bg-white p-8 rounded-xl shadow w-96">

                <h1 class="text-2xl font-bold mb-4">
                    User Profile
                </h1>

                <p class="mb-2">
                    <strong>ID:</strong> ${user.id}
                </p>

                <p class="mb-2">
                    <strong>Name:</strong> ${user.name}
                </p>

                <p class="mb-2">
                    <strong>Email:</strong> ${user.email}
                </p>

                <p class="mb-2">
                    <strong>Status:</strong> ${user.is_active}
                </p>

                <p class="mb-4">
                    <strong>Role:</strong> ${payload.role}
                </p>

                <div class="flex gap-2">

                    <button
                        onclick="editMyProfile()"
                        class="bg-blue-500 text-white px-4 py-2 rounded"
                    >
                        Edit
                    </button>

                    <button
                        onclick="deleteMyAccount()"
                        class="bg-red-500 text-white px-4 py-2 rounded"
                    >
                        Delete
                    </button>

                    <button
                        onclick="logout()"
                        class="bg-gray-600 text-white px-4 py-2 rounded"
                    >
                        Logout
                    </button>

                </div>

            </div>

        </div>
        `;

    } finally {

        hideLoader();
    }
}

async function editUser(userId) {
    console.log("EDIT CLICKED");


    const name = prompt("Enter new name");
    const email = prompt("Enter new email");
    const password = prompt("Enter new password");

    console.log("NAME:", name);
console.log("EMAIL:", email);
console.log("PASSWORD:", password);
console.log("ABOUT TO SEND PUT");

    if (!name || !email || !password) {
        return;
    }

    showLoader();

    try {

        const response = await fetch(
            API + `/api/v1/users/${userId}`,
            {
                method: "PUT",

                headers: {
                    Authorization: "Bearer " + token,
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            }
        );

        const result = await response.json();

        if (result.status !== "success") {
            alert(result.error.message);
            return;
        }

        

        alert("User updated successfully");

if (payload.role === "admin") {

    loadUsers();

} else {

    loadProfile();
}

    } finally {

        hideLoader();
    }
}

async function blockUser(userId) {

    if (!confirm("Block this user?")) {
        return;
    }

    showLoader();

    try {

        const response = await fetch(
            API + `/api/v1/users/${userId}/block`,
            {
                method: "PATCH",

                headers: {
                    Authorization: "Bearer " + token
                }
            }
        );

        const result = await response.json();

        if (result.status !== "success") {
            alert(result.error.message);
            return;
        }

        alert("User blocked successfully");

        loadUsers();

    } finally {

        hideLoader();
    }
}

async function deleteUser(userId) {

    if (!confirm("Delete this user?")) {
        return;
    }

    showLoader();

    try {

        const response = await fetch(
            API + `/api/v1/users/${userId}`,
            {
                method: "DELETE",

                headers: {
                    Authorization: "Bearer " + token
                }
            }
        );

        const result = await response.json();

        if (result.status !== "success") {
            alert(result.error.message);
            return;
        }

        alert("User deleted successfully");

        loadUsers();

    } finally {

        hideLoader();
    }
}

async function editMyProfile() {

    await editUser(payload.user_id);
}

async function deleteMyAccount() {

    if (!confirm("Delete your account?")) {
        return;
    }

    showLoader();

    try {

        const response = await fetch(
            API + `/api/v1/users/${payload.user_id}`,
            {
                method: "DELETE",

                headers: {
                    Authorization: "Bearer " + token
                }
            }
        );

        const result = await response.json();

        if (result.status !== "success") {
            alert(result.error.message);
            return;
        }

        alert("Account deleted successfully");

        logout();

    } finally {

        hideLoader();
    }
}

function logout() {

    localStorage.removeItem('token');

    window.location.href = 'login.html';
}

function toggleTheme() {

    document.body.classList.toggle('bg-slate-900');
}

(async () => {

    const valid =
        await validateToken();

    if (valid) {

        loadDashboard();
    }

})();
