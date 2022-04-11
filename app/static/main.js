const form = document.querySelector('#edit-profile-picture')

const toggleForm = () => {
    form.classList.toggle('d-none')
    form.classList.toggle('active')
}

window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    const introduction = document.querySelector('.introduction')
    header.classList.toggle('sticky', window.scrollY > 10);
    introduction.classList.toggle('on-scroll', window.scrollY > 0)
})

const setDisplayButtons = Array.from(document.getElementsByClassName('set-display'))

for (let i = 0; i < setDisplayButtons.length; i++){
    setDisplayButtons[i].addEventListener('click', () => {
        const artId = setDisplayButtons[i].data.ID
        const url = `/display/${artId}`
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        }).then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
    })
}