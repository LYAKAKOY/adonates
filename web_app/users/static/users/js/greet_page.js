const navSlide = () => {
    const burger = document.querySelector('.burger');
    const header = document.querySelector('.items-list');
    const itemLinks =  document.querySelectorAll('.items-list li');

    burger.addEventListener('click', ()=>{
        //Toggle Nav
        header.classList.toggle('item-active');

        //Animate Links
        itemLinks.forEach((link, index)=>{
            if(link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = `headerLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });
        //Burger animation
        burger.classList.toggle('toggle');
    });

}

navSlide();

function onEntry(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('element-show');
        }
    });
}

window.onload = () => {
    let options = {
        threshold: 0.5
    };
    let observer = new IntersectionObserver(onEntry, options);
    let elementsTitle = document.querySelectorAll('.title');
    let elementsSubtitle = document.querySelectorAll('.subtitle');
    let elementsButton = document.querySelectorAll('.button');
    let elementsImg = document.querySelectorAll('.platform-section-img');
    let elementsItem = document.querySelectorAll('.advantages__item');

    
    for (let elm of elementsTitle) {
        observer.observe(elm);
    }
    
    for (let elm of elementsSubtitle) {
        observer.observe(elm);
    }

    for (let elm of elementsButton) {
        observer.observe(elm);
    }

    for (let elm of elementsImg) {
        observer.observe(elm);
    }

    for (let elm of elementsItem) {
        observer.observe(elm);
    }
}
