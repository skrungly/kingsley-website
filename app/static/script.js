function showViewer(clicked_image) {
    img_name = clicked_image.getAttribute("src").split("/").pop()
    img_path = "/static/gallery/" + img_name

    // only show the viewer once the image is loaded
    clicked_image.addEventListener("load", function() {
        document.getElementById("gallery_viewer").classList.remove("gallery__viewer--hidden")
    })

    document.getElementById("gallery_fullsize").setAttribute("src", img_path)
    document.getElementById("gallery_original").setAttribute("href", img_path)
    document.getElementById("gallery_caption").innerText = clicked_image.dataset.metadata
    clicked_image.setAttribute("src", img_path)
}

window.addEventListener("load", function () {
    viewer_element = document.getElementById("gallery_viewer")

    // we want the photo viewer to close when clicking outside any images.
    // to do this, we have to add a click listener and check the target
    viewer_element.addEventListener("click", function (event) {
        if (event.target === viewer_element) {
            viewer_element.classList.add("gallery__viewer--hidden")
        }
    });
});
