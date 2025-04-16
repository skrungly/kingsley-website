function blankViewer() {
    // embed a blank gif for improved speed
    document.getElementById("gallery__fullsize").setAttribute("src", "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=")
}

function showViewer(clicked_image) {
    img_name = clicked_image.getAttribute("src").split("/").pop()
    img_path = "/static/gallery/" + img_name

    blankViewer()
    document.getElementById("gallery__fullsize").setAttribute("src", img_path)
    document.getElementById("gallery__original").setAttribute("href", img_path)
    document.getElementById("gallery__metadata").innerText = clicked_image.dataset.metadata

    document.getElementById("gallery__viewer").classList.remove("gallery__viewer--hidden")
}

function clickViewer(event) {
    // we want the photo viewer to close when clicking outside any images.
    // to do this, we have to add a click listener and check the target
    if (event.target.nodeName != "IMG" && event.target.nodeName != "P") {
        viewer_element.classList.add("gallery__viewer--hidden")
        blankViewer()
    }
}

function toggleNav(event) {
    navClassList = document.getElementById("nav").classList;
    buttonClassList = document.getElementById("nav__collapse-button").classList;

    if (navClassList.contains("nav--top-collapsed")) {
        buttonClassList.remove("fa-chevron-down");
        buttonClassList.add("fa-chevron-up");
        navClassList.remove("nav--top-collapsed");
    } else {
        buttonClassList.remove("fa-chevron-up");
        buttonClassList.add("fa-chevron-down");
        navClassList.add("nav--top-collapsed");
    }
}

window.addEventListener("load", function () {
    document.getElementById("nav__collapse-button").addEventListener("click", toggleNav);

    // if the gallery viewer is on the page, make it functional
    viewer_element = document.getElementById("gallery__viewer");
    if (viewer_element !== null) {
        viewer_element.addEventListener("click", clickViewer);
    }
});
