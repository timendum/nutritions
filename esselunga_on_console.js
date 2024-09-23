const allData = [];

let handleEvent = function (e) {
    // console.log(e.target.responseURL, e.target.responseText);
    const rURL = e.target.responseURL;
    if (!rURL.startsWith("https://spesaonline.esselunga.it/commerce/resources/") || rURL.indexOf("/displayable/detail/") < 0) {
        return;
    }
    const jData = JSON.parse(e.target.responseText);
    allData.push([rURL, jData]);
    try {
        console.log("Last", allData[allData.length-1][1].displayableProduct.description)
    } catch(e) {
    }
}

const orig_open = XMLHttpRequest.prototype.open;
XMLHttpRequest.prototype.open = function(...args) {
    orig_open.apply(this, args);
    this.addEventListener("loadend", handleEvent);
};
(function(console) {

    console.save = function(data, filename) {

        if (!data) {
            console.error("Console.save: No data");
            return;
        }

        if (!filename) {
            filename = "console.json";
        }

        if (typeof data === "object") {
            data = JSON.stringify(data, undefined, 4);
        }

        const blob = new Blob([data], {
                type: "text/json",
            });
        const e = document.createEvent("MouseEvents");
        const a = document.createElement("a");

        a.download = filename;
        a.href = window.URL.createObjectURL(blob);
        a.dataset.downloadurl = ["text/json", a.download, a.href].join(":");
        e.initMouseEvent("click", true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        a.dispatchEvent(e);
    };
})(console);


// console.save(allData)