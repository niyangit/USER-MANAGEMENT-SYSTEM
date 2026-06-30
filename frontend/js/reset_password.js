const API =
'https://user-management-system-36zz.onrender.com';

async function resetPassword() {

    const password =
    document.getElementById(
        "password"
    ).value;


    let resetToken =
    localStorage.getItem(
        "reset_token"
    );


    if (!resetToken) {

        const params =
        new URLSearchParams(
            window.location.search
        );

        resetToken =
        params.get(
            "token"
        );
    }

    const response =
    await fetch(
        API +
        "/api/v1/auth/reset-password",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                reset_token:
                resetToken,

                password:
                password
            })
        }
    );

    const result =
    await response.json();

    if (
        result.status !==
        "success"
    ) {

        alert(
            result.error.message
        );

        return;
    }

    alert(
        "Password reset successful"
    );

    localStorage.removeItem(
        "reset_token"
    );

    localStorage.removeItem(
        "reset_email"
    );

    window.location.href =
    "login.html";
}