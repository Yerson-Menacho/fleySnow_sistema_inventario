document.addEventListener("DOMContentLoaded", () => {
    const agricultorHidden = document.getElementById("id_agricultor");
    const tabla = document.querySelector("#tablaDetalles tbody");
    const detallesInput = document.getElementById("detallesInput");

    const modal = document.getElementById("modalDetalle");
    const abrirModal = document.getElementById("abrirModalDetalle");
    const cerrarModal = document.getElementById("cerrarModal");
    const guardarDetalle = document.getElementById("guardarDetalle");

    let rowEditing = null; // fila en edición

    // ======================================
    // Función para limpiar modal
    function limpiarModal() {
        if ($("#id_variedad").length) $("#id_variedad").val(null).trigger("change");
        document.getElementById("modal_lote").value = "";
        document.getElementById("modal_peso").value = "";
        document.getElementById("modal_jabas").value = "";
        document.getElementById("modal_unidad").value = "kg";
    }

    // Escapar HTML para seguridad
    function escapeHtml(text) {
        return text.replace(/&/g, "&amp;")
                   .replace(/</g, "&lt;")
                   .replace(/>/g, "&gt;")
                   .replace(/"/g, "&quot;")
                   .replace(/'/g, "&#039;");
    }

    // ======================================
    // Abrir modal para agregar nueva fila
    if (abrirModal) {
        abrirModal.addEventListener("click", () => {
            rowEditing = null;
            limpiarModal();
            modal.style.display = "flex";
        });
    }

    if (cerrarModal) {
        cerrarModal.addEventListener("click", () => {
            modal.style.display = "none";
            limpiarModal();
        });
    }

    if (modal) {
        modal.addEventListener("click", e => {
            if (e.target === modal) {
                modal.style.display = "none";
                limpiarModal();
            }
        });
    }

    // ======================================
    // Guardar detalle (nuevo o editado)
    if (guardarDetalle) {
        guardarDetalle.addEventListener("click", () => {
            const variedadSelect = document.getElementById("id_variedad");
            const variedadId = variedadSelect.value;
            const variedadText = variedadSelect.options[variedadSelect.selectedIndex]?.text;

            const lote = document.getElementById("modal_lote").value;
            const peso = parseFloat(document.getElementById("modal_peso").value) || 0;
            const jabas = parseInt(document.getElementById("modal_jabas").value) || 0;
            const unidad = document.getElementById("modal_unidad").value;

            if (!variedadId || !variedadText || !lote || !peso || !jabas) {
                alert("⚠️ Completa todos los campos del detalle.");
                return;
            }

            // Editando fila existente
            if (rowEditing) {
                rowEditing.dataset.estado = rowEditing.dataset.idDetalle ? "modificado" : "nuevo";

                rowEditing.innerHTML = `
                    <td data-id="${variedadId}">${escapeHtml(variedadText)}</td>
                    <td>${escapeHtml(lote)}</td>
                    <td>${peso.toFixed(2)}</td>
                    <td>${jabas}</td>
                    <td>${escapeHtml(unidad)}</td>
                    <td class="text-center">
                        <button type="button" class="btn btn-sm btn-primary editarDetalle">✏️</button>
                        <button type="button" class="btn btn-sm btn-danger eliminarDetalle">🗑️</button>
                    </td>
                `;
                rowEditing = null;
            } else {
                // Nueva fila
                const fila = document.createElement("tr");
                fila.dataset.estado = "nuevo";
                fila.dataset.idDetalle = ""; // vacío porque es nueva
                fila.innerHTML = `
                    <td data-id="${variedadId}">${escapeHtml(variedadText)}</td>
                    <td>${escapeHtml(lote)}</td>
                    <td>${peso.toFixed(2)}</td>
                    <td>${jabas}</td>
                    <td>${escapeHtml(unidad)}</td>
                    <td class="text-center">
                        <button type="button" class="btn btn-sm btn-primary editarDetalle">✏️</button>
                        <button type="button" class="btn btn-sm btn-danger eliminarDetalle">🗑️</button>
                    </td>
                `;
                tabla.appendChild(fila);
            }

            modal.style.display = "none";
            limpiarModal();
        });
    }

    // ======================================
    // Editar / Eliminar fila
    if (tabla) {
        tabla.addEventListener("click", e => {
            const fila = e.target.closest("tr");
            if (!fila) return;

            // ELIMINAR
            if (e.target.classList.contains("eliminarDetalle")) {
                // Marcamos como eliminado si tiene id_detalle (para backend)
                if (fila.dataset.idDetalle) {
                    fila.dataset.estado = "eliminado";
                    fila.style.display = "none"; // lo ocultamos
                } else {
                    // Si no tiene id_detalle (nuevo detalle), simplemente lo eliminamos del DOM
                    fila.remove();
                }
            } 

            // EDITAR
            else if (e.target.classList.contains("editarDetalle")) {
                rowEditing = fila;

                const tdVar = fila.querySelector("td[data-id]");
                if (!tdVar) return;

                const selVariedad = document.getElementById("id_variedad");
                selVariedad.value = tdVar.dataset.id;
                $("#id_variedad").trigger("change");

                document.getElementById("modal_lote").value = fila.cells[1].innerText;
                document.getElementById("modal_peso").value = fila.cells[2].innerText;
                document.getElementById("modal_jabas").value = fila.cells[3].innerText;
                document.getElementById("modal_unidad").value = fila.cells[4].innerText;

                modal.style.display = "flex";
            }
        });
    }

    // ======================================
    // Envío de formulario
    const form = document.getElementById("recepcionForm");
    if (form) {
        form.addEventListener("submit", e => {
            const detalles = [];
            tabla.querySelectorAll("tr").forEach(fila => {
                const tdVar = fila.querySelector("td[data-id]");
                if (!tdVar) return;

                // Incluir filas eliminadas también para que backend las procese
                detalles.push({
                    id_detalle: fila.dataset.idDetalle || null,
                    id_variedad: parseInt(tdVar.dataset.id),
                    lote: fila.cells[1].innerText,
                    peso_bruto: parseFloat(fila.cells[2].innerText) || 0,
                    cantidad_jabas: parseInt(fila.cells[3].innerText) || 0,
                    unidad_medida: fila.cells[4].innerText,
                    estado: fila.dataset.estado || "nuevo" // nuevo, modificado, eliminado
                });
            });

            if (detalles.length === 0) {
                e.preventDefault();
                alert("❌ Debe agregar al menos un detalle.");
                return;
            }

            detallesInput.value = JSON.stringify(detalles);
        });
    }

    // ======================================
    // Modal estado (opcional)
    const modalEstado = document.getElementById("modalEstado");
    const cerrarModalEstado = document.getElementById("cerrarModalEstado");
    const selectEstado = document.getElementById("estado");

    if (modalEstado) {
        document.querySelectorAll(".btn-cambiar-estado").forEach(btn => {
            btn.addEventListener("click", function () {
                const id = this.dataset.id;
                const form = document.getElementById("formCambiarEstado");
                form.action = `/recepcion/actualizar_estado/${id}`;
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
});

// buscar recepcion
document.addEventListener("DOMContentLoaded", () => {
    const inputBusqueda = document.getElementById("buscarRecepcion");

    if (inputBusqueda) {
        inputBusqueda.addEventListener("keyup", async function () {
            const q = this.value.trim();

            try {
                const respuesta = await fetch(`/recepcion/buscar?q=${encodeURIComponent(q)}`);
                if (!respuesta.ok) throw new Error("Error al buscar recepciones");

                const html = await respuesta.text();
                const tbody = document.querySelector("table tbody");
                tbody.innerHTML = html;
            } catch (error) {
                console.error("❌ Error:", error);
            }
        });
    }
});
