// To access the stars
let stars = document.getElementsByClassName("star");
let output = document.getElementById("output");

// Function to update rating
function gfg(n) {
    remove();
    for (let i = 0; i < n; i++) {
        stars[i].classList.add("active");
    }
    output.innerText = "Rating is: " + n + "/5";
}

// To remove the pre-applied styling
function remove() {
    for (let i = 0; i < stars.length; i++) {
        stars[i].classList.remove("active");
    }
}

