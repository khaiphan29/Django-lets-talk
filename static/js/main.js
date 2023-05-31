console.log('Hello World')

const searchInput = document.getElementById('search-input')
const resultBox = document.getElementById('livesearch-result')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

console.log(resultBox)
console.log(searchInput.offsetWidth)

const sendSearchData = (data) => {
    resultBox.innerHTML = ""
    $.ajax({
        type: 'POST',
        url: '/search-room',
        data: {
            'csrfmiddlewaretoken': csrf,
            'room': data
        },
        success: (res) => {
            console.log(res.data)
            const rooms = res.data
            if(Array.isArray(rooms)) {
                rooms.forEach((room) => {
                    resultBox.innerHTML += `
                        <div>
                            <a href="/room/${room.id}"> ${room.name} <a>
                        <div>`
                })
            } else {
                resultBox.innerHTML = rooms
            }
        },
        error: (err) => {
            console.log(err)
        }

    })
}

searchInput.addEventListener('keyup', e => {
    let input = e.target.value
    let style = window.getComputedStyle(resultBox)

    if (style.visibility === 'hidden') {
        resultBox.style.visibility = 'visible'
        resultBox.style.width = searchInput.offsetWidth
    }
    if (input.length === 0) {
        resultBox.style.visibility = 'hidden'
    }
    sendSearchData(e.target.value)
})