function blankViewer() {
    // embed a blank gif for improved speed
    document.getElementById("gallery__fullsize").setAttribute("src", "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=")
}

function showViewer(clicked_image) {
    img_name = clicked_image.getAttribute("src").split("/").pop()
    img_path = "/static/gallery/" + img_name

    blankViewer()
    //
    document.getElementById("gallery__fullsize").setAttribute("src", img_path)
    document.getElementById("gallery__original").setAttribute("href", img_path)
    document.getElementById("gallery__metadata").innerText = clicked_image.dataset.metadata

    document.getElementById("gallery__viewer").classList.remove("gallery__viewer--hidden")
}

window.addEventListener("load", function () {
    viewer_element = document.getElementById("gallery__viewer")

    // we want the photo viewer to close when clicking outside any images.
    // to do this, we have to add a click listener and check the target
    viewer_element.addEventListener("click", function (event) {
        if (event.target.nodeName != "IMG") {
            viewer_element.classList.add("gallery__viewer--hidden")
            blankViewer()
        }
    });
});
