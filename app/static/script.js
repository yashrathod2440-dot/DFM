
async function analyzeFile() {
    const fileInput = document.getElementById("stepFile");
    const result = document.getElementById("result");
    const button = document.getElementById("analyzeButton");

    if (!fileInput.files.length) {
        alert("Please select a STEP file.");
        return;
    }

    const file = fileInput.files[0];

    if (
        !file.name.toLowerCase().endsWith(".step") &&
        !file.name.toLowerCase().endsWith(".stp")
    ) {
        alert("Please select a STEP file (.step or .stp).");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    button.disabled = true;
    button.innerText = "Analyzing...";

    result.innerHTML = "<p>Analyzing STEP file...</p>";

    try {
        const response = await fetch("/analyze-step", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed");
        }

        result.innerHTML = `
            <h2>Analysis Completed</h2>

            <p class="score">
                DFM Score: ${data.dfm_score.score}/100
            </p>

            <p>
                Total Checks: ${data.dfm_score.total_checks}
            </p>

            <p>
                Passed: ${data.dfm_score.passed}
            </p>

            <p>
                Warnings: ${data.dfm_score.warning}
            </p>

            <p>
                Critical: ${data.dfm_score.critical}
            </p>

            <a
                class="download"
                href="/download-report/${encodeURIComponent(data.pdf_report.filename)}"
                target="_blank"
            >
                Download PDF Report
            </a>
        `;

    } catch (error) {

        result.innerHTML = `
            <p class="error">
                Error: ${error.message}
            </p>
        `;

    } finally {
        button.disabled = false;
        button.innerText = "Analyze STEP";
    }
}