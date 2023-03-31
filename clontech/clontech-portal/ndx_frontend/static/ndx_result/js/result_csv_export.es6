document.getElementById("result-csv-button").onclick = event => {
    event.preventDefault();
    const button = event.target;
    error_el.innerText = "";
    let filter_fields = [];
    let query_string = [];

    if (usingDateRange()) {
        if (new Date(start_date_el.value) >= new Date(end_date_el.value)) {
            error_el.innerText = "End date must be after start date.";
            return;
        }
        if (!start_date_el.value || !end_date_el.value) {
            error_el.innerText = "Date fields must be specified with valid dates.";
            return;
        }
        filter_fields = ["end_date", "start_date", "assay_type", "lot_no"];
    } else {
        filter_fields = ["assay_type", "lot_no"];
    }

    filter_fields.map(field => {
        let value = document.getElementById(field).value;
        if (value) {
            query_string.push(`${field}=${encodeURIComponent(value)}`);
        }
    });

    // The element containing the text is the last element of the button
    button.lastChild.innerHTML = "Downloading...";
    button.disabled = true;
    fetch("/api/result/csv?" + query_string.join("&"), {
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
            a.download = "results_" + date.toISOString() + ".csv";
            // Click the invisible a
            a.click();
            // reset the DOM to how it was before the click
            document.body.removeChild(a);
            button.disabled = false;
            button.lastChild.innerHTML = "Download CSV";
        });
};

const clearDate = fieldName => {
    // Function for clearing the datefield value, then removing the button (it is only visible
    // when there is a date to clear)
    const innerFunc = e => {
        e.preventDefault();
        document.getElementById(fieldName).value = "";
        document.getElementById(`${fieldName}_clear`).style.visibility = "hidden";
    };
    return innerFunc;
};

const enableClearButtonForEdge = fieldName => {
    let el = document.getElementById(`${fieldName}_clear`);
    if (isEdge && e.target.value) {
        el.style.visibility = "visible";
        el.disabled = false;
    } else {
        el.style.visibility = "hidden";
        el.disabled = true;
    }
};

const updateInfo = () => {
    let html;
    if (usingDateRange()) {
        let no_value = "(no date selected)";
        let start_date = start_date_el.value || no_value;
        let end_date = end_date_el.value || no_value;
        html = `Selecting results from <b>${start_date}</b> to <b>${end_date}</b>.`;
    } else {
        html = `Selecting results for all time.`;
    }
    info_el.innerHTML = html;
};

const c = console;
const getById = n => document.getElementById(n);
const usingDateRange = () => date_option_el.value == "range";
// Determine if using MS Edge
const isEdge = navigator.userAgent.indexOf("Edg") != -1;

// Elements
const start_date_el = getById("start_date");
const end_date_el = getById("end_date");
const error_el = getById("error");
const info_el = getById("form-info");
const date_option_el = getById("date_option");
const datepicker_field_group = getById("datepicker-fields-group");

// The date clear buttons for Edge, as edge's html date picker
// by default has no clear button
getById("start_date_clear").onclick = clearDate("start_date");
getById("end_date_clear").onclick = clearDate("end_date");

start_date_el.onblur = updateInfo();
start_date_el.onchange = e => {
    enableClearButtonForEdge("start_date");
    updateInfo();
};
end_date_el.onblur = updateInfo();
end_date_el.onchange = e => {
    enableClearButtonForEdge("end_date");
    updateInfo();
};

date_option_el.onchange = (e) => {
    let option = e.target.value;
    showHideDateFields(option);
}

function showHideDateFields(option) {
    let classList = datepicker_field_group.classList;
    if (usingDateRange()) {
        classList.add("active");
    } else {
        classList.remove("active");
    }
    updateInfo();
};

// Set the initial state
updateInfo();
enableClearButtonForEdge("start_date");
enableClearButtonForEdge("end_date");
showHideDateFields(date_option_el.value)
