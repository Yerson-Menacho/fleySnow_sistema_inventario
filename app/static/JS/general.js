document.addEventListener("DOMContentLoaded", () => {
    // ==========================
    // 🔹 SweetAlert Flash Messages
    // ==========================
    const flashScript = document.getElementById("flash-messages");
    if (flashScript) {
        try {
            const flashMessages = JSON.parse(flashScript.textContent);
            if (Array.isArray(flashMessages)) {
                flashMessages.forEach(([category, message]) => {
                    let icon;
                    switch (category) {
                        case "warning": icon = "warning"; break;
                        case "danger": icon = "error"; break;
                        default: icon = "success";
                    }
                    Swal.fire({
                        icon: icon,
                        title: message,
                        confirmButtonColor: "#2e7d32",
                        confirmButtonText: "Entendido"
                    });
                });
            }
        } catch (e) {
            console.error("Error parseando flashMessages:", e);
        }
    }
});

$(document).ready(function() {
    const path = window.location.pathname;

    // Ejecutar búsqueda SOLO en /usuarios o /usuarios/*
    if (path === '/usuarios' || path.startsWith('/usuarios/')) {
        const $input = $('#q');
        if ($input.length) {
            $input.on('keyup', function() {
                const query = $(this).val();
                $.ajax({
                    url: '/usuarios/buscar_usuario',
                    type: 'GET',
                    data: { q: query },
                    success: function(html) {
                        $('table tbody').html(html);
                    }
                });
            });
        }
    }
});
