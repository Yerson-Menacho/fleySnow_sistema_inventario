// ============================================
// 📄 insumos_list.js
// Búsqueda en tiempo real de insumos
// ============================================
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("buscarInsumo");
    const tablaBody = document.getElementById("tablaInsumosBody");

    // Solo se ejecuta si existen los elementos del listado
    if (!searchInput || !tablaBody) return;

    let typingTimer;
    const delay = 300; // 0.3s después de dejar de escribir

    searchInput.addEventListener("keyup", function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(buscarInsumos, delay);
    });

    async function buscarInsumos() {
        const query = searchInput.value.trim();

        try {
            const response = await fetch(
                `/insumos/buscar_insumo?q=${encodeURIComponent(query)}`
            );
            if (!response.ok) throw new Error("Error en la búsqueda");

            const html = await response.text();
            tablaBody.innerHTML = html;
        } catch (error) {
            console.error("Error al buscar insumos:", error);
        }
    }
});
