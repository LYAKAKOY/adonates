let btnSide = document.querySelector('#btnside');
let sidebar = document.querySelector('.sidebar');
let diagramItems = document.querySelectorAll('.diagram__item');
let editButton = document.querySelector('#edit');   
let changingInput = document.querySelector("#changing__input");


btnSide.onclick = function () {
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('toggle');
};


for(let item of diagramItems) {
    item.addEventListener('mouseover', function() {
        this.classList.add('selected');
    });
    item.addEventListener('mouseout', function() {
        this.classList.remove('selected');
    });
}

editButton.addEventListener("click", function() {
    changingInput.disabled = !changingInput.disabled;
})