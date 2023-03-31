document.getElementById("feedback-csv-button").onclick = event => {
    const button = event.target;
    const csvUrl = button["data-url"];
    // The element containing the text is the last element of the button
    button.lastChild.innerHTML = "Downloading...";
    button.disabled = true;
    fetch("/api/feedback/csv", {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": button["data-csrf-token"]
        }
    })
        .then(r => r.blob())
        .then(blob => {
            // In order for the CSV to be downloaded it must be given as a blob url for a DOM link
            // A blob must be used as the CSV is sent through an HTTP stream
            const a = document.createElement("a");
            a.style.visibility = null;
            document.body.appendChild(a);
            a.href = URL.createObjectURL(blob);
            const date = new Date();
            a.download = "feedback_results_" + date.toISOString() + ".csv";
            // Click the invisible a
            a.click();
            // reset the DOM to how it was before the click
            document.body.removeChild(a);
            button.disabled = false;
            button.lastChild.innerHTML = "Download CSV";
        });
};
