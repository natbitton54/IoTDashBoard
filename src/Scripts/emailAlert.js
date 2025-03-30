let tempPopupShown = false;
let lightPopupShown = false;

// Check every 3 seconds
setInterval(() => {

    // --- Check temperature email alert ---
    fetch('/email-status')
        .then(res => res.json())
        .then(data => {
            if (data.email_sent && !tempPopupShown) {
                tempPopupShown = true;
                Swal.fire({
                    title: 'Temperature Alert!',
                    text: 'An email has been sent due to high temperature.',
                    icon: 'info',
                    confirmButtonText: 'OK'
                }).then(() => {
                    fetch('/acknowledge-email', { method: 'POST' })
                        .then(() => { tempPopupShown = false; });
                });
            }
        });

    // --- Check light intensity email alert ---
    fetch('/light-email-status')
        .then(res => res.json())
        .then(data => {
            if (data.email_sent && !lightPopupShown) {
                lightPopupShown = true;
                Swal.fire({
                    title: 'Light Intensity Alert!',
                    text: 'An email has been sent due to low light intensity.',
                    icon: 'info',
                    confirmButtonText: 'OK'
                }).then(() => {
                    fetch('/acknowledge-light-email', { method: 'POST' })
                        .then(() => { lightPopupShown = false; });
                });
            }
        });
}, 3000);


