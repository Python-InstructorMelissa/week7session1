var gitUrl = 'https://api.github.com/users/dojo24/followers'

// console.log(gitUrl)

async function getGitHub() {
    var response = await fetch(`${gitUrl}`)
    var data = await response.json()
    console.log("github url json res: ", data)
    console.log("1st index: ", data[0])
    console.log('1st index login id: ', data[0].login)
        // var node = document.createElement('div')  // Create a div section
        // var h2 = document.createElement('h2') // Create a h2
        // var login = document.createTextNode(data[0].login) // set var login to equal data by telling it that it is text
        // h2.appendChild(login) // Add data to the h2
        // node.appendChild(h2)  // put h2 inside the div
        // document.getElementById('gitHub').appendChild(node) // Add div to page
    for (var i = 0; i < data.length; i++) {
        var node = document.createElement('div')  // Create a div section
        var h2 = document.createElement('h2') // Create a h2
        var login = document.createTextNode(data[i].login) // set var login to equal data by telling it that it is text
        h2.appendChild(login) // Add data to the h2
        node.appendChild(h2)  // put h2 inside the div
        document.getElementById('gitHub').appendChild(node) // Add div to page
    }
}

// getGitHub()