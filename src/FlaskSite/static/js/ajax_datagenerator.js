// fetch data
debug = true;
function requestData() {
    $.ajax({
        type: 'GET',
        url: '/data',
        success :(data) => {
            updateData(data);
            if(debug)
                $('#debug').text(data)
        }
    })
        .then(function () {
        setTimeout(requestData, 50) //call itself every 50ms
    });
}
function requestStructureData() {
      $.ajax({
        type: 'GET',
        url: '/data/structure',
        success :(data) => {
            updateData(data);
            if(debug)
                $('#debug').text(data)
        }
    });
}

function requestStructureActivity() {
      $.ajax({
        type: 'GET',
        url: '/data/activity',
        success :(data) => {
            updateData(data);
            if(debug)
                $('#debug').text(data)
        }
    });
}

requestData();
requestStructureData();