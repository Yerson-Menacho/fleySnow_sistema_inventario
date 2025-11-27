document.addEventListener("DOMContentLoaded", () => {
    const tabla = document.querySelector("#detalleTabla tbody");
    const detallesInput = document.getElementById("detallesInput");

    const modal = document.getElementById("modalInsumo");
    const abrirModal = document.getElementById("agregarFila");
    const cerrarModal = document.getElementById("cerrarModal");
    const guardarInsumo = document.getElementById("guardarInsumo");

    let filaEditando = null;

    // 🔹 Limpiar campos del modal
    function limpiarModal() {
        $("#insumo").val(null).trigger("change");
        document.getElementById("modal_cantidad").value = "";
        document.getElementById("modal_unidad").value = "";
    }

    // 🔹 Escapar HTML para seguridad
    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;")
                   .replace(/</g, "&lt;")
                   .replace(/>/g, "&gt;")
                   .replace(/"/g, "&quot;")
                   .replace(/'/g, "&#039;");
    }

    // ======================================
    // 👉 Abrir modal
    abrirModal.addEventListener("click", () => {
        filaEditando = null;
        limpiarModal();
        modal.style.display = "flex";
    });

    // 👉 Cerrar modal
    cerrarModal.addEventListener("click", () => {
        modal.style.display = "none";
        limpiarModal();
    });

    modal.addEventListener("click", e => {
        if (e.target === modal) {
            modal.style.display = "none";
            limpiarModal();
        }
    });

    // ======================================
    // 👉 Guardar detalle (nuevo o editado)
    guardarInsumo.addEventListener("click", () => {
        const insumo = $("#insumo").select2("data")[0];
        const cantidad = parseFloat(document.getElementById("modal_cantidad").value) || 0;
        const unidad = document.getElementById("modal_unidad").value;

        if (!insumo || cantidad <= 0 || !unidad) {
            alert("⚠️ Completa todos los campos correctamente.");
            return;
        }

        if (filaEditando) {
            // 🔹 Editando fila existente
            filaEditando.dataset.estado = filaEditando.dataset.idDetalle ? "modificado" : "nuevo";

            filaEditando.innerHTML = `
                <td data-id="${insumo.id}">${escapeHtml(insumo.text)}</td>
                <td>${cantidad}</td>
                <td>${escapeHtml(unidad)}</td>
                <td class="text-center">
                    <button type="button" class="btn btn-primary btn-sm editar">✏️</button>
                    <button type="button" class="btn btn-danger btn-sm eliminar">🗑️</button>
                </td>
            `;
        } else {
            // 🔹 Nueva fila
            const fila = document.createElement("tr");
            fila.dataset.estado = "nuevo";
            fila.dataset.idDetalle = ""; // vacío hasta guardar
            fila.innerHTML = `
                <td data-id="${insumo.id}">${escapeHtml(insumo.text)}</td>
                <td>${cantidad}</td>
                <td>${escapeHtml(unidad)}</td>
                <td class="text-center">
                    <button type="button" class="btn btn-primary btn-sm editar">✏️</button>
                    <button type="button" class="btn btn-danger btn-sm eliminar">🗑️</button>
                </td>
            `;
            tabla.appendChild(fila);
        }

        modal.style.display = "none";
        limpiarModal();
    });

    // ======================================
    // 👉 Editar / Eliminar fila (delegado)
    tabla.addEventListener("click", e => {
        const fila = e.target.closest("tr");
        if (!fila) return;

        // 🔹 Eliminar fila
        if (e.target.classList.contains("eliminar")) {
            if (fila.dataset.idDetalle) {
                fila.dataset.estado = "eliminado";
                fila.style.display = "none";
            } else {
                fila.remove();
            }
        }

        // 🔹 Editar fila
        if (e.target.classList.contains("editar")) {
            filaEditando = fila;

            const tdInsumo = fila.querySelector("td[data-id]");
            const id = tdInsumo.dataset.id;
            const nombre = tdInsumo.innerText;
            const cantidad = fila.cells[1].innerText;
            const unidad = fila.cells[2].innerText;

            $("#insumo").append(new Option(nombre, id, true, true)).trigger("change");
            document.getElementById("modal_cantidad").value = cantidad;
            document.getElementById("modal_unidad").value = unidad;

            modal.style.display = "flex";
        }
    });

    // ======================================
    // 👉 Envío del formulario
    const form = document.getElementById("notaForm");
    form.addEventListener("submit", e => {
        const detalles = [];

        tabla.querySelectorAll("tr").forEach(fila => {
            const tdInsumo = fila.querySelector("td[data-id]");
            if (!tdInsumo) return;

            detalles.push({
                id_detalle: fila.dataset.idDetalle || null,
                id_insumo: parseInt(tdInsumo.dataset.id),
                cantidad: parseFloat(fila.cells[1].innerText) || 0,
                unidad_medida: fila.cells[2].innerText,
                estado: fila.dataset.estado || "nuevo"
            });
        });

        if (detalles.length === 0) {
            e.preventDefault();
            alert("⚠️ Debes agregar al menos un detalle.");
            return;
        }

        detallesInput.value = JSON.stringify(detalles);
    });
});

// ======================================
// Modal de cambio de estado
// ======================================
const modalEstado = document.getElementById("modalEstado");
const cerrarModalEstado = document.getElementById("cerrarModalEstado");
const selectEstado = document.getElementById("estado");

if (modalEstado) {
    document.querySelectorAll(".btn-cambiar-estado").forEach(btn => {
        btn.addEventListener("click", function () {
            const id = this.dataset.id;
            const form = document.getElementById("formCambiarEstado");
            form.action = `/movimientos/actualizar_estado/${id}`;
            modalEstado.style.display = "flex";
        });
    });

    if (cerrarModalEstado) {
        cerrarModalEstado.addEventListener("click", () => {
            modalEstado.style.display = "none";
            selectEstado.value = "";
        });
    }

    modalEstado.addEventListener("click", e => {
        if (e.target === modalEstado) {
            modalEstado.style.display = "none";
            selectEstado.value = "";
        }
    });
}

// ======================================
// 🔎 Búsqueda dinámica en index movimientos
// ======================================
document.addEventListener("DOMContentLoaded", () => {
    const inputBusqueda = document.getElementById("buscarMovimiento");

    if (inputBusqueda) {
        inputBusqueda.addEventListener("keyup", async function () {
            const q = this.value.trim();

            try {
                const respuesta = await fetch(`/movimientos/buscar?q=${encodeURIComponent(q)}`);
                if (!respuesta.ok) throw new Error("Error al buscar movimientos");

                const html = await respuesta.text();
                const tbody = document.querySelector("table tbody");
                tbody.innerHTML = html;
            } catch (error) {
                console.error("❌", error);
            }
        });
    }
});
