const links = document.querySelectorAll('#link')

export function detectPage(links) {
    for(let item of links) {
        if ((document.URL.includes(`${item.getAttribute('href')}`))) {
            item.parentNode.style.background = "rgba(255, 255, 255, 0.2)";
        }
    }
}

detectPage(links);

export { links }
