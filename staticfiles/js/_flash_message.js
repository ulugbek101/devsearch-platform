

const flashMessage = function () {
    const alertCloseBtn = document.querySelector('.alert__close');
    if (alertCloseBtn) {
        alertCloseBtn.addEventListener('click', (e) => {
            e.target.parentNode.style.display = 'none';
        })
    }
}

export default flashMessage


