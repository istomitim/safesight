const e = React.createElement;

function ScannerTabs(props) {
    // which tab is active 
    
    const [tab, setTab] = React.useState("file");

    // CSRF token
    const csrfToken = props.csrfToken;

    // File / Link
    const tabButtons = e("div", { className: "tabs" },
        e("button", {
            type: "button",
            className: "tab-btn" + (tab === "file" ? " active" : ""),
            onClick: () => setTab("file")
        }, e("i", { className: "ti ti-file" }), " File"),

        e("button", {
            type: "button",
            className: "tab-btn" + (tab === "url" ? " active" : ""),
            onClick: () => setTab("url")
        }, e("i", { className: "ti ti-link" }), " Link")
    );

    //  FILE form 
    const fileForm = e("div", null,
        e("p", { className: "muted-note" }, "Upload a file to scan it for malware."),
        e("form", { method: "post", encType: "multipart/form-data" },
            e("input", { type: "hidden", name: "csrfmiddlewaretoken", value: csrfToken }),
            e("input", { type: "hidden", name: "form_type", value: "file" }),
            e("label", { htmlFor: "fileInput", className: "file-drop" },
                e("i", { className: "ti ti-cloud-upload" }),
                e("span", { id: "fileLabel" }, "Choose a file or drag it here")
            ),
            e("input", {
                type: "file", name: "file", id: "fileInput", required: true, hidden: true,
                onChange: (ev) => {
                    // show the chosen file's name in the label
                    if (ev.target.files.length > 0) {
                        document.getElementById("fileLabel").textContent = ev.target.files[0].name;
                    }
                }
            }),
            e("button", { type: "submit" },
                e("i", { className: "ti ti-shield-check" }), " Check file")
        )
    );

    //  URL form 
    const urlForm = e("div", null,
        e("p", { className: "muted-note" }, "Check a suspicious link without opening it yourself."),
        e("form", { method: "post" },
            e("input", { type: "hidden", name: "csrfmiddlewaretoken", value: csrfToken }),
            e("input", { type: "hidden", name: "form_type", value: "url" }),
            e("input", {
                type: "url", name: "url", placeholder: "https://example.com",
                required: true, className: "url-input"
            }),
            e("button", { type: "submit" },
                e("i", { className: "ti ti-shield-check" }), " Check link")
        )
    );

    // the whole card
    return e("div", { className: "card" },
        tabButtons,
        tab === "file" ? fileForm : urlForm
    );
}

const mountNode = document.getElementById("scanner-tabs");
const csrfToken = mountNode.dataset.csrf;
ReactDOM.createRoot(mountNode).render(e(ScannerTabs, { csrfToken: csrfToken }));