document.addEventListener("DOMContentLoaded", () => {
    const d = window.DASHBOARD;

    // =====================================================
    // DARK MODE GLOBAL
    // =====================================================
    Chart.defaults.color = "#e5e7eb";
    Chart.defaults.font.family = "Poppins, sans-serif";
    Chart.defaults.plugins.legend.labels.color = "#fff";

    const COLORS = {
        primary: "#4d8bf5",
        primary40: "rgba(77,139,245,0.35)",
        success: "#4ade80",
        danger: "#f87171",
        grayGrid: "rgba(255,255,255,0.08)"
    };

    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 900,
            easing: "easeOutQuart"
        },
        plugins: {
            legend: {
                labels: { padding: 12 }
            },
            tooltip: {
                backgroundColor: "rgba(30,30,30,0.85)",
                titleColor: "#fff",
                bodyColor: "#e5e7eb",
                borderColor: "#444",
                borderWidth: 1
            }
        }
    };

    // =====================================================
    // 1️⃣ Stock por Categoría
    // =====================================================
    if (d.categoriasLabels?.length) {
        new Chart(chartCategorias, {
            type: "bar",
            data: {
                labels: d.categoriasLabels,
                datasets: [{
                    label: "Stock disponible",
                    data: d.categoriasData,
                    backgroundColor: COLORS.primary,
                    borderRadius: 10,
                }]
            },
            options: {
                ...baseOptions,
                scales: {
                    y: { grid: { color: COLORS.grayGrid } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // =====================================================
    // 2️⃣ Entradas vs Salidas
    // =====================================================
    if (d.esLabels?.length) {
        new Chart(chartEntradasSalidas, {
            type: "line",
            data: {
                labels: d.esLabels,
                datasets: [
                    {
                        label: "Entradas",
                        data: d.esEntradas,
                        borderColor: COLORS.success,
                        backgroundColor: COLORS.success,
                        tension: 0.3,
                        borderWidth: 2
                    },
                    {
                        label: "Salidas",
                        data: d.esSalidas,
                        borderColor: COLORS.danger,
                        backgroundColor: COLORS.danger,
                        tension: 0.3,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                ...baseOptions,
                scales: { y: { grid: { color: COLORS.grayGrid } } }
            }
        });
    }

    // =====================================================
    // 3️⃣ Peso Neto por Variedad
    // =====================================================
    if (d.varLabels?.length) {
        new Chart(chartVariedades, {
            type: "bar",
            data: {
                labels: d.varLabels,
                datasets: [{
                    label: "Peso total (kg)",
                    data: d.varData,
                    backgroundColor: COLORS.primary40,
                    borderColor: COLORS.primary,
                    borderWidth: 2,
                    borderRadius: 10
                }]
            },
            options: {
                ...baseOptions,
                indexAxis: "y",
                scales: {
                    x: { grid: { color: COLORS.grayGrid } },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    // =====================================================
    // 4️⃣ Actividad del Sistema
    // =====================================================
    if (d.actividadLabels?.length) {
        new Chart(chartActividad, {
            type: "line",
            data: {
                labels: d.actividadLabels,
                datasets: [{
                    label: "Acciones registradas",
                    data: d.actividadData,
                    borderColor: COLORS.primary,
                    backgroundColor: COLORS.primary40,
                    fill: true,
                    tension: 0.25,
                    borderWidth: 2
                }]
            },
            options: {
                ...baseOptions,
                scales: {
                    y: { grid: { color: COLORS.grayGrid } },
                }
            }
        });
    }
});
