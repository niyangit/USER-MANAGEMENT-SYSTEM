const API =
'http://127.0.0.1:8000';

async function forgotPassword() {

    const email =
    document.getElementById(
        "email"
    ).value;

    const method =
    document.getElementById(
        "method"
    ).value;

    const response =
    await fetch(
        API +
        "/api/v1/auth/forgot-password",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                email,
                method
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
        result.message
    );

    if (
        method === "otp"
    ) {

        localStorage.setItem(
            "reset_email",
            email
        );

        window.location.href =
        "verify_otp.html";
    }
}