function getGetParameter(name) {
    let args = window.location.search.substr(1).split('&');
    for (let arg of args) {
        let data = arg.split('=');
        if (data.length > 1 && data[0] === name) {
            return data[1];
        }
    }
    return '';
}

function request(method, url, data, callback) {
    let xhr = new XMLHttpRequest();

    let args = '';
    for (let arg in data) {
        args += arg + '=' + data[arg] + '&';
    }
    args.substr(0, args.length - 1);

    let send;
    if (method === 'POST') {
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        send = function () { xhr.send(args); };
    } else if (method === 'GET') {
        if (args) {
            args = '?' + args;
        }
        xhr.open(method, url + args);
        send = function () { xhr.send(); };
    } else {
        throw 'Unknown method ' + method;
    }

    xhr.addEventListener('load', function () {
        callback(xhr.status, xhr.response);
    });
    send();
}