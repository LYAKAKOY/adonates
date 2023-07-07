let btnSide = document.querySelector('#btnside');
let sidebar = document.querySelector('.sidebar');
let changeBtn = document.querySelector('.subtitle-change');
let lastChange = document.querySelector('.donate__last');

function createFiller() {
    let elem = document.createElement('div');
    elem.style.position = 'fixed';
    elem.style.top = 0;
    elem.style.width = '100vw';
    elem.style.height = '100vh';
    elem.style.zIndex = '100';
    elem.style.background = 'rgba(0, 0, 0, 0.2)';
    return elem
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        sidebar.classList.remove('active');
        sidebar.classList.remove('toggle');
        document.getElementsByTagName('html')[0].style.overflowY = "hidden" ? '' : document.getElementsByTagName('html')[0].style.overflowY = "scroll"
        if (sidebar.classList.contains('active')) {
            document.body.append(filler);
        }
    
        else {
            filler.remove();
        }
    }
})

let filler = createFiller();
btnSide.onclick = function () {
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('toggle');
    if (sidebar.classList.contains('active')) {
        document.body.append(filler);
    }
    else {
        filler.remove();
    }
};

changeBtn.onclick = () => {
    document.querySelector('.donate__input').disabled = !document.querySelector('.donate__input').disabled;
    document.querySelector('.donate__input').disabled ? lastChange.innerHTML = new Date() : new Date()

}