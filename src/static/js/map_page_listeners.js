window.addEventListener('load', function () {
    [...document.getElementsByClassName("left-bar-statut-element")].forEach(element => {
        element.addEventListener("click", (elm) => {
            [...document.getElementsByClassName("left-bar-statut-element")].forEach(element => element.selected = false)
            elm.path[0].selected = true
            this.document.getElementById("gratuit-input").checked = this.document.getElementById("gratuit-option").selected
            this.document.getElementById("payant-input").checked = this.document.getElementById("payant-option").selected
            console.log(elm.path[0].id.toString().split("-")[0] + "-input")
            document.getElementById(elm.path[0].id.toString().split("-")[0] + "-input").checked = true
        })
    });
    [...document.getElementsByClassName("tag")].forEach(element => {
        element.addEventListener("click", (elm) => {
            if(elm.path[0].className == "tag tag-selected"){
                elm.path[0].className = "tag"
            } else {
                elm.path[0].className = "tag tag-selected"
            }
            checkTag(elm.path[0])
        })
    });
    [...document.getElementsByClassName("type")].forEach(element => {
        element.addEventListener("click", (elm) => {
            if(elm.path[0].className == "type type-selected"){
                elm.path[0].className = "type"
            } else {
                elm.path[0].className = "type type-selected"
            }
            checkType(elm.path[0])
        })
    });
    [...document.getElementsByClassName("tag")].forEach(element => checkTag(element));
    [...document.getElementsByClassName("type")].forEach(element => checkType(element))
        
})

function checkTag(elm){
    if(elm.className == "tag tag-selected"){
        document.getElementById(elm.innerText + "-input").checked = true
    } else {
        document.getElementById(elm.innerText + "-input").checked = false
    }
}

function checkType(elm){
    if (elm.innerText.includes("ferme")) {
        document.getElementById("ferme-input").checked = (elm.className == "type type-selected")
    } else if (elm.innerText.includes("indépend")) {
        document.getElementById("inde-input").checked = (elm.className == "type type-selected")
    } else if (elm.innerText.includes("AMAPS")) {
        document.getElementById("amaps-input").checked = (elm.className == "type type-selected")
    }else {
        document.getElementById("jardin-input").checked = (elm.className == "type type-selected")
    }
}