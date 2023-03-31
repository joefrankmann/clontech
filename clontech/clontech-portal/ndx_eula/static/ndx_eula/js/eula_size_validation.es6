// The below code is for frontend validation of file upload size

// These elements are okay to get once as they are invariant under new fields being added
const submitButton = document.querySelector("input[type=submit]");
const errorsEl = document.getElementById("form-errors");

// maximum file size in megabytes
const fileUploadLimit = 10;

const blockSubmit = () => {
    submitButton.disabled = true;
    errorsEl.innerText = `Selected file exceeds limit of ${fileUploadLimit} MB.`;
};

const allowSubmit = () => {
    submitButton.disabled = false;
    errorsEl.innerText = "";
};

const acceptableSize = inputNode => {
    if (inputNode.files && inputNode.files.length > 0) {
        return inputNode.files[0].size < fileUploadLimit * 1024 * 1024;
    } else {
        return true;
    }
};

const scanFileFields = () => {
    // we need to find these on the fly instead of once at the start as the number can change
    let fileInputs = document.querySelectorAll("input[type=file]");
    // an old fashioned for loop must be used as querySelectorAll returns a NodeList which is a bit weird
    // NodeLists have a .forEach method, however this isn't supported on all browsers
    for (let i = 0; i < fileInputs.length; i++) {
        if (!acceptableSize(fileInputs[i])) {
            blockSubmit();
            return;
        }
    }
    // only if all of the fields are okay
    allowSubmit();
};

const addFileWatchers = e => {
    // This function needs to be called to be done every time new file inputs are added
    let fileInputs = document.querySelectorAll("input[type=file]");
    for (let i = 0; i < fileInputs.length; i++) {
        fileInputs[i].onchange = fileSizeWatcher;
    }
};

const fileSizeWatcher = e => {
    if (!acceptableSize(e.target)) {
        blockSubmit();
    } else {
        // we need to check every file field before allowing submission
        scanFileFields();
    }
};

addFileWatchers();
// DOMNodeInserted is used instead of click, as the click comes before the nodes are inserted
window.addEventListener("DOMNodeInserted", addFileWatchers);
