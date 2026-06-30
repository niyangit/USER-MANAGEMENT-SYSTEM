const API =
'https://user-management-system-36zz.onrender.com';

async function verifyOtp() {

    const email =
    localStorage.getItem(
        "reset_email"
    );

    const otp =
    document.getElementById(
        "otp"
    ).value;

    const response =
    await fetch(
        API +
        "/api/v1/auth/verify-otp",
        {
            method: "POST",

            headers: {
                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
                email,
                otp
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

    localStorage.setItem(
        "reset_token",
        result.data.reset_token
    );

    window.location.href =
    "reset_password.html";
}