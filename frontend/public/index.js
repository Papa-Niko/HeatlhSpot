// document.addEventListener('DOMContentLoaded', function() {
//     const healthIdInput = document.getElementById('health-id');

//     // Call the function to generate a random ID when the page loads
//     generateRandomId();

//     function generateRandomId() {
//         const min = 100000000; // 9 digits starting from 100,000,000
//         const max = 999999999; // 9 digits ending at 999,999,999
//         const randomId = Math.floor(Math.random() * (max - min + 1)) + min;
//         healthIdInput.value = randomId;
//     }
// });

// function openNewPageWithDelay() {
//     var newPageUrl = "/public/hid.html";
//     setTimeout(function() {
//         window.open(newPageUrl, "_blank");
//     }, 1000); 
// }
document.addEventListener('DOMContentLoaded', function() {
    const healthIdInput = document.getElementById('health-id');
    generateRandomId();

    function generateRandomId() {
        const min = 100000000;
        const max = 999999999;
        const randomId = Math.floor(Math.random() * (max - min + 1)) + min;
        if (healthIdInput) {
            healthIdInput.value = randomId;
        }
    }

    const registerBtn = document.querySelector('button[onclick="openNewPageWithDelay()"]');
    if (registerBtn) {
        registerBtn.addEventListener('click', async function(event) {
            event.preventDefault();

            const name = document.getElementById('regUsername').value;
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;
            const healthId = document.getElementById('health-id')?.value || "";

            const user = {
                name: name,
                email: email,
                password: password,
                health_id: healthId
            };

            try {
                const response = await fetch("https://heatlhspot.onrender.com", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(user)
                });

                const result = await response.json();
                console.log("User registered:", result);
                openNewPageWithDelay();
            } catch (error) {
                console.error("Registration failed:", error);
            }
        });
    }
});

function openNewPageWithDelay() {
    const newPageUrl = "/public/hid.html";
    setTimeout(function() {
        window.open(newPageUrl, "_blank");
    }, 1000);
}
